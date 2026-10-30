import csv
import sqlite3
import os

from clear import nettoyer # Import du fichier clear pour nettoyer les variables
# INSERTION DES DONNÉES
# Une fonction qui s'occupe de l'insertion des données dans notre base de donnée
def insertion_data(curs):
    # INSERTION GEO_CLIMATIQUES
    # Avec un mode r pour la lecture et un encoding='utf-8' pour gerer l'encodage
    data1 = []
    with open('donnees_geo_climatiques.csv', mode='r', encoding='utf-8') as geo:
        reader = csv.DictReader(geo)
        for r in reader:
            data1.append((
                nettoyer(r["code_insee_com"], int), 
                r["nom_com"],
                nettoyer(r["reg_code"], int),
                r["reg_nom"],
                nettoyer(r["dep_code"], int), 
                r["dep_nom"],
                nettoyer(r["population"], int), 
                nettoyer(r["superficie_km2"]),
                nettoyer(r["densite"]), 
                nettoyer(r["latitude"]),
                nettoyer(r["longitude"]), 
                r["densite_cat"],
                nettoyer(r["alti_med"]), 
                nettoyer(r["RR_med"]),
                nettoyer(r["NBJRR1_med"]), 
                nettoyer(r["NBJRR5_med"]),
                nettoyer(r["NBJRR10_med"]), 
                nettoyer(r["Tmin_med"]),
                nettoyer(r["Tmax_med"]), 
                nettoyer(r["Tens_vap_med"]),
                nettoyer(r["Force_vent_med"]), 
                nettoyer(r["Insolation_med"]),
                nettoyer(r["Rayonnement_med"])
            ))
    curs.executemany("INSERT OR REPLACE INTO Geo_climatiques VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", data1)

    # On a pensé à récupérer les codes valides pour éviter l'IntegrityError et s'assurer qu'au niveau des jointures
    # on a vraiment des lignes qui se correspondent entre elles
    curs.execute("SELECT code_insee_com FROM Geo_climatiques")
    codes_valides = {row[0] for row in curs.fetchall()}

    # INSERTION SOCIO_ECONOMIQUES
    # Avec un mode r pour la lecture et un encoding='utf-8' pour gerer l'encodage
    data2 = [] 
    with open('donnees_socio_economiques.csv', mode='r', encoding='utf-8') as socio:
        reader = csv.DictReader(socio)
        for r in reader:
            code = nettoyer(r["code_insee_com"], int)
            if code in codes_valides: # On ne prend que ce qui existe dans GEO_CLIMATIQUES
                data2.append((
                    code, 
                    r["nom_com"],
                    nettoyer(r["niveau_vie_median_2021"]),
                    nettoyer(r["nb_logements_2022"], int),
                    nettoyer(r["Pourcentage_appartements_2022"]),
                    nettoyer(r["pourcentage_locataires_dans_résidence_principale_2022"]),
                    nettoyer(r["evolution_annuelle_moy_de_la_population_entre_2017_et_2023_en_pourcentage"]),
                    nettoyer(r["population_municipale_2023"], int),
                    nettoyer(r["Taux_activite_tranche_15_64_en_2022"])
                ))
    curs.executemany("INSERT OR REPLACE INTO Socio_economiques VALUES (?,?,?,?,?,?,?,?,?)", data2)

    # INSERTION MESURE_POLLUTION
    # Avec un mode r pour la lecture et un encoding='utf-8' pour gerer l'encodage
    data3 = []
    with open('mesures_occitanie_journaliere_pollution.csv', mode='r', encoding='utf-8') as pollution:
        reader = csv.DictReader(pollution)
        for r in reader:
            code = nettoyer(r["code_insee_com"], int)
            if code in codes_valides: # On ne prend que ce qui existe dans GEO_CLIMATIQUES
                data3.append((
                    r["nom_dept"], 
                    r["nom_com"], 
                    code,
                    r["nom_station"], 
                    r["code_station"], 
                    r["typologie"], 
                    r["influence"],
                    r["nom_poll"], 
                    nettoyer(r["valeur_poll"]),
                    nettoyer(r["jour"], int), 
                    nettoyer(r["mois"], int),
                    nettoyer(r["annee"], int)
                ))
    curs.executemany("""
        INSERT INTO Mesures_pollution 
        (nom_dept, nom_com, code_insee_com, nom_station, code_station, typologie, influence, nom_poll, valeur_poll, jour, mois, annee)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, data3)