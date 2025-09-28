"""
Analyse de la volatilité historique de l'or pour alimenter les simulations Monte Carlo
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

class GoldVolatilityAnalysis:
    def __init__(self, data_file: str = "data/annual.csv"):
        """
        Analyse la volatilité historique des prix de l'or
        """
        self.df = pd.read_csv(data_file)
        self.df['Date'] = self.df['Date'].astype(int)
        self.df = self.df.set_index('Date').sort_index()
        
        # Calculer les rendements annuels
        self.df['Returns'] = self.df['Price'].pct_change()
        self.df['Log_Returns'] = np.log(self.df['Price'] / self.df['Price'].shift(1))
        
        # Supprimer les valeurs NaN
        self.df = self.df.dropna()
        
    def calculate_volatility_metrics(self) -> dict:
        """
        Calcule les métriques de volatilité et de rendement
        """
        returns = self.df['Returns'].dropna()
        log_returns = self.df['Log_Returns'].dropna()
        
        metrics = {
            'mean_return': returns.mean(),
            'std_return': returns.std(),
            'mean_log_return': log_returns.mean(),
            'std_log_return': log_returns.std(),
            'min_return': returns.min(),
            'max_return': returns.max(),
            'skewness': stats.skew(returns),
            'kurtosis': stats.kurtosis(returns),
            'sharpe_ratio': returns.mean() / returns.std() if returns.std() > 0 else 0
        }
        
        return metrics
    
    def analyze_periods(self) -> dict:
        """
        Analyse la volatilité par périodes historiques
        """
        periods = {
            'Gold_Standard': (1833, 1971),
            'Post_Bretton_Woods': (1972, 1980), 
            'Stabilization': (1981, 2000),
            'Modern_Era': (2001, 2024)
        }
        
        period_analysis = {}
        
        for period_name, (start, end) in periods.items():
            period_data = self.df[(self.df.index >= start) & (self.df.index <= end)]
            if len(period_data) > 1:
                returns = period_data['Returns'].dropna()
                if len(returns) > 0:
                    period_analysis[period_name] = {
                        'years': f"{start}-{end}",
                        'mean_return': returns.mean(),
                        'std_return': returns.std(),
                        'min_return': returns.min(),
                        'max_return': returns.max(),
                        'count': len(returns)
                    }
        
        return period_analysis
    
    def get_monte_carlo_params(self, period: str = 'Modern_Era') -> dict:
        """
        Obtient les paramètres pour les simulations Monte Carlo
        """
        period_analysis = self.analyze_periods()
        
        if period in period_analysis:
            params = period_analysis[period]
        else:
            # Utiliser les données complètes si la période n'est pas trouvée
            metrics = self.calculate_volatility_metrics()
            params = {
                'mean_return': metrics['mean_return'],
                'std_return': metrics['std_return']
            }
        
        return {
            'drift': params['mean_return'],
            'volatility': params['std_return'],
            'period_used': period
        }
    
    def plot_historical_analysis(self):
        """
        Crée des graphiques d'analyse historique
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Analyse Historique des Prix de l\'Or', fontsize=16, fontweight='bold')
        
        # Prix historiques
        axes[0, 0].plot(self.df.index, self.df['Price'], linewidth=1)
        axes[0, 0].set_title('Prix Historique de l\'Or')
        axes[0, 0].set_xlabel('Année')
        axes[0, 0].set_ylabel('Prix (USD/oz)')
        axes[0, 0].grid(True, alpha=0.3)
        
        # Rendements annuels
        axes[0, 1].plot(self.df.index[1:], self.df['Returns'].dropna(), linewidth=1, color='green')
        axes[0, 1].axhline(y=0, color='red', linestyle='--', alpha=0.7)
        axes[0, 1].set_title('Rendements Annuels')
        axes[0, 1].set_xlabel('Année')
        axes[0, 1].set_ylabel('Rendement (%)')
        axes[0, 1].grid(True, alpha=0.3)
        
        # Distribution des rendements
        returns = self.df['Returns'].dropna()
        axes[1, 0].hist(returns, bins=30, alpha=0.7, color='blue', edgecolor='black')
        axes[1, 0].axvline(returns.mean(), color='red', linestyle='--', label=f'Moyenne: {returns.mean():.3f}')
        axes[1, 0].set_title('Distribution des Rendements')
        axes[1, 0].set_xlabel('Rendement')
        axes[1, 0].set_ylabel('Fréquence')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # Volatilité roulante (10 ans)
        rolling_vol = self.df['Returns'].rolling(window=10).std()
        axes[1, 1].plot(rolling_vol.index, rolling_vol, linewidth=1, color='orange')
        axes[1, 1].set_title('Volatilité Roulante (10 ans)')
        axes[1, 1].set_xlabel('Année')
        axes[1, 1].set_ylabel('Volatilité')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def print_analysis_report(self):
        """
        Imprime un rapport d'analyse détaillé
        """
        print("=" * 80)
        print("ANALYSE DE LA VOLATILITÉ HISTORIQUE DE L'OR")
        print("=" * 80)
        
        # Métriques globales
        metrics = self.calculate_volatility_metrics()
        
        print("\nMÉTRIQUES GLOBALES (1834-2024):")
        print(f"Rendement annuel moyen: {metrics['mean_return']:.3f} ({metrics['mean_return']*100:.1f}%)")
        print(f"Volatilité (écart-type): {metrics['std_return']:.3f} ({metrics['std_return']*100:.1f}%)")
        print(f"Rendement minimum: {metrics['min_return']:.3f} ({metrics['min_return']*100:.1f}%)")
        print(f"Rendement maximum: {metrics['max_return']:.3f} ({metrics['max_return']*100:.1f}%)")
        print(f"Asymétrie (skewness): {metrics['skewness']:.3f}")
        print(f"Aplatissement (kurtosis): {metrics['kurtosis']:.3f}")
        print(f"Ratio de Sharpe: {metrics['sharpe_ratio']:.3f}")
        
        # Analyse par périodes
        period_analysis = self.analyze_periods()
        
        print(f"\nANALYSE PAR PÉRIODES:")
        print(f"{'Période':<20} {'Années':<12} {'Rend. Moy.':<12} {'Volatilité':<12} {'Min':<10} {'Max':<10}")
        print("-" * 80)
        
        for period_name, data in period_analysis.items():
            print(f"{period_name.replace('_', ' '):<20} "
                  f"{data['years']:<12} "
                  f"{data['mean_return']*100:<11.1f}% "
                  f"{data['std_return']*100:<11.1f}% "
                  f"{data['min_return']*100:<9.1f}% "
                  f"{data['max_return']*100:<9.1f}%")

def main():
    """
    Fonction principale pour l'analyse de volatilité
    """
    print("Analyse de la volatilité de l'or pour Monte Carlo")
    print("=" * 50)
    
    # Créer l'analyse
    analyzer = GoldVolatilityAnalysis()
    
    # Afficher le rapport
    analyzer.print_analysis_report()
    
    # Obtenir les paramètres Monte Carlo pour différentes périodes
    print(f"\nPARAMÈTRES MONTE CARLO PAR PÉRIODE:")
    periods = ['Gold_Standard', 'Post_Bretton_Woods', 'Stabilization', 'Modern_Era']
    
    for period in periods:
        params = analyzer.get_monte_carlo_params(period)
        if 'drift' in params:
            print(f"\n{period.replace('_', ' ')}:")
            print(f"  Drift (rendement moyen): {params['drift']:.4f}")
            print(f"  Volatilité: {params['volatility']:.4f}")
    
    # Créer les graphiques
    print("\nCréation des graphiques d'analyse...")
    analyzer.plot_historical_analysis()

if __name__ == "__main__":
    main()