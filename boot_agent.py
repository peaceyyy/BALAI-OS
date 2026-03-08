import os
import shutil
import sys

def boot_project(project_root):
    """
    Initializes a new project with BALAI OS Agent Workflows (Self-Contained).
    Copies the entire .agent/ folder into the target project.
    
    USAGE:
    1. Open terminal in THIS repository (The Brain).
    2. Run: python boot_agent.py "C:/Path/To/Your/New/Project"
    """
    print(f"Booting BALAI OS Agent in: {project_root}")

    # 1. Define Paths
    athena_root = os.path.dirname(os.path.abspath(__file__))
    src_agent = os.path.join(athena_root, ".agent")
    
    target_agent = os.path.join(project_root, ".agent")
    target_logs = os.path.join(project_root, "logs", "sessions")

    # 2. Check source
    if not os.path.exists(src_agent):
        print(f"❌ Error: Source .agent folder not found at {src_agent}")
        return

    # 3. Copy .agent folder
    print(f"📦 Copying .agent folder...")
    try:
        if os.path.exists(target_agent):
            print(f"  -> Target .agent folder already exists. Merging/Overwriting...")
        
        shutil.copytree(src_agent, target_agent, dirs_exist_ok=True)
        print(f"✅ Successfully copied .agent to {target_agent}")
    except Exception as e:
        print(f"❌ Error copying .agent folder: {e}")
        return

    # 4. Create Logs Directory
    if not os.path.exists(target_logs):
        os.makedirs(target_logs)
        print(f"✅ Created directory: {target_logs}")
    else:
        print(f"  -> Logs directory already exists at {target_logs}")

    print("\n✨ Agent Boot Complete.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_dir = sys.argv[1]
    else:
        target_dir = os.getcwd()
        print(f"ℹ️  No path provided. Installing into CURRENT directory: {target_dir}")
        print("💡 Tip: To install elsewhere, run: python boot_agent.py <path_to_project>")
    
    boot_project(target_dir)
