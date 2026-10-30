import csv
import sqlite3
import os
# EXTRAICTION DES DONNÉES
# Une fonction qui s'occupe de l'extraction des données dans notre base de donnée
def extraction_data(curs):
    # PARTIE Problématique
    '''
        Problématique 1:
        Dans quelle mesure les caractéristiques géographiques et climatiques, ainsi que 
        les indicateurs socio-économiques influencent-ils la qualité de l'air dans les communes
        d'Occitanie ?   
    '''
    # Requette pour Problématique 1 
    curs.execute("""
        SELECT 
        Geo_climatiques.nom_com, 
        Geo_climatiques.population, 
        Geo_climatiques.densite,
        Geo_climatiques.Force_vent_med, 
        Socio_economiques.nb_logements_2022,
        Socio_economiques.pourcentage_locataires_2022,
        AVG(Mesures_pollution.valeur_poll) as Moyenne_Mesure_Pollution, 
        Mesures_pollution.influence,
		COUNT(DISTINCT Mesures_pollution.nom_station) AS nb_Stations
    FROM Geo_climatiques
    INNER JOIN Socio_economiques USING(code_insee_com)
    INNER JOIN Mesures_pollution USING(code_insee_com)
    WHERE Mesures_pollution.nom_poll = "NOX" and Geo_climatiques.reg_code = 76
    GROUP BY Geo_climatiques.nom_com, 
    Geo_climatiques.code_insee_com
    ORDER BY Moyenne_Mesure_Pollution DESC;
    """)

    # On exécute
    tab1 = curs.fetchall()
    # Avec un mode w pour l'ecriture, un encoding='utf-8' pour gerer l'encodage et un newline='' pour les sauts de lignes
    with open('P1_analyse_geoClimatique.csv', mode='w', encoding='utf-8', newline='') as prob1:
        writer = csv.writer(prob1)
        
        # On écrit les entêtes (les noms des colonnes)
        writer.writerow(['nom_com', 'population', 'densite', 'Force_vent_med', 'nb_logements_2022',
                        'pourcentage_locataires_2022', 'Moyenne_Mesure_Pollution',
                        'influence', 'nb_Stations'])
        
        # On écrit toutes les lignes de données
        writer.writerows(tab1)

    '''
        Problématique 2: 
        Est-ce que la densité de population et la proportion d'appartements 
        aggravent la pollution au NO2 ?
    '''
    # Requette pour Problématique 2
    curs.execute("""
        SELECT 
        Geo_climatiques.nom_com,
        Geo_climatiques.densite,                     
        Socio_economiques.Pourcentage_appartements_2022, 
        AVG(Mesures_pollution.valeur_poll) AS moy_NO2    
    FROM Geo_climatiques 
    INNER JOIN Socio_economiques 
        ON Geo_climatiques.code_insee_com = Socio_economiques.code_insee_com
    INNER JOIN Mesures_pollution 
        ON Geo_climatiques.code_insee_com = Mesures_pollution.code_insee_com
    WHERE Mesures_pollution.nom_poll = 'NO2' 
    AND Geo_climatiques.reg_nom = 'Occitanie'
    GROUP BY Geo_climatiques.code_insee_com
    ORDER BY Geo_climatiques.densite DESC;
    """)

    # On exécute
    tab2 = curs.fetchall()
    # Avec un mode w pour l'ecriture, un encoding='utf-8' pour gerer l'encodage et un newline='' pour les sauts de lignes
    with open('P2_analyse_densite_population.csv', mode='w', encoding='utf-8', newline='') as prob2:
        writer = csv.writer(prob2)
        
        # On écrit les entêtes (les noms des colonnes)
        writer.writerow(['nom_com', 'densite', 'prop_appart', 'moy_no2'])
        
        # On écrit toutes les lignes de données
        writer.writerows(tab2)

    '''
        Problematique 3:
        Les niveaux de pollution résultent-ils davantage des caractéristiques naturelles ou de 
        l’intensité des activités humaines ?
    '''
    # Requette pour Problématique 3 
    curs.execute("""
        SELECT
        Mesures_pollution.nom_com,
        Mesures_pollution.typologie,
        Mesures_pollution.influence,
        Mesures_pollution.nom_poll,
        AVG(valeur_poll) AS valeur_moyenne
    FROM mesures_pollution
    INNER JOIN Geo_climatiques USING(code_insee_com)
    INNER JOIN Socio_economiques USING(code_insee_com)
    WHERE Geo_climatiques.reg_nom = 'Occitanie'
    GROUP BY Mesures_pollution.nom_com,  
    Mesures_pollution.nom_poll,  
    Mesures_pollution.typologie, Mesures_pollution.influence
    ORDER BY valeur_moyenne DESC;
    """)

    # On exécute
    tab3 = curs.fetchall()
    # Avec un mode w pour l'ecriture, un encoding='utf-8' pour gerer l'encodage et un newline='' pour les sauts de lignes
    with open('P3_analyse_niveaux_de_pollution.csv', mode='w', encoding='utf-8', newline='') as prob3:
        writer = csv.writer(prob3)
        
        # On écrit les entêtes (les noms des colonnes)
        writer.writerow(['nom_com', 'typologie', 'influence', 'nom_poll', 'valeur_moyenne'])
        
        # On écrit toutes les lignes de données
        writer.writerows(tab3)

    
    '''
        Problematique 4:
        Les conditions climatiques moderent-elles l'exposition à la pollution selon
        les types de station ?
    '''
    # Requette pour Problématique 4
    curs.execute("""
        SELECT 
        Geo_climatiques.nom_com,
        Mesures_pollution.typologie,
        Geo_climatiques.Tmax_med, 
        Geo_climatiques.Force_vent_med,
        Geo_climatiques.RR_med, 
        AVG(Mesures_pollution.valeur_poll) AS pollution_moyenne
    FROM Mesures_pollution
    INNER JOIN Geo_climatiques 
    ON Mesures_pollution.code_insee_com = Geo_climatiques.code_insee_com
    WHERE Geo_climatiques.reg_nom = 'Occitanie'
    GROUP BY Geo_climatiques.code_insee_com, Mesures_pollution.typologie
    ORDER BY Mesures_pollution.typologie;
    """)

    # On exécute
    tab4 = curs.fetchall()
    # Avec un mode w pour l'ecriture, un encoding='utf-8' pour gerer l'encodage et un newline='' pour les sauts de lignes
    with open('P4_analyse_conditions_climatique.csv', mode='w', encoding='utf-8', newline='') as prob4:
        writer = csv.writer(prob4)
        
        # On écrit les entêtes (les noms des colonnes)
        writer.writerow(['typologie', 'Tmax_med', 'Force_vent_med', 'RR_med', 'pollution_moyenne'])
        
        # On écrit toutes les lignes de données
        writer.writerows(tab4)

    '''
        Problematique 5:
        Comment la pollution atmosphérique varie-t-elle mois par mois dans une année donnée 
        pour les communes d’Occitanie ? 
    '''
    # Requette pour Problématique 5
    curs.execute("""
        SELECT
        Mesures_pollution.mois,
        Mesures_pollution.nom_poll,
        AVG(Mesures_pollution.valeur_poll) AS moyenne_pollution
    FROM Mesures_pollution 
    JOIN Geo_climatiques  ON Mesures_pollution.code_insee_com  = Geo_climatiques.code_insee_com
    WHERE Geo_climatiques.reg_nom = 'Occitanie' AND Mesures_pollution.annee = 2023
    GROUP BY Mesures_pollution.mois, Mesures_pollution.nom_poll
    ORDER BY Mesures_pollution.mois;
    """)
    
    # On exécute
    tab5 = curs.fetchall()
    # Avec un mode w pour l'ecriture, un encoding='utf-8' pour gerer l'encodage et un newline='' pour les sauts de lignes
    with open('P5_analyse_pollution_atmospherique.csv', mode='w', encoding='utf-8', newline='') as prob5:
        writer = csv.writer(prob5)
        
        # On écrit les entêtes (les noms des colonnes)
        writer.writerow(['mois', 'nom_poll', 'moyenne_pollution'])
        
        # On écrit toutes les lignes de données
        writer.writerows(tab5)