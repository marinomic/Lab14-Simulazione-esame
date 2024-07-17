import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._listConnectedGenes = None
        self._grafo = nx.DiGraph()
        self._nodes = DAO.getAllChromosomes()
        self._edges = []
        self._genes = DAO.getAllGenes()

        self.idMap = {}
        for gene in self._genes:
            self.idMap[gene.GeneID] = gene.Chromosome  # devo mappare l'id del gene con il cromosoma, CIOè CON IL NODO

        self.solBest = []

    def creaGrafo(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._nodes)
        # Il peso di ciascun arco dovrà essere calcolato come la somma algebrica della correlazione (tabella
        # interactions, campo Expression_Corr), facendo attenzione a contare ogni coppia di geni una sola volta.
        self._listConnectedGenes = DAO.getAllConnectedGenes()

        edges = {}
        # Io devo aggiungere i due cromosomi e il peso al grafo come archi, non i due geni perchè i cromosomi sono i nodi
        # per questo devo mappare l'id del gene con il cromosoma, CIOè CON IL NODO
        for g1, g2, corr in self._listConnectedGenes:
            if (self.idMap[g1], self.idMap[g2]) not in edges:
                edges[(self.idMap[g1], self.idMap[g2])] = float(corr)
            else:
                edges[(self.idMap[g1], self.idMap[g2])] += float(corr)
        # Per ogni chiave (tupla con i due cromosomi) e per ogni valore (il peso) aggiungo l'arco al a una lista di tuple
        # (cromosoma1, cromosoma2, peso) e poi aggiungo gli archi al grafo perchè la funzione add_weighted_edges_from
        # accetta una lista di tuple (cromosoma1, cromosoma2, peso)
        for k, v in edges.items():
            self._edges.append((k[0], k[1], v))
        self._grafo.add_weighted_edges_from(self._edges)

    def getMinAndMaxWeight(self):
        # Si restituiscano i valori minimo e massimo dei pesi degli archi del grafo.
        archiPesoMax = []
        for u, v, w in self._grafo.edges.data('weight'):
            archiPesoMax.append((u, v, w))
        return min(archiPesoMax, key=lambda x: x[2])[2], max(archiPesoMax, key=lambda x: x[2])[2]

    def countEdges(self, flSoglia):
        # Si restituiscano il numero di archi con peso minore di S e il numero di archi con peso maggiore o uguale a S.
        numSmaller = 0
        numBigger = 0
        for u, v, w in self._edges:
            if w < flSoglia:
                numSmaller += 1
            else:
                numBigger += 1
        return numSmaller, numBigger

    def searchPath(self, t):

        for n in self.get_nodes():
            partial = []
            # Scelta di partial_edges: La lista partial_edges è essenziale per tenere traccia degli archi specifici
            # che compongono il percorso corrente. Questo è importante perché, in un grafo diretto,
            # la direzione degli archi influisce sulla validità del percorso. Inoltre, il peso totale
            # del percorso, che è un criterio chiave per trovare il percorso più lungo, dipende dagli archi specifici inclusi nel percorso
            partial_edges = []

            partial.append(n)
            self.ricorsione(partial, partial_edges, t)

        return self.solBest, self.computeWeightPath(self.solBest)

    def ricorsione(self, partial, partial_edges, t):
        """
        L'algoritmo di ricorsione in questione è progettato per esplorare un grafo diretto, cercando di trovare il percorso più lungo
         (in termini di peso totale degli archi) che soddisfa un certo criterio, definito da una soglia t.
        """
        n_last = partial[-1]
# 1) Ricerca dei Vicini Ammissibili:
# Viene chiamata la funzione getAdmissibleNeighbs per trovare tutti i vicini di n_last che non sono già presenti
# nel percorso parziale e che hanno un arco con un peso maggiore della soglia t. Questo passaggio assicura che il
# percorso esplorato sia sempre diretto in avanti e che il peso degli archi soddisfi il criterio specificato.
        neigh = self.getAdmissibleNeighbs(n_last, partial_edges, t)

# 2) Caso Base (Terminale) della Ricorsione:
# Se non ci sono vicini ammissibili, significa che il percorso non può essere ulteriormente esteso. A questo punto,
# il peso totale del percorso corrente viene calcolato e confrontato con il peso del miglior percorso trovato fino a quel momento (solBest).
# Se il percorso corrente è migliore, diventa il nuovo miglior percorso.
        if len(neigh) == 0:
            weight_path = self.computeWeightPath(partial_edges)
            weight_path_best = self.computeWeightPath(self.solBest)
            if weight_path > weight_path_best:
                self.solBest = partial_edges[:]
            return

# Espansione del Percorso:
# Se ci sono vicini ammissibili, l'algoritmo itera su ciascuno di essi. Per ogni vicino:
        for n in neigh:
            partial.append(n)  # Viene aggiunto al percorso parziale.
            partial_edges.append((n_last, n, self._grafo.get_edge_data(n_last, n)))  # Viene aggiunto l'arco corrispondente (da n_last al vicino) a partial_edges.
            self.ricorsione(partial, partial_edges, t)  # Viene effettuata una chiamata ricorsiva per continuare l'esplorazione a partire dal nuovo nodo aggiunto.
            partial.pop()          # Dopo la chiamata ricorsiva, il nodo e l'arco appena aggiunti vengono rimossi per permettere l'esplorazione di altri percorsi potenziali.
            partial_edges.pop()
# Terminazione: La ricorsione termina quando tutti i percorsi possibili sono stati esplorati. Il miglior percorso trovato (solBest) e il suo peso sono il risultato dell'algoritmo.

# La funzione get_edge_data(n_last, n) restituisce un dizionario contenente i dati associati all'arco che collega
# il nodo n_last al nodo n nel grafo diretto self._grafo. Questi dati includono tipicamente il peso dell'arco,
# rappresentato dalla chiave 'weight' nel dizionario, oltre ad altre possibili informazioni specifiche dell'arco.
    def getAdmissibleNeighbs(self, n_last, partial_edges, t):
        all_neigh = self._grafo.edges(n_last, data=True)
        result = []
        for e in all_neigh:
            if e[2]["weight"] > t:
                # Per ogni arco e che parte da n_last, viene creato un arco inverso e_inv. Questo passaggio è necessario
                # per verificare che l'arco non sia già stato percorso in direzione inversa, mantenendo la coerenza del percorso in un grafo diretto.
                e_inv = (e[1], e[0], e[2])
                if (e_inv not in partial_edges) and (e not in partial_edges):
                    # Questo controllo previene l'inclusione di cicli nel percorso, garantendo che ogni arco sia considerato
                    # una sola volta e solo in una direzione, in linea con la definizione di un percorso semplice in un grafo diretto
                    result.append(e[1])
                    # il nodo destinazione dell'arco, indicato con e[1], viene aggiunto all'elenco result
        return result

    def computeWeightPath(self, mylist):
        if not isinstance(mylist, list):
            return 0  # Return 0 or some other default value indicating no weight
        weight = 0
        for e in mylist:
            weight += e[2]['weight']
        return weight

    def get_nodes(self):
        return self._grafo.nodes()

    def get_edges(self):
        return list(self._grafo.edges(data=True))

    def get_num_of_nodes(self):
        return self._grafo.number_of_nodes()

    def get_num_of_edges(self):
        return self._grafo.number_of_edges()
