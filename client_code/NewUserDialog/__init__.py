from ._anvil_designer import NewUserDialogTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables



class NewUserDialog(NewUserDialogTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.check_user_role_label()


  def check_user_role_label(self):
    user = anvil.users.get_user()
    if user:
      if user['role'] == 'admin':
        self.label_check_admin.text = 'Type in the role of user choose between user/superuser/admin'
      elif user['role'] == 'superuser':
        self.label_check_su.text = 'Type in the role of user choose between user/superuser'


  