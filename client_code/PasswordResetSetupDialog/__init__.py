from ._anvil_designer import PasswordResetSetupDialogTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class PasswordResetSetupDialog(PasswordResetSetupDialogTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    
  def focus_pw_repeat_box(self, **kws):
    """Focus on the password repeat box."""
    self.pw_repeat_box.focus()

  def close_alert(self, **kws):
    """Close any alert we might be in with True value."""
    self.raise_event('x-close-alert', value=True)