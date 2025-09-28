# Fichier de configuration pour les simulations DCA
# Vous pouvez modifier ces valeurs selon vos besoins

# Configuration par défaut
DEFAULT_CONFIG = {
    "investissement_annuel": 1000.0,  # USD
    "nombre_annees": 10,
    "annee_debut": 2010,
    "frais_par_once": 25.0  # USD par once par an
}

# Configurations prédéfinies pour différents scénarios
SCENARIOS = {
    "conservateur": {
        "investissement_annuel": 500.0,
        "nombre_annees": 20,
        "annee_debut": 2000,
        "frais_par_once": 20.0
    },
    
    "modere": {
        "investissement_annuel": 2000.0,
        "nombre_annees": 15,
        "annee_debut": 2005,
        "frais_par_once": 25.0
    },
    
    "agressif": {
        "investissement_annuel": 5000.0,
        "nombre_annees": 10,
        "annee_debut": 2010,
        "frais_par_once": 35.0
    },
    
    "crise_2008": {
        "investissement_annuel": 3000.0,
        "nombre_annees": 15,
        "annee_debut": 2008,
        "frais_par_once": 30.0
    },
    
    "post_covid": {
        "investissement_annuel": 4000.0,
        "nombre_annees": 5,
        "annee_debut": 2020,
        "frais_par_once": 40.0
    }
}

# Périodes historiques intéressantes pour l'analyse
PERIODES_HISTORIQUES = {
    "bretton_woods_fin": (1968, 1975),  # Fin du système de Bretton Woods
    "inflation_70s": (1970, 1980),      # Grande inflation des années 70
    "recession_80s": (1980, 1990),      # Récessions des années 80
    "dot_com": (1995, 2005),            # Bulle internet
    "crise_2008": (2005, 2015),         # Crise financière mondiale
    "QE_era": (2010, 2020),             # Ère de l'assouplissement quantitatif
    "post_covid": (2020, 2024)          # Période post-COVID
}