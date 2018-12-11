'''
Name: Uly and Jude
Date: 12/11/2018
The purpose of this project is to use a graphical data structure to emulate the oracle of Kevin Bacon website.
Collaborators: us
On My Honor: UA and JB


'''
import json, csv, os

globalActors = [None]*1000000#00
globalMovies = [None]*1000000#00
class ActorNode():#you would need different inits so it makes no sense to extend
    def __init__(self, id, name, movies):
        self.id = id
        self.name = name
        self.links = movies
    def __repr__(self):
        return self.name

class MovieNode():
    def __init__(self, id, actors):
        self.id = id
        self.links = actors
    def __repr__(self):
        return self.id

def makeActorFile(input):
    data = {}
    print("Opening Actor File")
    with open(input, encoding='utf-8') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            if row[0] != 'nconst':
                data[row[0]] = {"name": row[1], "movies": row[5]}
    print("Actor File Loaded")
    print("Saving Actor Data")
    f = open("actor.json", "w")
    f.write(json.dumps(data))
    print("Actor Data Saved")

def makeMovieFile(input):
    data = {}
    print("Opening Movie File")
    with open(input, encoding='utf-8') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        cur = ""
        curActors = []
        for row in reader:
            if row[0] != 'tconst':
                if row[0] != cur:
                    data[cur] = {"actors": curActors}
                    curActors = [row[2]]
                    cur = row[0]
                else:
                    curActors.append(row[2])
    print("Movie File Loaded")
    print("Saving Movie Data")
    f = open("movie.json", "w")
    f.write(json.dumps(data))
    print("Movie Data Saved")

def addActor(node):
    globalActors[int(node.id[2:])] = node

def addMovie(node):
    if node.id != '':
        globalMovies[int(node.id[2:])] = node

def getActorFile():
    data = {}
    print("Loading Actor File")
    with open('actor.json') as f:
        data = json.loads(f.read())
        i = 0
        print("Actor File Loaded")
        for key in data:
            i += 1
        print(str(i) + " Actors found")
        print("Parsing Actor File Into RAM")
        for key in data:
            addActor(ActorNode(str(key), str(data[key]['name']), data[key]['movies'].split(',')))
        print("Actor File Parsed Into RAM")

def getMovieFile():
    data = {}
    print("Loading Movie File")
    with open('movie.json') as f:
        data = json.loads(f.read())
        i = 0
        print("Movie File Loaded")
        for key in data:
            i += 1
        print(str(i) + " Movies found")
        print("Parsing Movie File Into RAM")
        for key in data:
            addMovie(MovieNode(str(key), data[key]['actors']))
        print("Movie File Parsed Into RAM")

def findActor(nconst):
    if int(nconst[2:]) <= len(globalActors):
        return globalActors[int(nconst[2:])]
    else:
        return None

def findActorName(name):
    for actor in globalActors:
        if actor is not None:
            if actor.name.lower() == name.lower():
                return actor
    return None

def findMovie(tconst):
    if tconst == "\\N":
        return None
    if int(tconst[2:]) <= len(globalMovies):
        return globalMovies[int(tconst[2:])]
    else:
        return None

def linkData():
    print("Linking Actors")
    for actor in globalActors:
        if actor != None:
            tempArr = []
            for link in actor.links:
                if findMovie(link) != None:
                    tempArr.append(findMovie(link))
            actor.links = tempArr
    print("Actors Linked")
    print("------")
    print("Linking Movies")
    for movie in globalMovies:
        if movie != None:
            tempArr = []
            for link in movie.links:
                if findActor(link) != None:
                    tempArr.append(findActor(link))
            movie.links = tempArr
    print("Movies Linked")
    print("------")
'''
Our BFS worst case scenario should have a run time of O(2^n), which is very long. 
In the worst case scenario, this BFS search would look through every single node in the graph, taking an exponential amount of time going down each branch.
'''
def BFS(node1, node2): 
    checked = []
    counter = 0
    queue1 = [node1]
    queue2 = []
    while counter < 10:
        for item in queue1:
            if item.id == node2.id:
                return counter
            for link in item.links:
                if link not in checked:
                    queue2.append(link)
        counter += 1
        queue1 = []
        for item in queue2:
            if item.id == node2.id:
                return counter
            for link in item.links:
                if link not in checked:
                    queue1.append(link)
        counter += 1
        queue2 = []
    return -1

'''
This uses BFS which is O(2^n), so the function itself is exponential.
'''
def calculateNumber(actor, targetActor):
    if findActorName(actor) is None or findActorName(targetActor) is None:
        return -1
    return BFS(findActorName(actor), findActorName(targetActor))/2

'''
This uses BFS which is O(2^n), so the function itself is exponential.
'''
def calculateBaconNumber(actor):# no overloading so we changed the name
    if findActorName(actor) is None:
        return -1
    return BFS(findActorName(actor), findActor("nm0000102"))/2

'''This runtime is O(n*2^n), but that simplifies down to O(2^n) because it loops through each actor and then runs BFS.'''
def calculateAvgBacon():
    actorNum = 0
    links = 0
    for actor in globalActors:
        if actor is not None:
            temp = calculateBaconNumber(actor.name)
            if temp != -1:
                actorNum += 1
                links += temp
    return 1.0*links/actorNum


'''This runtime is O(n*2^n), but that simplifies down to O(2^n) because it loops through each actor and then runs BFS.'''
def calculateAvgHollyWood(actorIn):
    actorNum = 0
    links = 0 
    for actor in globalActors:
        if actor is not None:
            temp = calculateNumber(actor.name, actorIn)
            if temp != -1:
                actorNum += 1
                links += temp
    return 1.0*links/actorNum

def prepData():
    if os.path.isfile('actor.json'):
        print('Actor File Found') 
    else:
        print('Actor File Not Found')
        makeActorFile('name.tsv')#change to big one
    print("------")
    if os.path.isfile('movie.json'):
        print('Movie File Found') 
    else:
        print('Movie File Not Found')
        makeMovieFile('title.tsv')#change to big one
    print("------")
    getActorFile()
    print("------")
    getMovieFile()
    print("------")
    linkData()

def driver():
    prepData()
    inp = ''
    while inp is not 'q':
        print("Bacon Number : B, Other Number : O, Avg Bacon: A, Avg Other: V, Quit: Q")
        inp = input("Choose One : ").lower()
        if inp == 'b':
            temp = input("Other Actor : ")
            print(calculateBaconNumber(temp))
            print("------")
        elif inp == 'o':
            tempOne = input("Actor 1 : ")
            tempTwo = input("Actor 2 : ")
            print(calculateNumber(tempOne, tempTwo))
            print("------")
        elif inp == 'a':
            print(calculateAvgBacon())
        elif inp == 'v':
            temp = input("Actor : ")
            print(calculateAvgHollyWood(temp))
        elif inp == 'q':
            return

driver()
#Herbert Beerbohm Tree
#Fred Astaire