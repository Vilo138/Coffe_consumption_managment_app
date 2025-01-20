from ._anvil_designer import DatePickerDialogTemplate
from anvil import *
import anvil.server
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class DatePickerDialog(DatePickerDialogTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
    
    def button_ok_click(self, **event_args):
        # Vráti vybrané dátumy
        start_date = self.start_date_picker.date
        end_date = self.end_date_picker.date
        self.raise_event("x-close", value=(start_date, end_date))
    
    def button_cancel_click(self, **event_args):
        # Zruší dialóg
        self.raise_event("x-close", value=None)
