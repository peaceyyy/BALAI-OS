import os
import shutil
import sys
import argparse
import time

def sync_protocols(target_root=None, force_mode=False, sync_refs=True):
    """
    Synchronizes .agent/protocols and .agent/protocols/references to a target directory.
    Target directory defaults to cwd, or ~/.copilot if --copilot is used.
    """
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    if target_root is None:
        target_root = os.getcwd()
    
    target_root = os.path.abspath(target_root)
    
    print(f"🚀 Starting Sync Protocols Script")
    print(f"📂 Project Root: {project_root}")
    print(f"🎯 Target Root:  {target_root}")
    if force_mode:
        print(f"⚠️  FORCE MODE ENABLED: (Reserved for future use)")
    print("-" * 40)
    
    # 1. Sync References
    if sync_refs:
        src_refs = os.path.join(project_root, ".agent", "protocols", "references")
        dst_refs = os.path.join(target_root, "references")
        
        print(f"\nEvaluating 'references':")
        if os.path.exists(src_refs):
            try:
                if sys.version_info >= (3, 8):
                    shutil.copytree(src_refs, dst_refs, dirs_exist_ok=True)
                else:
                    shutil.copytree(src_refs, dst_refs, dirs_exist_ok=True)
                print(f"  ✅ Successfully synced 'references'")
            except Exception as e:
                print(f"  ❌ Error syncing 'references': {e}")
        else:
            print(f"  ❌ Source not found: {src_refs}")
    else:
        print("\nSkipping 'references' sync (disabled).")

    # 2. Sync Protocols
    src_protocols = os.path.join(project_root, ".agent", "protocols")
    dst_protocols = os.path.join(target_root, "protocols")
    
    print(f"\nEvaluating 'protocols':")
    if not os.path.exists(src_protocols):
        print(f"  ❌ Source not found: {src_protocols}")
        return

    # Create destination protocols folder if missing
    if not os.path.exists(dst_protocols):
        try:
            os.makedirs(dst_protocols)
        except Exception as e:
            print(f"  ❌ Failed to create directory {dst_protocols}: {e}")
            return

    start_time = time.time()
    
    print(f"\n🔄 PHASE 1: Syncing Protocols")
    
    try:
        shutil.copytree(src_protocols, dst_protocols, dirs_exist_ok=True)
        print(f"  ✅ Successfully synced 'protocols'")
        
        # Count items for summary
        item_count = len(os.listdir(src_protocols))
        print(f"     Synced {item_count} items.")
        
    except Exception as e:
        print(f"  ❌ Failed to sync protocols: {e}")

    print("-" * 40)
    print(f"🎉 Protocols Sync Complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync Protocols & References")
    parser.add_argument("target", nargs="?", default=None, help="Target directory")
    parser.add_argument("--force", action="store_true", help="Force sync (reserved)")
    parser.add_argument("--copilot", action="store_true", help="Sync to ~/.copilot (includes references)")
    
    args = parser.parse_args()
    
    try:
        if sys.stdout.encoding != 'utf-8':
            sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass # Older python or specific environments

    target_root = args.target
    do_sync_refs = True
    
    if args.copilot:
        target_root = os.path.expanduser("~/.copilot")
        # User requested protocols AND references for copilot, so we keep do_sync_refs=True
        do_sync_refs = True 
        print(f"🤖  Targeting Copilot Directory: {target_root}")
        
        # Ensure the .copilot directory itself exists
        if not os.path.exists(target_root):
            try:
                os.makedirs(target_root)
                print(f"  ✅ Created missing directory: {target_root}")
            except Exception as e:
                print(f"  ❌ Failed to create directory {target_root}: {e}")
                sys.exit(1)

    try:
        sync_protocols(target_root, args.force, do_sync_refs)
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
