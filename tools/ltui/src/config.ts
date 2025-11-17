import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

export interface ProfileConfig {
  workspace: string;
  keyRef: string;
}

export interface LtuiConfig {
  defaultProfile?: string;
  profiles?: Record<string, ProfileConfig>;
}

export interface ProjectConfig {
  profile?: string;
  teamKey?: string;
  projectId?: string;
  defaultIssueState?: string;
  defaultLabels?: string[];
  defaultAssignee?: string;
}

export interface ResolvedConfig {
  profileName: string;
  apiKey?: string;
  config: LtuiConfig;
  projectConfig: ProjectConfig;
}

function configDir(): string {
  const override = process.env.LTUI_CONFIG_DIR;
  if (override && override.length > 0) return override;
  return path.join(os.homedir(), '.config', 'ltui');
}

export function getConfigDirectory(): string {
  return configDir();
}

function readJsonFile<T>(filePath: string): T | {} {
  try {
    const data = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(data) as T;
  } catch {
    return {};
  }
}

function writeJsonFile(filePath: string, data: unknown): void {
  const dir = path.dirname(filePath);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2), { mode: 0o600 });
}

export function loadGlobalConfig(): LtuiConfig {
  const file = path.join(configDir(), 'config.json');
  return readJsonFile<LtuiConfig>(file) as LtuiConfig;
}

export function saveGlobalConfig(config: LtuiConfig): void {
  const file = path.join(configDir(), 'config.json');
  writeJsonFile(file, config);
}

export function loadProfilesFile(): Record<string, { apiKey: string }> {
  const file = path.join(configDir(), 'profiles.json');
  return readJsonFile<Record<string, { apiKey: string }>>(file) as Record<
    string,
    { apiKey: string }
  >;
}

export function saveProfilesFile(profiles: Record<string, { apiKey: string }>): void {
  const file = path.join(configDir(), 'profiles.json');
  writeJsonFile(file, profiles);
}

export function loadProjectConfig(cwd: string = process.cwd()): ProjectConfig {
  const file = path.join(cwd, '.ltui.json');
  return readJsonFile<ProjectConfig>(file) as ProjectConfig;
}

export function saveProjectConfig(config: ProjectConfig, cwd: string = process.cwd()): void {
  const file = path.join(cwd, '.ltui.json');
  writeJsonFile(file, config);
}

export function resolveConfig(explicitProfile?: string, cwd: string = process.cwd()): ResolvedConfig {
  const globalConfig = loadGlobalConfig();
  const profilesFile = loadProfilesFile();
  const projectConfig = loadProjectConfig(cwd);

  let profileName =
    explicitProfile ||
    projectConfig.profile ||
    process.env.LTUI_PROFILE ||
    globalConfig.defaultProfile ||
    '';

  const envKey = process.env.LINEAR_API_KEY;
  if (envKey && envKey.length > 0) {
    return {
      profileName,
      apiKey: envKey,
      config: globalConfig,
      projectConfig,
    };
  }

  if (!profileName) {
    throw new Error('auth_missing No profile configured and LINEAR_API_KEY not set');
  }

  const profileKeys = profilesFile[profileName];
  const apiKey = profileKeys?.apiKey;

  if (!apiKey) {
    throw new Error(`auth_missing No API key configured for profile '${profileName}'`);
  }

  return {
    profileName,
    apiKey,
    config: globalConfig,
    projectConfig,
  };
}
