from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.list import ThreeLineIconListItem, IconLeftWidget
from kivymd.uix.screen import MDScreen
from utils import load_kv  # cargar ruta del script
import sqlite3

load_kv(__name__)

# Esta clase es la clase que se encarga de las acciones que va a realizar el buscador.

data = []


def get_data_sqlite():
    conn = sqlite3.connect("pymeshield.db")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM budgets")

    rows = cursor.fetchall()

    data = []

    for row in rows:
        data.append(
            {
                "id": row[0],
                "price": row[1],
                "accepted": row[2],
            }
        )

    data = data

    return data


class BudgetScreen(MDScreen):
    def calc(self, item):
        # Cancelar búsquedas previas
        if hasattr(self, "search_event"):
            self.search_event.cancel()

        # Añadir delay
        self.search_event = Clock.schedule_once(
            lambda dt: self.hacer_busqueda(item), 0.5
        )

    def hacer_busqueda(self, item):
        # variable que guarda el resultado el método getTareasData()
        data = get_data_sqlite()

        # Filtramos los datos según el precio de búsqueda
        search_results = [
            search_text
            for search_text in data
            if (str(item) in str(search_text["price"]))
            or (item.lower() in search_text["accepted"].lower())
            or (str(item) in str(search_text["id"]))
        ]

        # Actualizamos la lista de resultados de búsqueda en la interfaz de usuario
        search_results_list = self.ids.presupuesto
        # Borramos todos los elementos de la lista
        search_results_list.clear_widgets()

        for result in search_results:
            search_results_list.add_widget(
                ThreeLineIconListItem(  # método que nos deja trabajar con 1 linea que previamente lo hemos importado en la parte superior
                    IconLeftWidget(  # método que nos permite agregar un icono
                        icon="account-cash"
                    ),
                    id=f"Presupuesto {result['id']}",
                    text=f"Presupuesto número {result['id']}",  # línea 1
                    secondary_text=f"Total presupuesto: {result['price']} €",  # línea 2
                    tertiary_text=f"Aceptado: {result['accepted']}",  # línea 3
                    on_press=self.detalles,
                )
            )

    def open(self):
        self.manager.current = "budgets"

    def on_leave(self, *args):
        self.ids.presupuesto.clear_widgets()

    def on_enter(self):
        data = get_data_sqlite()

        for i in data:  # bucle que recorre el rango que le pasemos como parametro
            self.ids.presupuesto.add_widget(  # añade widgets, despues de ids. va el id con el que podremos trabajar en el documento .kv
                ThreeLineIconListItem(  # método que nos deja trabajar con 3 lineas que previamente lo hemos importado en la parte superior
                    IconLeftWidget(  # método que nos permite agregar un icono
                        icon="account-cash"
                    ),
                    id=f"Presupuesto {i['id']}",
                    text=f"Presupuesto número {i['id']}",  # línea 1
                    secondary_text=f"Total presupuesto: {i['price']} €",  # línea 2
                    tertiary_text=f"Aceptado: {i['accepted']}",  # línea 3
                    on_press=self.detalles,
                )
            )  # Lista que muestra las tareas

    def detalles(self, row):  # inicializamos una función con el parametro row
        # Variable que utilizaremos para acceder a la applicacion que esta ejecutada.
        app = MDApp.get_running_app()
        app.setRowDetails(row.id)
        self.manager.current = "details_budgets"
