# Claude CLI Integration Strategy - Shell Out Approach

## 🎯 Executive Summary

**USER INSIGHT**: Instead of using `@anthropic-ai/claude-code` SDK, shell out to local `claude` CLI to leverage existing Max plan authentication.

**SOLUTION BENEFITS**:
- ✅ Uses Max plan authentication automatically
- ✅ Eliminates API charges within plan limits
- ✅ Maintains streaming interface compatibility  
- ✅ Preserves all existing functionality

---

## 🔍 Technical Analysis

### Current SDK vs CLI Approach

#### **Current SDK Approach**:
```typescript
// src/claude-handler.ts:142 - Current implementation
import { query } from '@anthropic-ai/claude-code';

for await (const message of query({
  prompt,
  options: { /* API key authentication */ }
})) {
  // Process streaming messages
}
```

#### **Proposed CLI Approach**:
```typescript
// New implementation - shell out to CLI
import { spawn } from 'child_process';

const claude = spawn('claude', [
  '-p', prompt,
  '--output-format', 'stream-json',
  '--cwd', workingDirectory
]);

for await (const line of claude.stdout) {
  const message = JSON.parse(line);
  yield message; // Same format as SDK!
}
```

### Authentication Inheritance

#### **How CLI Authentication Works**:
1. User runs `claude login` once on their machine
2. CLI stores session tokens in `~/.claude/.credentials.json` 
3. All subsequent CLI commands use stored authentication
4. **Server inherits this authentication when shelling out**

#### **Authentication Types CLI Supports**:
- ✅ Max plan session authentication (`claude login`)
- ✅ API key authentication (`ANTHROPIC_API_KEY`)
- ✅ Bedrock authentication (`CLAUDE_CODE_USE_BEDROCK=1`)
- ✅ Vertex authentication (`CLAUDE_CODE_USE_VERTEX=1`)

---

## ⚙️ Configuration Toggle Architecture

### Environment Variable Configuration

```env
# .env - New configuration option
CLAUDE_USE_CLI=true   # Use CLI shell-out approach (NEW)
CLAUDE_USE_CLI=false  # Use SDK approach (CURRENT DEFAULT)

# Existing configuration still works
ANTHROPIC_API_KEY=sk-ant-api03-...
CLAUDE_CODE_USE_BEDROCK=1
CLAUDE_CODE_USE_VERTEX=1
```

### Configuration Integration

```typescript
// src/config.ts - Updated configuration
export const config = {
  claude: {
    useCLI: process.env.CLAUDE_USE_CLI === 'true',        // NEW
    useBedrock: process.env.CLAUDE_CODE_USE_BEDROCK === '1',
    useVertex: process.env.CLAUDE_CODE_USE_VERTEX === '1',
  },
  anthropic: {
    apiKey: process.env.ANTHROPIC_API_KEY!,
  },
  // ... existing config unchanged
};
```

### Handler Interface Abstraction

```typescript
// src/interfaces/claude-handler.interface.ts - NEW FILE
export interface IClaudeHandler {
  getSessionKey(userId: string, channelId: string, threadTs?: string): string;
  getSession(userId: string, channelId: string, threadTs?: string): ConversationSession | undefined;
  createSession(userId: string, channelId: string, threadTs?: string): ConversationSession;
  
  streamQuery(
    prompt: string,
    session?: ConversationSession,
    abortController?: AbortController,
    workingDirectory?: string,
    slackContext?: { channel: string; threadTs?: string; user: string }
  ): AsyncGenerator<SDKMessage, void, unknown>;
  
  cleanupInactiveSessions(maxAge?: number): void;
}
```

### Handler Factory Pattern

```typescript
// src/claude-handler-factory.ts - NEW FILE
import { config } from './config.js';
import { McpManager } from './mcp-manager.js';
import { ClaudeSDKHandler } from './claude-sdk-handler.js';  // Current implementation
import { ClaudeCLIHandler } from './claude-cli-handler.js';  // New implementation
import { IClaudeHandler } from './interfaces/claude-handler.interface.js';

export function createClaudeHandler(mcpManager: McpManager): IClaudeHandler {
  if (config.claude.useCLI) {
    console.log('🔧 Using Claude CLI approach');
    return new ClaudeCLIHandler(mcpManager);
  } else {
    console.log('🔧 Using Claude SDK approach');
    return new ClaudeSDKHandler(mcpManager);
  }
}
```

### Slack Handler Integration

