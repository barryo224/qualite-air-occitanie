import csv
import sqlite3
import os

# CONNEXION ET CRÉATION DES TABLES
# Une fonction qui s'occupe de la connexion et la création des tables
def connect_and_createTable(name_BD):
    # Si le fichier existe, on le supprime pour recommencer proprement
    if os.path.exists(name_BD):
        os.remove(name_BD)
        print(f"Ancienne base {name_BD} supprimée pour remise à zéro.")

    db = sqlite3.connect(name_BD)
    curs = db.cursor()

    # Ici on a pensé à activer les clés étrangères à travers PRAGMA foreign_keys car 
    # après un run de notre code, on avait des erreurs de contrainte d'integrigté concernanant les clés 
    # Aide : Documentation SQlite
    # Source : https://sqlite.org/foreignkeys.html
    curs.execute("PRAGMA foreign_keys = ON;")

    # TABLE 1 : GEO_CLIMATIQUES (code_insee_com INTEGER PRIMARY KEY)
    # Table de référence de toutes les autres tables
    curs.execute("""
    CREATE TABLE IF NOT EXISTS Geo_climatiques (
        code_insee_com INTEGER PRIMARY KEY,
        nom_com TEXT, 
        reg_code INTEGER, 
        reg_nom TEXT, 
        dep_code INTEGER, 
        dep_nom TEXT,
        population INTEGER, 
        superficie_km2 REAL, 
        densite REAL, 
        latitude REAL, 
        longitude REAL,
        densite_cat TEXT, 
        alti_med REAL, 
        RR_med REAL, 
        NBJRR1_med REAL, 
        NBJRR5_med REAL,
        NBJRR10_med REAL, 
        Tmin_med REAL, 
        Tmax_med REAL, 
        Tens_vap_med REAL, 
        Force_vent_med REAL, 
        Insolation_med REAL, 
        Rayonnement_med REAL
    );
    """)

    # TABLE 2 : SOCIO_ECONOMIQUES (code_insee_com INTEGER PRIMARY KEY, FOREIGN KEY (code_insee_com) REFERENCES Geo_climatiques(code_insee_com))
    # Table liée à Geo_climatiques
    curs.execute("""
    CREATE TABLE IF NOT EXISTS Socio_economiques (
        code_insee_com INTEGER PRIMARY KEY,
        nom_com TEXT, 
        niveau_vie_median_2021 REAL, 
        nb_logements_2022 INTEGER,
        Pourcentage_appartements_2022 REAL, 
        pourcentage_locataires_2022 REAL,
        evolution_pop_pourcentage REAL, 
        population_municipale_2023 INTEGER,
        taux_activite_15_64_2022 REAL,
        FOREIGN KEY (code_insee_com) REFERENCES Geo_climatiques(code_insee_com)
    );
    """)

    # TABLE 3 : MESURE_POLLUTION (id_mesure INTEGER PRIMARY KEY AUTOINCREMENT, FOREIGN KEY (code_insee_com) REFERENCES Geo_climatiques(code_insee_com))
    # Table Pollution liée à Geo_climatiques
    # Ici on a pensé à avoir une clé primaire qui n'est pas dans le csv car avec code_insee_com, on perdait beaucoup d'informations
    curs.execute("""
    CREATE TABLE IF NOT EXISTS Mesures_pollution (
        id_mesure INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_dept TEXT, 
        nom_com TEXT, 
        code_insee_com INTEGER,
        nom_station TEXT, 
        code_station TEXT, 
        typologie TEXT, 
        influence TEXT,
        nom_poll TEXT, 
        valeur_poll REAL, 
        jour INTEGER, 
        mois INTEGER, 
        annee INTEGER,
        FOREIGN KEY (code_insee_com) REFERENCES Geo_climatiques(code_insee_com)
    );
    """)
    return db, curs