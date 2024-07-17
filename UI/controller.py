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
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {self._model.get_num_of_nodes()} -- Numero di archi: {self._model.get_num_of_edges()}"))
        self._view.txt_result.controls.append(ft.Text(f"Peso minimo: {self._minPeso}"))
        self._view.txt_result.controls.append(ft.Text(f"Peso massimo: {self._maxPeso}"))
        self._view.txtSoglia.disabled = False
        self._view.btn_countedges.disabled = False
        self._view.btn_search.disabled = False
        self._view.update_page()

    def handle_countedges(self, e):
        strSoglia = self._view.txtSoglia.value
        try:
            flSoglia = float(strSoglia)
        except ValueError:
            self._view.create_alert("Inserire un valore numerico usando il punto come separatore decimale")
            return

        self._view.txt_result2.controls.clear()
        if flSoglia < self._minPeso or flSoglia > self._maxPeso:
            self._view.create_alert("Soglia non valida. Inserire un valore compreso tra il peso minimo e massimo degli archi")
            return
        numSmaller, numBigger = self._model.countEdges(flSoglia)
        self._view.txt_result2.controls.append(ft.Text(f"Numero di archi con peso minore di {flSoglia}: {numSmaller}"))
        self._view.txt_result2.controls.append(
            ft.Text(f"Numero di archi con peso maggiore o uguale a {flSoglia}: {numBigger}"))
        self._view.update_page()

    def handle_search(self, e):
        strSoglia = self._view.txtSoglia.value
        try:
            flSoglia = float(strSoglia)
        except ValueError:
            self._view.create_alert("Inserire un valore numerico usando il punto come separatore decimale")
            return
        if flSoglia < self._minPeso or flSoglia > self._maxPeso:
            self._view.create_alert(
                "Soglia non valida. Inserire un valore compreso tra il peso minimo e massimo degli archi")
            return
        path, peso = self._model.searchPath(flSoglia)
        self._view.txt_result3.controls.clear()
        self._view.txt_result3.controls.append(ft.Text(f"Peso massimo trovato: {peso}"))
        self._view.txt_result3.controls.append(ft.Text("Percorso:"))
        for u, v, w in path:
            self._view.txt_result3.controls.append(ft.Text(f"{u} --> {v} (peso: {w['weight']})"))
        self._view.update_page()
