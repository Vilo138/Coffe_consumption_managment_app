from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.users
from datetime import datetime
from anvil.tables import app_tables

class Form1(Form1Template):
    def __init__(self, **properties):
        # Toto nastaví komponenty na formulári
        self.init_components(**properties)



       # Načítanie emailov zo servera a ich vypísanie
        self.get_users()

    def get_users(self):
        """Načíta používateľov z tabuľky Users a vytvorí tlačidlá"""
        users = anvil.server.call('get_users')
        
        for user in users:
            # Dynamicky pridávame tlačidlo pre každého používateľa
            button = Button(text=user['email'])
            button.tag.user_row = user  # Uložíme user_id do tagu tlačidla
            button.set_event_handler('click', self.zaznam_kavy)
            self.flow_panel_1.add_component(button)

            
            

    def zaznam_kavy(self, **event_args):
        """Pri kliknutí na tlačidlo zaznamená výber kávy do tabuľky"""
        user_row = event_args['sender'].tag.user_row  # Získame user_id z tagu tlačidla
        print(f"User ID: {user_row}")
        
        # Zobrazenie dialógového okna s otázkou
        response = alert("Si si istý, že si si dal kávu?", buttons=[("Áno", True), ("Nie", False)])
        if response:
            # Uloženie záznamu do tabuľky pomocou serverovej funkcie
            anvil.server.call('add_coffee_record', user_row)
            alert(f"Zaznamenaná káva pre používateľa s ID: {user_row}")

    def link_2_click(self, **event_args):
        """Pri kliknutí na link sa používateľ prihlási"""
        anvil.users.login_with_form()

#print(users)