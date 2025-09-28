"""
Script interactif pour la simulation DCA personnalisée sur l'or
Inclut maintenant les simulations Monte Carlo
"""

from dca_simulation import GoldDCASimulator
from monte_carlo_dca import MonteCarloGoldDCA
from hybrid_dca_simulator import HybridDCASimulator
from volatility_analysis import GoldVolatilityAnalysis

def simulation_personnalisee():
    """
    Interface pour créer une simulation DCA personnalisée
    """
    print("=" * 60)
    print("SIMULATION DCA PERSONNALISÉE SUR L'OR")
    print("=" * 60)
    
    # Créer l'instance du simulateur
    simulator = GoldDCASimulator()
    
    # Demander les paramètres à l'utilisateur (ou utiliser des valeurs par défaut)
    print("\nConfiguration de votre simulation:")
    print("(Appuyez sur Entrée pour utiliser la valeur par défaut)")
    
    # 1. Niveau d'investissement annuel
    investissement_str = input("Montant d'investissement annuel en USD [1000]: ").strip()
    investissement_annuel = float(investissement_str) if investissement_str else 1000.0
    
    # 2. Nombre d'années d'investissement
    annees_str = input("Nombre d'années d'investissement [10]: ").strip()
    nombre_annees = int(annees_str) if annees_str else 10
    
    # 3. Année de début
    debut_str = input("Année de début de l'investissement [2010]: ").strip()
    annee_debut = int(debut_str) if debut_str else 2010
    
    # 4. Frais par once
    frais_str = input("Frais annuels par once d'or en USD [25]: ").strip()
    frais_par_once = float(frais_str) if frais_str else 25.0
    
    # Configurer et exécuter la simulation
    try:
        simulator.configure_simulation(
            investissement_annuel=investissement_annuel,
            nombre_annees=nombre_annees,
            annee_debut=annee_debut,
            frais_par_once=frais_par_once
        )
        
        print("\nExécution de la simulation...")
        resultats = simulator.simuler_dca()
        
        # Afficher les résultats
        simulator.afficher_resultats(resultats)
        
        # Demander si l'utilisateur veut voir le tableau détaillé
        voir_detail = input("\nVoulez-vous voir le tableau détaillé année par année? (o/n) [n]: ").strip().lower()
        if voir_detail in ['o', 'oui', 'y', 'yes']:
            simulator.afficher_tableau_detaille(resultats)
        
        # Demander si l'utilisateur veut voir les graphiques
        voir_graphiques = input("\nVoulez-vous voir les graphiques? (o/n) [n]: ").strip().lower()
        if voir_graphiques in ['o', 'oui', 'y', 'yes']:
            simulator.creer_graphiques(resultats)
            
    except ValueError as e:
        print(f"\nErreur: {e}")
        print("Vérifiez que l'année de début et la période sont disponibles dans les données (1833-2024)")

def exemples_predefinies():
    """
    Exécute plusieurs exemples de simulations prédéfinies
    """
    simulator = GoldDCASimulator()
    
    exemples = [
        {
            "nom": "Investissement Conservateur (2000-2010)",
            "investissement": 1000,
            "annees": 11,
            "debut": 2000,
            "frais": 20
        },
        {
            "nom": "Investissement Moderne (2010-2020)",
            "investissement": 2500,
            "annees": 11,
            "debut": 2010,
            "frais": 30
        },
        {
            "nom": "Investissement Récent (2015-2024)",
            "investissement": 5000,
            "annees": 10,
            "debut": 2015,
            "frais": 35
        },
        {
            "nom": "Investissement Crise Financière (2008-2018)",
            "investissement": 3000,
            "annees": 11,
            "debut": 2008,
            "frais": 25
        }
    ]
    
    for i, exemple in enumerate(exemples, 1):
        print(f"\n🔸 EXEMPLE {i}: {exemple['nom']}")
        
        simulator.configure_simulation(
            investissement_annuel=exemple['investissement'],
            nombre_annees=exemple['annees'],
            annee_debut=exemple['debut'],
            frais_par_once=exemple['frais']
        )
        
        resultats = simulator.simuler_dca()
        simulator.afficher_resultats(resultats)

