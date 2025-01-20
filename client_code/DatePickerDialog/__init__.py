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
    # Inicializácia návratovej hodnoty
    self.result = None

    # Any code you write here will run before the form opens.
    
  def button_ok_click(self, **event_args):
        """Po kliknutí na OK vráti vybrané dátumy"""
        print("OK clicked")
        start_date = self.start_date_picker.date
        end_date = self.end_date_picker.date
        self.result = (start_date, end_date)
        print(self.result)
        if self.result:  # Ak sú vrátené dátumy
          start_date, end_date = self.result
          if start_date and end_date:
            print(f"Generating PDF for dates: {start_date} - {end_date}")  # Debugging
        # Volanie serverovej funkcie na načítanie dát
            data = anvil.server.call("get_filtered_data", start_date=start_date, end_date=end_date)
            if data:  # Ak sú dáta na generovanie
              pdf = anvil.server.call("generate_pdf", data=data)
              anvil.media.download(pdf)  # Stiahnutie PDF
              print("PDF has been downloaded.")  # Debugging
            else:
              alert("No data available for the selected dates.")
          else:
            alert("Please select valid start and end dates.")
        else:
          print("Action was canceled.")  # Debugging
          alert("Action was canceled.")
        #close_alert()  # Zatvorí dialóg
    
  def button_cancel_click(self, **event_args):
        """Po kliknutí na Cancel zatvorí dialóg bez hodnôt"""
        print("Cancel clicked")
        self.result = None
        #close_alert()  # Zatvorí dialóg
