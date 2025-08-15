import os
import json

# Créer la structure de fichiers pour NUTRIKAL
project_structure = {
    "frontend": [
        "package.json",
        "next.config.js",
        "pages/index.js",
        "pages/profile.js",
        "pages/dashboard.js",
        "pages/api/auth.js",
        "components/ProfileForm.jsx",
        "components/Dashboard.jsx",
        "components/MealPlan.jsx",
        "components/ScoreChart.jsx",
        "lib/supabase.js",
        "styles/globals.css"
    ],
    "backend": [
        "package.json",
        "server.js",
        "routes/users.js",
        "routes/mealplans.js",
        "routes/scores.js",
        "middleware/auth.js",
        "utils/nutritionScore.js",
        "config/database.js"
    ],
    "database": [
        "schema.sql",
        "seed_data.sql",
        "nutrition_kb.csv"
    ],
    "ai": [
        "system_prompts.json",
        "rag_setup.py",
        "jan_config.json"
    ],
    "deployment": [
        "docker-compose.yml",
        "Dockerfile.frontend",
        "Dockerfile.backend",
        ".env.example"
    ],
    "docs": [
        "README.md",
        "SETUP.md"
    ]
}

print("Structure du projet NUTRIKAL générée :")
for folder, files in project_structure.items():
    print(f"\n📁 {folder}/")
    for file in files:
        print(f"  📄 {file}")