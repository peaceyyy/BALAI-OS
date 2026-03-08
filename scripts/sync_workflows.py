import os
import re
import shutil
import argparse
import sys

def sync_workflows(project_root, target_selection=None, force_mode=False):
    """
    Synchronizes Workflows to Global VS Code User Workflows and Antigravity Global Workflows.
    
    Source: .agent/workflows/*.md
    Targets:
      1. VS Code Copilot: %APPDATA%/Code/User/workflows/*.prompt.md
      2. Antigravity: %USERPROFILE%/.gemini/antigravity/global_workflows/*.prompt.md
    
    Transformation:
    1. Extract description from source YAML frontmatter or markdown headers
    2. Preserve VSCode YAML frontmatter (name, argument-hint) from existing target files
    3. Merge: VSCode frontmatter + cleaned source content
    4. Clean source content: remove duplicate description headers
    """
    
    print("=" * 60)
    print("🔄 SYNCING WORKFLOWS")
    print("=" * 60)
    
    # Source: .agent/workflows/*.md
    workflow_dir = os.path.join(project_root, ".agent", "workflows")
    
    if not os.path.exists(workflow_dir):
        print(f"❌ Source not found: {workflow_dir}")
        return False

    # Define targets
    targets = []
    
    # Target 1: VS Code Copilot
    copilot_dir = os.path.expandvars(r"%APPDATA%\Code\User\workflows")
    if target_selection == "copilot" or target_selection is None:
        targets.append({
            "name": "VS Code Copilot",
            "dir": copilot_dir,
            "ext": ".prompt.md"
        })
        
    # Target 2: Antigravity Global Workflows
    antigravity_dir = os.path.expandvars(r"%USERPROFILE%\.gemini\antigravity\global_workflows")
    if target_selection == "antigravity" or target_selection is None:
        targets.append({
            "name": "Antigravity Global Workflows",
            "dir": antigravity_dir,
            "ext": ".md"
        })

    total_success = True

    # Validation function
    def validate_workflow(content, filename):
        # 1. Check description existence
        if "description:" not in content:
            # Check for ## description: format as fallback logic matches main loop
            if not re.search(r'^##\s*description:', content, re.MULTILINE):
                return False, "Missing 'description' field."
        
        return True, ""

    print(f"\n🔍 PHASE 1: Validation")
    validation_failed = False
    invalid_files = []

    # Pre-validation pass
    for filename in os.listdir(workflow_dir):
        if not filename.endswith(".md") or filename.startswith("archive"):
            continue
            
        src_path = os.path.join(workflow_dir, filename)
        try:
            with open(src_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            is_valid, err = validate_workflow(content, filename)
            if not is_valid:
                invalid_files.append((filename, err))
                validation_failed = True
        except Exception as e:
            invalid_files.append((filename, f"Read error: {e}"))
            validation_failed = True

    if validation_failed:
        print(f"\n❌ Found {len(invalid_files)} invalid workflows:")
        for fname, err in invalid_files:
            print(f"  - {fname}: {err}")
            
        if not force_mode:
            print(f"\n⛔ Sync aborted. Fix errors or run with --force to override.")
            return False
        else:
            print(f"\n⚠️  Force mode enabled. Proceeding despite errors...")
    else:
        print("✅  All workflows passed validation.")

    print(f"\n🔄 PHASE 2: Syncing")
    
    for target in targets:
        target_name = target["name"]
        target_dir = target["dir"]
        target_ext = target["ext"]
        
        print(f"\n📍 Target: {target_name} ({target_dir})")
        
        # Create directory if needed
        if not os.path.exists(target_dir):
            try:
                os.makedirs(target_dir)
                print(f"  ✅ Created directory: {target_dir}")
            except OSError as e:
                print(f"  ❌ Error creating directory: {e}")
                total_success = False
                continue
        
        updated_files = set()
        count = 0
        
        # Process each source file
        for filename in os.listdir(workflow_dir):
            if not filename.endswith(".md") or filename.startswith("archive"):
                continue
                
            src_path = os.path.join(workflow_dir, filename)
            base_name = filename.replace(".md", "")
            
            try:
                with open(src_path, 'r', encoding='utf-8') as f:
                    source_content = f.read()
            except Exception as e:
                print(f"  ❌ Failed to read source {filename}: {e}")
                continue
            
            # Extract description from source
            source_description = None
            
            # Try YAML frontmatter first
            yaml_match = re.search(r'^---\s*\n.*?^description:\s*(.+?)\s*\n.*?^---\s*\n', source_content, re.MULTILINE | re.DOTALL)
            if yaml_match:
                source_description = yaml_match.group(1).strip()
            
            # Try markdown header format: ## description: ...
            if not source_description:
                desc_match = re.search(r'^##\s*description:\s*(.+?)$', source_content, re.MULTILINE)
                if desc_match:
                    source_description = desc_match.group(1).strip()
            
            # Clean source content: remove frontmatter and description headers
            cleaned_content = source_content
            
            # Remove YAML frontmatter
            cleaned_content = re.sub(r'^---\s*\n.*?^---\s*\n', '', cleaned_content, flags=re.MULTILINE | re.DOTALL)
            
            # Remove standalone description headers
            cleaned_content = re.sub(r'^##\s*description:.*?$\n?', '', cleaned_content, flags=re.MULTILINE)
            
            # Remove description in triple-dash blocks
            cleaned_content = re.sub(r'^---\s*\n\s*description:.*?\n---\s*\n', '', cleaned_content, flags=re.MULTILINE)
            
            # Target file path
            dst_filename = f"{base_name}{target_ext}"
            dst_path = os.path.join(target_dir, dst_filename)
            
            # Read existing target file to preserve frontmatter (argument-hint)
            existing_argument_hint = None
            if os.path.exists(dst_path):
                try:
                    with open(dst_path, 'r', encoding='utf-8') as f:
                        existing_content = f.read()
                    
                    # Extract argument-hint from existing file
                    hint_match = re.search(r'^argument-hint:\s*(.+?)$', existing_content, re.MULTILINE)
                    if hint_match:
                        existing_argument_hint = hint_match.group(1).strip()
                except Exception:
                    pass # Ignore read errors on target, just overwrite
            
            # Build new frontmatter
            frontmatter_lines = [
                "---",
                f"name: {base_name}",
                f"description: {source_description or base_name}",
            ]
            
            if existing_argument_hint:
                frontmatter_lines.append(f"argument-hint: {existing_argument_hint}")
            
            frontmatter_lines.append("---")
            frontmatter = "\n".join(frontmatter_lines)
            
            # Merge: frontmatter + cleaned content
            final_content = f"{frontmatter}\n\n{cleaned_content.strip()}\n"
            
            # Write to target
            try:
                with open(dst_path, 'w', encoding='utf-8') as f:
                    f.write(final_content)
                
                updated_files.add(dst_filename)
                count += 1
                # print(f"  ✓ {dst_filename}") # Be less verbose
            except Exception as e:
                print(f"  ❌ Failed to write {dst_filename}: {e}")
        
        print(f"  ✨ Synced {count} workflows.")
        
        # Report orphaned files
        orphaned_files = []
        try:
            for f in os.listdir(target_dir):
                if f.endswith(target_ext) and f not in updated_files:
                    orphaned_files.append(f)
        except Exception:
            pass
            
        if orphaned_files:
            print(f"  ⚠️  Found {len(orphaned_files)} orphaned files (in target only):")
            # Only suggest deletion command, don't auto-delete
            # print("  To remove orphans, run manually:")
            # for orphan in sorted(orphaned_files):
            #     print(f"  Remove-Item '{os.path.join(target_dir, orphan)}'")
        else:
            print("  ✅ No orphaned files found.")

    return total_success

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync Workflows")
    parser.add_argument("project_root", nargs="?", default=os.getcwd(), help="Root directory of the project")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--antigravity", action="store_true", help="Sync only to Antigravity global workflows")
    group.add_argument("--copilot", action="store_true", help="Sync only to VS Code Copilot workflows")
    parser.add_argument("--force", action="store_true", help="Force sync ignoring validation errors")
    
    args = parser.parse_args()
    
    target_arg = None
    if args.antigravity:
        target_arg = "antigravity"
    elif args.copilot:
        target_arg = "copilot"
        
    success = sync_workflows(args.project_root, target_arg, args.force)
    
    print("\n" + "=" * 60)
    if success:
        print("Done.")
    else:
        print("⚠️  Sync completed with errors or aborted.")
    print("=" * 60)
