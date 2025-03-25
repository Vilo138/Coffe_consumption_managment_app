from ._anvil_designer import DB_coflogsTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class DB_coflogs(DB_coflogsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.load_data()

    # Any code you write here will run before the form opens.

  def load_data(self):
      #self.repeating_panel_1.items = app_tables.users.search(tables.order_by("id", ascending=True))
      self.repeating_panel_1.items = app_tables.coffee_logs.client_writable().search(tables.order_by("id", ascending=True))

  def button_new_click(self, **event_args):
      #app_tables.coffee_logs.add_row()
      anvil.server.call('addRowCofLogs')
      self.load_data()
