import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "F1 - Calendario dei circuiti"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._page.bgcolor = "#ebf4f4"
        self._page.window_height = 800
        page.window_center()
        self._controller = None
        # graphical elements
        self._title = None
        self._ddAnno1 = None
        self._ddAnno2 = None
        self._btnCreaGrafo = None
        self._btnDettagli = None
        self._ddPartenza = None
        self._ddArrivo = None
        self._txtInK = None
        self._btnCammino = None
        self._txt_result = None

    def load_interface(self):
        # title
        self._title = ft.Text("F1 - Calendario dei circuiti", color="blue", size=24)
        self._page.controls.append(self._title)

        # ROW 1: anni + crea grafo
        self._ddAnno1 = ft.Dropdown(label="Da", hint_text="Anno di inizio")
        self._ddAnno2 = ft.Dropdown(label="A", hint_text="Anno di fine")
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea Grafo",
                                               on_click=self._controller.handleCreaGrafo)
        row1 = ft.Row([ft.Container(self._ddAnno1, width=250),
                       ft.Container(self._ddAnno2, width=250),
                       self._btnCreaGrafo],
                      alignment=ft.MainAxisAlignment.CENTER,
                      vertical_alignment=ft.CrossAxisAlignment.END)

        # ROW 2: stampa dettagli
        self._btnDettagli = ft.ElevatedButton(text="Stampa Dettagli",
                                              on_click=self._controller.handleDettagli)
        row2 = ft.Row([ft.Container(self._btnDettagli, width=250)],
                      alignment=ft.MainAxisAlignment.CENTER)

        # ROW 3: punto 2
        self._ddPartenza = ft.Dropdown(label="Circuito di partenza")
        self._ddArrivo = ft.Dropdown(label="Circuito di arrivo")
        self._txtInK = ft.TextField(label="Max archi K")
        self._btnCammino = ft.ElevatedButton(text="Cerca Calendario",
                                             on_click=self._controller.handleCammino)
        row3 = ft.Row([ft.Container(self._ddPartenza, width=280),
                       ft.Container(self._ddArrivo, width=280),
                       ft.Container(self._txtInK, width=130),
                       self._btnCammino],
                      alignment=ft.MainAxisAlignment.CENTER,
                      vertical_alignment=ft.CrossAxisAlignment.END)

        self._page.controls.append(row1)
        self._page.controls.append(row2)
        self._page.controls.append(row3)

        # risultati
        self._txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self._txt_result)

        # riempio i menu degli anni all'avvio
        self._controller.fillDDAnni()

        self._page.update()

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()