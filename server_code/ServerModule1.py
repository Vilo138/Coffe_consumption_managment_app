import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables
from datetime import datetime

@anvil.server.callable
def get_users():
    # Načíta používateľov z tabuľky Users a vráti zoznam emailov
    return [{'id': user.get_id(), 'email': user['email']} for user in app_tables.users.search()]

@anvil.server.callable
def add_coffee_record(user_id):
  
    user_id = app_tables.users.get_by_id(user_id)

    max_id_row = list(app_tables.coffee_logs.search(tables.order_by("id", ascending=False)))[:1]
    if max_id_row:
        max_id = max_id_row[0]['id']
    else:
        max_id = 0

  # Priradenie nového ID ako najvyššie existujúce ID plus jeden
    new_id = (max_id or 0) + 1
  
    # Pridá záznam o káve do tabuľky pocet_kav
    app_tables.coffee_logs.add_row(
        id=new_id,
        user_id=user_id,
        time_log=datetime.now()
    )

