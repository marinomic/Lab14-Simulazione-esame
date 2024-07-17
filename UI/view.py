import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Template application using MVC and DAO"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None

        # graphical elements
        self._title = None

        self.btn_graph = None
        self.txtSoglia = None
        self.btn_countedges = None
        self.btn_search = None

        self.txt_result = None
        self.txt_result2 = None
        self.txt_result3 = None

        self.txt_container = None

    def load_interface(self):
        # title
        self._title = ft.Text("Lab14-Simulazione esame gene_small",
                              color="blue",
                              size=24)
        self._page.controls.append(self._title)

        # ROW 1 with some controls
        self.btn_graph = ft.ElevatedButton(text="Crea Grafo",
                                           on_click=self._controller.handle_graph)
        row1 = ft.Row([self.btn_graph],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1,
                                      spacing=10,
                                      padding=20,
                                      auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

        # ROW 2
        # text field for the name
        self.txtSoglia = ft.TextField(
                label="soglia",
                width=200,
                hint_text="Soglia (s)",
                disabled=True
        )
        self.btn_countedges = ft.ElevatedButton(text="Conta Archi",
                                                on_click=self._controller.handle_countedges,
                                                disabled=True)

        row2 = ft.Row([self.txtSoglia, self.btn_countedges],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        # List View where the reply is printed
        self.txt_result2 = ft.ListView(expand=1,
                                       spacing=10,
                                       padding=20,
                                       auto_scroll=True)
        self._page.controls.append(self.txt_result2)
        self._page.update()

        self.btn_search = ft.ElevatedButton(text="Cerca cammino",
                                            on_click=self._controller.handle_search,
                                            disabled=True)
        row3 = ft.Row([self.btn_search],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row3)

        # List View where the reply is printed
        self.txt_result3 = ft.ListView(expand=1,
                                       spacing=10,
                                       padding=20,
                                       auto_scroll=True)
        self._page.controls.append(self.txt_result3)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