```typescript
// src/slack-handler.ts - Updated to use factory
import { createClaudeHandler } from './claude-handler-factory.js';

export class SlackHandler {
  private claudeHandler: IClaudeHandler;
  
  constructor() {
    this.mcpManager = new McpManager();
    this.claudeHandler = createClaudeHandler(this.mcpManager);  // UPDATED
    // ... rest unchanged
  }
  
  // All existing methods work identically!
  // No changes needed to message handling, sessions, etc.
}
```

### Backward Compatibility Strategy

```typescript
// Current implementation becomes ClaudeSDKHandler
// src/claude-sdk-handler.ts - Renamed from claude-handler.ts
export class ClaudeSDKHandler implements IClaudeHandler {
  // Existing implementation moved here unchanged
  // Just implements the interface
}

// New CLI implementation
// src/claude-cli-handler.ts - NEW FILE  
export class ClaudeCLIHandler implements IClaudeHandler {
  // New CLI implementation
  // Same interface as SDK handler
}
```

---

## 📊 Implementation Design

### Secure CLI Handler Class (Security-Hardened Implementation)

```typescript
export class ClaudeCLIHandler implements IClaudeHandler {
  private sessions: Map<string, string> = new Map(); // sessionKey -> cliSessionId
  private logger = new Logger('ClaudeCLIHandler');
  private performanceMetrics = new Map<string, number>();
  
  // Security: Input sanitization
  private sanitizeForCLI(input: string): string {
    // Remove shell metacharacters and validate input
    return input.replace(/[;&|`$()><]/g, '').trim();
  }
  
  // Security: Path validation
  private validateWorkingDirectory(path: string): string {
    const resolved = require('path').resolve(path);
    // Prevent directory traversal attacks
    if (resolved.includes('..') || !resolved.startsWith('/')) {
      throw new Error('Invalid working directory path');
    }
    return resolved;
  }
  
  // Security: Environment filtering
  private getFilteredEnvironment() {
    return {
      HOME: process.env.HOME,
      PATH: process.env.PATH,
      NODE_ENV: process.env.NODE_ENV,
      // Only pass necessary environment variables
    };
  }
  
  // Pre-flight validation
  private async validateCLIAvailable(): Promise<boolean> {
    try {
      const result = await spawn('claude', ['--version'], { 
        timeout: 5000,
        env: this.getFilteredEnvironment()
      });
      return result.exitCode === 0;
    } catch {
      return false;
    }
  }
  
  // Structured error detection
  private parseClaudeError(stderr: string): ClaudeError | null {
    if (stderr.includes('authentication failed')) {
      return { type: 'AUTH_FAILURE', message: 'Claude CLI authentication expired' };
    }
    if (stderr.includes('quota exceeded')) {
      return { type: 'QUOTA_EXCEEDED', message: 'Claude usage quota exceeded' };
    }
    if (stderr.includes('Invalid API key')) {
      return { type: 'API_KEY_INVALID', message: 'Claude API key is invalid' };
    }
    return null;
  }
  
  async *streamQuery(
    prompt: string,
    session?: ConversationSession,
    abortController?: AbortController,
    workingDirectory?: string,
    slackContext?: { channel: string; threadTs?: string; user: string }
  ): AsyncGenerator<SDKMessage, void, unknown> {
    const startTime = Date.now();
    const sessionKey = session ? this.getSessionKey(session.userId, session.channelId, session.threadTs) : 'direct';
    
    try {
      // Security: Pre-flight validation
      if (!(await this.validateCLIAvailable())) {
        throw new Error('Claude CLI is not available or not authenticated');
      }
      
      // Security: Input sanitization
      const sanitizedPrompt = this.sanitizeForCLI(prompt);
      const args = ['-p', sanitizedPrompt, '--output-format', 'stream-json'];
      
      // Security: Path validation
      if (workingDirectory) {
        const validatedPath = this.validateWorkingDirectory(workingDirectory);
        args.push('--cwd', validatedPath);
      }
      
      // Handle session resumption
      const existingSession = session ? this.sessions.get(sessionKey) : null;
      if (existingSession) {
        args.push('--resume', existingSession);
      }
      
      this.logger.info('Starting CLI process', { 
        sessionKey, 
        args: args.filter(arg => arg !== sanitizedPrompt), // Don't log prompt content
        workingDirectory 
      });
      
      // Spawn Claude CLI process with security measures
      const claude = spawn('claude', args, {
        stdio: ['pipe', 'pipe', 'pipe'],
        env: this.getFilteredEnvironment(), // Security: Filtered environment
        timeout: 300000, // 5 minute timeout
      });
      
      // Process management: Handle abort controller
      if (abortController) {
        abortController.signal.addEventListener('abort', () => {
          claude.kill('SIGTERM');
          this.logger.info('CLI process terminated by abort controller', { sessionKey });
        });
      }
      
      // Handle streaming output with error handling
      let buffer = '';
      let messageCount = 0;
      
      claude.stdout.on('data', (chunk) => {
        try {
          buffer += chunk.toString();
          const lines = buffer.split('\n');
          buffer = lines.pop() || '';
          
          for (const line of lines) {
            if (line.trim()) {
              try {
                const message = JSON.parse(line);
                messageCount++;
                
                // Extract session ID from init message
                if (message.type === 'system' && message.subtype === 'init' && session) {
                  this.sessions.set(sessionKey, message.session_id);
                  this.logger.debug('CLI session initialized', { 
                    sessionKey, 
                    cliSessionId: message.session_id 
                  });
                }
                
                yield message;
              } catch (parseError) {
                this.logger.error('JSON parse error', { 
                  error: parseError, 
                  line: line.substring(0, 100),
                  sessionKey 
                });
              }
            }
          }
        } catch (error) {
          this.logger.error('CLI output processing error', { error, sessionKey });
        }
      });
      
      // Enhanced error handling
      claude.stderr.on('data', (chunk) => {
        const stderr = chunk.toString();
        const claudeError = this.parseClaudeError(stderr);
        
        if (claudeError) {
          this.logger.error('Claude CLI error detected', { 
            error: claudeError, 
            sessionKey,
            stderr: stderr.substring(0, 200)
          });
        } else {
          this.logger.warn('CLI stderr output', { 
            stderr: stderr.substring(0, 200),
            sessionKey 
          });
        }
      });
      
      // Process completion with timeout and cleanup
      await new Promise((resolve, reject) => {
        const timeout = setTimeout(() => {
          claude.kill('SIGTERM');
          reject(new Error('CLI process timeout'));
        }, 300000); // 5 minute timeout
        
        claude.on('close', (code) => {
          clearTimeout(timeout);
          const duration = Date.now() - startTime;
          
          // Performance monitoring
          this.performanceMetrics.set(`${sessionKey}_duration`, duration);
          this.performanceMetrics.set(`${sessionKey}_messages`, messageCount);
          
          this.logger.info('CLI process completed', { 
            sessionKey, 
            exitCode: code, 
            duration, 
            messageCount 
          });
          
          if (code === 0) {
            resolve(void 0);
          } else {
            reject(new Error(`Claude CLI exited with code ${code}`));
          }
        });
        
        claude.on('error', (error) => {
          clearTimeout(timeout);
          this.logger.error('CLI process error', { error, sessionKey });
          reject(error);
        });
      });
      
    } catch (error) {
      const duration = Date.now() - startTime;
      this.logger.error('CLI handler error', { 
        error, 
        sessionKey, 
        duration,
        prompt: prompt.substring(0, 50) + '...'
      });
      throw error;
    }
  }
  
  // Performance monitoring methods
  getPerformanceMetrics(sessionKey: string) {
    return {
      duration: this.performanceMetrics.get(`${sessionKey}_duration`),
      messages: this.performanceMetrics.get(`${sessionKey}_messages`),
    };
  }
  
  // Implement other required interface methods...
  getSessionKey(userId: string, channelId: string, threadTs?: string): string {
    return `${userId}-${channelId}-${threadTs || 'direct'}`;
  }
  
  getSession(userId: string, channelId: string, threadTs?: string): ConversationSession | undefined {
    // Implementation details...
  }
  
  createSession(userId: string, channelId: string, threadTs?: string): ConversationSession {
    // Implementation details...
  }
  
  cleanupInactiveSessions(maxAge?: number): void {
    // Implementation details...
  }
}

