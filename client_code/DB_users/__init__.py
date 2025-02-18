from ._anvil_designer import DB_usersTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class DB_users(DB_usersTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #self.repeating_panel_1.items = app_tables.users.search(tables.order_by('id'))
    #self.repeating_panel_1.items = app_tables.users.client_writable()
    self.repeating_panel_1.items = app_tables.users.client_writable().search(tables.order_by("id", ascending=True))

    self.data_grid_1.role = 'wide'
    #self.get_data()

    # Any code you write here will run before the form opens.
  #def get_data(self):
    #db_data = 
    #self.repeating_panel_1.items = anvil.server.call("get_users_data").search()

  #def save_changes(self, item, **event_args):
  #      """Uloží zmeny pri úprave tabuľky"""
   #     anvil.server.call('update_row', item)