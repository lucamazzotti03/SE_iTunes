import networkx as nx

from database.dao import DAO


class Model:
    def __init__(self):
        self.G = nx.Graph()
        self.dao = DAO()
        self.album_dict = {}

    def crea_grafo(self, durata):
        self.album = self.dao.get_album(durata)
        self.G.clear()
        self.album_dict.clear()

        for a in self.album:
            self.album_dict[a.id] = a
            self.G.add_node(a.id)

        playlists = self.dao.get_playlist()

        for playlist, tracks in playlists.items():
            if len(tracks) < 2:
                continue

            for i in range(len(tracks)):
                for j in range(i + 1, len(tracks)):
                    if tracks[i] in self.G and tracks[j] in self.G:
                        self.G.add_edge(tracks[i], tracks[j])
        print(self.G)
        return self.G.number_of_nodes(), self.G.number_of_edges()

    def read_componente_connessa(self, nome):
        comp_connessa = nx.connected_components(self.G)
        self.id_album = 0
        for id in self.album_dict:

            if self.album_dict[id].title == nome:
                self.id_album = id
        self.connessa = []
        for comp in comp_connessa:
            if self.id_album in comp:
                self.connessa = comp

        durata = 0
        for album in self.album:
            if album.id in self.connessa:
                durata += album.durata
        durata = round(durata/1000/60, 2)
        return len(self.connessa), durata

    def trova_set(self, soglia, nome):
        self.combinazione_migliore = []
        self.durata_migliore = 0
        id_album = None
        for a in self.album_dict:
            if self.album_dict[a].title == nome:
                id_album = self.album_dict[a].id
        for nodo in self.connessa:
            durata = round(self.album_dict[nodo].durata/60000,2) #convertire in minuti
            if durata < soglia:
                self.ricorsione(parziale = [nodo], durata_corrente = durata, soglia = soglia, id = id_album)
        return self.combinazione_migliore, self.durata_migliore

    def ricorsione(self , parziale, durata_corrente, soglia, id):
        if  id in parziale and ((len(parziale) > len(self.combinazione_migliore)) or (len(parziale) == len(self.combinazione_migliore) and durata_corrente > self.durata_migliore)):
            self.combinazione_migliore = parziale.copy()
            self.durata_migliore = durata_corrente
            print(self.combinazione_migliore, self.durata_migliore)

        for nodo in self.connessa:
            if nodo not in parziale:
                nuova_durata = round(durata_corrente + self.album_dict[nodo].durata / 60000, 2)
                if nuova_durata < soglia:
                    parziale.append(nodo)

                    self.ricorsione(parziale, nuova_durata, soglia, id)

                    parziale.pop()












