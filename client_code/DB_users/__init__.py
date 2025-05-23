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
from .. import login_flow
from ..Home import Home
from ..AuthMenu import AuthMenu


class DB_users(DB_usersTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.load_data()

  def load_data(self):
    #self.repeating_panel_1.items = app_tables.users.search(tables.order_by("id", ascending=True))
    self.repeating_panel_1.items = app_tables.users.client_writable().search(tables.order_by("id", ascending=True))


  def addNewUser_click(self, **event_args):
    login_flow.add_new_user()
    self.load_data()

  
