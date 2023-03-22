import requests
import bs4
import json

def liste_liens(page):
    url = f"https://iceandfire.fandom.com/wiki/{page}"
    req = requests.get(url)
    html = bs4.BeautifulSoup(req.content, "html.parser")
    links = html.find_all("a") # on récupère tous les liens
    noms_pages = []
    for link in links:
        if(link.get("href") and link.get("href").startswith("/wiki/")): # on vérifie que le lien existe et qu'il commence par "/wiki/"
            noms_pages.append(link.get("href")[6:]) # on ajoute le nom de la page à la liste
    return noms_pages
    
#on sauvegarde le dictionnaire contenant les liens de chaque page dans un fichier json
def svg_dico(dico, fichier):
    with open(fichier, 'w') as f:
        json.dump(dico, f)
            
#on charge le dictionnaire contenant les liens de chaque page à partir d'un fichier json
def chg_dico(fichier ):
    with open(fichier) as f:
        return json.load(f)

def nombre_charactere(cible):
    return len(cible)

def nombre_voyelles(cible):
    cible = cible.lower()
    voyelles = ["a", "e", "i", "o", "u", "y"]
    nombre = 0
    for lettre in cible:
        if lettre in voyelles:
            nombre += 1
    return nombre

pages = chg_dico("pages.json")
def plus_court_chemin(source, target):
    aExplorer = [(0, source, [source])] # liste de tuples (poids, page, chemin)
    visited = set() # ensemble de pages déjà explorées
    while aExplorer: 
        # recuperer le tuple avec le plus petit poids
        poids, page, chemin = min(aExplorer, key= lambda x : x[0]) # on recupere le tuple avec le plus petit poids
        aExplorer.remove((poids, page, chemin)) # on supprime le tuple de la liste des pages à explorer
        # on verifie si la page est la page cible
        if page == target:
            return chemin
        # si la page a déjà été explorée, on passe à la page suivante
        if page in visited:
            continue
        # on ajoute la page à l'ensemble des pages explorées
        visited.add(page)
        # on recupere les liens de la page depuis le site si la page n'est pas dans le dictionnaire
        if(page not in pages.keys()):
            liens = liste_liens(page)
            pages[page] = liens
        else:
            liens = pages[page] # mode offline pour recuperer les liens de la page à partir du dictionnaire
        # on ajoute les liens de la page à la liste des pages à explorer
        for lien in liens:
            if lien not in visited:
                aExplorer.append((poids + 1, lien, chemin + [lien])) # on ajoute un poids de 1 à chaque lien 
    return None

def plus_court_chemin_voyelles(source, target):
    aExplorer = [(0, source, [source])] # liste de tuples (poids, page, chemin)
    visited = set() # ensemble de pages déjà explorées
    while aExplorer: 
        # recuperer le tuple avec le plus petit poids
        poids, page, chemin = min(aExplorer, key= lambda x : x[0]) # on recupere le tuple avec le plus petit poids
        aExplorer.remove((poids, page, chemin)) # on supprime le tuple de la liste des pages à explorer
        # on verifie si la page est la page cible
        if page == target:
            return chemin
        # si la page a déjà été explorée, on passe à la page suivante
        if page in visited:
            continue
        # on ajoute la page à l'ensemble des pages explorées
        visited.add(page)
        # on recupere les liens de la page depuis le site si la page n'est pas dans le dictionnaire
        if(page not in pages.keys()):
            liens = liste_liens(page)
            pages[page] = liens
        else:
            liens = pages[page] # mode offline pour recuperer les liens de la page à partir du dictionnaire
        # on ajoute les liens de la page à la liste des pages à explorer
        for lien in liens:
            if lien not in visited:
                cout = nombre_charactere(lien) + nombre_voyelles(lien)
                aExplorer.append((poids + cout, lien, chemin + [lien])) # on ajoute un poids de 1 à chaque lien 
    return None

source = "Dorne" 
target = "Rhaego"
chemin = plus_court_chemin(source, target)
print("Plus court chemin entre", source, "et", target, ":")
print(chemin)
print("plus court chemin en nombre de voyelles")
chemin = plus_court_chemin_voyelles(source, target)
print(chemin)

svg_dico(pages,"pages.json")