def analyser_periodes():
    """
    Analyse comparative de différentes périodes d'investissement
    """
    print("\n" + "=" * 80)
    print("ANALYSE COMPARATIVE DE DIFFÉRENTES PÉRIODES")
    print("=" * 80)
    
    simulator = GoldDCASimulator()
    
    periodes = [
        {"nom": "Avant la fin de Bretton Woods", "debut": 1960, "fin": 1970},
        {"nom": "Crise des années 70-80", "debut": 1970, "fin": 1980},
        {"nom": "Stabilisation années 80-90", "debut": 1980, "fin": 1990},
        {"nom": "Dot-com et 2000s", "debut": 1995, "fin": 2005},
        {"nom": "Crise financière 2008", "debut": 2005, "fin": 2015},
        {"nom": "Ère moderne", "debut": 2010, "fin": 2020},
        {"nom": "Post-COVID", "debut": 2020, "fin": 2024}
    ]
    
    resultats_comparaison = []
    
    for periode in periodes:
        annees = periode["fin"] - periode["debut"] + 1
        if annees > 0:
            try:
                simulator.configure_simulation(
                    investissement_annuel=1000,  # Standardisé à 1000 USD
                    nombre_annees=annees,
                    annee_debut=periode["debut"],
                    frais_par_once=25  # Frais standardisés
                )
                
                resultats = simulator.simuler_dca()
                rendement_final = resultats['rendement_pourcent'][-1]
                
                resultats_comparaison.append({
                    "periode": periode["nom"],
                    "debut": periode["debut"],
                    "fin": periode["fin"],
                    "duree": annees,
                    "rendement": rendement_final,
                    "investissement_total": resultats['investissement_cumule'][-1],
                    "valeur_finale": resultats['valeur_portefeuille'][-1],
                    "onces_finales": resultats['onces_totales'][-1]
                })
                
            except (ValueError, KeyError):
                continue  # Ignorer les périodes sans données
    
    # Afficher la comparaison
    print(f"\n{'Période':<30} {'Début':<6} {'Fin':<6} {'Durée':<6} {'Rendement':<12} {'Onces':<8}")
    print("-" * 80)
    
    for result in resultats_comparaison:
        print(f"{result['periode']:<30} "
              f"{result['debut']:<6} "
              f"{result['fin']:<6} "
              f"{result['duree']:<6} "
              f"{result['rendement']:<11.1f}% "
              f"{result['onces_finales']:<8.2f}")

def simulation_monte_carlo():
    """
    Interface pour simulation Monte Carlo
    """
    print("=" * 60)
    print("SIMULATION MONTE CARLO DCA")
    print("=" * 60)
    
    simulator = MonteCarloGoldDCA()
    
    print("\nConfiguration de la simulation Monte Carlo:")
    
    # Paramètres d'investissement
    investissement_str = input("Investissement annuel en USD [2000]: ").strip()
    investissement_annuel = float(investissement_str) if investissement_str else 2000.0
    
    annees_str = input("Nombre d'années [15]: ").strip()
    nombre_annees = int(annees_str) if annees_str else 15
    
    prix_str = input("Prix initial de l'or en USD [2400]: ").strip()
    prix_initial = float(prix_str) if prix_str else 2400.0
    
    frais_str = input("Frais par once par an [30]: ").strip()
    frais_par_once = float(frais_str) if frais_str else 30.0
    
    simulations_str = input("Nombre de simulations [2000]: ").strip()
    nb_simulations = int(simulations_str) if simulations_str else 2000
    
    # Choix de la période de volatilité
    print("\nChoisissez la période de référence pour la volatilité:")
    print("1. Ère moderne (2001-2024)")
    print("2. Post-Bretton Woods (1972-1980)")
    print("3. Stabilisation (1981-2000)")
    print("4. Étalon-or (1833-1971)")
    
    period_choice = input("Période [1]: ").strip() or "1"
    periods = {"1": "Modern_Era", "2": "Post_Bretton_Woods", "3": "Stabilization", "4": "Gold_Standard"}
    period = periods.get(period_choice, "Modern_Era")
    
    # Configuration et exécution
    simulator.configure_simulation(
        investissement_annuel=investissement_annuel,
        nombre_annees=nombre_annees,
        prix_initial=prix_initial,
        frais_par_once=frais_par_once,
        nb_simulations=nb_simulations,
        period=period
    )
    
    print(f"\nExécution de {nb_simulations:,} simulations Monte Carlo...")
    resultats = simulator.simuler_dca_monte_carlo()
    statistiques = simulator.calculer_statistiques(resultats)
    
    simulator.afficher_resultats_monte_carlo(resultats, statistiques)
    
    voir_graphiques = input("\nVoir les graphiques? (o/n) [n]: ").strip().lower()
    if voir_graphiques in ['o', 'oui', 'y', 'yes']:
        simulator.creer_graphiques_monte_carlo(resultats, statistiques)

