from ._anvil_designer import ItemTemplate3Template
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate3(ItemTemplate3Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.text_box_id.text = self.item['id']
    self.text_box_user_id.text = self.item['user_id']['id']
    self.text_box_name.text = self.item['user_id']['name']
    self.text_box_time_log.text = self.item['time_log']

  def button_del_click(self, **event_args):
    self.item.delete()
    self.remove_from_parent()
