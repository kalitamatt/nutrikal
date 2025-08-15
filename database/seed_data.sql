-- Données de démarrage pour NUTRIKAL

-- Insérer des aliments de base dans food_database
INSERT INTO food_database (food_name, calories_per_100g, protein_per_100g, omega3_per_100g, magnesium_per_100g, food_category) VALUES
('Saumon', 208, 25.4, 1.8, 29, 'Poisson'),
('Flocons d''avoine', 389, 16.9, 0.1, 177, 'Céréales'),
('Épinards', 23, 2.9, 0.1, 79, 'Légumes'),
('Noix', 654, 15.2, 9.1, 158, 'Fruits à coque'),
('Myrtilles', 57, 0.7, 0.1, 6, 'Fruits'),
('Quinoa', 368, 14.1, 0.3, 197, 'Céréales'),
('Brocoli', 34, 2.8, 0.1, 21, 'Légumes'),
('Graines de chia', 486, 17.0, 17.8, 335, 'Graines'),
('Poulet', 165, 31.0, 0.0, 25, 'Viande'),
('Patate douce', 86, 1.6, 0.0, 25, 'Légumes'),
('Truite', 148, 20.8, 1.0, 27, 'Poisson'),
('Lentilles', 352, 24.6, 0.2, 122, 'Légumineuses'),
('Yaourt grec', 59, 10.0, 0.1, 11, 'Produits laitiers'),
('Graines de lin', 534, 18.3, 22.8, 392, 'Graines'),
('Framboises', 52, 1.2, 0.1, 22, 'Fruits');

-- Objectifs nutritionnels de référence par âge/sexe
INSERT INTO nutrition_targets (user_id, calories_target, protein_target, omega3_target, magnesium_target) VALUES
-- Ces valeurs seront remplacées par les vraies données utilisateur
('00000000-0000-0000-0000-000000000000', 2000, 80, 1.1, 350); -- Exemple pour femme 40 ans

