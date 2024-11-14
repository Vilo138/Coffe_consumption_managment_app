from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.users
from datetime import datetime

class Form1(Form1Template):
    def __init__(self, **properties):
        # Toto nastaví komponenty na formulári
        self.init_components(**properties)
        
        # Načítanie používateľov zo servera a dynamické pridanie tlačidiel
        self.nacitaj_pouzivatelov()

    def nacitaj_pouzivatelov(self):
        """Načíta používateľov z tabuľky Users a vytvorí tlačidlá"""
        users = anvil.server.call('get_users')
        #print(users)
        for user in users:

          
            print(user['email'])
            #print(email[0])
            # Priamy prístup k atribútom user objektu
            email = user['email']
            user_id = user['id']
            
            if email:
                # Dynamicky pridávame tlačidlo pre každého používateľa
                button = Button(text=email)
                button.tag.user_id = user_id  # Uložíme user_id do tagu tlačidla
                button.set_event_handler('click', self.zaznam_kavy)
                
                # Pridanie tlačidla do flow_panelu (uisti sa, že flow_panel_1 existuje)
                if hasattr(self, 'flow_panel_1'):
                    self.flow_panel_1.add_component(button)
                else:
                    alert("Flow panel 'flow_panel_1' neexistuje!")

    def zaznam_kavy(self, **event_args):
        """Pri kliknutí na tlačidlo zaznamená výber kávy do tabuľky"""
        user_id = event_args['sender'].tag.user_id  # Získame user_id z tagu tlačidla
        
        # Zobrazenie dialógového okna s otázkou
        response = alert("Si si istý, že si si dal kávu?", buttons=[("Áno", True), ("Nie", False)])
        if response:
            # Uloženie záznamu do tabuľky pomocou serverovej funkcie
            anvil.server.call('add_coffee_record', user_id)
            alert(f"Zaznamenaná káva pre používateľa s ID: {user_id}")

    def link_2_click(self, **event_args):
        """Pri kliknutí na link sa používateľ prihlási"""
        anvil.users.login_with_form()

#print(users)