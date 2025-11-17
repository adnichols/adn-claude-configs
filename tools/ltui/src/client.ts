import { createRequire } from 'node:module';
import path from 'node:path';
import { LinearClient } from '@linear/sdk';
import type { ResolvedConfig } from './config.js';

let cachedClient: any = null;
const requireFn = createRequire(import.meta.url);

export function createLinearClient(resolved: ResolvedConfig): LinearClient {
  if (cachedClient) return cachedClient;
  const mockModule = process.env.LTUI_TEST_CLIENT_MODULE;
  if (mockModule) {
    const resolvedPath = path.resolve(mockModule);
    const factory = requireFn(resolvedPath);
    if (typeof factory.createMockLinearClient !== 'function') {
      throw new Error('mock_error Invalid LTUI_TEST_CLIENT_MODULE');
    }
    cachedClient = factory.createMockLinearClient(resolved);
    return cachedClient;
  }
  if (!resolved.apiKey) {
    throw new Error('auth_missing No API key available for Linear client');
  }
  cachedClient = new LinearClient({ apiKey: resolved.apiKey });
  return cachedClient;
}
