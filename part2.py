import requests
from bs4 import BeautifulSoup
import json
def getCharacters():
    pages = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z","¡"]
    characters = []
    for page in pages:
        url = f"https://iceandfire.fandom.com/wiki/Category:Characters?from={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        for li in soup.find_all('li', {'class': 'category-page__member'}):
            atags = li.findAll('a')
            for a in atags:
                character = a.text.strip() # recuperer l'element a et recuperer le text puis supprimer les espaces
                if characters != "":
                    characters.append(character)
    return characters

def svg_dico(dico, fichier):
    with open(fichier, 'w') as f:
        json.dump(dico, f, indent=4)
            
#on charge le dictionnaire contenant les liens de chaque page à partir d'un fichier json
def chg_dico(fichier ):
    with open(fichier) as f:
        return json.load(f)
    

def getRelationships():
    characters_relationship = {}
    #saved_relationships = chg_dico("characters_relationship.json")
    #saved_characters = saved_relationships.keys()
    for index, character in enumerate(characters):
        print(f"{index}/{len(characters)}")
        character_url = f"https://iceandfire.fandom.com/wiki/{character}"
        character_response = requests.get(character_url)
        character_soup = BeautifulSoup(character_response.content, 'html.parser')
        characters_relationship[character] = {
            "fatherhood": {"parents": [], "children": []},
            "siblings": [],
            "lovers": [],
        }
        
        for father in character_soup.select('div[data-source="father"] a'):
            characters_relationship[character]['fatherhood']["parents"].append(father.text)
        
        for mother in character_soup.select('div[data-source="mother"] a'):
            characters_relationship[character]['fatherhood']['parents'].append(mother.text)
        
        for child in character_soup.select('div[data-source="children"] a'):
            characters_relationship[character]['fatherhood']['children'].append(child.text)
        
        for sibling in character_soup.select('div[data-source="siblings"] a'):
            characters_relationship[character]['siblings'].append(sibling.text)
        
        for spouce in character_soup.select('div[data-source="spouse"] a'):
            characters_relationship[character]['lovers'].append(spouce.text)
        
        for lover in character_soup.select('div[data-source="lover"] a'):
            characters_relationship[character]['lovers'].append(lover.text)
    return characters_relationship
        


def getIncestous(character):
    fatherhood = characters_relationship[character]['fatherhood']['parents']
    fatherhood.extend(characters_relationship[character]['fatherhood']['children'])
    siblings = characters_relationship[character]['siblings']
    lovers = characters_relationship[character]['lovers']
    parentsSiblingsUnion = set(fatherhood).union(set(siblings))
    loversIntersection = set(lovers).intersection(parentsSiblingsUnion)
    return loversIntersection

def getChildren(character):
    children = []
    try:
        for child in characters_relationship[character]['fatherhood']['children']:
            children.append(child)
        return children
    except:
        return []

def ancestorsGraph():
    characters_decendants = {}
    for index,character in enumerate(characters):
        print(f"{index}/{len(characters)}")
        if(index == 1663 or index == 111 or index == 497 or index == 731 or index == 1156 or index == 1356 or index == 1583):
        #    print(character)
            continue
        
        decendants = []
        toBeProcessed = [character]
        while len(toBeProcessed) > 0:
            current = toBeProcessed.pop()
            decendants.extend(getChildren(current))
            toBeProcessed.extend(getChildren(current))
            #print(current)
        characters_decendants[character] = decendants
    return characters_decendants
        
#svg_dico(getCharacters(), "characters.json")
characters = chg_dico("characters.json")
#characters_relationship = getRelationships() #
#svg_dico(characters_relationship,"characters_relationship.json")
characters_relationship = chg_dico("characters_relationship.json")

   
def main():
    #afficher la liste des characters
    #mode online
    #characters = getCharacters()
    #svg_dico(characters, "characters.json")
    #mode offline : a partir d'un fichier json
    characters = chg_dico("characters.json")
    print("Liste des characters :")
    print(characters)
    #afficher les relations entre les characters (parents, enfants, freres, soeurs, amants)
    #characters_relationship = getRelationships()
    #svg_dico(characters_relationship, "characters_relationship.json")
    #mode offline : a partir d'un fichier json
    characters_relationship = chg_dico("characters_relationship.json")
    #exemple : afficher les relations de Jaime Lannister
    character = "Tywin Lannister"
    print(f"Les relations de {character} sont :")
    print(characters_relationship[character])
    #afficher les relations incestueuses de Jaime Lannister
    print(f"Les relations incestueuses de {character} sont avec :")
    print(getIncestous(character))
    #afficher les ancetres de Jaime Lannister
    graphAncestors = ancestorsGraph()
    svg_dico(graphAncestors, "graphAncestors.json")
    print(f"{character} est un ancetre de :")
    print(graphAncestors[character])
main()