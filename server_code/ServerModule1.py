import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables
from datetime import datetime

@anvil.server.callable
def get_users():
    # Načíta používateľov z tabuľky Users a vráti zoznam používateľov
    return [(user['id'], user['email']) for user in app_tables.users.search()]

@anvil.server.callable
def add_coffee_record(user_id):
    # Pridá záznam o káve do tabuľky pocet_kav
    app_tables.pocet_kav.add_row(
        user_id=user_id,
        cas_vyberu=datetime.now()
    )
