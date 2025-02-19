from ._anvil_designer import RowTemplate7Template
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate7(RowTemplate7Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.text_box_1.text = self.item['name']
    self.text_box_2.text = self.item['email']
    self.text_box_3.text = self.item['id']
    #self.text_box_1.width = 500
    #self.text_box_2.width = 500
    #self.text_box_3.width = 500
    # Any code you write here will run before the form opens.

    def button_2_click(self, **event_args):
      self.item.delete()
      self.remove_from_parent()