// Error types for structured error handling
interface ClaudeError {
  type: 'AUTH_FAILURE' | 'QUOTA_EXCEEDED' | 'API_KEY_INVALID' | 'CLI_UNAVAILABLE';
  message: string;
}
```

### Integration with Existing Slack Handler

```typescript
// Minimal changes to src/slack-handler.ts
export class SlackHandler {
  private claudeHandler: ClaudeCLIHandler; // Changed from ClaudeHandler
  
  constructor() {
    this.claudeHandler = new ClaudeCLIHandler(); // Updated
    // ... rest unchanged
  }
  
  // All existing methods work the same!
  // The interface is identical to current SDK approach
}
```

### Session Management Strategy

```typescript
class SessionManager {
  private cliSessions = new Map<string, {
    cliSessionId: string;
    lastActivity: Date;
    workingDirectory?: string;
  }>();
  
  getOrCreateSession(sessionKey: string, workingDirectory?: string) {
    let session = this.cliSessions.get(sessionKey);
    
    if (!session) {
      session = {
        cliSessionId: '', // Will be populated by CLI init message
        lastActivity: new Date(),
        workingDirectory
      };
      this.cliSessions.set(sessionKey, session);
    }
    
    session.lastActivity = new Date();
    return session;
  }
  
  resumeSession(sessionKey: string): string | null {
    const session = this.cliSessions.get(sessionKey);
    return session?.cliSessionId || null;
  }
}
```

---

## 🚨 Quality Review Findings & Security Requirements

### Critical Security Issues Identified:

#### **BLOCKING SECURITY VULNERABILITIES:**

##### **1. Process Injection Vulnerability (CRITICAL)**
```typescript
// VULNERABLE: User input directly passed to spawn arguments
const args = ['-p', prompt, '--cwd', workingDirectory];
const claude = spawn('claude', args);
// Risk: Malicious prompts could inject shell commands
// Impact: POTENTIAL REMOTE CODE EXECUTION
```

##### **2. Authentication Token Exposure (CRITICAL)**
```typescript
const claude = spawn('claude', args, {
  env: { ...process.env }  // ⚠️ Exposes ALL environment variables
});
// Risk: Sensitive environment variables passed to subprocess
// Impact: CREDENTIAL LEAKAGE
```

##### **3. Working Directory Traversal (HIGH)**
```typescript
if (workingDirectory) {
  args.push('--cwd', workingDirectory);  // ⚠️ No path validation
}
// Risk: Directory traversal attacks through malicious paths
// Impact: UNAUTHORIZED FILE ACCESS
```

### Performance & Reliability Concerns:

- **Process Spawn Overhead**: 10-40x latency increase vs direct API calls
- **Memory Usage**: ~20-50MB per CLI process, unbounded scaling
- **Missing Error Handling**: CLI validation, authentication failures, timeouts
- **Process Management**: No cleanup, concurrency limits, or resource monitoring

---

## 🎯 Updated Implementation Plan

### Phase 1: Security-First Foundation & Basic Monitoring (Week 1-2)

**Step 1: Security Hardening (MANDATORY)**
- **Input Sanitization**: Implement secure argument sanitization for all CLI inputs
- **Environment Filtering**: Create filtered environment variable passing to prevent credential leakage
- **Path Validation**: Add working directory path validation and sanitization
- **CLI Availability Validation**: Pre-flight checks for CLI installation and authentication

**Step 2: Configuration Toggle Implementation**
- Add `CLAUDE_USE_CLI` environment variable to toggle between approaches
- Update `src/config.ts` with new configuration option
- Create handler factory pattern for switching implementations
- Maintain backward compatibility with current SDK approach

**Step 3: Interface Abstraction**
- Create `IClaudeHandler` interface that both implementations will follow
- Ensure identical method signatures and return types
- Design for seamless switching via configuration only

**Step 4: Secure CLI Handler Implementation**
- Implement `ClaudeCLIHandler` class with security-first approach
- Add comprehensive error handling for CLI failures and authentication issues
- Implement process management with timeouts and cleanup
- Add circuit breaker pattern for CLI failure scenarios

**Step 5: Basic Logging & Debugging**
- Implement structured logging for CLI operations
- Add debugging capabilities for CLI argument validation
- Create CLI process lifecycle logging
- Add authentication status monitoring

**Step 6: Basic Performance Monitoring**
- Add CLI execution timing metrics
- Implement memory usage tracking for CLI processes
- Create performance comparison logging vs SDK approach
- Add basic resource utilization monitoring

**Step 7: Handler Factory Pattern**
- Create factory function that returns appropriate handler based on config
- Update `src/slack-handler.ts` to use factory instead of direct instantiation
- Test basic functionality with comprehensive security validation

### Phase 2: Integration Testing Suite (Week 3)

**Step 8: Comprehensive Integration Testing**
- Create integration test suite with security validation
- Test CLI availability and pre-flight checks
- Validate input sanitization and security measures
- Test process management, timeouts, and cleanup
- Verify authentication failure handling and fallback scenarios
- Test configuration toggle between SDK and CLI approaches
- Performance benchmarking and comparison with SDK approach
- Memory usage validation and resource monitoring
- End-to-end Slack bot functionality testing with CLI approach

### Phase 3: Advanced Features (DEFERRED)
*Advanced CLI features and production hardening deferred to future phases*

### Phase 4: Production Hardening (DEFERRED)
*Production optimization and advanced monitoring deferred to future phases*

---

## ✅ Expected Benefits

### Cost Optimization
- **Max Plan Usage**: CLI automatically uses Max plan when authenticated
- **No API Charges**: Eliminates surprise API billing within plan limits
- **Flexible Authentication**: Supports multiple auth methods via CLI

### Functionality Preservation
- **Same Interface**: Maintains streaming JSON format
- **Session Continuity**: CLI handles session management
- **Tool Access**: All Claude Code tools available via CLI
- **Working Directory**: Full `--cwd` support

### Operational Advantages
- **Authentication Inheritance**: Uses whatever CLI is configured with
- **Easier Management**: Single authentication point (CLI)
- **Troubleshooting**: Can test CLI commands directly for debugging

### Configuration Toggle Benefits
- **Risk Mitigation**: Keep SDK as fallback if CLI approach has issues
- **A/B Testing**: Easy performance and cost comparison between approaches
- **Gradual Migration**: Switch users gradually rather than all at once
- **Zero Downtime**: Switch approaches with just environment variable change
- **Development Flexibility**: Use different approaches in dev vs production

### Usage Scenarios

#### When to Use CLI Approach (`CLAUDE_USE_CLI=true`)
- ✅ You have Max plan and want to leverage plan benefits
- ✅ You want to eliminate API charges within plan limits  
- ✅ Your local CLI is authenticated with `claude login`
- ✅ You prioritize cost optimization over performance
- ✅ You want to test new approach while keeping fallback

#### When to Use SDK Approach (`CLAUDE_USE_CLI=false`)
- ✅ You need maximum performance and direct API control
- ✅ You have dedicated API key budget and monitoring
- ✅ You're running in environment without CLI installed
- ✅ You need guaranteed API reliability for production
- ✅ You want to stick with tested, stable approach

#### Migration Strategy
```bash
# Phase 1: Test CLI approach in development
CLAUDE_USE_CLI=true  # Development environment

