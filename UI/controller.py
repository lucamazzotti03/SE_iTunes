import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        # TODO
        nodi, archi = self._model.crea_grafo(float(self._view.txt_durata.value))
        self.get_selected_album(e)
        self._view.lista_visualizzazione_1.controls.clear()
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Grafo creato: {nodi} album, {archi} archi"))
        self._view.update()

    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        # TODO
        self._view.dd_album.options = []

        for album in self._model.G.nodes():
            self._view.dd_album.options.append(
                ft.dropdown.Option(self._model.album_dict[album].title)
            )

        self._view.dd_album.update()


    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        # TODO
        lunghezza, durata = self._model.read_componente_connessa(self._view.dd_album.value)
        self._view.lista_visualizzazione_2.controls.clear()
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Dimensione componente connessa: {lunghezza}"))
        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Durata totale: {durata}minuti"))
        self._view.update()
    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        # TODO
        combinazione, durata = self._model.trova_set(int(self._view.txt_durata_totale.value), self._view.dd_album.value)
        self._view.lista_visualizzazione_3.controls.clear()
        self._view.lista_visualizzazione_3.controls.append(ft.Text(f"Set trovato({len(combinazione)} album, durata: {durata}minuti"))
        for nodo in combinazione:
            self._view.lista_visualizzazione_3.controls.append(ft.Text(f"-{self._model.album_dict[nodo].title}({round(self._model.album_dict[nodo].durata/60000, 2)} min)"))
        self._view.update()