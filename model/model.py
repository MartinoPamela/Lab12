import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._years = DAO.getAllYears()
        self._countries = DAO.getAllCountries()
        self._grafo = nx.Graph()
        self._idMap = {}
        self._bestPath = []
        self._bestObjFun = 0

    def getBestPath(self, t):

        self._bestPath = []
        self._bestObjFun = 0

        for r in self._ret_connected:
            parziale = [r]
            self._ricorsione(parziale, t)

        return self._bestPath, self._bestObjFun, self.getWeightsOfPath(self._bestPath)

    def _ricorsione(self, parziale, t):

        if len(parziale) == t+1:
            if self.getObjFun(parziale) > self._bestObjFun and parziale[-1] == parziale[0]:
                self._bestObjFun = self.getObjFun(parziale)
                self._bestPath = copy.deepcopy(parziale)
            return

        for n in self._grafo.neighbors(parziale[-1]):
            if len(parziale) <= t and n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale, t)
                parziale.pop()
            elif len(parziale) == t and parziale[0] == n:
                parziale.append(n)
                self._ricorsione(parziale, t)
                parziale.pop()

    def getObjFun(self, listOfNodes):
        objVal = 0

        for i in range(0, len(listOfNodes) - 1):
            objVal += self._grafo[listOfNodes[i]][listOfNodes[i + 1]]["weight"]

        return objVal

    def getWeightsOfPath(self, path):
        listTuples = [(path[0], 0)]
        for i in range(0, len(path)-1):
            listTuples.append((path[i+1], self._grafo[path[i]][path[i+1]]["weight"]))

        return listTuples

    def buildGraph(self, year, country):

        nodes = DAO.getAllRetailers(country)
        self._grafo.add_nodes_from(nodes)
        for n in nodes:
            self._idMap[n.Retailer_code] = n

        self._addEdges(year, country)

    def _addEdges(self, year, country):
        edges = DAO.getAllEdges(year, country, self._idMap)
        for e in edges:
            self._grafo.add_edge(e.v0, e.v1, weight=e.peso)

    def getViciniPesati(self):

        self._volume_ret = []
        self._ret_connected = []
        for n in self._grafo.nodes():
            volume = 0
            for edge in self._grafo.edges(n, data=True):
                volume += edge[2]["weight"]
            if volume > 0:
                self._ret_connected.append((n))
                self._volume_ret.append((n.Retailer_name, volume))

        self._volume_ret_sort = sorted(self._volume_ret, key=lambda x: x[1], reverse=True)

    def getYears(self):
        return self._years

    def getCountries(self):
        return self._countries

    def graphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)
