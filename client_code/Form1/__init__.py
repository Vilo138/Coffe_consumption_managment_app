import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables
from ._anvil_designer import Form1Template
from anvil import *
import anvil.users
import anvil.server

@anvil.server.callable
def get_users():
    return app_tables.users.search()

@anvil.server.callable
def update_user_count(user_id):
    user = app_tables.users.get_by_id(user_id)
    if user:
        user['count'] += 1
        user.update()
        return user
    return None



class Form1(Form1Template):
    def __init__(self, **properties):
        self.init_components(**properties)

       
        self.users = anvil.server.call('get_users')  
        self.buttons = []
        self.create_buttons()

    def create_buttons(self):
        for user in self.users:
            button = Button(text=f"{user['name']}: {user['count']}", user=user)
            button.role = "raised"
            button.set_event_handler('click', self.button_click)
            self.buttons.append(button)
            self.add_component(button)

    def button_click(self, **event_args):
        button = event_args['sender']
        user = button.user
        updated_user = anvil.server.call('update_user_count', user.get_id())  
        if updated_user:
            button.text = f"{updated_user['name']}: {updated_user['count']}"

    def link_2_click(self, **event_args):
        anvil.users.login_with_form()

    def button_1_click(self, **event_args):
      """This method is called when the button is clicked"""
      pass
