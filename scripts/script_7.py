# AI - System Prompts pour Jan
system_prompts = {
    "main_prompt": {
        "role": "system",
        "content": """Tu es NUTRIKAL AI, un assistant spécialisé en nutrition cérébrale pour dirigeants d'entreprise.

MISSION: Aider les dirigeants à optimiser leur performance cérébrale grâce à l'alimentation.

PERSONNALITÉ:
- Expert en nutrition et neurosciences
- Bienveillant mais direct
- Adapté au rythme soutenu des dirigeants
- Basé sur des données scientifiques

WORKFLOW PRINCIPAL:
1. COLLECTE DU PROFIL (si nouveau utilisateur):
   - Âge et sexe
   - Poids et taille  
   - Niveau d'activité physique
   - Heures de sommeil par nuit
   - Niveau de stress (1-10)
   - Allergies alimentaires
   - Aliments détestés
   - Objectifs cérébraux prioritaires

2. SUIVI QUOTIDIEN:
   - Demander ce que l'utilisateur a mangé réellement
   - Comparer avec son plan nutritionnel
   - Identifier les écarts et leurs impacts
   - Proposer des ajustements

3. FEEDBACK ET ENCOURAGEMENT:
   - Calculer un score de performance cérébrale
   - Expliquer les bénéfices des bons choix
   - Suggérer des améliorations concrètes
   - Célébrer les progrès

RÈGLES IMPORTANTES:
- Pose UNE question à la fois
- Sois concis (max 2-3 phrases)
- Utilise des émojis avec parcimonie 🧠
- Concentre-toi sur les nutriments clés: oméga-3, magnésium, antioxydants
- Adapte tes conseils au profil spécifique de l'utilisateur
- Ne donne jamais de conseils médicaux, réfère à un professionnel si besoin

DONNÉES NUTRITIONNELLES À PRIORISER:
- Oméga-3 (DHA/EPA): 1-2g/jour pour la mémoire
- Magnésium: 300-400mg/jour pour le stress
- Antioxydants: pour la protection neuronale
- Protéines: pour la synthèse des neurotransmetteurs
- Glucides complexes: pour l'énergie stable

Commence toujours par te présenter brièvement et demander où en est l'utilisateur dans son parcours NUTRIKAL."""
    },
    
    "daily_tracking_prompt": {
        "role": "system", 
        "content": """Tu es en mode SUIVI QUOTIDIEN. L'utilisateur a un profil établi et un plan nutritionnel.

OBJECTIF: Collecter ce qu'il a réellement mangé aujourd'hui et comparer avec son plan.

PROCESS:
1. Demande pour chaque repas (petit-déj, déjeuner, dîner):
   - Qu'as-tu mangé exactement?
   - En quelle quantité approximativement?

2. Pour chaque aliment mentionné:
   - Identifie-le dans ta base de données
   - Estime les apports nutritionnels
   - Note les écarts vs le plan prévu

3. Donne un feedback immédiat:
   - Points positifs (ce qui était bien)
   - Écarts identifiés
   - Impact sur la performance cérébrale
   - Suggestion d'ajustement pour demain

4. Propose un score sur 100 basé sur:
   - Adhérence au plan (40%)
   - Qualité nutritionnelle (40%) 
   - Équilibre global (20%)

Reste encourageant même si la journée n'était pas parfaite. Focus sur les solutions pour demain."""
    },

    "meal_analysis_prompt": {
        "role": "system",
        "content": """Tu analyses un repas spécifique pour calculer son impact sur la performance cérébrale.

ÉVALUATION NUTRITIONNELLE:
- Calories: impact sur l'énergie stable
- Protéines: synthèse neurotransmetteurs  
- Oméga-3: fluidité membranaire, mémoire
- Magnésium: gestion du stress neuronal
- Antioxydants: protection contre l'inflammation

CRITÈRES DE SCORING:
- Excellent (9-10): Repas optimal pour le cerveau
- Très bien (7-8): Bon équilibre avec bénéfices clairs
- Bien (5-6): Correct mais peut être optimisé
- À améliorer (3-4): Quelques bénéfices mais lacunes importantes
- Insuffisant (1-2): Peu de bénéfices pour la performance cérébrale

Pour chaque repas analysé, donne:
1. Score sur 10
2. Points forts nutritionnels
3. Manques identifiés
4. Suggestions d'amélioration concrètes
5. Bénéfice attendu sur la performance cérébrale

Sois précis et factuel, avec des références scientifiques simples."""
    }
}

with open('system_prompts.json', 'w') as f:
    f.write(json.dumps(system_prompts, indent=2, ensure_ascii=False))

# AI - Configuration Jan
jan_config = {
    "models": [
        {
            "name": "nutrikal-assistant", 
            "model": "llama2-7b-chat",
            "temperature": 0.7,
            "max_tokens": 512,
            "system_prompt": "nutrikal_main"
        }
    ],
    "api_server": {
        "host": "0.0.0.0",
        "port": 1337,
        "cors_enabled": True,
        "api_key": "nutrikal-api-key-2024"
    },
    "data_folder": "/app/jan_data",
    "conversation_memory": True,
    "max_conversation_length": 50
}

with open('jan_config.json', 'w') as f:
    f.write(json.dumps(jan_config, indent=2))

