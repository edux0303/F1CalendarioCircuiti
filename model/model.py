from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._idMap = {}
        self._arrivo = None
        self._maxPassi = None
        self._pesoBest = None
    def buildGraph(self,minimo,massimo):
        self._grafo.clear()
        self._idMap = {}
        nodi = DAO.getNodi(minimo, massimo)
        archi = DAO.getEdges(minimo, massimo)
        self._idMap = {at.circuitId: at for at in nodi}
        self._grafo.add_nodes_from(nodi)
        for s1,s2,peso in archi:
            if s1 in self._idMap and s2 in self._idMap:
                self._grafo.add_edge(self._idMap[s1],self._idMap[s2],weight=peso)

    def getAnni(self):
        return DAO.getAllYears()

    def getNumNodi(self):
        return self._grafo.number_of_nodes()

    def getNumArchi(self):
        return self._grafo.number_of_edges()

    def getNodiOrdinati(self):
        return sorted(self._grafo.nodes, key=lambda c: c.name)

    def getTop3(self):
        archi = []
        for u,v,dati in self._grafo.edges(data=True):
            archi.append((u,v,dati['weight']))
        archi.sort(key=lambda c: (-c[2],c[0].name,c[1].name))
        return archi[:3]

    def getComponentiForti(self):
        componenti = list(nx.strongly_connected_components(self._grafo))
        piuGrande = max(componenti, key=len)
        return len(componenti), len(piuGrande)

    def getOutMax(self):
        best = max(self._grafo.nodes, key=lambda c: self._grafo.out_degree(c))
        return best, self._grafo.out_degree(best)


    def getPercorso(self,a1,a2,t):
        self._percorsoBest = []
        self._arrivo = a2
        self._maxPassi = t
        self._pesoBest = -1
        self._ricorsione([a1],0)
        return self._percorsoBest, self._pesoBest


    def _ricorsione(self,parziale,peso):
        if parziale[-1] == self._arrivo:
            if peso > self._pesoBest:
                self._percorsoBest = list(parziale)
                self._pesoBest = peso
            return

        if len(parziale) -1== self._maxPassi:
            return

        for v in self._grafo.successors(parziale[-1]):
            paesiUsati = [c.country for c in parziale]
            if v in parziale or v.country  in paesiUsati :
                continue
            pesoA = self._grafo[parziale[-1]][v]["weight"]

            parziale.append(v)
            self._ricorsione(parziale,peso+pesoA)
            parziale.pop()

    def getPesoArco(self, u, v):
        return self._grafo[u][v]["weight"]

