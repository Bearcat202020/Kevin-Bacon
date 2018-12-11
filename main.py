import json, csv, heapq

globalActors = [None]*100000
globalMovies = [None]*10000
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
    with open(input, encoding='utf-8') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            if row[0] != 'nconst':
                data[row[0]] = {"name": row[1], "movies": row[5]}
    f = open("actor.json", "w")
    f.write(json.dumps(data))

def makeMovieFile(input):
    data = {}
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
    f = open("movie.json", "w")
    f.write(json.dumps(data))

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

def findMovie(tconst):
    if tconst == "\\N":
        return None
    if int(tconst[2:]) <= len(globalMovies):
        return globalMovies[int(tconst[2:])]
    else:
        return None

def makeFiles():
    makeActorFile('test.tsv')
    makeMovieFile('test1.tsv')

def getFiles():
    getActorFile()
    print("------")
    getMovieFile()
    print("------")

def linkData():
    for actor in globalActors:
        if actor != None:
            tempArr = []
            for link in actor.links:
                if findMovie(link) != None:
                    tempArr.append(findMovie(link))
            actor.links = tempArr
    for movie in globalMovies:
        if movie != None:
            tempArr = []
            for link in movie.links:
                if findActor(link) != None:
                    tempArr.append(findActor(link))
            movie.links = tempArr

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
        print("2:", queue2)
        for item in queue2:
            if item.id == node2.id:
                return counter
            for link in item.links:
                if link not in checked:
                    queue1.append(link)
        counter += 1
        queue2 = []
        print("1:", queue1)
    return -1
makeFiles()
getFiles()
print(findActor("nm0002504"))
linkData()
print(findActor("nm0002504").links)
print(findActor("nm0002504").links[0].links)
print("----")
print(BFS(findActor("nm0002504"), findActor("nm0000001")))
