import os
import shutil
import argparse
import sys

def sync_agent_directory(target=None):
    """
    Syncs the .agent directory to global root and Copilot directories.
    target: 'root', 'copilot', or None (both)
    """
    
    print("=" * 60)
    print("[SYNC] SYNCING .AGENT DIRECTORY")
    print("=" * 60)

    # Source: The Single Source of Truth
    # Located in .agent relative to the project root
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src_agent = os.path.join(base_dir, ".agent")
    
    if not os.path.exists(src_agent):
        print(f"\n[ERR] Source directory not found at {src_agent}")
        return False

    targets = []
    
    # 1. Root .agent directory
    # "the .agent file [directory] goes to root"
    root_dir = os.path.expandvars(r"%USERPROFILE%\.agent")
    
    # 2. Copilot directory
    # "EVERYTHING INSIDE .agent is to be copied here as well: C:\Users\Peace\.copilot"
    copilot_dir = os.path.expandvars(r"%USERPROFILE%\.copilot")

    # Define targets based on arguments
    if target == "root" or target is None:
        targets.append({
            "name": "Root .agent Directory",
            "dir": root_dir
        })
        
    if target == "copilot" or target is None:
        targets.append({
            "name": "Copilot Directory",
            "dir": copilot_dir
        })

    success = True
    
    for t in targets:
        dst_dir = t["dir"]
        
        print(f"\n[SRC] Source: {src_agent}")
        print(f"[DST] Target ({t['name']}): {dst_dir}")
        
        try:
            # Ensure target directory base exists (handled by copytree with dirs_exist_ok=True)
            # copytree copies the *contents* of src_agent directly into dst_dir
            shutil.copytree(src_agent, dst_dir, dirs_exist_ok=True)
                
            print(f"[OK] Synced successfully to {t['name']}")
            
        except Exception as e:
            print(f"[ERR] Failed to sync to {t['name']}: {e}")
            success = False

    return success

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync .agent directory to global locations")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--root", action="store_true", help="Sync only to root .agent directory")
    group.add_argument("--copilot", action="store_true", help="Sync only to Copilot directory")
    
    args = parser.parse_args()
    
    target = None
    if args.root:
        target = "root"
    elif args.copilot:
        target = "copilot"
        
    run_success = sync_agent_directory(target)
    
    print("\n" + "=" * 60)
    if run_success:
        print("[DONE] Done.")
    else:
        print("[WARN]  Sync incomplete.")
    print("=" * 60)
