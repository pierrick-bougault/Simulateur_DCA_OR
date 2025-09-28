# Simulateur DCA (Dollar Cost Averaging) pour l'Or avec Monte Carlo

Ce projet permet de simuler des investissements DCA sur l'or en utilisant :
- **Données historiques** de prix de 1833 à 2024
- **Simulations Monte Carlo** pour les projections futures
- **Analyse de volatilité** par périodes historiques

## Fonctionnalités

### 📊 Variables DCA de base :

1. **Variable d'investissement annuel** : Montant fixe investi chaque année
2. **Calcul de valeur sur n années** : Évolution de la valeur du portefeuille
3. **Nombre d'années d'investissement** : Durée de la stratégie DCA
4. **Nombre d'onces possédées** : Accumulation d'or au cours du temps
5. **Frais par once** : Coûts de stockage/gestion par once détenue

### 🎲 Nouvelles fonctionnalités Monte Carlo :

- **Simulations probabilistes** : Milliers de scénarios futurs possibles
- **Analyse de volatilité** : Basée sur différentes périodes historiques
- **Intervalles de confiance** : Probabilités de profit/perte
- **Value at Risk (VaR)** : Estimation des pertes potentielles
- **Simulation hybride** : Comparaison historique vs projections Monte Carlo

## Fichiers du projet

### 📁 Simulations DCA de base :
- `dca_simulation.py` : Classe principale du simulateur DCA historique
- `exemple_utilisation.py` : Exemples d'utilisation simple DCA
- `config.py` : Configurations prédéfinies pour différents scénarios

### 🎯 Simulations Monte Carlo :
- `volatility_analysis.py` : Analyse de la volatilité historique de l'or
- `monte_carlo_dca.py` : Simulateur Monte Carlo pour projections DCA
- `hybrid_dca_simulator.py` : Combinaison historique + Monte Carlo
- `exemples_monte_carlo.py` : Exemples complets Monte Carlo

### 🖥️ Interface utilisateur :
- `simulation_interactive.py` : Menu interactif complet (historique + Monte Carlo)

### 📊 Données :
- `data/annual.csv` : Données historiques des prix de l'or (1833-2024)

## Installation des dépendances

```bash
pip install pandas numpy matplotlib seaborn scipy
```

## Utilisation

### 1. 🎯 Interface interactive complète (recommandée)

```bash
python simulation_interactive.py
```

**Menu disponible :**
- Simulation DCA historique personnalisée
- Exemples prédéfinis DCA  
- Analyse comparative des périodes
- **🆕 Simulation Monte Carlo DCA**
- **🆕 Simulation Hybride (Historique + Monte Carlo)**
- **🆕 Analyse de volatilité**

### 2. 🎲 Exemples Monte Carlo

```bash
python exemples_monte_carlo.py
```

Démontre :
- Simulation Monte Carlo simple
- Comparaison de scénarios
- Analyse de sensibilité
- Impact des périodes de volatilité
- Recommandations stratégiques

### 3. 📊 Utilisation programmatique

#### Simulation DCA historique :
```python
from dca_simulation import GoldDCASimulator

simulator = GoldDCASimulator()
simulator.configure_simulation(
    investissement_annuel=2000,  # 2000 USD par an
    nombre_annees=15,            # 15 ans d'investissement  
    annee_debut=2009,            # Début en 2009
    frais_par_once=30            # 30 USD de frais par once/an
)

resultats = simulator.simuler_dca()
simulator.afficher_resultats(resultats)
```

#### 🆕 Simulation Monte Carlo :
```python
from monte_carlo_dca import MonteCarloGoldDCA

mc_sim = MonteCarloGoldDCA()
mc_sim.configure_simulation(
    investissement_annuel=2000,
    nombre_annees=15,
    prix_initial=2400,           # Prix de départ pour projections
    nb_simulations=5000,         # Nombre de scénarios
    period='Modern_Era'          # Période de référence pour volatilité
)

resultats = mc_sim.simuler_dca_monte_carlo()
statistiques = mc_sim.calculer_statistiques(resultats)
mc_sim.afficher_resultats_monte_carlo(resultats, statistiques)
```

#### 🔄 Simulation hybride :
```python
from hybrid_dca_simulator import HybridDCASimulator

hybrid_sim = HybridDCASimulator()
resultats = hybrid_sim.simulation_complete(
    investissement_annuel=3000,
    nombre_annees=15,
    annee_debut_historique=2009, # Comparaison historique
    nb_simulations_mc=2000       # Projections Monte Carlo
)
```

## Variables principales

### 📊 Variables DCA de base

#### 1. Investissement annuel
Montant fixe investi chaque année en USD. Cette variable détermine la régularité de votre stratégie DCA.

