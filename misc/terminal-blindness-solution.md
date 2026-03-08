# Antigravity Terminal Blindness - Comprehensive Solution

## 🚨 Problem Summary

Antigravity has a **critical terminal integration bug** where commands hang indefinitely in RUNNING state.

### 🐛 The "Phantom Quote" Bug (Discovered Feb 2026)

Diagnositcs reveal that the agent's runner **appends a trailing double quote (`"`)** to the last argument of every command.

- `dir` becomes `dir"` (Syntax Error)
- `cmd /c dir` becomes `cmd /c dir"` (Valid, but risky)
- `cmd /c "dir"` becomes `cmd /c "dir""` (Syntax Error)

### 🛡️ The Fix: Padding with `& REM`

To neutralize this, we must append `& REM` to **every** command.

- Agent sends: `cmd /c dir & REM`
- System executes: `cmd /c dir & REM"`
- Result: `dir` executes perfectly. `REM"` acts as a comment and absorbs the garbage quote.

| Environment     | Issue                          | Workaround                      |
| --------------- | ------------------------------ | ------------------------------- |
| **Cursor IDE**  | Agent blind, human sees output | Human reports output to agent   |
| **Antigravity** | Blind + Phantom Quote          | **MUST** use `cmd /c ... & REM` |

## ✅ Working Solutions

### 1. CMD Commands with Chaining

Combine the `cmd /c` prefix with command chaining patterns:

```bash
# ✅ WORKS - Single chained command
cmd /c cd C:\path\to\project && dir && echo Done

# ✅ WORKS - File operations with verification
cmd /c copy file1.txt dest\ && copy file2.txt dest\ && dir dest\

# ✅ WORKS - Multi-step with absolute paths
cmd /c cd C:\Users\Peace\Documents\project && mkdir build && echo Build folder created && dir
```

### 2. PowerShell Commands via Script Files

For PowerShell, write commands to a `.ps1` file first:

```bash
# Step 1: Create script file (using write_to_file tool)
# script.ps1 contents:
Get-Date
$PSVersionTable.PSVersion
Get-ChildItem -Path "C:\target\path"
Write-Output "✅ Script complete"

# Step 2: Execute with cmd /c
cmd /c powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File script.ps1
```

**Output:**

```
Tuesday, February 17, 2026 11:22:18 PM

Major         : 5
Minor         : 1
Build         : 22621
Revision      : 4249

    Directory: C:\target\path
Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---          2/17/2026  11:15 PM           1234 file1.txt

✅ Script complete
```

## 📋 Command Templates

### File Operations

```bash
# Create directory structure
cmd /c mkdir C:\project\src && mkdir C:\project\docs && echo Directories created && dir C:\project

# Copy files with verification
cmd /c copy *.md ..\docs\ && echo Files copied && dir ..\docs\

# Move and organize
cmd /c move temp_*.log archive\ && echo Cleanup complete && dir archive\
```

### Development Commands

```bash
# Install dependencies
cmd /c cd C:\project && npm install && echo Dependencies installed

# Build project
cmd /c cd C:\project && npm run build && echo Build complete && dir dist\

# Run tests
cmd /c cd C:\project && npm test && echo Tests complete
```

### PowerShell Operations (via script file)

```powershell
# analyze.ps1
Set-Location "C:\project"
$files = Get-ChildItem -Recurse -Filter "*.ts"
Write-Output "Total TypeScript files: $($files.Count)"
$files | Select-Object Name, Length | Format-Table
Write-Output "✅ Analysis complete"

# Execute:
cmd /c powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File analyze.ps1
```

## 🎯 Best Practices (Adapted from Cursor Solutions)

### ✅ DO: Command Chaining

```bash
cmd /c cd C:\absolute\path && command1 && command2 && echo Done && dir
```

### ✅ DO: Absolute Paths

```bash
cmd /c cd C:\Users\Peace\Documents\project && npm install
```

### ✅ DO: Built-in Verification

```bash
cmd /c copy file.txt dest\ && echo Copy complete && dir dest\
```

### ✅ DO: PowerShell via Files

```bash
# Create temp.ps1, then:
cmd /c powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File temp.ps1
```

### ❌ DON'T: Multiple Separate Commands

```bash
# ❌ These will hang
dir
cd project
npm install
```

### ❌ DON'T: PowerShell -Command with Inline Code

```bash
# ❌ Quote escaping breaks this
cmd /c powershell -Command "Get-Date"
```

### ❌ DON'T: Relative Paths

```bash
# ❌ Current directory unknown
cmd /c cd ..\project
```

## 🔧 Advanced Patterns

### Multi-Step Workflow with Error Handling

```bash
# Each && ensures previous command succeeded
cmd /c cd C:\project && npm install && npm run build && npm test && echo All steps complete
```

### PowerShell with Multiple Operations

```powershell
# workflow.ps1
try {
    Set-Location "C:\project"
    Write-Output "📁 Current directory: $(Get-Location)"

    $files = Get-ChildItem -Filter "*.md"
    Write-Output "📄 Found $($files.Count) markdown files"

    Copy-Item "*.md" -Destination "C:\backup\" -Force
    Write-Output "✅ Backup complete"

    Get-ChildItem "C:\backup\" | Select-Object Name, Length
} catch {
    Write-Output "❌ Error: $_"
}

# Execute:
cmd /c powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File workflow.ps1
```

### Environment Verification

```powershell
# verify-env.ps1
Write-Output "=== Environment Check ==="
Write-Output "Node: $(node --version)"
Write-Output "NPM: $(npm --version)"
Write-Output "Git: $(git --version)"
Write-Output "PowerShell: $($PSVersionTable.PSVersion)"
Write-Output "Current Path: $(Get-Location)"
Write-Output "✅ Environment verified"

# Execute:
cmd /c powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File verify-env.ps1
```

## 🚫 Anti-Patterns to Avoid

1. **Running commands without `cmd /c` prefix** - They will hang
2. **Using PowerShell `-Command` with inline code** - Quote escaping fails
3. **Assuming current directory** - Always use absolute paths
4. **Multiple separate command calls** - Chain them with `&&` instead
5. **Continuing after failures** - Use `&&` to auto-stop on errors

## 📊 Success Indicators

- ✅ Commands complete within 3-5 seconds
- ✅ Full output visible in tool response
- ✅ Verification commands show expected results
- ✅ No "RUNNING" state that persists indefinitely

## 🏢 Credits

This solution combines:

- **Antigravity-specific workarounds** discovered through testing
- **Command chaining patterns** from [terminal-blindness-solutions](https://github.com/thomisont/terminal-blindness-solutions)
- **Best practices** from PowerShift Intelligence's research

## 📄 Related Resources

- [Cursor Terminal Blindness Solutions](https://github.com/thomisont/terminal-blindness-solutions)
- [Terminal Process Guide](https://github.com/thomisont/terminal-blindness-solutions/blob/main/docs/terminal-process-guide.md)
- [Command Templates](https://github.com/thomisont/terminal-blindness-solutions/blob/main/examples/command-templates.md)

---

**This is a temporary workaround. The Antigravity team should fix the core terminal integration to properly capture command output without requiring the `cmd /c` prefix.**
