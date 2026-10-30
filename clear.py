# FONCTION DE NETTOYAGE
def nettoyer(val, type_cible=float):
    if val is None: 
        return None
    # On nettoie les guillemets et les espaces et on remplace tout ce qui est est virgule
    # par un point pour donner la meme structure à tous les valeurs flottantes
    val = str(val).strip().replace('"', '').replace(',', '.')
    # On a ciblé ces chaines de caractères dans nos fichiers csv, donc on les remplace tous par null
    textes_na = ["", "NA", "N/A", "N/A - RÉSULTAT NON DISPONIBLE", "RESULTAT NON DISPONIBLE"]
    if val.upper() in textes_na:
        return None
    try:
        return type_cible(float(val))
    except (ValueError, TypeError):
        return None