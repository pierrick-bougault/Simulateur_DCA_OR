"""
Simulation d'investissement DCA (Dollar Cost Averaging) annuel sur l'or
Basé sur les données historiques de prix de l'or de 1833 à 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple

class GoldDCASimulator:
    def __init__(self, data_file: str = "data/annual.csv"):
        """
        Initialise la simulation DCA avec les données historiques de l'or
        
        Args:
            data_file: Chemin vers le fichier CSV contenant les données de prix
        """
        self.df = pd.read_csv(data_file)
        self.df['Date'] = self.df['Date'].astype(int)
        self.df = self.df.set_index('Date')
        
        # Variables de configuration
        self.investissement_annuel = 1000.0  # Montant investi chaque année (USD)
        self.nombre_annees = 10               # Nombre d'années d'investissement
        self.frais_par_once = 50.0           # Frais de stockage/gestion par once par an (USD)
        self.annee_debut = 2000              # Année de début de l'investissement
        
    def configure_simulation(self, 
                           investissement_annuel: float,
                           nombre_annees: int,
                           annee_debut: int,
                           frais_par_once: float = 50.0):
        """
        Configure les paramètres de la simulation
        
        Args:
            investissement_annuel: Montant investi chaque année en USD
            nombre_annees: Nombre d'années d'investissement répété
            annee_debut: Année de début de l'investissement
            frais_par_once: Frais annuels par once détenue en USD
        """
        self.investissement_annuel = investissement_annuel
        self.nombre_annees = nombre_annees
        self.annee_debut = annee_debut
        self.frais_par_once = frais_par_once
        
    def simuler_dca(self) -> Dict:
        """
        Exécute la simulation DCA et retourne les résultats
        
        Returns:
            Dictionnaire contenant tous les résultats de la simulation
        """
        annee_fin = self.annee_debut + self.nombre_annees - 1
        
        # Vérifier que nous avons les données pour la période demandée
        if self.annee_debut not in self.df.index:
            raise ValueError(f"Année de début {self.annee_debut} non disponible dans les données")
        if annee_fin not in self.df.index:
            raise ValueError(f"Année de fin {annee_fin} non disponible dans les données")
            
        # Initialisation des variables de suivi
        resultats = {
            'annees': [],
            'prix_or': [],
            'investissement_cumule': [],
            'onces_achetees_annee': [],
            'onces_totales': [],
            'valeur_portefeuille': [],
            'frais_totaux': [],
            'profit_perte': [],
            'rendement_pourcent': []
        }
        
        onces_totales = 0.0
        investissement_cumule = 0.0
        
        for i, annee in enumerate(range(self.annee_debut, annee_fin + 1)):
            # Prix de l'or cette année
            prix_or = self.df.loc[annee, 'Price']
            
            # Investissement cette année
            investissement_cumule += self.investissement_annuel
            
            # Calcul du nombre d'onces achetées cette année
            onces_achetees = self.investissement_annuel / prix_or
            onces_totales += onces_achetees
            
            # Valeur actuelle du portefeuille (sans frais)
            valeur_portefeuille_brute = onces_totales * prix_or
            
            # Calcul des frais cumulés (frais sur toutes les onces détenues)
            frais_totaux = onces_totales * self.frais_par_once * (i + 1)  # Frais accumulés
            
            # Valeur nette du portefeuille
            valeur_portefeuille_nette = valeur_portefeuille_brute - frais_totaux
            
            # Profit/Perte
            profit_perte = valeur_portefeuille_nette - investissement_cumule
            
            # Rendement en pourcentage
            rendement_pourcent = (profit_perte / investissement_cumule) * 100 if investissement_cumule > 0 else 0
            
            # Stocker les résultats
            resultats['annees'].append(annee)
            resultats['prix_or'].append(prix_or)
            resultats['investissement_cumule'].append(investissement_cumule)
            resultats['onces_achetees_annee'].append(onces_achetees)
            resultats['onces_totales'].append(onces_totales)
            resultats['valeur_portefeuille'].append(valeur_portefeuille_nette)
            resultats['frais_totaux'].append(frais_totaux)
            resultats['profit_perte'].append(profit_perte)
            resultats['rendement_pourcent'].append(rendement_pourcent)
        
        return resultats
    
    def afficher_resultats(self, resultats: Dict):
        """
        Affiche un résumé des résultats de la simulation
        """
        print("=" * 60)
        print("SIMULATION D'INVESTISSEMENT DCA SUR L'OR")
        print("=" * 60)
        print(f"Période d'investissement: {self.annee_debut} - {self.annee_debut + self.nombre_annees - 1}")
        print(f"Investissement annuel: {self.investissement_annuel:,.2f} USD")
        print(f"Nombre d'années: {self.nombre_annees}")
        print(f"Frais par once par an: {self.frais_par_once:,.2f} USD")
        print()
        
        # Résultats finaux
        investissement_total = resultats['investissement_cumule'][-1]
        onces_finales = resultats['onces_totales'][-1]
        valeur_finale = resultats['valeur_portefeuille'][-1]
        frais_totaux = resultats['frais_totaux'][-1]
        profit_final = resultats['profit_perte'][-1]
        rendement_final = resultats['rendement_pourcent'][-1]
        
        print("RÉSULTATS FINAUX:")
        print(f"Investissement total: {investissement_total:,.2f} USD")
        print(f"Onces d'or possédées: {onces_finales:.4f} oz")
        print(f"Valeur du portefeuille (nette): {valeur_finale:,.2f} USD")
        print(f"Frais totaux payés: {frais_totaux:,.2f} USD")
        print(f"Profit/Perte: {profit_final:,.2f} USD")
        print(f"Rendement: {rendement_final:.2f}%")
        print()
        
        # Prix moyen d'achat
        prix_moyen_achat = investissement_total / onces_finales if onces_finales > 0 else 0
        prix_final = resultats['prix_or'][-1]
        print(f"Prix moyen d'achat: {prix_moyen_achat:.2f} USD/oz")
        print(f"Prix final de l'or: {prix_final:.2f} USD/oz")
        
    def afficher_tableau_detaille(self, resultats: Dict):
        """
        Affiche un tableau détaillé année par année
        """
        print("\n" + "=" * 120)
        print("TABLEAU DÉTAILLÉ ANNÉE PAR ANNÉE")
        print("=" * 120)
        
        header = f"{'Année':<6} {'Prix Or':<10} {'Invest.':<10} {'Onces':<8} {'Total Oz':<10} {'Valeur':<12} {'Frais':<10} {'P&L':<12} {'Rend.':<8}"
        print(header)
        print("-" * 120)
        
        for i in range(len(resultats['annees'])):
            row = f"{resultats['annees'][i]:<6} " \
                  f"{resultats['prix_or'][i]:<10.2f} " \
                  f"{resultats['investissement_cumule'][i]:<10.0f} " \
                  f"{resultats['onces_achetees_annee'][i]:<8.4f} " \
                  f"{resultats['onces_totales'][i]:<10.4f} " \
                  f"{resultats['valeur_portefeuille'][i]:<12.0f} " \
                  f"{resultats['frais_totaux'][i]:<10.0f} " \
                  f"{resultats['profit_perte'][i]:<12.0f} " \
                  f"{resultats['rendement_pourcent'][i]:<8.1f}%"
            print(row)
            
    def creer_graphiques(self, resultats: Dict):
        """
        Crée des graphiques pour visualiser les résultats
        """
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Simulation DCA - Investissement Or', fontsize=16, fontweight='bold')
        
        annees = resultats['annees']
        
        # Graphique 1: Évolution de la valeur du portefeuille vs investissement
        axes[0, 0].plot(annees, resultats['investissement_cumule'], label='Investissement cumulé', linewidth=2)
        axes[0, 0].plot(annees, resultats['valeur_portefeuille'], label='Valeur portefeuille (nette)', linewidth=2)
        axes[0, 0].set_title('Évolution de la Valeur du Portefeuille')
        axes[0, 0].set_xlabel('Année')
        axes[0, 0].set_ylabel('Valeur (USD)')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Graphique 2: Évolution du prix de l'or
        axes[0, 1].plot(annees, resultats['prix_or'], color='gold', linewidth=2)
        axes[0, 1].set_title('Prix de l\'Or')
        axes[0, 1].set_xlabel('Année')
        axes[0, 1].set_ylabel('Prix (USD/oz)')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Graphique 3: Accumulation d'onces
        axes[1, 0].plot(annees, resultats['onces_totales'], color='orange', linewidth=2)
        axes[1, 0].set_title('Accumulation d\'Onces d\'Or')
        axes[1, 0].set_xlabel('Année')
        axes[1, 0].set_ylabel('Onces détenues')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Graphique 4: Rendement en pourcentage
        axes[1, 1].plot(annees, resultats['rendement_pourcent'], color='green', linewidth=2)
        axes[1, 1].axhline(y=0, color='red', linestyle='--', alpha=0.7)
        axes[1, 1].set_title('Rendement (%)')
        axes[1, 1].set_xlabel('Année')
        axes[1, 1].set_ylabel('Rendement (%)')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

# Fonction principale pour exécuter la simulation
def main():
    """
    Fonction principale pour exécuter des simulations DCA
    """
    # Créer l'instance du simulateur
    simulator = GoldDCASimulator()
    
    print("Simulation DCA sur l'Or - Paramètres configurables")
    print("=" * 50)
    
    # Exemple de simulation 1: Investissement moderne (2000-2020)
    print("\n🔸 SIMULATION 1: Investissement 2000-2020")
    simulator.configure_simulation(
        investissement_annuel=2000,    # 2000 USD par an
        nombre_annees=21,              # 21 ans (2000-2020)
        annee_debut=2000,              # Début en 2000
        frais_par_once=25              # 25 USD de frais par once par an
    )
    
    resultats1 = simulator.simuler_dca()
    simulator.afficher_resultats(resultats1)
    
    # Exemple de simulation 2: Investissement récent (2010-2024)
    print("\n🔸 SIMULATION 2: Investissement 2010-2024")
    simulator.configure_simulation(
        investissement_annuel=5000,    # 5000 USD par an
        nombre_annees=15,              # 15 ans (2010-2024)
        annee_debut=2010,              # Début en 2010
        frais_par_once=30              # 30 USD de frais par once par an
    )
    
    resultats2 = simulator.simuler_dca()
    simulator.afficher_resultats(resultats2)
    
    # Exemple de simulation 3: Investissement conservateur long terme (1980-2000)
    print("\n🔸 SIMULATION 3: Investissement 1980-2000")
    simulator.configure_simulation(
        investissement_annuel=1000,    # 1000 USD par an
        nombre_annees=21,              # 21 ans (1980-2000)
        annee_debut=1980,              # Début en 1980
        frais_par_once=20              # 20 USD de frais par once par an
    )
    
    resultats3 = simulator.simuler_dca()
    simulator.afficher_resultats(resultats3)
    
    # Créer les graphiques pour la dernière simulation
    print("\nCréation des graphiques pour la simulation 1980-2000...")
    simulator.creer_graphiques(resultats3)

if __name__ == "__main__":
    main()