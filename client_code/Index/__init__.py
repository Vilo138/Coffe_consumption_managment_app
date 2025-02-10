from ._anvil_designer import IndexTemplate
from anvil import *
import anvil.server
import anvil.users
from datetime import datetime
from anvil.tables import app_tables
import sys
from ..DatePickerDialog import DatePickerDialog
from anvil import alert



import anvil.tables as tables
import anvil.tables.query as q
#from anvil.tables import app_tables
from anvil import open_form
import custom_signup.login_flow

class Index(IndexTemplate):
    def __init__(self, **properties):
        # Toto nastaví komponenty na formulári
        self.init_components(**properties)

        # Zmena textu na prihlasovacom tlačidle
        self.update_sign_in_text()
        #print(sys.path)

        # Načítanie emailov zo servera a ich vypísanie
        self.get_users()

    def update_sign_in_text(self):
        """Aktualizuje text prihlasovacieho tlačidla"""
        user = anvil.users.get_user()
        if user:
            email = user["email"]
            self.sign_in.text = email
        else:
            self.sign_in.text = "Sign In"

    def get_users(self):
        """Načíta používateľov z tabuľky Users a vytvorí tlačidlá"""
        users = anvil.server.call('get_users')

        for user in users:
            # Dynamicky pridávame tlačidlo pre každého používateľa
            button = Button(text=user['email'])
            button.tag.user_id = user['id']  # Uložíme user_id do tagu tlačidla
            button.tag.user_email = user['email']
            button.set_event_handler('click', self.zaznam_kavy)
            self.flow_panel_1.add_component(button)

    def zaznam_kavy(self, **event_args):
        """Pri kliknutí na tlačidlo zaznamená výber kávy do tabuľky"""
        user_id = event_args['sender'].tag.user_id  # Získame user_id z tagu tlačidla
        user_email = event_args['sender'].tag.user_email
        print(f"User ID: {user_email}")
        
        # Zobrazenie dialógového okna s otázkou
        response = alert(f"Do you want to confirm this coffee log for {user_email}?", buttons=[("Yes", True), ("No", False)])
        if response:
            # Uloženie záznamu do tabuľky pomocou serverovej funkcie
            anvil.server.call('add_coffee_record', user_id)
            alert(f"Coffee log recorded for user: {user_email}")

    def sign_in_button(self, **event_args):
        """Pri kliknutí na tlačidlo sa používateľ prihlási"""
        #user = anvil.users.get_user()
        #if user:
        #  confirm_logout = confirm('Would you like to logout?')
        #  if confirm_logout:
        #    anvil.users.logout()
        #else:
        #  anvil.users.login_with_form(allow_cancel=True)
        #self.update_sign_in_text()  
        custom_signup.login_flow.do_email_confirm_or_reset()
        open_form('Test')

# funkcia pre button generate pdf
#    def generate_pdf_button_click(self, **event_args):
        # Nastavenie filtra (scope)
#        start_date = self.start_date_picker.date
#        end_date = self.end_date_picker.date
        # Načítanie filtrovaných dát zo servera
#        data = anvil.server.call('get_filtered_data', start_date, end_date)
        # Generovanie PDF zo získaných dát
#       pdf = anvil.server.call('generate_pdf', data)
        # Stiahnutie PDF
#        anvil.media.download(pdf)

    def generate_pdf_button_click(self, **event_args):
        # Zobrazenie modálneho dialógu na výber dátumov
        #dates = DatePickerDialog().show()
        dialog = DatePickerDialog()
        result = alert(content=dialog, large=True, buttons=[])
        if result is None:
          print("Používateľ zrušil dialóg.")
        else:
          print("Výsledok:", result)
          start_date, end_date = result
          data = anvil.server.call('get_filtered_data', start_date, end_date)
          pdf = anvil.server.call('generate_pdf', data)
          anvil.media.download(pdf)  # Stiahnutie PDF
        #dates = dialog.show()
        
        
        

    


