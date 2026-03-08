import os
import shutil
import sys
import argparse
import time

def sync_protocols(target_root=None, force_mode=False, sync_refs=True):
    """
    Synchronizes .agent/protocols/ (guidelines + references) to a target directory.

    Structure:
      .agent/protocols/
        |-- guidelines/     <- 20 cognitive protocols (01-20) + guideline_index.md
        +-- references/     <- llms.txt, learning_profile.md, code-documentation/

    The entire protocols/ folder is copied recursively in a single pass.
    References are included automatically. The sync_refs flag is kept for
    backwards compatibility but no longer triggers a separate copy pass.
    """

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    if target_root is None:
        target_root = os.getcwd()

    target_root = os.path.abspath(target_root)

    print(f"Starting Sync Protocols Script")
    print(f"Project Root: {project_root}")
    print(f"Target Root:  {target_root}")
    if force_mode:
        print(f"FORCE MODE ENABLED (reserved for future use)")
    if not sync_refs:
        print("Note: sync_refs=False passed, but references/ is already included via the full protocols/ copy.")
    print("-" * 40)

    # Sync the entire protocols/ directory recursively.
    # This includes both:
    #   - guidelines/ (01-20 protocol files + guideline_index.md)
    #   - references/ (llms.txt, learning_profile.md, code-documentation/)
    src_protocols = os.path.join(project_root, ".agent", "protocols")
    dst_protocols = os.path.join(target_root, "protocols")

    print(f"\nEvaluating 'protocols':")
    if not os.path.exists(src_protocols):
        print(f"  FAIL: Source not found: {src_protocols}")
        return

    start_time = time.time()
    print(f"\nSyncing 'protocols' (recursive - includes guidelines/ and references/)...")
    try:
        shutil.copytree(src_protocols, dst_protocols, dirs_exist_ok=True)
        elapsed = time.time() - start_time
        subdirs = [d for d in os.listdir(src_protocols) if os.path.isdir(os.path.join(src_protocols, d))]
        print(f"  OK: Synced {len(subdirs)} subfolder(s) in {elapsed:.1f}s: {', '.join(subdirs)}")
    except Exception as e:
        print(f"  FAIL: Failed to sync protocols: {e}")

    print("-" * 40)
    print(f"Protocols Sync Complete.")

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
        pass  # Older python or specific environments

    target_root = args.target
    do_sync_refs = True

    if args.copilot:
        target_root = os.path.expanduser("~/.copilot")
        do_sync_refs = True
        print(f"Targeting Copilot Directory: {target_root}")

        # Ensure the .copilot directory itself exists
        if not os.path.exists(target_root):
            try:
                os.makedirs(target_root)
                print(f"  OK: Created missing directory: {target_root}")
            except Exception as e:
                print(f"  FAIL: Failed to create directory {target_root}: {e}")
                sys.exit(1)

    try:
        sync_protocols(target_root, args.force, do_sync_refs)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nFatal Error: {e}")
