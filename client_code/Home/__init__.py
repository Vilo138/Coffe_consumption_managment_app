from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Home(HomeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.get_users()

    # Any code you write here will run before the form opens.
  def get_users(self):
        """Načíta používateľov z tabuľky Users a vytvorí tlačidlá"""
        users = anvil.server.call('get_users')

        for user in users:
            # Dynamicky pridávame tlačidlo pre každého používateľa
            button = Button(text=user['name'])
            button.tag.user_id = user['id']  # Uložíme user_id do tagu tlačidla
            button.tag.user_email = user['email']
            button.set_event_handler('click', self.zaznam_kavy)
            self.flow_panel_buttons_users.add_component(button)
            #self.content_panel.add_component(button)

  def zaznam_kavy(self, **event_args):
        """Pri kliknutí na tlačidlo zaznamená výber kávy do tabuľky"""
        user_id = event_args['sender'].tag.user_id  # Získame user_id z tagu tlačidla
        user_email = event_args['sender'].tag.user_email
        #print(f"User ID: {user_email}")
        
        # Zobrazenie dialógového okna s otázkou
        response = alert(f"Do you want to confirm this coffee log for {user_email}?", buttons=[("Yes", True), ("No", False)])
        if response:
            # Uloženie záznamu do tabuľky pomocou serverovej funkcie
            anvil.server.call('add_coffee_record', user_id)
            alert(f"Coffee log recorded for user: {user_email}")