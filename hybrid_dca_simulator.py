"""
Simulateur DCA hybride : Historique + Monte Carlo
Combine les simulations sur données historiques avec les projections Monte Carlo
"""

from dca_simulation import GoldDCASimulator
from monte_carlo_dca import MonteCarloGoldDCA
from volatility_analysis import GoldVolatilityAnalysis
import numpy as np
import matplotlib.pyplot as plt

class HybridDCASimulator:
    def __init__(self, data_file: str = "data/annual.csv"):
        """
        Simulateur hybride combinant historique et Monte Carlo
        """
        self.historical_simulator = GoldDCASimulator(data_file)
        self.monte_carlo_simulator = MonteCarloGoldDCA(data_file)
        self.volatility_analyzer = GoldVolatilityAnalysis(data_file)
        
    def simulation_complete(self,
                          investissement_annuel: float,
                          nombre_annees: int,
                          annee_debut_historique: int = None,
                          frais_par_once: float = 25.0,
                          nb_simulations_mc: int = 1000,
                          period_volatility: str = 'Modern_Era'):
        """
        Exécute une simulation complète : historique + Monte Carlo
        """
        
        print("=" * 80)
        print("SIMULATION DCA HYBRIDE : HISTORIQUE + MONTE CARLO")
        print("=" * 80)
        
        resultats = {
            'historique': None,
            'monte_carlo': None,
            'comparaison': None
        }
        
        # 1. Simulation historique (si une année de début est fournie)
        if annee_debut_historique:
            print(f"\n🔹 PARTIE 1: SIMULATION HISTORIQUE ({annee_debut_historique}-{annee_debut_historique + nombre_annees - 1})")
            print("-" * 50)
            
            try:
                self.historical_simulator.configure_simulation(
                    investissement_annuel=investissement_annuel,
                    nombre_annees=nombre_annees,
                    annee_debut=annee_debut_historique,
                    frais_par_once=frais_par_once
                )
                
                resultats_historique = self.historical_simulator.simuler_dca()
                self.historical_simulator.afficher_resultats(resultats_historique)
                
                resultats['historique'] = {
                    'resultats': resultats_historique,
                    'rendement_final': resultats_historique['rendement_pourcent'][-1],
                    'valeur_finale': resultats_historique['valeur_portefeuille'][-1],
                    'onces_finales': resultats_historique['onces_totales'][-1]
                }
                
            except ValueError as e:
                print(f"Erreur simulation historique: {e}")
        
        # 2. Simulation Monte Carlo (projections futures)
        print(f"\n🔹 PARTIE 2: PROJECTIONS MONTE CARLO ({nombre_annees} ans)")
        print("-" * 50)
        
        # Obtenir le prix actuel (2024) comme point de départ
        df_prix = self.volatility_analyzer.df
        prix_actuel = df_prix.loc[2024, 'Price']
        
        self.monte_carlo_simulator.configure_simulation(
            investissement_annuel=investissement_annuel,
            nombre_annees=nombre_annees,
            prix_initial=prix_actuel,
            frais_par_once=frais_par_once,
            nb_simulations=nb_simulations_mc,
            period=period_volatility
        )
        
        resultats_mc = self.monte_carlo_simulator.simuler_dca_monte_carlo()
        statistiques_mc = self.monte_carlo_simulator.calculer_statistiques(resultats_mc)
        
        self.monte_carlo_simulator.afficher_resultats_monte_carlo(resultats_mc, statistiques_mc)
        
        resultats['monte_carlo'] = {
            'resultats': resultats_mc,
            'statistiques': statistiques_mc
        }
        
        # 3. Comparaison et analyse
        print(f"\n🔹 PARTIE 3: ANALYSE COMPARATIVE")
        print("-" * 50)
        
        self._afficher_comparaison(resultats, investissement_annuel, nombre_annees)
        
        return resultats
    
    def _afficher_comparaison(self, resultats: dict, investissement_annuel: float, nombre_annees: int):
        """
        Affiche la comparaison entre simulation historique et Monte Carlo
        """
        investissement_total = investissement_annuel * nombre_annees
        
        print(f"Investissement total analysé: {investissement_total:,.2f} USD")
        print(f"Période d'investissement: {nombre_annees} ans")
        
        if resultats['historique']:
            hist = resultats['historique']
            print(f"\nRÉSULTATS HISTORIQUES:")
            print(f"  Rendement: {hist['rendement_final']:8.1f}%")
            print(f"  Valeur finale: {hist['valeur_finale']:10,.2f} USD")
            print(f"  Onces finales: {hist['onces_finales']:8.4f} oz")
        
        if resultats['monte_carlo']:
            mc_stats = resultats['monte_carlo']['statistiques']
            print(f"\nPROJECTIONS MONTE CARLO:")
            print(f"  Rendement moyen: {mc_stats['rendement_moyen']:8.1f}%")
            print(f"  Rendement médian: {mc_stats['rendement_median']:8.1f}%")
            print(f"  Intervalle 90% confiance: [{mc_stats['rendement_p5']:6.1f}% - {mc_stats['rendement_p95']:6.1f}%]")
            print(f"  Valeur moyenne: {mc_stats['valeur_moyenne']:10,.2f} USD")
            print(f"  Probabilité de profit: {mc_stats['prob_profit']:6.1f}%")
        
        # Recommandations basées sur l'analyse
        self._generer_recommandations(resultats, investissement_annuel)
    
    def _generer_recommandations(self, resultats: dict, investissement_annuel: float):
        """
        Génère des recommandations basées sur les résultats
        """
        print(f"\n📋 RECOMMANDATIONS STRATÉGIQUES:")
        print("-" * 40)
        
        if resultats['monte_carlo']:
            mc_stats = resultats['monte_carlo']['statistiques']
            
            # Analyse du risque
            if mc_stats['prob_profit'] > 70:
                print("✅ Probabilité de profit élevée (>70%)")
                print("   → Stratégie DCA recommandée pour ce profil")
            elif mc_stats['prob_profit'] > 50:
                print("⚠️  Probabilité de profit modérée (50-70%)")
                print("   → Stratégie DCA acceptable, surveiller la volatilité")
            else:
                print("❌ Probabilité de profit faible (<50%)")
                print("   → Reconsidérer la stratégie ou réduire l'exposition")
            
            # Analyse de la volatilité
            ecart_rendement = mc_stats['rendement_p95'] - mc_stats['rendement_p5']
            if ecart_rendement > 200:
                print("📊 Volatilité très élevée")
                print("   → Considérer un investissement plus étalé dans le temps")
            elif ecart_rendement > 100:
                print("📊 Volatilité modérée")
                print("   → Stratégie DCA bien adaptée")
            else:
                print("📊 Volatilité faible")
                print("   → Envisager des investissements plus importants")
            
            # Recommandations sur le montant
            if investissement_annuel < 1000:
                print("💰 Investissement conservateur")
                print("   → Peut augmenter progressivement selon les capacités")
            elif investissement_annuel > 5000:
                print("💰 Investissement agressif")  
                print("   → S'assurer de la diversification du portefeuille")
            
            # VaR Analysis
            if abs(mc_stats['var_5pct']) > investissement_annuel * 2:
                print("⚠️  VaR élevé - Risque de perte importante")
                print("   → Considérer une réduction de l'exposition")
    
    def comparaison_periodes_volatilite(self, investissement_annuel: float, nombre_annees: int):
        """
        Compare les projections Monte Carlo selon différentes périodes de volatilité
        """
        print("\n" + "=" * 80)
        print("COMPARAISON DES PROJECTIONS SELON DIFFÉRENTES PÉRIODES DE VOLATILITÉ")
        print("=" * 80)
        
        periodes = ['Gold_Standard', 'Post_Bretton_Woods', 'Stabilization', 'Modern_Era']
        
        resultats_comparaison = {}
        
        for periode in periodes:
            print(f"\n🔸 Analyse période: {periode.replace('_', ' ')}")
            
            # Obtenir les paramètres de volatilité
            params = self.volatility_analyzer.get_monte_carlo_params(periode)
            if 'drift' not in params:
                continue
            
            print(f"   Drift: {params['drift']:.3f} ({params['drift']*100:.1f}%)")
            print(f"   Volatilité: {params['volatility']:.3f} ({params['volatility']*100:.1f}%)")
            
            # Configurer et exécuter Monte Carlo
            df_prix = self.volatility_analyzer.df
            prix_actuel = df_prix.loc[2024, 'Price']
            
            self.monte_carlo_simulator.configure_simulation(
                investissement_annuel=investissement_annuel,
                nombre_annees=nombre_annees,
                prix_initial=prix_actuel,
                nb_simulations=1000,
                period=periode
            )
            
            resultats_mc = self.monte_carlo_simulator.simuler_dca_monte_carlo()
            stats_mc = self.monte_carlo_simulator.calculer_statistiques(resultats_mc)
            
            resultats_comparaison[periode] = stats_mc
            
            print(f"   Rendement moyen: {stats_mc['rendement_moyen']:6.1f}%")
            print(f"   Probabilité profit: {stats_mc['prob_profit']:6.1f}%")
            print(f"   VaR 5%: {stats_mc['var_5pct']:,.0f} USD")
        
        # Tableau de comparaison
        print(f"\n{'Période':<20} {'Rend.Moy':<10} {'Prob.Profit':<12} {'VaR 5%':<12} {'Volatilité':<10}")
        print("-" * 70)
        
        for periode, stats in resultats_comparaison.items():
            params = self.volatility_analyzer.get_monte_carlo_params(periode)
            print(f"{periode.replace('_', ' '):<20} "
                  f"{stats['rendement_moyen']:<9.1f}% "
                  f"{stats['prob_profit']:<11.1f}% "
                  f"{stats['var_5pct']:<11,.0f} "
                  f"{params['volatility']*100:<9.1f}%")
    
    def creer_graphique_comparaison(self, resultats: dict):
        """
        Crée un graphique de comparaison entre historique et Monte Carlo
        """
        if not (resultats.get('historique') and resultats.get('monte_carlo')):
            print("Données insuffisantes pour créer le graphique de comparaison")
            return
        
        fig, axes = plt.subplots(1, 2, figsize=(15, 6))
        fig.suptitle('Comparaison Historique vs Monte Carlo', fontsize=16, fontweight='bold')
        
        # Graphique 1: Comparaison des rendements
        hist_rendement = resultats['historique']['rendement_final']
        mc_rendements = resultats['monte_carlo']['resultats']['rendements_finaux']
        
        axes[0].hist(mc_rendements, bins=50, alpha=0.7, color='blue', 
                    label=f'Monte Carlo (moyenne: {np.mean(mc_rendements):.1f}%)')
        axes[0].axvline(hist_rendement, color='red', linewidth=3, 
                       label=f'Historique: {hist_rendement:.1f}%')
        axes[0].set_title('Distribution des Rendements')
        axes[0].set_xlabel('Rendement (%)')
        axes[0].set_ylabel('Fréquence')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Graphique 2: Comparaison des valeurs finales
        hist_valeur = resultats['historique']['valeur_finale']
        mc_valeurs = resultats['monte_carlo']['resultats']['valeurs_finales']
        
        axes[1].hist(mc_valeurs, bins=50, alpha=0.7, color='green',
                    label=f'Monte Carlo (moyenne: {np.mean(mc_valeurs):,.0f}$)')
        axes[1].axvline(hist_valeur, color='red', linewidth=3,
                       label=f'Historique: {hist_valeur:,.0f}$')
        axes[1].set_title('Distribution des Valeurs Finales')
        axes[1].set_xlabel('Valeur Finale (USD)')
        axes[1].set_ylabel('Fréquence')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

def main():
    """
    Exemple d'utilisation du simulateur hybride
    """
    # Créer le simulateur hybride
    hybrid_sim = HybridDCASimulator()
    
    # Configuration
    investissement_annuel = 3000
    nombre_annees = 15
    annee_debut_historique = 2009  # Début après la crise de 2008
    
    # Simulation complète
    resultats = hybrid_sim.simulation_complete(
        investissement_annuel=investissement_annuel,
        nombre_annees=nombre_annees,
        annee_debut_historique=annee_debut_historique,
        frais_par_once=30,
        nb_simulations_mc=2000,
        period_volatility='Modern_Era'
    )
    
    # Comparaison des périodes de volatilité
    hybrid_sim.comparaison_periodes_volatilite(investissement_annuel, nombre_annees)
    
    # Graphique de comparaison
    print("\nCréation du graphique de comparaison...")
    hybrid_sim.creer_graphique_comparaison(resultats)

if __name__ == "__main__":
    main()