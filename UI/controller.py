import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        dailySalesList = self._model.getYears()

        for n in dailySalesList:
            if n._Date.year not in self._listYear:
                self._listYear.append(n._Date.year)

        self._listYear.sort()

        for a in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(a))

        self._listYear = self._model.getCountries()
        for a in self._listYear:
            self._view.ddcountry.options.append(ft.dropdown.Option(a))

        self._view.update_page()

    def handle_graph(self, e):

        country = self._view.ddcountry.value
        year = self._view.ddyear.value

        if country is None:
            self._view.create_alert("Inserire l'anno")
            return
        if year is None:
            self._view.create_alert("Inserire la nazione")
            return

        self._model.buildGraph(year, country)
        n, a = self._model.graphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato con {n} nodi e {a} archi"))

        self._view.update_page()

    def handle_volume(self, e):

        self._model.getViciniPesati()

        for elem in self._model._volume_ret_sort:
            self._view.txtOut2.controls.append(ft.Text(f"{elem[0]} --> {elem[1]}"))

        self._view.update_page()

    def handle_path(self, e):
        lun = self._view.txtN.value
        try:
            intLun = int(lun)
        except ValueError:
            self._view.txtOut3.controls.append("Il valore inserito non è un numero")
            self._view.update_page()
            return

        if intLun < 2:
            self._view.create_alert("lunghezza percorso non valida (minore di 2)!")
            return

        path, costo, pesoArchi = self._model.getBestPath(intLun)
        self._view.txtOut3.controls.clear()
        self._view.txtOut3.controls.append(ft.Text(f"Peso cammino massimo: {costo}"))
        for p in range(0, len(path)-1):
            self._view.txtOut3.controls.append(ft.Text(f"{path[p]} --> {path[p+1]}: {pesoArchi[p+1][1]}"))
        self._view.update_page()