#### 2. Calcul de valeur sur n années
Le simulateur calcule :
- La valeur brute du portefeuille (onces × prix actuel)
- La valeur nette (après déduction des frais)
- Le profit/perte par rapport à l'investissement total

#### 3. Nombre d'années d'investissement
Durée de votre stratégie DCA. Le simulateur répète l'achat annuel sur cette période.

#### 4. Nombre d'onces possédées
Accumulation progressive d'or calculée comme :
```
Onces achetées année N = Investissement annuel / Prix or année N
Onces totales = Somme de toutes les onces achetées
```

#### 5. Frais par once
Coûts annuels (stockage, assurance, gestion) par once détenue :
```
Frais totaux = Onces détenues × Frais par once × Nombre d'années
```

### 🎲 Variables Monte Carlo additionnelles

#### 6. Prix initial
Prix de l'or au début des projections Monte Carlo (généralement prix actuel).

#### 7. Nombre de simulations
Quantité de scénarios générés (recommandé : 1000-5000 pour des résultats stables).

#### 8. Période de volatilité de référence
Période historique utilisée pour calibrer les paramètres Monte Carlo :
- **Étalon-or** (1833-1971) : Faible volatilité
- **Post-Bretton Woods** (1972-1980) : Très haute volatilité
- **Stabilisation** (1981-2000) : Volatilité modérée
- **Ère moderne** (2001-2024) : Volatilité élevée

#### 9. Paramètres stochastiques
- **Drift** : Tendance moyenne des rendements annuels
- **Volatilité** : Écart-type des rendements (mesure du risque)

Ces paramètres sont calculés automatiquement à partir des données historiques.

## Exemples de scénarios

Le fichier `config.py` contient des scénarios prédéfinis :

- **Conservateur** : 500 USD/an sur 20 ans
- **Modéré** : 2000 USD/an sur 15 ans  
- **Agressif** : 5000 USD/an sur 10 ans
- **Crise 2008** : 3000 USD/an à partir de 2008
- **Post-COVID** : 4000 USD/an à partir de 2020

## Résultats fournis

### 📈 Simulations DCA historiques
- **Investissement total** : Somme de tous les versements
- **Onces possédées** : Quantité d'or accumulée
- **Valeur du portefeuille** : Valeur actuelle (nette des frais)
- **Profit/Perte** : Gain ou perte par rapport à l'investissement
- **Rendement** : Performance en pourcentage
- **Prix moyen d'achat** : Prix moyen payé par once
- **Tableau détaillé** : Évolution année par année

### 🎯 Simulations Monte Carlo additionnelles
- **Distribution des rendements** : Histogramme de tous les scénarios possibles
- **Intervalles de confiance** : 5e, 25e, 75e, 95e percentiles
- **Probabilités** : Chances de profit, de perte, de rendement positif
- **Value at Risk (VaR)** : Perte maximale probable à 1% et 5%
- **Statistiques descriptives** : Moyenne, médiane, écart-type, min/max
- **Trajectoires de prix** : Évolution des prix simulés dans le temps

### 📊 Visualisations
#### Graphiques DCA historique :
- Évolution valeur du portefeuille vs investissement
- Prix de l'or dans le temps
- Accumulation d'onces
- Rendement en pourcentage

#### 🆕 Graphiques Monte Carlo :
- Distribution des rendements finaux
- Trajectoires de prix simulées (échantillon)
- Box plot des rendements
- Distribution des valeurs finales  
- Scatter plot rendement vs valeur
- Intervalles de confiance temporels

#### 🔄 Graphiques hybrides :
- Comparaison historique vs Monte Carlo
- Analyse comparative des périodes de volatilité

## Données historiques

Le fichier utilise des données de prix de l'or de 1833 à 2024, permettant d'analyser :
- L'ère de l'étalon-or (1833-1971)
- La fin du système de Bretton Woods (1971)
- Les crises des années 70-80
- La bulle internet (2000s)
- La crise financière de 2008
- L'ère du QE (2010s)
- La période post-COVID (2020+)

## Conseils d'utilisation

1. **Testez différentes périodes** : Les performances varient énormément selon la période
2. **Ajustez les frais** : Les frais de stockage impactent significativement le rendement
3. **Comparez les scénarios** : Utilisez l'option de comparaison pour optimiser votre stratégie
4. **Analysez les graphiques** : Les visualisations révèlent les tendances importantes

## Limitations

- Les données sont annuelles (pas de variation intra-annuelle)
- Les frais sont simplifiés (frais fixes par once)
- Ne prend pas en compte l'inflation
- Les prix historiques peuvent différer selon les sources