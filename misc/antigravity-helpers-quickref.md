# Antigravity Terminal Workaround - Quick Reference

## 🚀 Quick Start

The `AntigravityHelpers` module is now installed and will auto-load in your PowerShell sessions.

## 📋 Available Commands

### `agcmd` - Run CMD Commands

```powershell
# Simple command
agcmd -Command "dir"

# With working directory
agcmd -Command "npm install" -WorkingDirectory "C:\project"

# Command chaining (recommended!)
agcmd -Command "cd C:\project && npm install && npm run build && echo Done"
```

### `agscript` - Run PowerShell Script Files

```powershell
# Execute a .ps1 file
agscript -ScriptPath "C:\scripts\analyze.ps1"
```

### `agrun` - Run PowerShell Code Blocks

```powershell
# Quick PowerShell execution
agrun -ScriptBlock {
    Get-Date
    Get-ChildItem C:\project
    Write-Output "Done"
}

# Keep temp file for debugging
agrun -ScriptBlock { Get-Process } -KeepTempFile
```

## 💡 Common Patterns

### File Operations

```powershell
agcmd -Command "copy *.md backup\ && dir backup\"
agcmd -Command "mkdir C:\project\build && echo Created && dir C:\project"
```

### Development Workflow

```powershell
# Install and build
agcmd -Command "npm install && npm run build" -WorkingDirectory "C:\project"

# Run tests
agcmd -Command "npm test" -WorkingDirectory "C:\project"
```

### PowerShell Analysis

```powershell
agrun -ScriptBlock {
    Set-Location "C:\project"
    $files = Get-ChildItem -Recurse -Filter "*.ts"
    Write-Output "Found $($files.Count) TypeScript files"
    $files | Select-Object Name, Length | Format-Table
}
```

### Environment Checks

```powershell
agrun -ScriptBlock {
    Write-Output "Node: $(node --version)"
    Write-Output "NPM: $(npm --version)"
    Write-Output "Git: $(git --version)"
}
```

## 🎯 Best Practices

1. **Use command chaining** with `&&` for multi-step operations
2. **Always use absolute paths** - don't assume current directory
3. **Add verification** with `echo` and `dir` at the end
4. **For PowerShell**, use `agrun` for quick scripts or `agscript` for files

## 📚 Full Documentation

- **Module README**: `C:\Users\Peace\Documents\PowerShell\Modules\AntigravityHelpers\README.md`
- **Comprehensive Guide**: `terminal-blindness-solution.md` in your Project Workflows folder

## ⚙️ Module Location

```
C:\Users\Peace\Documents\PowerShell\Modules\AntigravityHelpers\
├── AntigravityHelpers.psm1  (Main module)
├── AntigravityHelpers.psd1  (Manifest)
└── README.md                (Documentation)
```

## 🔄 Reload Module

If you make changes to the module:

```powershell
Remove-Module AntigravityHelpers -ErrorAction SilentlyContinue
Import-Module AntigravityHelpers -Force
```

---

**Note**: This is a workaround for Antigravity's terminal integration bug. The Antigravity team should fix the core issue so these helpers become unnecessary.
