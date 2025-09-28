"""
Exemple d'utilisation des simulations Monte Carlo pour DCA sur l'or
Démontre les différentes fonctionnalités et cas d'usage
"""

from monte_carlo_dca import MonteCarloGoldDCA
from hybrid_dca_simulator import HybridDCASimulator
from volatility_analysis import GoldVolatilityAnalysis
import numpy as np

def exemple_monte_carlo_simple():
    """
    Exemple simple de simulation Monte Carlo
    """
    print("=" * 70)
    print("EXEMPLE 1: SIMULATION MONTE CARLO SIMPLE")
    print("=" * 70)
    
    # Créer le simulateur
    mc_sim = MonteCarloGoldDCA()
    
    # Configuration conservative
    mc_sim.configure_simulation(
        investissement_annuel=2000,    # 2000 USD par an
        nombre_annees=10,              # 10 ans
        prix_initial=2400,             # Prix actuel approximatif
        frais_par_once=25,             # 25 USD de frais par once par an
        nb_simulations=3000,           # 3000 simulations
        period='Modern_Era'            # Utiliser la volatilité moderne
    )
    
    # Exécuter la simulation
    print("Exécution de 3,000 simulations Monte Carlo...")
    resultats = mc_sim.simuler_dca_monte_carlo()
    statistiques = mc_sim.calculer_statistiques(resultats)
    
    # Afficher les résultats
    mc_sim.afficher_resultats_monte_carlo(resultats, statistiques)
    
    return resultats, statistiques

def exemple_comparaison_scenarios():
    """
    Comparaison de différents scénarios d'investissement avec Monte Carlo
    """
    print("\n" + "=" * 70)
    print("EXEMPLE 2: COMPARAISON DE SCÉNARIOS D'INVESTISSEMENT")
    print("=" * 70)
    
    scenarios = [
        {"nom": "Conservative", "invest": 1000, "annees": 20, "frais": 20},
        {"nom": "Modéré", "invest": 2500, "annees": 15, "frais": 25},
        {"nom": "Agressif", "invest": 5000, "annees": 10, "frais": 35},
    ]
    
    mc_sim = MonteCarloGoldDCA()
    
    resultats_scenarios = []
    
    for scenario in scenarios:
        print(f"\n🔸 Scénario {scenario['nom']}:")
        print(f"   Investissement: {scenario['invest']} USD/an")
        print(f"   Durée: {scenario['annees']} ans")
        print(f"   Frais: {scenario['frais']} USD/once/an")
        
        mc_sim.configure_simulation(
            investissement_annuel=scenario['invest'],
            nombre_annees=scenario['annees'],
            prix_initial=2400,
            frais_par_once=scenario['frais'],
            nb_simulations=2000,
            period='Modern_Era'
        )
        
        resultats = mc_sim.simuler_dca_monte_carlo()
        stats = mc_sim.calculer_statistiques(resultats)
        
        scenario_result = {
            'nom': scenario['nom'],
            'investissement_total': scenario['invest'] * scenario['annees'],
            'rendement_moyen': stats['rendement_moyen'],
            'rendement_median': stats['rendement_median'],
            'prob_profit': stats['prob_profit'],
            'var_5pct': stats['var_5pct'],
            'valeur_moyenne': stats['valeur_moyenne']
        }
        
        resultats_scenarios.append(scenario_result)
        
        print(f"   Rendement moyen: {stats['rendement_moyen']:6.1f}%")
        print(f"   Probabilité profit: {stats['prob_profit']:6.1f}%")
        print(f"   VaR 5%: {stats['var_5pct']:8,.0f} USD")
    
    # Tableau de comparaison
    print(f"\n{'Scénario':<12} {'Invest.Total':<12} {'Rend.Moy.':<10} {'Prob.Profit':<12} {'VaR 5%':<12}")
    print("-" * 65)
    
    for result in resultats_scenarios:
        print(f"{result['nom']:<12} "
              f"{result['investissement_total']:<12,.0f} "
              f"{result['rendement_moyen']:<9.1f}% "
              f"{result['prob_profit']:<11.1f}% "
              f"{result['var_5pct']:<12,.0f}")

