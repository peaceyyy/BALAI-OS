# Bug Report: Terminal Integration - Commands Hang Indefinitely

- Generated with the help of Antigravity

## Summary

**Severity**: Critical  
**Impact**: All terminal command execution  
**Affected Platform**: Windows (cmd.exe and PowerShell)  
**Status**: Workaround available, core fix needed

Terminal commands executed via the `run_command` tool hang indefinitely in RUNNING state, preventing both the AI agent and user from seeing command output. This breaks automated workflows and requires manual workarounds.

---

## Problem Description

### What Happens

1. Agent calls `run_command` with any command (e.g., `dir`, `npm install`, `powershell -Command "Get-Date"`)
2. Command enters RUNNING state and never completes
3. No output is captured or returned
4. Command hangs indefinitely until manually terminated
5. Both agent and user are blind to execution results

### Expected Behavior

1. Command executes
2. Output is captured
3. Command completes with exit code
4. Output is returned to agent within reasonable time (< 5 seconds for simple commands)

### Actual Behavior

```
Status: RUNNING
Output delta since last status check:
Microsoft Windows [Version 10.0.22621.4317]
(c) Microsoft Corporation. All rights reserved.

c:\Users\User\.gemini\antigravity\playground\charged-observatory>
```

Command never proceeds beyond the prompt. No actual command output appears.

---

## Reproduction Steps

### Minimal Test Case

```python
# Any of these commands will hang:
run_command("dir")
run_command("echo test")
run_command("powershell -Command 'Get-Date'")
run_command("node --version")
```

**Result**: All hang in RUNNING state indefinitely.

### 🐛 The "Phantom Quote" Bug (Critical Discovery)

Diagnostics reveal that the agent runner **appends a trailing double quote (`"`)** to the last argument of every command.

- `dir` -> `dir"` (Syntax Error)
- `cmd /c dir` -> `cmd /c dir"` (Starts interactive shell or waits?)
- `cmd /c "dir"` -> `cmd /c "dir""` (Syntax Error)

### Working Workaround

```python
# These work correctly (The Padding Workaround):
run_command("cmd /c dir & REM")
run_command("cmd /c echo test & REM")
run_command("cmd /c powershell.exe ... -File script.ps1 & REM")
```

**Result**: Commands complete successfully and return output.

---

## Root Cause Analysis

### Hypothesis

Antigravity is spawning an **interactive cmd.exe shell** AND simultaneously **appending a phantom trailing quote** to commands. The shell waits for input (or fails silently due to syntax errors), causing the hang.

### Evidence

1. **Commands with `cmd /c` prefix work** - This forces non-interactive execution
2. **Output shows only the shell banner and prompt** - No command execution
3. **Sending newline via `send_command_input` advances the prompt** - Confirms interactive shell behavior
4. **Similar to Cursor IDE issue** - Documented at https://github.com/thomisont/terminal-blindness-solutions

### Comparison with Working Implementation

**VS Code GitHub Copilot** does NOT have this issue, suggesting they use a different terminal integration approach (likely the VS Code terminal API directly).

---

## Proposed Fix

### Option 1: Auto-Prefix Commands (Quick Fix)

Automatically wrap all commands with `cmd /c` before execution:

```python
def run_command(command: str, cwd: str, ...):
    # Current (broken):
    # subprocess.Popen(command, shell=True, cwd=cwd, ...)

    # Fixed:
    wrapped_command = f"cmd /c {command}"
    subprocess.Popen(wrapped_command, shell=True, cwd=cwd, ...)
```

**Pros**: Minimal code change, immediate fix  
**Cons**: Doesn't address root cause

### Option 2: Use Non-Interactive Shell (Proper Fix)

Execute commands directly without spawning an interactive shell:

```python
def run_command(command: str, cwd: str, ...):
    # Parse command into executable and args
    # Execute directly without shell=True
    subprocess.Popen(
        command,
        shell=False,  # Don't spawn interactive shell
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.DEVNULL,  # No interactive input
        creationflags=subprocess.CREATE_NO_WINDOW  # Windows-specific
    )
```

**Pros**: Proper fix, better security, faster execution  
**Cons**: Requires more testing

### Option 3: Use PowerShell Core Directly (Modern Approach)

For Windows, use PowerShell Core (pwsh) with explicit non-interactive flags:

```python
def run_command(command: str, cwd: str, ...):
    if platform.system() == "Windows":
        wrapped_command = [
            "pwsh.exe",
            "-NoProfile",
            "-NonInteractive",
            "-Command",
            command
        ]
        subprocess.Popen(wrapped_command, cwd=cwd, ...)
```

**Pros**: Modern, consistent, works with PowerShell scripts  
**Cons**: Requires PowerShell Core installation

---

## User-Created Workaround

While waiting for a fix, we've created:

### 1. PowerShell Helper Module

Location: `C:\Users\User\Documents\PowerShell\Modules\AntigravityHelpers\`

Functions:

- `agcmd` - Wraps commands with `cmd /c` automatically
- `agrun` - Executes PowerShell script blocks
- `agscript` - Runs PowerShell script files

### 2. Documentation

- Comprehensive guide: `terminal-blindness-solution.md`

### 3. Knowledge Item

Created KI at `.gemini/antigravity/knowledge/terminal-blindness-workaround/` for future agent awareness.

---

## Impact Assessment

### Current Impact

- **100% of terminal commands affected** on Windows
- **Severe productivity loss** - agents cannot automate workflows
- **Manual intervention required** for every command
- **User frustration** - need to explain workaround in every conversation

### Post-Fix Impact

- Automated workflows function correctly
- No manual workarounds needed
- Consistent behavior across platforms
- Better user experience

---

## Testing Recommendations

### Test Cases

```python
# Basic commands
assert run_command("dir").status == "COMPLETED"
assert run_command("echo test").output.contains("test")

# PowerShell
assert run_command("powershell -Command 'Get-Date'").status == "COMPLETED"

# Command chaining
assert run_command("cd C:\\project && npm install").status == "COMPLETED"

# Error handling
assert run_command("invalid_command").status == "FAILED"
assert run_command("invalid_command").exit_code != 0
```

### Platforms to Test

- ✅ Windows 10/11 (cmd.exe)
- ✅ Windows PowerShell 5.1
- ✅ PowerShell Core 7.x
- ✅ macOS (bash/zsh)
- ✅ Linux (bash)

---

## Related Issues

- **Cursor IDE Terminal Blindness**: GitHub Issue #2977
- **Community Research**: https://github.com/thomisont/terminal-blindness-solutions
- **VS Code API Limitations**: `terminal.shellIntegration.executeCommand` level

---

## Additional Context

### Environment Details

- **OS**: Windows 10.0.22621.4317
- **Shell**: cmd.exe (default), PowerShell 5.1
- **Antigravity Version**: [Current version]
- **Workspace**: Multiple tested, issue consistent

### Logs

Command execution logs show:

```
Background command ID: [uuid]
Output snapshot:
Microsoft Windows [Version 10.0.22621.4317]
(c) Microsoft Corporation. All rights reserved.

c:\path\to\directory>
[hangs here indefinitely]
```

---

## Recommendation

**Implement Option 2 (Non-Interactive Shell)** as the proper fix, with Option 1 as a temporary hotfix if needed urgently.

This is a **critical bug** affecting core functionality. The fix is straightforward and should be prioritized for the next release.

---
