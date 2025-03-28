import anvil.tz
import sys
import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables
from datetime import datetime
from anvil import Media
from weasyprint import HTML
import collections # stare, pod tymto nove
import anvil.email
from decimal import *
import anvil.users
from anvil.http import url_encode
import bcrypt
from random import SystemRandom
import anvil.tables.query as q
import pandas as pd
random = SystemRandom()

#import tables
#from tables import app_tables
#naive_local = datetime.now()
# 2019-08-09 10:10:00.406000
#aware_local = datetime.now(anvil.tz.tzlocal())


@anvil.server.callable
def get_users():
    # Načíta používateľov z tabuľky Users a vráti zoznam emailov
    return [{'id': user.get_id(), 'email': user['email'], 'name': user['name']} for user in app_tables.users.search()]

@anvil.server.callable
def add_coffee_record(user_id):
    user_id = app_tables.users.get_by_id(user_id)

    max_id_row = list(app_tables.coffee_logs.search(tables.order_by("id", ascending=False)))[:1]
    if max_id_row:
        max_id = max_id_row[0]['id']
    else:
        max_id = 1

    new_id = (max_id or 0) + 1
  
    # Pridá záznam o káve do tabuľky pocet_kav
    app_tables.coffee_logs.add_row(
        id=new_id,
        user_id=user_id,
        time_log=datetime.now(anvil.tz.tzoffset(hours=1)) 
    )
@anvil.server.callable
def get_filtered_data(start_date=None, end_date=None, user_name=None):
    rows = app_tables.coffee_logs.search()
    if start_date and end_date and user_name:
      rows = [row for row in rows if start_date <= row['time_log'].date() <= end_date and row['user_id']['name'] == user_name]
    elif start_date and end_date:
      rows = [row for row in rows if start_date <= row['time_log'].date() <= end_date]
    elif user_name: 
        rows = [row for row in rows if row['user_id']['name'] == user_name]
    
    names = [row['user_id']['name'] if row['user_id'] and row['user_id']['name'] else 'Unknown' for row in rows]
    names_counts = collections.Counter(names)
    #print(emails, email_counts)

    results = []

    for name, count in names_counts.items():
        results.append({
            "name": name,
            "pocet": count,
            "suma": round(count * 0.6, 2)
        })
    #print(results)
    return results
@anvil.server.callable
def get_filtered_data_csv():
    rows = app_tables.coffee_logs.search()
    # Konvertovanie na pandas DataFrame
    data_list = [{'id': r['id'], 'user_id': r['user_id']['id'], 'name': r['user_id']['name'], 'time_log': r['time_log']} for r in rows]
    df = pd.DataFrame(data_list)
    # Vytvorenie CSV ako stringu
    csv_string = df.to_csv(index=False)

    # Vrátenie CSV ako Anvil Media objekt
    return anvil.BlobMedia("text/csv", csv_string.encode("utf-8"), name="data.csv")

# funkcia na generovanie pdf reportu
@anvil.server.callable
def generate_pdf(data, start_date, end_date):
    rows_html = ''.join(
        f"<tr><td>{row['name']}</td><td>{row['pocet']}</td><td>{row['suma']}</td></tr>"
        for row in data
    ) if data else "<tr><td colspan='3'>No data available</td></tr>"

    html_template = f"""
    <html>
      <head>
        <style>
          table {{
            width: 100%;
            border-collapse: collapse;
          }}
          th, td {{
            border: 1px solid black;
            padding: 8px;
            text-align: left;
          }}
          th {{
            background-color: #f2f2f2;
          }}
        </style>
      </head>
      <body>
        <h1>Report from {start_date} to {end_date}</h1>
        <table>
          <tr>
            <th>Name</th>
            <th>Count</th>
            <th>Sum</th>
          </tr>
          {rows_html}
        </table>
      </body>
    </html>
    """
    # Generovanie PDF
    pdf = HTML(string=html_template).write_pdf()
    return anvil.BlobMedia("application/pdf", pdf, name=f"report {start_date} to {end_date}.pdf")