def exemple_analyse_sensibilite():
    """
    Analyse de sensibilité : impact de différents paramètres
    """
    print("\n" + "=" * 70)
    print("EXEMPLE 3: ANALYSE DE SENSIBILITÉ")
    print("=" * 70)
    
    mc_sim = MonteCarloGoldDCA()
    
    # Test 1: Impact du prix initial
    print("\n🔸 Impact du prix initial de l'or:")
    prix_initiaux = [2000, 2200, 2400, 2600, 2800]
    
    for prix in prix_initiaux:
        mc_sim.configure_simulation(
            investissement_annuel=2000,
            nombre_annees=10,
            prix_initial=prix,
            frais_par_once=25,
            nb_simulations=1000,
            period='Modern_Era'
        )
        
        resultats = mc_sim.simuler_dca_monte_carlo()
        stats = mc_sim.calculer_statistiques(resultats)
        
        print(f"   Prix initial {prix:4.0f}$: Rendement moyen {stats['rendement_moyen']:6.1f}%, "
              f"Prob. profit {stats['prob_profit']:5.1f}%")
    
    # Test 2: Impact des frais
    print("\n🔸 Impact des frais par once:")
    frais_list = [10, 20, 30, 40, 50]
    
    for frais in frais_list:
        mc_sim.configure_simulation(
            investissement_annuel=2000,
            nombre_annees=10,
            prix_initial=2400,
            frais_par_once=frais,
            nb_simulations=1000,
            period='Modern_Era'
        )
        
        resultats = mc_sim.simuler_dca_monte_carlo()
        stats = mc_sim.calculer_statistiques(resultats)
        
        print(f"   Frais {frais:2.0f}$/once/an: Rendement moyen {stats['rendement_moyen']:6.1f}%, "
              f"Prob. profit {stats['prob_profit']:5.1f}%")
    
    # Test 3: Impact de la durée d'investissement
    print("\n🔸 Impact de la durée d'investissement:")
    durees = [5, 10, 15, 20, 25]
    
    for duree in durees:
        mc_sim.configure_simulation(
            investissement_annuel=2000,
            nombre_annees=duree,
            prix_initial=2400,
            frais_par_once=25,
            nb_simulations=1000,
            period='Modern_Era'
        )
        
        resultats = mc_sim.simuler_dca_monte_carlo()
        stats = mc_sim.calculer_statistiques(resultats)
        
        print(f"   Durée {duree:2.0f} ans: Rendement moyen {stats['rendement_moyen']:6.1f}%, "
              f"Prob. profit {stats['prob_profit']:5.1f}%")

def exemple_volatilite_periodes():
    """
    Compare les projections selon différentes périodes de volatilité
    """
    print("\n" + "=" * 70)
    print("EXEMPLE 4: IMPACT DES DIFFÉRENTES PÉRIODES DE VOLATILITÉ")
    print("=" * 70)
    
    mc_sim = MonteCarloGoldDCA()
    analyzer = GoldVolatilityAnalysis()
    
    periodes = {
        'Gold_Standard': 'Étalon-or (1833-1971)',
        'Post_Bretton_Woods': 'Post-Bretton Woods (1972-1980)',
        'Stabilization': 'Stabilisation (1981-2000)',
        'Modern_Era': 'Ère moderne (2001-2024)'
    }
    
    print(f"\nConfiguration: 2000$/an, 15 ans, prix initial 2400$, frais 25$/once/an")
    print(f"\n{'Période':<25} {'Drift':<8} {'Vol.':<8} {'Rend.Moy.':<10} {'Prob.Profit':<12}")
    print("-" * 70)
    
    for period_key, period_name in periodes.items():
        # Obtenir les paramètres de la période
        params = analyzer.get_monte_carlo_params(period_key)
        
        if 'drift' in params:
            mc_sim.configure_simulation(
                investissement_annuel=2000,
                nombre_annees=15,
                prix_initial=2400,
                frais_par_once=25,
                nb_simulations=1500,
                period=period_key
            )
            
            resultats = mc_sim.simuler_dca_monte_carlo()
            stats = mc_sim.calculer_statistiques(resultats)
            
            print(f"{period_name[:24]:<25} "
                  f"{params['drift']*100:<7.1f}% "
                  f"{params['volatility']*100:<7.1f}% "
                  f"{stats['rendement_moyen']:<9.1f}% "
                  f"{stats['prob_profit']:<11.1f}%")

