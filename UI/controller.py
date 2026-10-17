import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def _errore(self, msg):
        self._view._txt_result.controls.append(ft.Text(msg, color="red"))
        self._view.update_page()

    def fillDDAnni(self):          # punto 1a: riempie "Anno da" e "Anno a"
        for a in self._model.getAnni():
            self._view._ddAnno1.options.append(ft.dropdown.Option(str(a)))
            self._view._ddAnno2.options.append(ft.dropdown.Option(str(a)))
        self._view.update_page()

    # -------------------- PUNTO 1 --------------------

    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()

        try:
            rMin = int(self._view._ddAnno1.value)
            rMax = int(self._view._ddAnno2.value)
        except (ValueError, TypeError):
            self._errore("Selezionare entrambi gli anni!")
            return
        if rMin > rMax:
            self._errore("L'anno di inizio non può essere successivo all'anno di fine!")
            return

        self._model.buildGraph(rMin, rMax)
        self._view._txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view._txt_result.controls.append(
            ft.Text(f"Numero di vertici: {self._model.getNumNodi()}"))
        self._view._txt_result.controls.append(
            ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))

        # riempio il dropdown degli attori (punto 2)
        self._view._ddPartenza.options.clear()
        self._view._ddArrivo.options.clear()
        self._view._ddPartenza.value = None
        self._view._ddArrivo.value = None

        for a in self._model.getNodiOrdinati():
            self._view._ddArrivo.options.append(ft.dropdown.Option(key=str(a.circuitId), text=a.name))
            self._view._ddPartenza.options.append(ft.dropdown.Option(key=str(a.circuitId), text=a.name))
        self._view.update_page()

    def handleDettagli(self, e):
        self._view._txt_result.controls.clear()

        # il grafo deve esistere (max su grafo vuoto darebbe errore)
        if self._model.getNumNodi() == 0:
            self._errore("Creare prima il grafo!")
            return

        # a. i 3 archi di peso maggiore (partenza -> arrivo)
        self._view._txt_result.controls.append(ft.Text("Top 3 archi di peso maggiore:"))
        for i, (u, v, peso) in enumerate(self._model.getTop3(), start=1):
            self._view._txt_result.controls.append(ft.Text(f"{i}. {u} -> {v} (peso: {peso})"))

        # b. componenti fortemente connesse
        numComp, dimMax = self._model.getComponentiForti()
        self._view._txt_result.controls.append(ft.Text(""))
        self._view._txt_result.controls.append(
            ft.Text(f"Numero di componenti fortemente connesse: {numComp}"))
        self._view._txt_result.controls.append(
            ft.Text(f"Dimensione della componente più grande: {dimMax}"))

        # c. circuito con grado uscente maggiore
        circuito, grado = self._model.getOutMax()
        self._view._txt_result.controls.append(ft.Text(""))
        self._view._txt_result.controls.append(
            ft.Text(f"Circuito con grado uscente maggiore: {circuito} (grado uscente: {grado})"))

        self._view.update_page()

    # -------------------- PUNTO 2 --------------------
    def handleCammino(self, e):
        self._view._txt_result.controls.clear()

        # 1. il grafo deve esistere
        if self._model.getNumNodi() == 0:
            self._errore("Creare prima il grafo!")
            return

        # 2. circuiti di partenza e arrivo
        if self._view._ddPartenza.value is None or self._view._ddArrivo.value is None:
            self._errore("Selezionare circuito di partenza e di arrivo!")
            return
        partenza = self._model._idMap[int(self._view._ddPartenza.value)]
        arrivo = self._model._idMap[int(self._view._ddArrivo.value)]

        # 3. devono essere diversi
        if partenza == arrivo:
            self._errore("Partenza e arrivo devono essere diversi!")
            return

        # 4. K
        try:
            k = int(self._view._txtInK.value)
        except (ValueError, TypeError):
            self._errore("K deve essere un numero intero!")
            return
        if k < 1:
            self._errore("K deve essere almeno 1!")
            return

        # 5. ricorsione
        percorso, peso = self._model.getPercorso(partenza, arrivo, k)

        # 6. stampa
        if len(percorso) == 0:
            self._errore(f"Nessun cammino da {partenza} a {arrivo} con al massimo {k} archi "
                         f"senza ripetere paesi")
            return

        self._view._txt_result.controls.append(
            ft.Text(f"Calendario migliore da {partenza} a {arrivo} ({len(percorso) - 1} archi):"))
        self._view._txt_result.controls.append(
            ft.Text(f"1. {percorso[0]} ({percorso[0].country})"))
        for i in range(1, len(percorso)):
            p = self._model.getPesoArco(percorso[i - 1], percorso[i])
            self._view._txt_result.controls.append(
                ft.Text(f"{i + 1}. {percorso[i]} ({percorso[i].country}) - peso arco: {p}"))
        self._view._txt_result.controls.append(ft.Text(f"Peso totale: {peso}"))

        self._view.update_page()

