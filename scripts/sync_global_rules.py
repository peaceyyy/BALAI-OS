import os
import shutil
import argparse
import sys

def sync_global_rules(target=None):
    """
    Syncs the Global Rules to specified targets.
    target: 'antigravity', 'copilot', or None (both)
    """
    
    print("=" * 60)
    print("🌐 SYNCING GLOBAL RULES")
    print("=" * 60)

    # Source: The Single Source of Truth
    # Located in .agent/global_instructions.md relative to the project root
    # script is in /scripts, so we go up one level to root, then into .agent
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src_rules = os.path.join(base_dir, ".agent", "global_instructions.md")
    
    if not os.path.exists(src_rules):
        print(f"\n❌ ERROR: Source file not found at {src_rules}")
        return False

    targets = []
    
    # 1. Antigravity Global Rules
    # Directory: %USERPROFILE%\.gemini
    antigravity_dir = os.path.expandvars(r"%USERPROFILE%\.gemini")
    
    # 2. VS Code Copilot Rules
    # Directory: %APPDATA%\Code\User\.github
    vscode_github_dir = os.path.expandvars(r"%APPDATA%\Code\User\.github")

    # Define targets based on arguments
    if target == "antigravity" or target is None:
        targets.append({
            "name": "Antigravity Global Rules",
            "dir": antigravity_dir,
            "filename": "GEMINI.md" 
        })
        
    if target == "copilot" or target is None:
        targets.append({
            "name": "VS Code Copilot Rules",
            "dir": vscode_github_dir,
            "filename": "copilot-instructions.md"
        })

    success = True
    
    for t in targets:
        dst_dir = t["dir"]
        dst_file = os.path.join(dst_dir, t["filename"])
        
        print(f"\n📂 Source: {src_rules}")
        print(f"🎯 Target ({t['name']}): {dst_file}")
        
        try:
            # Ensure directory exists
            os.makedirs(dst_dir, exist_ok=True)
            
            # Read source content
            with open(src_rules, 'r', encoding='utf-8') as f_src:
                content = f_src.read()
            
            # Write to destination
            with open(dst_file, 'w', encoding='utf-8') as f_dst:
                f_dst.write(content)
                
            print(f"✅ Synced successfully to {t['name']}")
            
        except Exception as e:
            print(f"❌ Failed to sync to {t['name']}: {e}")
            success = False

    return success

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync Global Rules (GEMINI.md / global_instructions.md)")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--antigravity", action="store_true", help="Sync only to Antigravity global rules")
    group.add_argument("--copilot", action="store_true", help="Sync only to VS Code Copilot rules")
    
    args = parser.parse_args()
    
    target = None
    if args.antigravity:
        target = "antigravity"
    elif args.copilot:
        target = "copilot"
        
    run_success = sync_global_rules(target)
    
    print("\n" + "=" * 60)
    if run_success:
        print("✨ Done.")
    else:
        print("⚠️  Sync incomplete.")
    print("=" * 60)
