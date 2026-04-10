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
python antenna_optimizer.py
```

### Exécution des tests
```bash
python test_antenna.py
```

### Test des composants individuels
```bash
# Tester la structure GA
python genetic_algorithm.py

# Tester les utilitaires
python utils.py
```

---

## 📊 Phases d'Implémentation

### ✅ Phase 1 : Configuration et Structure (Complete)
- [x] Structure des fichiers
- [x] Classe GA de base
- [x] Fonctions utilitaires (squelettes)
- [x] Suite de tests
- [x] Gestion de données (save/load)

### 🔄 Phase 2 : Calcul du Array Factor (En cours)
- [ ] Implémentation de `compute_array_factor()`
- [ ] Évaluation sur grille 2D
- [ ] Tests de validation
- [ ] Visualisation 2D

### 🔄 Phase 3 : Recherche Continue (À venir)
- [ ] Optimisation continue (scipy)
- [ ] Fonction `find_max_angles()`
- [ ] Tests de convergence

### 🔄 Phase 4 : Optimisation GA (À venir)
- [ ] Fonction fitness complète
- [ ] Boucle principale GA
- [ ] Tests d'optimisation

### 🔄 Phase 5 : Visualisations (À venir)
- [ ] Graphiques 2D et 3D
- [ ] Comparaisons avant/après
- [ ] Courbes de convergence

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

La suite de tests valide :
- ✓ Initialisation de la classe GA
- ✓ Création de population
- ✓ Conversion chromosome ↔ matrice
- ✓ Opérateurs génétiques (sélection, croisement, mutation)
- ✓ Sauvegarde/chargement de données
- ⏳ Calcul du Array Factor (Phase 2)
- ⏳ Recherche continue (Phase 3)
- ⏳ Convergence du GA (Phase 4)

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

**Phase actuelle :** Phase 1 ✅ Complete  
**Prochaine étape :** Phase 2 - Implémentation du Array Factor

**Dernière mise à jour :** 4 Mars 2026
