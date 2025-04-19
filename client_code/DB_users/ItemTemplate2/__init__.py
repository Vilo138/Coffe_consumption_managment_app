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
    self.text_box_4.text = self.item['role']
    self.text_box_5.text = self.item['last_login']

    #self.text_box_2.enabled = False


    # Any code you write here will run before the form opens.

  def button_del_click(self, **event_args):
    #self.repeating_panel_1.items = app_tables.users.client_writable().search(tables.order_by("id", ascending=True))
    if confirm('Are you sure you want to PERMANENTLY delete this user and all associated data?'):
      result = anvil.server.call('delete_users_all_logs', self.item['id'])
      if result == 'permission':
        alert("You don't have permission to delete admin acount")
      else:
        self.item.delete()
        self.remove_from_parent()
  


  def text_box_2_lost_focus(self, **event_args): 
      self.item['name'] = self.text_box_2.text  # Aktualizácia 

  def text_box_3_lost_focus(self, **event_args):
      self.item['email'] = self.text_box_3.text

  def text_box_4_lost_focus(self, **event_args):
    proposed_role = self.text_box_4.text
    result = anvil.server.call('update_row_name', self.item['id'], proposed_role)
    if result == 'permission':
        alert("You don't have permission to set admin account")
        self.text_box_4.text = self.item['role']
    elif result == 'invalid':
        alert("Invalid input")
        self.text_box_4.text = self.item['role']
    else:
        self.item['role'] = proposed_role
        alert("You have successfully changed the role")




  

  

  

  

    
      
