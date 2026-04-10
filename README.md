# Antenna Array Optimizer with Genetic Algorithm 📡

**Optimization d'un réseau d'antennes M×N pour minimiser le niveau maximal du facteur de réseau (Array Factor)**

---

## 🎯 Objectif

Optimiser la matrice de phase `φ_mn` (8×8) d'un réseau d'antennes pour **fixer ou limiter** la valeur maximale de la fonction Array Factor `f_max`.

**Méthode :** Algorithme Génétique (Genetic Algorithm) combinant recherche continue et optimisation binaire.

---

## 📐 Formulation Mathématique

### Fonction Array Factor

```
f(θ, φ) = Σ(m=1 to M) Σ(n=1 to N) 
          exp(j(m-1)(kd·sin(θ)·sin(φ))) × 
          exp(j(m-1)(kd·sin(θ)·cos(φ))) × 
          exp(jφ_mn)
```

**Où :**
- `θ ∈ [0, π]` : angle d'élévation (radians)
- `φ ∈ [0, 2π]` : angle d'azimut (radians)
- `φ_mn = {0, π}` : matrice de phase (0 ou 1 en binaire)
- `d = 0.5` : espacement entre éléments
- `k = 2π` : nombre d'onde

### Objectif d'Optimisation

**Minimiser** ou **contraindre** :
```
f_max = max(|f(θ, φ)|) pour θ ∈ [0, π], φ ∈ [0, 2π]
```

---

## 🏗️ Architecture du Projet

```
gildas-projet/
├── antenna_optimizer.py        # Script principal
├── genetic_algorithm.py        # Algorithme Génétique
├── utils.py                    # Fonctions utilitaires
├── test_antenna.py            # Suite de tests
├── requirements.txt           # Dépendances Python
├── README.md                  # Documentation
├── optim.pdf                  # Énoncé du projet
└── results/                   # Résultats sauvegardés
    ├── plots/                 # Graphiques
    └── data/                  # Données CSV/JSON
```

---

## 🚀 Installation

### Prérequis
- Python 3.8+
- pip

### Installation des dépendances
```bash
pip install -r requirements.txt
```

---

## 💻 Utilisation

### Exécution de l'optimisation
```bash
python3 antenna_optimizer.py
```

### Exécution des tests
```bash
python3 test_antenna.py
```

### Test des composants individuels
```bash
# Tester la structure GA
python3 genetic_algorithm.py

# Tester les utilitaires
python3 utils.py
```

---

## 📊 Phases d'Implémentation

### ✅ Phase 1 : Configuration et Structure (Complete)
- [x] Structure des fichiers
- [x] Classe GA de base
- [x] Fonctions utilitaires (squelettes)
- [x] Suite de tests (7/7 passing)
- [x] Gestion de données (save/load)

### ✅ Phase 2a : Calcul du Array Factor (Complete)
- [x] Implémentation de `compute_array_factor()` - Vectorisée NumPy
- [x] Évaluation sur grille 2D avec `evaluate_array_factor_grid()`
- [x] Tests de validation (5/5 passing)
- [x] Démonstration dans antenna_optimizer.py

### ✅ Phase 2b : Recherche Continue (Complete)
- [x] Optimisation continue avec scipy.optimize.differential_evolution
- [x] Fonction `find_max_angles()` - Trouve θ,φ optimal
- [x] `evaluate_array_factor_max()` - Wrapper de commodité
- [x] Tests de convergence et déterminisme (5/5 passing)

### 🔄 Phase 2c : Visualisation 2D (En cours)
- [ ] Implémentation de `plot_array_factor_2d()` avec Matplotlib
- [ ] 2D cuts : |f(θ)| vs θ ou |f(φ)| vs φ
- [ ] Export PNG dans results/plots/
- [ ] Tests de validation

### ⏳ Phase 3 : Optimisation GA (À venir)
- [ ] Fonction fitness complète
- [ ] Boucle principale GA.run()
- [ ] Convergence tracking
- [ ] Tests d'optimisation

### ⏳ Phase 4 : Visualisations Avancées (À venir)
- [ ] Graphiques 3D sphériques
- [ ] Comparaisons avant/après (side-by-side)
- [ ] Courbes de convergence GA

---

## 🧬 Algorithme Génétique - Détails

### Représentation
- **Chromosome** : Vecteur binaire de 64 bits (matrice 8×8 aplatie)
- **Gène** : Un bit → φ_mn ∈ {0, π}

### Opérateurs
- **Sélection** : Tournoi (taille 3)
- **Croisement** : Un point (probabilité 0.7)
- **Mutation** : Bit-flip (probabilité 0.05)
- **Élitisme** : Conservation des 5 meilleurs

### Paramètres par défaut
```python
Population: 50 individus
Générations: 100
Taux de mutation: 0.05
Taux de croisement: 0.7
```

---

## 📈 Résultats Attendus

### Sorties
1. **Matrice φ_mn optimale** (8×8)
2. **Valeur f_max minimale**
3. **Graphiques de convergence**
4. **Comparaisons visuelles** (avant/après)

### Format de sauvegarde
- `results/data/optimization_results_matrix.csv` : Matrice optimale
- `results/data/optimization_results_metadata.json` : Métadonnées et historique
- `results/plots/*.png` : Visualisations

---

## 🧪 Tests

**PHASE 1 (7/7 tests ✓):**
- ✓ Initialisation de la classe GA
- ✓ Création de population
- ✓ Conversion chromosome ↔ matrice
- ✓ Opérateurs génétiques (sélection, croisement, mutation)
- ✓ Sauvegarde/chargement de données

**PHASE 2a (5/5 tests ✓):**
- ✓ Calcul Array Factor single-point
- ✓ Évaluation grille 2D
- ✓ Cas tests (all-zeros, magnitude, consistency)

**PHASE 2b (5/5 tests ✓):**
- ✓ Recherche continue (find_max_angles)
- ✓ Déterminisme et convergence
- ✓ Comparaison avec grid search

**TOTAL: 17/17 tests passing ✓**

**Exécuter tous les tests :**
```bash
python test_antenna.py
```

---

## 📚 Références

- **PDF du projet** : `optim.pdf`
- **Cours sur les AG** : `course_Genetic_Algorithm.md`
- Holland, J. H. (1992). *Adaptation in Natural and Artificial Systems*
- Goldberg, D. E. (1989). *Genetic Algorithms in Search, Optimization and Machine Learning*

---

## 👥 Auteurs

**Gildas Project Team** - Mars 2026

---

## 📝 License

Projet académique - Usage éducatif uniquement

---

## 🔄 Statut du Projet

**Phase actuelle :** Phase 2c - Visualisation 2D 🔄  
**Progression :** 60% (Phase 1, 2a, 2b complètes / 5 phases totales)  
**Tests globaux :** 17/17 passing ✓  
**Workflow:** Code (Copilot) → Test (Utilisateur) → Validate → Commit

**Dernière mise à jour :** 10 Avril 2026