def mk_token():
  """Generate a random 14-character token"""
  return "".join([random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789") for i in range(14)])

@anvil.server.callable
def _send_password_reset(email):
  """Send a password reset email to the specified user"""
  user = app_tables.users.get(email=email)
  if user is not None:
    user['link_key'] = mk_token()
    anvil.email.send(to=user['email'], subject="Reset your password", text=f"""
Hi,

Someone has requested a password reset for your account. If this wasn't you, just delete this email.
If you do want to reset your password, click here:

{anvil.server.get_app_origin('published')}#?email={url_encode(user['email'])}&pwreset={url_encode(user['link_key'])}

Thanks!
""")
    return True


@anvil.server.callable
def _send_email_confirm_link(email):
  """Send an email confirmation link if the specified user's email is not yet confirmed"""
  user = app_tables.users.get(email=email)
  if user is not None and not user['confirmed_email']:
    if user['link_key'] is None:
      user['link_key'] = mk_token()
    anvil.email.send(to=user['email'], subject="Confirm your email address", text=f"""
Hi,

Thanks for signing up for our service. To complete your sign-up, click here to confirm your email address:

{anvil.server.get_app_origin('published')}#?email={url_encode(user['email'])}&confirm={url_encode(user['link_key'])}

Thanks!
""")
    return True

def hash_password(password, salt):
  """Hash the password using bcrypt in a way that is compatible with Python 2 and 3."""
  if not isinstance(password, bytes):
    password = password.encode()
  if not isinstance(salt, bytes):
    salt = salt.encode()

  result = bcrypt.hashpw(password, salt)

  if isinstance(result, bytes):
    return result.decode('utf-8')


@anvil.server.callable
def _do_signup(email, name, password):
    #print('robim singup')
    if not name.strip():
        return "Must supply a name"
    if not email.strip():
        return "Must supply an email"

    pwhash = hash_password(password, bcrypt.gensalt())

    @tables.in_transaction
    def add_user_if_missing():
        user = app_tables.users.get(email=email)
        if user:
            return "User already exists" 

        max_id_row = app_tables.users.search(tables.order_by("id", ascending=False))
        first_row = next(iter(max_id_row), None)
        if first_row:
          max_id = first_row['id']
          new_id = max_id + 1
        else:
          new_id = 1

        

        user = app_tables.users.add_row(email=email, enabled=True, name=name, password_hash=pwhash, id=new_id)
        return user

    result = add_user_if_missing()
    if isinstance(result, str):
        return result  # Vráti chybovú správu, ak existuje.

    _send_email_confirm_link(email)
    return None  # No error = success

  
    
def get_user_if_key_correct(email, link_key):
  user = app_tables.users.get(email=email)

  if user is not None and user['link_key'] is not None:
    # Use bcrypt to hash the link key and compare the hashed version.
    # The naive way (link_key == user['link_key']) would expose a timing vulnerability.
    salt = bcrypt.gensalt()
    if hash_password(link_key, salt) == hash_password(user['link_key'], salt):
      return user


@anvil.server.callable
def _is_password_key_correct(email, link_key):
  return get_user_if_key_correct(email, link_key) is not None

@anvil.server.callable
def _perform_password_reset(email, reset_key, new_password):
  """Perform a password reset if the key matches; return True if it did."""
  user = get_user_if_key_correct(email, reset_key)
  if user is not None:
    user['confirmed_email'] = True
    user['password_hash'] = hash_password(new_password, bcrypt.gensalt())
    user['link_key'] = None
    anvil.users.force_login(user)
    return True
    
@anvil.server.callable
def _confirm_email_address(email, confirm_key):
  """Confirm a user's email address if the key matches; return True if it did."""
  user = get_user_if_key_correct(email, confirm_key)
  if user is not None:
    user['confirmed_email'] = True
    user['link_key'] = None
    anvil.users.force_login(user)
    return True

@anvil.server.callable
def get_users_data():
  return app_tables.users.client_writable()
  
@anvil.server.callable
def add_user(name, email, role):
  if not name.strip():
        return "Must supply a name"
  if not email.strip():
        return "Must supply an email"
  if not role.strip():
        return "Must supply a role"
  valid_roles = ['user', 'superuser', 'admin']
  if role not in valid_roles:
    print('Bad input')
    return 'Bad input'
    
  rows = list(app_tables.users.search(tables.order_by("id", ascending=False)))
  if rows:
    actual_max_id = rows[0]['id']
  else:
    actual_max_id = None

  if actual_max_id is None:  # Správne porovnanie s None
    new_id = 1
  else:
    new_id = actual_max_id + 1
  
  if role == 'admin':
    check_role = anvil.users.get_user()
    if check_role['role'] == 'admin':
      app_tables.users.add_row(email=email, enabled=True, name=name, id=new_id, role=role)
    else:
      print('You dont have permission to setup admin acount')
  elif role in ['user', 'superuser']:
    app_tables.users.add_row(email=email, enabled=True, name=name, id=new_id, role=role)

  

@anvil.server.callable
def _send_password_setup_link(email):
  """Send an email confirmation link if the specified user's email is not yet confirmed"""
  user = app_tables.users.get(email=email)
  if user is not None and not user['confirmed_email']:
    #user['confirmed_email'] = True
    if user['link_key'] is None:
      user['link_key'] = mk_token()
    anvil.email.send(to=user['email'], subject="Password set up", text=f"""
Hi,
You have been signed up to Coffee management application. To complete your sign-up, please, set up your password by clicking link below:

{anvil.server.get_app_origin('published')}#?email={url_encode(user['email'])}&setup={url_encode(user['link_key'])}

Thanks!
""")
    return True




@anvil.server.callable 
def update_row_name(item): 
  """Upraví existujúci riadok v databáze""" 
  row = app_tables.users.get(id=item['id']) 
  if row: 
    row.update(name=item['name'], email=item['email'], role=item['role'])  # Aktualizácia údajov

@anvil.server.callable
def get_user_role():
    user = anvil.users.get_user()
    if user:
      role = user['role']
      return role
    else:
      pass
  
  
@anvil.server.callable
def delete_users_all_logs(user_id):
    user_row = app_tables.users.get(id=user_id)
    if user_row:
      for row in app_tables.coffee_logs.search(user_id=user_row):
        row.delete()
  
  
@anvil.server.callable
def newIntake(user_regN, timelog):
  if not user_regN.strip():
    return "Must supply an user ID"
  if not timelog.strip():
    return "Must supply Date and Time"
  rows = list(app_tables.coffee_logs.search(tables.order_by('id', ascending = False)))
  #rows_users = list(app_tables.coffee_logs.search())
  #user_id = rows_users['user_id']['id']
  #user_id = app_tables.users['id']
  user_id_int = int(user_regN)
  userIDRow = app_tables.users.get(id=user_id_int)
  if rows:
    maxid = rows[0]['id']
    newid = maxid + 1
  else:
    newid = 1
  app_tables.coffee_logs.add_row(id=newid, user_id=userIDRow, time_log=datetime.strptime(timelog, '%Y-%m-%d %H:%M'))
    

#rows = app_tables.coffee_logs.search()
    # Filtrovanie na základe dátumu
    #if start_date and end_date:
        #rows = [row for row in rows if start_date <= row['time_log'].date() <= end_date]
    #names = [row['user_id']['name'] if row['user_id'] and row['user_id']['name'] else 'Unknown' for row in rows]
    #names_counts = collections.Counter(names)




