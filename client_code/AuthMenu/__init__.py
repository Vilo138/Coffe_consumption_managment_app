from ._anvil_designer import AuthMenuTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import login_flow
from ..Home import Home


class AuthMenu(AuthMenuTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run when the form opens.
    self.update_login_status()
    
    
  def update_login_status (self):
    user = anvil.users.get_user()
    if user is None:
      self.login_status_lbl.text = "You are not logged in."
    else:
      self.login_status_lbl.text = "You are logged in as %s" % user['email']

  def login_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    login_flow.login_with_form()
    self.update_login_status()
    #print('som tu')
    #anvil.server.raise_event('user_login_changed')


  def logout_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    #from ..Index import Index
    anvil.users.logout()
    try:
      anvil.js.call('location.reload()')
    except Exception as e:
          print(f"Error occurred: {e}")
          pass
    self.update_login_status()
    #print('som tu')
    #anvil.server.raise_event('user_login_changed')

    #index_instancia = Index()
    #index_instancia.update_sign_in_text()

  def signup_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    login_flow.signup_with_form()





