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
from anvil import alert


class DatePickerDialog(DatePickerDialogTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.dropdwn_items()
    self.result = None

    # Any code you write here will run before the form opens.
  def dropdwn_items(self):
    item_list = [("All Users", None)]  
    for row in app_tables.users.search():
      item_list.append((row["name"], row))
    self.drop_down_users.items = item_list

    
  def button_ok_click(self, **event_args):
        start_date = self.start_date_picker.date
        end_date = self.end_date_picker.date
        drpdwn_value = self.drop_down_users.selected_value
        
        if start_date and end_date:
          if drpdwn_value is None:
            data = anvil.server.call("get_filtered_data", start_date=start_date, end_date=end_date)
          else:
            data = anvil.server.call("get_filtered_data", start_date=start_date, end_date=end_date, user_name=drpdwn_value['name'])
          if data:  
            pdf = anvil.server.call("generate_pdf", data=data, start_date=start_date, end_date=end_date)
            anvil.media.download(pdf)
              #print("PDF has been downloaded.")
          else:
            alert("No data available for the selected dates.")
        else:  
          alert("Please select valid start and end dates.")
          
        #self.raise_event("x-close-alert", value=None)
        #if self.dropdown_users is None:
         # anvil.server.call('generate_pdf')
        #elif self.drop_down_users == row:
         # anvil.server.call('pdf_user')

  def button_cancel_click(self, **event_args):
        print("Cancel clicked")
        self.result = None
        self.raise_event("x-close-alert", value=None)

  

