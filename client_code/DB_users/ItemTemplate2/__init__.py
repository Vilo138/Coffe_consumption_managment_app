from ._anvil_designer import ItemTemplate2Template
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate2(ItemTemplate2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.text_box_1.text = self.item['id']
    self.text_box_2.text = self.item['name']
    self.text_box_3.text = self.item['email']

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    if confirm('Are you sure you want to PERMANENTLY delete this row?'):
      self.item.delete()
      self.remove_from_parent()

  def text_box_2_lost_focus(self, **event_args):
    """Uloží zmeny do databázy po úprave hodnoty v TextBoxe"""
    self.item['name'] = self.text_box_2.text  # Aktualizácia self.item
    anvil.server.call('update_row', self.item)