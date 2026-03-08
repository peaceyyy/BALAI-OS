import os
import shutil
import sys
import argparse
import time



def sync_skills(target_root=None, force_mode=False, sync_refs=True):
    """
    Synchronizes .agent/skills and .agent/protocols/references to a target directory.

    NOTE: Skills are now organized into category subdirectories:
      .agent/skills/
        ├── core-engineering/
        ├── ui-ux-design/
        ├── devops-and-ops/
        ├── meta-agent-tools/
        ├── specialized-domains/
        ├── skill_index_kairou.md
        ├── skill_index_sparks.md
        ├── skill_index_arc.md
        ├── skill_index_janitor.md
        └── skill_index_secondary.md

    The entire skills/ directory is copied recursively to preserve this structure.
    """

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    if target_root is None:
        target_root = os.getcwd()

    target_root = os.path.abspath(target_root)

    print(f"Starting Sync Skills Script")
    print(f"Project Root: {project_root}")
    print(f"Target Root:  {target_root}")
    if force_mode:
        print(f"FORCE MODE ENABLED.")
    print("-" * 40)

    # 1. Sync References
    if sync_refs:
        src_refs = os.path.join(project_root, ".agent", "protocols", "references")
        dst_refs = os.path.join(target_root, "references")

        print(f"\nEvaluating 'references':")
        if os.path.exists(src_refs):
            try:
                shutil.copytree(src_refs, dst_refs, dirs_exist_ok=True)
                print(f"  OK: Successfully synced 'references'")
            except Exception as e:
                print(f"  FAIL: Error syncing 'references': {e}")
        else:
            print(f"  FAIL: Source not found: {src_refs}")
    else:
        print("\nSkipping 'references' sync (disabled).")

    # 2. Sync Skills — Full Recursive Copy
    src_skills = os.path.join(project_root, ".agent", "skills")
    dst_skills = os.path.join(target_root, "skills")

    print(f"\nEvaluating 'skills':")
    if not os.path.exists(src_skills):
        print(f"  FAIL: Source not found: {src_skills}")
        return

    start_time = time.time()

    print(f"\nSyncing 'skills' (recursive — includes category subdirs and skill indexes)...")
    try:
        shutil.copytree(src_skills, dst_skills, dirs_exist_ok=True)
        elapsed = time.time() - start_time

        # Count top-level items for a useful summary
        categories = [d for d in os.listdir(src_skills) if os.path.isdir(os.path.join(src_skills, d))]
        indexes = [f for f in os.listdir(src_skills) if f.startswith("skill_index_") and f.endswith(".md")]
        print(f"  OK: Synced {len(categories)} category folder(s) and {len(indexes)} skill index file(s) in {elapsed:.1f}s.")
    except Exception as e:
        print(f"  FAIL: Failed to sync skills: {e}")

    print("-" * 40)
    print(f"Skills Sync Complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync Skills & References")
    parser.add_argument("target", nargs="?", default=None, help="Target directory")
    parser.add_argument("--force", action="store_true", help="Force sync ignoring validation errors")
    parser.add_argument("--copilot", action="store_true", help="Sync to ~/.copilot/skills (skips references)")
    
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
        do_sync_refs = False
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
        sync_skills(target_root, args.force, do_sync_refs)
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user.")
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
