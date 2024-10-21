from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables



from anvil.google.drive import app_files

import anvil.tables.query as q

import anvil.users




class Form1(Form1Template):  # Trieda Form1 dedí z triedy Form1Template
    def __init__(self, **properties):
        # Toto nastaví komponenty na formulári
        self.init_components(**properties)

    def button_1_click(self, **event_args):
        """Túto metódu zavolá systém pri kliknutí na tlačidlo 1"""
        response = alert("Si si istý, že si si dal kávu?", buttons=[("Áno", True), ("Nie", False)])
        if response:
            print("Áno")
        else:
            open_form('Form1')  # Otvorí domovskú obrazovku (Form1)

    def button_2_click(self, **event_args):
        """Túto metódu zavolá systém pri kliknutí na tlačidlo 2"""
        response = alert("Si si istý, že si si dal kávu?", buttons=[("Áno", True), ("Nie", False)])
        if response:
            print("Áno")
        else:
            open_form('Form1')  # Otvorí domovskú obrazovku (Form1)

    def button_3_click(self, **event_args):
        """Túto metódu zavolá systém pri kliknutí na tlačidlo 3"""
        response = alert("Si si istý, že si si dal kávu?", buttons=[("Áno", True), ("Nie", False)])
        if response:
            print("Áno")
        else:
            open_form('Form1')  # Otvorí domovskú obrazovku (Form1)

    def link_2_click(self, **event_args):
      """This method is called when the link is clicked"""
      anvil.users.login_with_form()