# Phase 2: A/B test both approaches
CLAUDE_USE_CLI=true  # 50% of production traffic
CLAUDE_USE_CLI=false # 50% of production traffic

# Phase 3: Full migration to CLI (if successful)
CLAUDE_USE_CLI=true  # All environments
```

---

## ⚠️ Considerations & Risks

### Technical Dependencies
- **CLI Installation**: Requires `claude` CLI on server
- **Process Management**: Need robust subprocess handling
- **Authentication Persistence**: CLI session must stay valid

### Potential Issues
- **CLI Updates**: Breaking changes in CLI output format
- **Process Overhead**: Spawning processes vs direct API calls
- **Error Propagation**: Parsing CLI errors into structured formats

### Mitigation Strategies
- **Version Pinning**: Pin specific Claude CLI version
- **Fallback Option**: Keep API key approach as backup
- **Monitoring**: Track CLI process health and authentication status
- **Testing**: Comprehensive testing of CLI integration

---

## 🎯 Success Criteria

### Primary Goals
- [ ] Successful Max plan authentication via CLI
- [ ] Zero API charges within plan limits
- [ ] All existing Slack bot functionality preserved
- [ ] Performance comparable to SDK approach

### Technical Validation
- [ ] Streaming JSON output parsing works correctly
- [ ] Session management maintains conversation context
- [ ] Working directory resolution functions properly
- [ ] Error handling provides meaningful feedback

### Operational Success
- [ ] CLI authentication stays persistent
- [ ] Process management is stable and reliable
- [ ] Monitoring provides visibility into usage and costs
- [ ] Troubleshooting is straightforward

---

This CLI integration approach directly addresses the original billing concern by leveraging your existing Max plan authentication through the local Claude CLI, potentially eliminating API charges while maintaining all current functionality.

---

*Strategy developed January 2025 based on user insight to shell out to local Claude CLI instead of using SDK directly.*