def exemple_simulation_hybride():
    """
    Exemple de simulation hybride combinant historique et Monte Carlo
    """
    print("\n" + "=" * 70)
    print("EXEMPLE 5: SIMULATION HYBRIDE (HISTORIQUE + MONTE CARLO)")
    print("=" * 70)
    
    hybrid_sim = HybridDCASimulator()
    
    # Configuration
    investissement_annuel = 2500
    nombre_annees = 15
    annee_debut_historique = 2009  # Début après la crise
    
    print(f"Configuration:")
    print(f"  Investissement annuel: {investissement_annuel:,} USD")
    print(f"  Période: {nombre_annees} ans")
    print(f"  Comparaison historique: {annee_debut_historique}-{annee_debut_historique + nombre_annees - 1}")
    print(f"  Projections Monte Carlo: À partir de 2024")
    
    # Simulation complète
    resultats = hybrid_sim.simulation_complete(
        investissement_annuel=investissement_annuel,
        nombre_annees=nombre_annees,
        annee_debut_historique=annee_debut_historique,
        frais_par_once=30,
        nb_simulations_mc=2000,
        period_volatility='Modern_Era'
    )
    
    return resultats

def recommandations_strategiques():
    """
    Génère des recommandations stratégiques basées sur Monte Carlo
    """
    print("\n" + "=" * 70)
    print("RECOMMANDATIONS STRATÉGIQUES BASÉES SUR MONTE CARLO")
    print("=" * 70)
    
    print("\n📋 PRINCIPES CLÉS POUR LE DCA SUR L'OR:")
    
    print("\n1. DIVERSIFICATION TEMPORELLE:")
    print("   ✓ Le DCA réduit l'impact de la volatilité sur le long terme")
    print("   ✓ Évite le timing du marché (difficile à prédire)")
    print("   ✓ Bénéficie des prix moyens sur la période")
    
    print("\n2. GESTION DES FRAIS:")
    print("   ⚠️ Les frais de stockage impactent significativement les rendements")
    print("   ✓ Négocier les frais pour les volumes importants")
    print("   ✓ Considérer les ETF or pour réduire les frais de stockage physique")
    
    print("\n3. HORIZON D'INVESTISSEMENT:")
    print("   ✓ Plus l'horizon est long, plus la probabilité de profit augmente")
    print("   ✓ Minimum 10-15 ans recommandé pour lisser la volatilité")
    print("   ✓ L'or est une couverture long terme contre l'inflation")
    
    print("\n4. ALLOCATION DANS LE PORTEFEUILLE:")
    print("   ⚠️ L'or ne doit représenter qu'une partie du portefeuille (5-15%)")
    print("   ✓ Complément aux actions/obligations, pas un remplacement")
    print("   ✓ Corrélation faible avec les autres actifs = diversification")
    
    print("\n5. PÉRIODES FAVORABLES:")
    print("   ✓ Crises économiques et géopolitiques")
    print("   ✓ Périodes d'inflation élevée")
    print("   ✓ Incertitudes sur les devises")
    print("   ⚠️ Performance plus faible en périodes de croissance forte")

def main():
    """
    Fonction principale exécutant tous les exemples
    """
    print("EXEMPLES MONTE CARLO - SIMULATION DCA OR")
    print("=" * 50)
    
    # Exemple 1: Simulation simple
    exemple_monte_carlo_simple()
    
    # Exemple 2: Comparaison scénarios
    exemple_comparaison_scenarios()
    
    # Exemple 3: Analyse de sensibilité
    exemple_analyse_sensibilite()
    
    # Exemple 4: Impact volatilité
    exemple_volatilite_periodes()
    
    # Exemple 5: Simulation hybride
    exemple_simulation_hybride()
    
    # Recommandations
    recommandations_strategiques()
    
    print("\n" + "=" * 70)
    print("EXEMPLES TERMINÉS")
    print("Pour des simulations personnalisées, utilisez: python simulation_interactive.py")
    print("=" * 70)

if __name__ == "__main__":
    main()