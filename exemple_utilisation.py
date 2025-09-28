"""
Exemple d'utilisation simple du simulateur DCA
Ce fichier montre comment utiliser la classe GoldDCASimulator
"""

from dca_simulation import GoldDCASimulator
from config import SCENARIOS

def exemple_simple():
    """
    Exemple d'utilisation simple du simulateur
    """
    print("Exemple Simple - Simulation DCA sur l'Or")
    print("=" * 50)
    
    # Créer une instance du simulateur
    simulator = GoldDCASimulator()
    
    # Configurer la simulation
    # 1. Variable qui indique le niveau d'investissement au cours de l'année n
    investissement_annuel = 2000.0  # 2000 USD par an
    
    # 2. & 3. Calculer la valeur sur n années et nombre d'années de répétition
    nombre_annees = 15  # 15 ans d'investissement
    annee_debut = 2009  # Commencer en 2009 (après la crise)
    
    # 5. Variable qui calcule les frais par once d'or détenus
    frais_par_once = 30.0  # 30 USD de frais par once par an
    
    # Configuration de la simulation
    simulator.configure_simulation(
        investissement_annuel=investissement_annuel,
        nombre_annees=nombre_annees, 
        annee_debut=annee_debut,
        frais_par_once=frais_par_once
    )
    
    # Exécution de la simulation
    resultats = simulator.simuler_dca()
    
    # Affichage des résultats
    simulator.afficher_resultats(resultats)
    simulator.afficher_tableau_detaille(resultats)
    
    print("\n" + "="*60)
    print("ANALYSE DES VARIABLES PRINCIPALES")
    print("="*60)
    
    # 1. Niveau d'investissement annuel
    print(f"1. Investissement annuel fixe: {investissement_annuel:,.2f} USD")
    
    # 2. Valeur de l'investissement sur n années  
    valeur_finale = resultats['valeur_portefeuille'][-1]
    print(f"2. Valeur finale après {nombre_annees} ans: {valeur_finale:,.2f} USD")
    
    # 3. Nombre d'années d'investissement
    print(f"3. Période d'investissement: {nombre_annees} années ({annee_debut}-{annee_debut + nombre_annees - 1})")
    
    # 4. Nombre d'onces possédées au cours du temps
    onces_finales = resultats['onces_totales'][-1]
    print(f"4. Onces d'or finales possédées: {onces_finales:.4f} oz")
    
    # 5. Frais par once
    frais_totaux = resultats['frais_totaux'][-1]
    print(f"5. Frais totaux payés: {frais_totaux:,.2f} USD")
    print(f"   Frais par once par an: {frais_par_once:.2f} USD")
    
    # Statistiques additionnelles
    investissement_total = resultats['investissement_cumule'][-1]
    prix_moyen_achat = investissement_total / onces_finales if onces_finales > 0 else 0
    prix_final = resultats['prix_or'][-1]
    
    print(f"\nPrix moyen d'achat: {prix_moyen_achat:.2f} USD/oz")
    print(f"Prix final de l'or: {prix_final:.2f} USD/oz")
    print(f"Évolution du prix: {((prix_final - prix_moyen_achat) / prix_moyen_achat * 100):.1f}%")

def comparaison_scenarios():
    """
    Compare plusieurs scénarios prédéfinis
    """
    print("\n" + "="*70)
    print("COMPARAISON DE SCÉNARIOS D'INVESTISSEMENT")
    print("="*70)
    
    simulator = GoldDCASimulator()
    
    print(f"{'Scénario':<15} {'Invest/An':<10} {'Années':<7} {'Début':<6} {'Frais':<8} {'Rendement':<10} {'Onces':<8}")
    print("-" * 70)
    
    for nom_scenario, config in SCENARIOS.items():
        try:
            simulator.configure_simulation(**config)
            resultats = simulator.simuler_dca()
            
            rendement = resultats['rendement_pourcent'][-1]
            onces = resultats['onces_totales'][-1]
            
            print(f"{nom_scenario:<15} "
                  f"{config['investissement_annuel']:<10.0f} "
                  f"{config['nombre_annees']:<7} "
                  f"{config['annee_debut']:<6} "
                  f"{config['frais_par_once']:<8.0f} "
                  f"{rendement:<9.1f}% "
                  f"{onces:<8.2f}")
                  
        except (ValueError, KeyError):
            print(f"{nom_scenario:<15} Données non disponibles")

if __name__ == "__main__":
    exemple_simple()
    comparaison_scenarios()