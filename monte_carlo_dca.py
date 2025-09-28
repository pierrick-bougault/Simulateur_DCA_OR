"""
Simulation Monte Carlo pour l'investissement DCA sur l'or
Combine la stratégie DCA avec des simulations de prix aléatoires
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from typing import Dict, List, Tuple
from volatility_analysis import GoldVolatilityAnalysis

class MonteCarloGoldDCA:
    def __init__(self, data_file: str = "data/annual.csv"):
        """
        Simulateur Monte Carlo pour investissement DCA sur l'or
        """
        # Charger l'analyse de volatilité
        self.volatility_analyzer = GoldVolatilityAnalysis(data_file)
        
        # Paramètres de simulation par défaut
        self.investissement_annuel = 1000.0
        self.nombre_annees = 10
        self.frais_par_once = 25.0
        self.prix_initial = 2000.0  # Prix de départ pour les simulations
        self.nb_simulations = 1000
        
        # Paramètres Monte Carlo
        self.drift = 0.05  # Rendement moyen annuel
        self.volatility = 0.20  # Volatilité annuelle
        
    def configure_simulation(self, 
                           investissement_annuel: float,
                           nombre_annees: int,
                           prix_initial: float,
                           frais_par_once: float = 25.0,
                           nb_simulations: int = 1000,
                           period: str = 'Modern_Era'):
        """
        Configure les paramètres de simulation Monte Carlo
        """
        self.investissement_annuel = investissement_annuel
        self.nombre_annees = nombre_annees
        self.prix_initial = prix_initial
        self.frais_par_once = frais_par_once
        self.nb_simulations = nb_simulations
        
        # Obtenir les paramètres historiques pour la période choisie
        mc_params = self.volatility_analyzer.get_monte_carlo_params(period)
        self.drift = mc_params.get('drift', 0.05)
        self.volatility = mc_params.get('volatility', 0.20)
        
    def generer_trajectoires_prix(self) -> np.ndarray:
        """
        Génère des trajectoires de prix aléatoires en utilisant le modèle géométrique brownien
        
        Returns:
            Array de forme (nb_simulations, nombre_annees) contenant les prix simulés
        """
        # Initialiser l'array des prix
        prix_simules = np.zeros((self.nb_simulations, self.nombre_annees))
        prix_simules[:, 0] = self.prix_initial
        
        # Générer les chocs aléatoires
        np.random.seed(42)  # Pour reproductibilité
        chocs_aleatoires = np.random.normal(0, 1, (self.nb_simulations, self.nombre_annees - 1))
        
        # Calculer les trajectoires de prix (modèle géométrique brownien)
        for t in range(1, self.nombre_annees):
            # Formule: S(t+1) = S(t) * exp((drift - 0.5*vol²)*dt + vol*sqrt(dt)*epsilon)
            # Avec dt = 1 an
            prix_simules[:, t] = prix_simules[:, t-1] * np.exp(
                (self.drift - 0.5 * self.volatility**2) + 
                self.volatility * chocs_aleatoires[:, t-1]
            )
        
        return prix_simules
    
    def simuler_dca_monte_carlo(self) -> Dict:
        """
        Exécute la simulation DCA Monte Carlo
        
        Returns:
            Dictionnaire contenant les résultats de toutes les simulations
        """
        # Générer les trajectoires de prix
        prix_trajectoires = self.generer_trajectoires_prix()
        
        # Initialiser les arrays de résultats
        resultats = {
            'valeurs_finales': np.zeros(self.nb_simulations),
            'rendements_finaux': np.zeros(self.nb_simulations),
            'onces_finales': np.zeros(self.nb_simulations),
            'investissement_total': self.investissement_annuel * self.nombre_annees,
            'prix_trajectoires': prix_trajectoires,
            'profits_finaux': np.zeros(self.nb_simulations)
        }
        
        # Simuler chaque trajectoire
        for sim in range(self.nb_simulations):
            onces_totales = 0.0
            
            # Pour chaque année de la simulation
            for annee in range(self.nombre_annees):
                prix_actuel = prix_trajectoires[sim, annee]
                
                # Acheter des onces avec l'investissement annuel
                onces_achetees = self.investissement_annuel / prix_actuel
                onces_totales += onces_achetees
            
            # Calculer la valeur finale du portefeuille
            prix_final = prix_trajectoires[sim, -1]
            valeur_brute = onces_totales * prix_final
            
            # Calculer les frais totaux
            frais_totaux = onces_totales * self.frais_par_once * self.nombre_annees
            
            # Valeur nette
            valeur_finale = valeur_brute - frais_totaux
            
            # Calculer le profit et le rendement
            profit_final = valeur_finale - resultats['investissement_total']
            rendement_final = (profit_final / resultats['investissement_total']) * 100
            
            # Stocker les résultats
            resultats['valeurs_finales'][sim] = valeur_finale
            resultats['rendements_finaux'][sim] = rendement_final
            resultats['onces_finales'][sim] = onces_totales
            resultats['profits_finaux'][sim] = profit_final
        
        return resultats
    
    def calculer_statistiques(self, resultats: Dict) -> Dict:
        """
        Calcule les statistiques sur les résultats Monte Carlo
        """
        rendements = resultats['rendements_finaux']
        valeurs = resultats['valeurs_finales']
        profits = resultats['profits_finaux']
        
        stats_dict = {
            # Statistiques sur les rendements
            'rendement_moyen': np.mean(rendements),
            'rendement_median': np.median(rendements),
            'rendement_std': np.std(rendements),
            'rendement_min': np.min(rendements),
            'rendement_max': np.max(rendements),
            
            # Percentiles des rendements
            'rendement_p5': np.percentile(rendements, 5),
            'rendement_p25': np.percentile(rendements, 25),
            'rendement_p75': np.percentile(rendements, 75),
            'rendement_p95': np.percentile(rendements, 95),
            
            # Statistiques sur les valeurs finales
            'valeur_moyenne': np.mean(valeurs),
            'valeur_mediane': np.median(valeurs),
            'valeur_p5': np.percentile(valeurs, 5),
            'valeur_p95': np.percentile(valeurs, 95),
            
            # Probabilités
            'prob_profit': np.mean(profits > 0) * 100,
            'prob_perte': np.mean(profits < 0) * 100,
            'prob_rendement_positif': np.mean(rendements > 0) * 100,
            
            # Value at Risk (VaR)
            'var_5pct': np.percentile(profits, 5),
            'var_1pct': np.percentile(profits, 1),
        }
        
        return stats_dict
    
    def afficher_resultats_monte_carlo(self, resultats: Dict, statistiques: Dict):
        """
        Affiche les résultats de la simulation Monte Carlo
        """
        print("=" * 80)
        print("RÉSULTATS SIMULATION MONTE CARLO - DCA OR")
        print("=" * 80)
        
        print(f"Nombre de simulations: {self.nb_simulations:,}")
        print(f"Période d'investissement: {self.nombre_annees} ans")
        print(f"Investissement annuel: {self.investissement_annuel:,.2f} USD")
        print(f"Investissement total: {resultats['investissement_total']:,.2f} USD")
        print(f"Prix initial de l'or: {self.prix_initial:.2f} USD/oz")
        print(f"Frais par once par an: {self.frais_par_once:.2f} USD")
        print()
        print(f"Paramètres Monte Carlo:")
        print(f"  Drift (rendement moyen): {self.drift:.3f} ({self.drift*100:.1f}%)")
        print(f"  Volatilité: {self.volatility:.3f} ({self.volatility*100:.1f}%)")
        
        print("\n" + "="*50)
        print("STATISTIQUES DES RENDEMENTS")
        print("="*50)
        print(f"Rendement moyen: {statistiques['rendement_moyen']:8.1f}%")
        print(f"Rendement médian: {statistiques['rendement_median']:8.1f}%")
        print(f"Écart-type: {statistiques['rendement_std']:8.1f}%")
        print(f"Minimum: {statistiques['rendement_min']:8.1f}%")
        print(f"Maximum: {statistiques['rendement_max']:8.1f}%")
        
        print(f"\nINTERVALLES DE CONFIANCE:")
        print(f"5e percentile: {statistiques['rendement_p5']:8.1f}%")
        print(f"25e percentile: {statistiques['rendement_p25']:8.1f}%")
        print(f"75e percentile: {statistiques['rendement_p75']:8.1f}%")
        print(f"95e percentile: {statistiques['rendement_p95']:8.1f}%")
        
        print(f"\nPROBABILITÉS:")
        print(f"Probabilité de profit: {statistiques['prob_profit']:6.1f}%")
        print(f"Probabilité de perte: {statistiques['prob_perte']:6.1f}%")
        print(f"Probabilité rendement > 0%: {statistiques['prob_rendement_positif']:6.1f}%")
        
        print(f"\nVALUE AT RISK:")
        print(f"VaR 5%: {statistiques['var_5pct']:,.2f} USD")
        print(f"VaR 1%: {statistiques['var_1pct']:,.2f} USD")
        
        print(f"\nVALEURS FINALES:")
        print(f"Valeur moyenne: {statistiques['valeur_moyenne']:,.2f} USD")
        print(f"Valeur médiane: {statistiques['valeur_mediane']:,.2f} USD")
        print(f"Intervalle 90% confiance: [{statistiques['valeur_p5']:,.0f} - {statistiques['valeur_p95']:,.0f}] USD")
    
    def creer_graphiques_monte_carlo(self, resultats: Dict, statistiques: Dict):
        """
        Crée des graphiques pour visualiser les résultats Monte Carlo
        """
        plt.style.use('seaborn-v0_8')
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle(f'Simulation Monte Carlo - DCA Or ({self.nb_simulations:,} simulations)', 
                    fontsize=16, fontweight='bold')
        
        # 1. Distribution des rendements finaux
        axes[0, 0].hist(resultats['rendements_finaux'], bins=50, alpha=0.7, color='blue', edgecolor='black')
        axes[0, 0].axvline(statistiques['rendement_moyen'], color='red', linestyle='--', 
                          label=f'Moyenne: {statistiques["rendement_moyen"]:.1f}%')
        axes[0, 0].axvline(statistiques['rendement_median'], color='green', linestyle='--',
                          label=f'Médiane: {statistiques["rendement_median"]:.1f}%')
        axes[0, 0].set_title('Distribution des Rendements Finaux')
        axes[0, 0].set_xlabel('Rendement (%)')
        axes[0, 0].set_ylabel('Fréquence')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Trajectoires de prix (échantillon)
        sample_trajectories = np.random.choice(self.nb_simulations, min(100, self.nb_simulations), replace=False)
        for i in sample_trajectories:
            axes[0, 1].plot(range(self.nombre_annees), resultats['prix_trajectoires'][i], 
                           alpha=0.1, color='gray', linewidth=0.5)
        
        # Trajectoire moyenne
        prix_moyen = np.mean(resultats['prix_trajectoires'], axis=0)
        axes[0, 1].plot(range(self.nombre_annees), prix_moyen, color='red', linewidth=3, 
                       label='Trajectoire moyenne')
        axes[0, 1].axhline(y=self.prix_initial, color='blue', linestyle='--', 
                          label=f'Prix initial: {self.prix_initial:.0f}$')
        axes[0, 1].set_title('Trajectoires de Prix Simulées')
        axes[0, 1].set_xlabel('Années')
        axes[0, 1].set_ylabel('Prix (USD/oz)')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # 3. Box plot des rendements par percentiles
        percentiles = [5, 25, 50, 75, 95]
        pct_values = [np.percentile(resultats['rendements_finaux'], p) for p in percentiles]
        axes[0, 2].boxplot(resultats['rendements_finaux'], patch_artist=True)
        axes[0, 2].set_title('Box Plot des Rendements')
        axes[0, 2].set_ylabel('Rendement (%)')
        axes[0, 2].grid(True, alpha=0.3)
        
        # 4. Distribution des valeurs finales
        axes[1, 0].hist(resultats['valeurs_finales'], bins=50, alpha=0.7, color='green', edgecolor='black')
        axes[1, 0].axvline(statistiques['valeur_moyenne'], color='red', linestyle='--',
                          label=f'Moyenne: {statistiques["valeur_moyenne"]:,.0f}$')
        axes[1, 0].axvline(resultats['investissement_total'], color='orange', linestyle='--',
                          label=f'Investi: {resultats["investissement_total"]:,.0f}$')
        axes[1, 0].set_title('Distribution des Valeurs Finales')
        axes[1, 0].set_xlabel('Valeur Finale (USD)')
        axes[1, 0].set_ylabel('Fréquence')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # 5. Scatter plot rendement vs valeur finale
        axes[1, 1].scatter(resultats['rendements_finaux'], resultats['valeurs_finales'], 
                          alpha=0.5, s=1)
        axes[1, 1].axvline(0, color='red', linestyle='--', alpha=0.7)
        axes[1, 1].axhline(resultats['investissement_total'], color='orange', linestyle='--', alpha=0.7)
        axes[1, 1].set_title('Rendement vs Valeur Finale')
        axes[1, 1].set_xlabel('Rendement (%)')
        axes[1, 1].set_ylabel('Valeur Finale (USD)')
        axes[1, 1].grid(True, alpha=0.3)
        
        # 6. Intervalles de confiance dans le temps
        prix_trajectoires = resultats['prix_trajectoires']
        prix_p5 = np.percentile(prix_trajectoires, 5, axis=0)
        prix_p25 = np.percentile(prix_trajectoires, 25, axis=0)
        prix_p75 = np.percentile(prix_trajectoires, 75, axis=0)
        prix_p95 = np.percentile(prix_trajectoires, 95, axis=0)
        prix_median = np.percentile(prix_trajectoires, 50, axis=0)
        
        years = range(self.nombre_annees)
        axes[1, 2].fill_between(years, prix_p5, prix_p95, alpha=0.2, color='gray', label='90% CI')
        axes[1, 2].fill_between(years, prix_p25, prix_p75, alpha=0.4, color='blue', label='50% CI')
        axes[1, 2].plot(years, prix_median, color='red', linewidth=2, label='Médiane')
        axes[1, 2].set_title('Intervalles de Confiance des Prix')
        axes[1, 2].set_xlabel('Années')
        axes[1, 2].set_ylabel('Prix (USD/oz)')
        axes[1, 2].legend()
        axes[1, 2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

def main():
    """
    Exemple d'utilisation de la simulation Monte Carlo
    """
    print("Simulation Monte Carlo - DCA Or")
    print("=" * 40)
    
    # Créer le simulateur
    mc_simulator = MonteCarloGoldDCA()
    
    # Configuration de la simulation
    mc_simulator.configure_simulation(
        investissement_annuel=2000,
        nombre_annees=15,
        prix_initial=2000,
        frais_par_once=30,
        nb_simulations=5000,
        period='Modern_Era'
    )
    
    # Exécuter la simulation
    print("Exécution de la simulation Monte Carlo...")
    resultats = mc_simulator.simuler_dca_monte_carlo()
    
    # Calculer les statistiques
    statistiques = mc_simulator.calculer_statistiques(resultats)
    
    # Afficher les résultats
    mc_simulator.afficher_resultats_monte_carlo(resultats, statistiques)
    
    # Créer les graphiques
    print("\nCréation des graphiques...")
    mc_simulator.creer_graphiques_monte_carlo(resultats, statistiques)

if __name__ == "__main__":
    main()