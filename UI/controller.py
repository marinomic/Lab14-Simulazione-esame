import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_graph(self, e):
        self._model.creaGrafo()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttaente creato"))
        # Si visualizzi il numero di vertici e archi del grafo, e i valori minimo e massimo dei pesi degli archi.
        self._minPeso, self._maxPeso = self._model.getMinAndMaxWeight()
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {len(self._model._grafo.nodes)}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {len(self._model._grafo.edges)}"))
        self._view.txt_result.controls.append(ft.Text(f"Peso minimo: {self._minPeso}"))
        self._view.txt_result.controls.append(ft.Text(f"Peso massimo: {self._maxPeso}"))
        self._view.update_page()

    def handle_countedges(self, e):
        strSoglia = self._view.txtSoglia.value
        try:
            flSoglia = float(strSoglia)
        except ValueError:
            self._view.txt_result2.controls.clear()
            self._view.txt_result2.controls.append(
                ft.Text("Inserire un valore numerico usando il punto come separatore decimale"))
            self._view.update_page()
            return
        self._view.txt_result2.controls.clear()
        if flSoglia < self._minPeso or flSoglia > self._maxPeso:
            self._view.txt_result2.controls.append(ft.Text("Soglia non valida"))
            self._view.update_page()
            return
        self._soglia = flSoglia
        numSmaller, numBigger = self._model.countEdges(flSoglia)
        self._view.txt_result2.controls.append(ft.Text(f"Numero di archi con peso minore di {flSoglia}: {numSmaller}"))
        self._view.txt_result2.controls.append(
            ft.Text(f"Numero di archi con peso maggiore o uguale a {flSoglia}: {numBigger}"))
        self._view.update_page()

    def handle_search(self, e):
        if self._soglia is None:
            self._view.txt_result3.controls.clear()
            self._view.txt_result3.controls.append(ft.Text("Inserire prima la soglia"))
            self._view.update_page()
            return
        path, peso = self._model.searchPath(self._soglia)
        self._view.txt_result3.controls.clear()
        self._view.txt_result3.controls.append(ft.Text(f"Peso massimo trovato: {peso}"))
        self._view.txt_result3.controls.append(ft.Text("Percorso:"))
        for u, v, w in path:
            self._view.txt_result3.controls.append(ft.Text(f"{u} --> {v} (peso: {w['weight']})"))
        self._view.update_page()
