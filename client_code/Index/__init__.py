from ._anvil_designer import IndexTemplate
from anvil import *
import anvil.server
import anvil.users
from datetime import datetime
from anvil.tables import app_tables
import sys
from ..DatePickerDialog import DatePickerDialog
from anvil import alert
from ..AuthMenu import AuthMenu
from ..Home import Home
from ..DB_users import DB_users
from ..DB_coflogs import DB_coflogs

import anvil.tables as tables
import anvil.tables.query as q
#from anvil.tables import app_tables
from anvil import open_form
from .. import login_flow
from anvil.js.window import moment

moment.updateLocale('en', { 'week': {
  'dow': 1, # First day of week is Monday
}})

class Index(IndexTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.update_sign_in_text()
        self.visible_db()
        #print(sys.path)
        self.content_panel.add_component(Home())
  
    def visible_db(self):
      current_role = anvil.server.call('get_current_user_role')
      self.link_DB_users.visible = current_role
      self.link_DB_cof_logs.visible = current_role
  
    def update_sign_in_text(self):
        user = anvil.users.get_user()
        if user:
            email = user["email"]
            self.sign_in.text = email
        else:
            self.sign_in.text = "Sign In"

    def sign_in_button(self, **event_args):  
        login_flow.do_email_confirm_or_reset()
        self.visible_db()
        self.update_sign_in_text()
        self.content_panel.clear()
        self.content_panel.add_component(AuthMenu())

    def generate_pdf_button_click(self, **event_args):
        #dates = DatePickerDialog().show()
        dialog = DatePickerDialog()
        result = alert(content=dialog, large=True, buttons=[])
        if result is None:
          print("Používateľ zrušil dialóg.")
        else:
          print("Výsledok:", result)
          start_date, end_date = result
          data = anvil.server.call('get_filtered_data', start_date, end_date)
          pdf = anvil.server.call('generate_pdf', data)
          anvil.media.download(pdf)  
        #dates = dialog.show()

    def title_click(self, **event_args):
      """This method is called when the link is clicked."""
      self.update_sign_in_text()
      self.visible_db()
      if not isinstance(self.content_panel.get_components()[-1], Home):
        self.content_panel.clear()
        self.content_panel.add_component(Home())

    def button_csv_click(self, **event_args):
      csv_file = anvil.server.call('get_filtered_data_csv')  
      anvil.media.download(csv_file)  

    def link_DB_users_click(self, **event_args):
      """This method is called when the link is clicked"""
      self.update_sign_in_text()
      self.content_panel.clear()
      self.content_panel.add_component(DB_users())  

    def link_DB_cof_logs_click(self, **event_args):
      self.update_sign_in_text()
      self.content_panel.clear()
      self.content_panel.add_component(DB_coflogs())
