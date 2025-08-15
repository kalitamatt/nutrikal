#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration RAG pour NUTRIKAL
Indexe la base de données nutritionnelle pour permettre à l'IA
de répondre avec des données factuelles sur les aliments
"""

import os
import pandas as pd
from langchain.document_loaders import CSVLoader
from langchain.text_splitter import CharacterTextSplitter  
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

def setup_nutrition_rag():
    """Configure le système RAG avec les données nutritionnelles"""

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
    """Crée un fichier CSV avec les données nutritionnelles de base"""

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
    """Teste différentes requêtes sur le système RAG"""

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
        print(f"\n❓ '{query}':")
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
        print("\n🎉 Configuration RAG terminée avec succès!")
    else:
        print("\n❌ Échec de la configuration RAG")
