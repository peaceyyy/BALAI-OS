import os
import shutil

# Get project root based on this script's location
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(PROJECT_ROOT, ".agent", "skills")

CATEGORIES = {
    "core-engineering": [
        "app-builder", "api-patterns", "architecture", "clean-code", "code-analysis",
        "code-review-checklist", "database-design", "error-handling", "nextjs-react-expert",
        "nodejs-best-practices", "python-patterns", "tailwind-patterns", "test-driven-development",
        "testing-patterns", "webapp-testing"
    ],
    "ui-ux-design": [
        "brand-identity", "designing-ui", "frontend-design", "ui-ux-pro-max",
        "vibe-check", "web-design-guidelines"
    ],
    "devops-and-ops": [
        "deploying-cost-optimized", "deployment-procedures", "managing-version-control",
        "performance-profiling", "securing-code", "server-management"
    ],
    "meta-agent-tools": [
        "analyzing-videos", "intelligent-routing", "mcp-builder", "parallel-agents",
        "plan-writing", "planning-project", "reasoning-complex-logic", "skill-creator",
        "systematic-debugging", "teaching-concepts"
    ],
    "specialized-domains": [
        "bash-linux", "documentation-templates", "game-development", "geo-fundamentals",
        "i18n-localization", "mobile-design", "powershell-windows", "seo-fundamentals"
    ]
}

def main():
    print(f"Organizing skills in {SKILLS_DIR}...\n")
    
    # 1. Create category folders
    for category in CATEGORIES.keys():
        category_path = os.path.join(SKILLS_DIR, category)
        if not os.path.exists(category_path):
            os.makedirs(category_path)
            print(f"Created category: {category}")
            
    # 2. Move skills
    print("\nMoving skills to categories...")
    moved_count = 0
    for category, skills in CATEGORIES.items():
        category_path = os.path.join(SKILLS_DIR, category)
        for skill in skills:
            skill_path = os.path.join(SKILLS_DIR, skill)
            if os.path.exists(skill_path) and os.path.isdir(skill_path):
                dest_path = os.path.join(category_path, skill)
                shutil.move(skill_path, dest_path)
                print(f"   => {skill} -> {category}/")
                moved_count += 1
            else:
                # Might already be moved or missing
                dest_path = os.path.join(category_path, skill)
                if os.path.exists(dest_path):
                    print(f"   - {skill} is already in {category}/")
                else:
                    print(f"   Warning: Skill '{skill}' not found at {skill_path}")
                
    print(f"\nDone! Moved {moved_count} skills.")

if __name__ == "__main__":
    main()