# AI - Script setup RAG
rag_setup = """#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
Configuration RAG pour NUTRIKAL
Indexe la base de données nutritionnelle pour permettre à l'IA
de répondre avec des données factuelles sur les aliments
\"\"\"

import os
import pandas as pd
from langchain.document_loaders import CSVLoader
from langchain.text_splitter import CharacterTextSplitter  
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

def setup_nutrition_rag():
    \"\"\"Configure le système RAG avec les données nutritionnelles\"\"\"
    
    print("🔧 Configuration du RAG NUTRIKAL...")
    
    # 1. Charger les données nutritionnelles
    if not os.path.exists('nutrition_kb.csv'):
        print("❌ Fichier nutrition_kb.csv manquant")
        return None
        
    loader = CSVLoader('nutrition_kb.csv', encoding='utf-8')
    documents = loader.load()
    print(f"✅ {len(documents)} aliments chargés")
    
    # 2. Diviser en chunks
    text_splitter = CharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20
    )
    docs = text_splitter.split_documents(documents)
    print(f"✅ {len(docs)} chunks créés")
    
    # 3. Créer les embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # 4. Créer l'index vectoriel
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("nutrikal_vectorstore")
    print("✅ Index vectoriel sauvegardé")
    
    # 5. Tester la recherche
    query = "aliments riches en oméga-3"
    results = vectorstore.similarity_search(query, k=3)
    print(f"🔍 Test recherche '{query}':")
    for i, result in enumerate(results):
        print(f"  {i+1}. {result.page_content[:100]}...")
    
    return vectorstore

def create_nutrition_kb_csv():
    \"\"\"Crée un fichier CSV avec les données nutritionnelles de base\"\"\"
    
    nutrition_data = [
        {
            "aliment": "Saumon",
            "categorie": "Poisson",
            "calories_100g": 208,
            "proteines_100g": 25.4,
            "omega3_100g": 1.8,
            "magnesium_100g": 29,
            "benefices_cerveau": "Riche en DHA pour la mémoire et la concentration. Améliore la fluidité des membranes neuronales.",
            "conseils_consommation": "2-3 fois par semaine, grillé ou cuit vapeur. Éviter la friture."
        },
        {
            "aliment": "Noix",
            "categorie": "Fruits à coque", 
            "calories_100g": 654,
            "proteines_100g": 15.2,
            "omega3_100g": 9.1,
            "magnesium_100g": 158,
            "benefices_cerveau": "Excellente source d'oméga-3 végétaux. Améliore les fonctions cognitives et réduit l'inflammation cérébrale.",
            "conseils_consommation": "30g par jour maximum (une poignée). Idéal en collation ou dans les salades."
        },
        {
            "aliment": "Épinards",
            "categorie": "Légumes verts",
            "calories_100g": 23,
            "proteines_100g": 2.9,
            "omega3_100g": 0.1,
            "magnesium_100g": 79,
            "benefices_cerveau": "Riche en magnésium pour réguler le stress neuronal. Contient des antioxydants protégeant les neurones.",
            "conseils_consommation": "Crus en salade ou cuits rapidement. Accompagne bien les poissons gras."
        },
        {
            "aliment": "Myrtilles",
            "categorie": "Fruits",
            "calories_100g": 57,
            "proteines_100g": 0.7,
            "omega3_100g": 0.1,
            "magnesium_100g": 6,
            "benefices_cerveau": "Très riches en antioxydants (anthocyanes). Améliorent la mémoire et ralentissent le vieillissement cérébral.",
            "conseils_consommation": "150g par jour. Fraîches, surgelées ou en smoothie. Parfait au petit-déjeuner."
        },
        {
            "aliment": "Avocat",
            "categorie": "Fruits",
            "calories_100g": 160,
            "proteines_100g": 2,
            "omega3_100g": 0.1,
            "magnesium_100g": 29,
            "benefices_cerveau": "Acides gras monoinsaturés pour la santé vasculaire cérébrale. Améliore la circulation sanguine vers le cerveau.",
            "conseils_consommation": "1/2 avocat par jour. En salade, toast ou smoothie vert."
        }
    ]
    
    df = pd.DataFrame(nutrition_data)
    df.to_csv('nutrition_kb.csv', index=False, encoding='utf-8')
    print(f"✅ Fichier nutrition_kb.csv créé avec {len(nutrition_data)} aliments")
    
    return df

def test_rag_queries():
    \"\"\"Teste différentes requêtes sur le système RAG\"\"\"
    
    test_queries = [
        "aliments pour améliorer la mémoire",
        "sources d'oméga-3",
        "réduire le stress avec l'alimentation", 
        "antioxydants pour le cerveau",
        "petit-déjeuner pour la concentration"
    ]
    
    if not os.path.exists("nutrikal_vectorstore"):
        print("❌ Index RAG non trouvé. Exécutez setup_nutrition_rag() d'abord.")
        return
        
    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.load_local("nutrikal_vectorstore", embeddings)
    
    print("🧪 Test des requêtes RAG:")
    for query in test_queries:
        results = vectorstore.similarity_search(query, k=2)
        print(f"\\n❓ '{query}':")
        for i, result in enumerate(results):
            print(f"  {i+1}. {result.page_content[:150]}...")

if __name__ == "__main__":
    # Créer les données nutritionnelles si elles n'existent pas
    if not os.path.exists('nutrition_kb.csv'):
        create_nutrition_kb_csv()
    
    # Configurer le RAG
    vectorstore = setup_nutrition_rag()
    
    if vectorstore:
        # Tester les requêtes
        test_rag_queries()
        print("\\n🎉 Configuration RAG terminée avec succès!")
    else:
        print("\\n❌ Échec de la configuration RAG")
"""

with open('rag_setup.py', 'w') as f:
    f.write(rag_setup)

print("✅ Configuration IA créée :")
print("  - system_prompts.json")
print("  - jan_config.json") 
print("  - rag_setup.py")