import os
import shutil
import sys
import argparse
import subprocess
import time

def run_agnix_validation(skill_path):
    """
    Runs agnix validation on a specific skill directory or file.
    Returns True if valid (0 exit code), False otherwise.
    """
    # Check if agnix is available
    try:
        # Check specific SKILL.md if it exists, or the folder
        target = os.path.join(skill_path, "SKILL.md")
        if not os.path.exists(target):
             target = skill_path # Fallback to folder
             
        # Run agnix --strict
        # We suppress output unless there's an error to keep sync clean?
        # Actually, let's capture output and print only on error.
        result = subprocess.run(
            ["agnix", target, "--strict"],
            capture_output=True,
            text=True,
            shell=True # Required on Windows for some path resolutions?
        )
        
        if result.returncode == 0:
            return True, ""
        else:
            return False, result.stdout + result.stderr
            
    except FileNotFoundError:
        return False, "agnix command not found in PATH."
    except Exception as e:
        return False, str(e)

def sync_skills(target_root=None, force_mode=False, sync_refs=True):
    """
    Synchronizes .agent/skills and .agent/protocols/references to a target directory.
    Enforces agnix validation on skills unless force_mode is True.
    """
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    if target_root is None:
        target_root = os.getcwd()
    
    target_root = os.path.abspath(target_root)
    
    print(f"🚀 Starting Sync Skills Script")
    print(f"📂 Project Root: {project_root}")
    print(f"🎯 Target Root:  {target_root}")
    if force_mode:
        print(f"⚠️  FORCE MODE ENABLED: Skipping validation checks.")
    print("-" * 40)
    
    # 1. Sync References (No validation required usually)
    if sync_refs:
        src_refs = os.path.join(project_root, ".agent", "protocols", "references")
        dst_refs = os.path.join(target_root, "references")
        
        print(f"\nEvaluating 'references':")
        if os.path.exists(src_refs):
            try:
                if sys.version_info >= (3, 8):
                    shutil.copytree(src_refs, dst_refs, dirs_exist_ok=True)
                else:
                     # Fallback/Older python logic if needed, but assuming 3.8+
                    shutil.copytree(src_refs, dst_refs, dirs_exist_ok=True)
                print(f"  ✅ Successfully synced 'references'")
            except Exception as e:
                print(f"  ❌ Error syncing 'references': {e}")
        else:
            print(f"  ❌ Source not found: {src_refs}")
    else:
        print("\nSkipping 'references' sync (disabled).")

    # 2. Sync Skills (With Validation)
    src_skills = os.path.join(project_root, ".agent", "skills")
    dst_skills = os.path.join(target_root, "skills")
    
    print(f"\nEvaluating 'skills':")
    if not os.path.exists(src_skills):
        print(f"  ❌ Source not found: {src_skills}")
        return

    # Create destination skills folder if missing
    if not os.path.exists(dst_skills):
        os.makedirs(dst_skills)

    start_time = time.time()
    
    print(f"\n🔍 PHASE 1: Validation")
    
    skills_to_sync = []
    validation_failed = False
    invalid_skills = []

    # Identify all skills
    all_skills = [d for d in os.listdir(src_skills) if os.path.isdir(os.path.join(src_skills, d)) and not d.startswith(".")]
    
    # Validation Pass
    for item in all_skills:
        skill_src = os.path.join(src_skills, item)
        
        if force_mode:
            # Skip validation in force mode
            skills_to_sync.append(item)
            continue
            
        is_valid, error_msg = run_agnix_validation(skill_src)
        if is_valid:
            skills_to_sync.append(item)
        else:
            invalid_skills.append((item, error_msg))
            validation_failed = True

    if validation_failed:
        print(f"\n❌ Found {len(invalid_skills)} invalid skills:")
        for name, msg in invalid_skills:
            print(f"  - {name}:")
            for line in msg.splitlines():
                if line.strip(): print(f"      {line}")
        
        if not force_mode:
            print(f"\n⛔ Sync aborted due to validation errors.")
            print(f"   Use --force to sync anyway.")
            return

    else:
        if not force_mode:
            print("✅  All skills passed validation.")
        else:
            print("⚠️  Force mode: Validation skipped.")

    print(f"\n🔄 PHASE 2: Syncing")
    
    skills_synced = 0
    skills_failed_copy = 0
    
    # Sync Pass
    for item in skills_to_sync:
        skill_src = os.path.join(src_skills, item)
        skill_dst = os.path.join(dst_skills, item)
        
        try:
             shutil.copytree(skill_src, skill_dst, dirs_exist_ok=True)
             skills_synced += 1
        except Exception as e:
            print(f"  ❌ Failed to copy '{item}': {e}")
            skills_failed_copy += 1

    print("-" * 40)
    print(f"🎉 Skills Sync Complete: {skills_synced}/{len(skills_to_sync)} synced.")
    if skills_failed_copy > 0:
        print(f"⚠️  {skills_failed_copy} skills failed copy.")

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