def simulation_hybride():
    """
    Interface pour simulation hybride (historique + Monte Carlo)
    """
    print("=" * 60)
    print("SIMULATION HYBRIDE DCA")
    print("=" * 60)
    
    simulator = HybridDCASimulator()
    
    print("\nConfiguration de la simulation hybride:")
    
    investissement_str = input("Investissement annuel en USD [3000]: ").strip()
    investissement_annuel = float(investissement_str) if investissement_str else 3000.0
    
    annees_str = input("Nombre d'années [15]: ").strip()
    nombre_annees = int(annees_str) if annees_str else 15
    
    debut_str = input("Année de début pour comparaison historique [2009]: ").strip()
    annee_debut = int(debut_str) if debut_str else 2009
    
    frais_str = input("Frais par once par an [30]: ").strip()
    frais_par_once = float(frais_str) if frais_str else 30.0
    
    simulations_str = input("Nombre de simulations Monte Carlo [2000]: ").strip()
    nb_simulations = int(simulations_str) if simulations_str else 2000
    
    # Exécution
    print(f"\nExécution de la simulation hybride...")
    resultats = simulator.simulation_complete(
        investissement_annuel=investissement_annuel,
        nombre_annees=nombre_annees,
        annee_debut_historique=annee_debut,
        frais_par_once=frais_par_once,
        nb_simulations_mc=nb_simulations
    )
    
    voir_comparaison = input("\nVoir comparaison des périodes de volatilité? (o/n) [n]: ").strip().lower()
    if voir_comparaison in ['o', 'oui', 'y', 'yes']:
        simulator.comparaison_periodes_volatilite(investissement_annuel, nombre_annees)
    
    voir_graphiques = input("\nVoir les graphiques de comparaison? (o/n) [n]: ").strip().lower()
    if voir_graphiques in ['o', 'oui', 'y', 'yes']:
        simulator.creer_graphique_comparaison(resultats)

def analyse_volatilite():
    """
    Interface pour l'analyse de volatilité
    """
    print("=" * 60)
    print("ANALYSE DE VOLATILITÉ DE L'OR")
    print("=" * 60)
    
    analyzer = GoldVolatilityAnalysis()
    
    print("Génération du rapport d'analyse...")
    analyzer.print_analysis_report()
    
    voir_graphiques = input("\nVoir les graphiques d'analyse? (o/n) [o]: ").strip().lower()
    if voir_graphiques in ['o', 'oui', 'y', 'yes', '']:
        analyzer.plot_historical_analysis()

def menu_principal():
    """
    Menu principal pour choisir le type de simulation
    """
    while True:
        print("\n" + "=" * 60)
        print("SIMULATEUR DCA OR - MENU PRINCIPAL")
        print("=" * 60)
        print("1. Simulation DCA personnalisée (historique)")
        print("2. Exemples prédéfinis DCA")
        print("3. Analyse comparative des périodes")
        print("4. Simulation Monte Carlo DCA")
        print("5. Simulation Hybride (Historique + Monte Carlo)")
        print("6. Analyse de volatilité")
        print("7. Quitter")
        
        choix = input("\nChoisissez une option (1-7): ").strip()
        
        if choix == "1":
            simulation_personnalisee()
        elif choix == "2":
            exemples_predefinies()
        elif choix == "3":
            analyser_periodes()
        elif choix == "4":
            simulation_monte_carlo()
        elif choix == "5":
            simulation_hybride()
        elif choix == "6":
            analyse_volatilite()
        elif choix == "7":
            print("Au revoir!")
            break
        else:
            print("Choix invalide. Veuillez choisir entre 1 et 7.")

if __name__ == "__main__":
    menu_principal()