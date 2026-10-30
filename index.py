import csv
import sqlite3
import os

# Importation des fichiers
from connect import connect_and_createTable
from insert import insertion_data
from extract import extraction_data
    

# PROGRAMME PRINCIPAL
if __name__ == "__main__":
    db, curs = connect_and_createTable("BD_Project.db") # On a retourner un tuple, donc on appele notre fonction avec un tuple
    insertion_data(curs) # La fonction insertion_data qui prends en paramètre le curseur
    db.commit() # On a fait le commit après la connexion, création des tables et l'insertion des données
                # Pas besoin pour l'extraction des données
    extraction_data(curs) # La fonction extraction_data qui prends en paramètre le curseur

    # Fermeture du curseur et de la base de donnée
    curs.close()
    db.close()

    print("La base de données a été clôturée avec succès !")