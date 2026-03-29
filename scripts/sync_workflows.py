import os
import re
import shutil
import argparse
import sys


LEGACY_TARGET_ALIASES = {
    "inject-debugger": ["debug-deploy"],
}


def parse_frontmatter(content):
    """Return (frontmatter_dict, body) for markdown content."""
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n?', content, re.DOTALL)
    if not fm_match:
        return {}, content

    frontmatter_text = fm_match.group(1)
    body = content[fm_match.end():]
    frontmatter = {}

    for line in frontmatter_text.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip()

    return frontmatter, body


def extract_source_description(content):
    """Extract description from source frontmatter, inline blocks, or markdown header."""
    source_fm, _ = parse_frontmatter(content)
    if source_fm.get("description"):
        return source_fm["description"].strip()

    # Antigravity style often stores description in an inline metadata block:
    # ---\n# description: ...\n# ---
    block_match = re.search(r'^---\s*\n\s*description:\s*(.+?)\s*\n---\s*$', content, re.MULTILINE)
    if block_match:
        return block_match.group(1).strip()

    desc_match = re.search(r'^##\s*description:\s*(.+?)\s*$', content, re.MULTILINE)
    if desc_match:
        return desc_match.group(1).strip()

    # Last-resort fallback for loose formatting.
    line_match = re.search(r'^\s*description:\s*(.+?)\s*$', content, re.MULTILINE)
    if line_match:
        return line_match.group(1).strip()

    return None


def clean_source_content(content):
    """Remove source metadata wrappers while preserving workflow body."""
    _, body = parse_frontmatter(content)

    # Remove markdown description headers that should live in frontmatter.
    body = re.sub(r'^##\s*description:\s*.*?$\n?', '', body, flags=re.MULTILINE)

    # Remove repeated inline frontmatter-like description blocks if present.
    body = re.sub(r'^---\s*\n\s*description:.*?\n---\s*\n', '', body, flags=re.MULTILINE)

    return body.strip()

def sync_workflows(project_root, target_selection=None, force_mode=False, dry_run=False):
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
        if not extract_source_description(content):
            return False, "Missing description (expected source frontmatter, inline description block, or '## description:' header)."
        
        return True, ""

    print(f"\n🔍 PHASE 1: Validation")
    validation_failed = False
    invalid_files = []

    # Pre-validation pass
    for filename in sorted(os.listdir(workflow_dir)):
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
        unchanged_count = 0
        shrink_warnings = []
        
        # Process each source file
        for filename in sorted(os.listdir(workflow_dir)):
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
            
            source_description = extract_source_description(source_content)
            cleaned_content = clean_source_content(source_content)

            # Guardrail: surface suspicious shrinkage early without blocking sync.
            src_non_empty_lines = len([ln for ln in source_content.splitlines() if ln.strip()])
            cleaned_non_empty_lines = len([ln for ln in cleaned_content.splitlines() if ln.strip()])
            if src_non_empty_lines >= 20 and cleaned_non_empty_lines / max(src_non_empty_lines, 1) < 0.7:
                shrink_warnings.append((filename, src_non_empty_lines, cleaned_non_empty_lines))
            
            # Target file path
            dst_filename = f"{base_name}{target_ext}"
            dst_path = os.path.join(target_dir, dst_filename)

            alias_paths = []
            for alias_name in LEGACY_TARGET_ALIASES.get(base_name, []):
                alias_filename = f"{alias_name}{target_ext}"
                alias_paths.append((alias_filename, os.path.join(target_dir, alias_filename)))
            
            # Read existing target file to preserve target-specific frontmatter fields.
            existing_target_frontmatter = {}
            metadata_source_path = None
            if os.path.exists(dst_path):
                metadata_source_path = dst_path
            else:
                for _, alias_path in alias_paths:
                    if os.path.exists(alias_path):
                        metadata_source_path = alias_path
                        break

            if metadata_source_path:
                try:
                    with open(metadata_source_path, 'r', encoding='utf-8') as f:
                        existing_content = f.read()

                    existing_target_frontmatter, _ = parse_frontmatter(existing_content)
                except Exception:
                    pass # Ignore read errors on target, just overwrite
            
            # Build new frontmatter by preserving target keys except authoritative source keys.
            merged_frontmatter = {
                "name": base_name,
                "description": source_description or base_name,
            }

            for key, value in existing_target_frontmatter.items():
                if key in ("name", "description"):
                    continue
                merged_frontmatter[key] = value

            frontmatter_lines = ["---"]
            for key, value in merged_frontmatter.items():
                frontmatter_lines.append(f"{key}: {value}")
            
            frontmatter_lines.append("---")
            frontmatter = "\n".join(frontmatter_lines)
            
            # Merge: frontmatter + cleaned content
            final_content = f"{frontmatter}\n\n{cleaned_content.strip()}\n"

            existing_text = None
            if os.path.exists(dst_path):
                try:
                    with open(dst_path, 'r', encoding='utf-8') as f:
                        existing_text = f.read()
                except Exception:
                    existing_text = None

            if existing_text == final_content:
                updated_files.add(dst_filename)
                unchanged_count += 1
                continue
            
            if dry_run:
                updated_files.add(dst_filename)
                count += 1
                continue

            # Write to target
            try:
                with open(dst_path, 'w', encoding='utf-8') as f:
                    f.write(final_content)

                updated_files.add(dst_filename)
                count += 1
                # print(f"  ✓ {dst_filename}") # Be less verbose
            except Exception as e:
                print(f"  ❌ Failed to write {dst_filename}: {e}")
        
        action_word = "Would sync" if dry_run else "Synced"
        print(f"  ✨ {action_word} {count} workflows ({unchanged_count} unchanged).")

        if shrink_warnings:
            print(f"  ⚠️  Detected {len(shrink_warnings)} potential source-cleaning shrink warnings:")
            for fname, src_lines, cleaned_lines in shrink_warnings:
                print(f"     - {fname}: source={src_lines} lines, cleaned={cleaned_lines} lines")
        
        # Report orphaned files
        orphaned_files = []
        legacy_alias_filenames = set()
        for source_name, aliases in LEGACY_TARGET_ALIASES.items():
            # Only ignore aliases when the source workflow exists.
            source_file = os.path.join(workflow_dir, f"{source_name}.md")
            if not os.path.exists(source_file):
                continue
            for alias_name in aliases:
                legacy_alias_filenames.add(f"{alias_name}{target_ext}")

        try:
            for f in sorted(os.listdir(target_dir)):
                if f.endswith(target_ext) and f not in updated_files and f not in legacy_alias_filenames:
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
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files")
    
    args = parser.parse_args()
    
    target_arg = None
    if args.antigravity:
        target_arg = "antigravity"
    elif args.copilot:
        target_arg = "copilot"
        
    success = sync_workflows(args.project_root, target_arg, args.force, args.dry_run)
    
    print("\n" + "=" * 60)
    if success:
        print("Done.")
    else:
        print("⚠️  Sync completed with errors or aborted.")
    print("=" * 60)
