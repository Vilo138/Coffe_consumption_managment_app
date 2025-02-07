import anvil.server
import anvil.tables as tables
from anvil.tables import app_tables
from datetime import datetime
from anvil import Media
from weasyprint import HTML
import collections


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
@anvil.server.callable
def get_filtered_data(start_date=None, end_date=None):
    rows = app_tables.coffee_logs.search()
    # Filtrovanie na základe rozsahu dátumu
    if start_date and end_date:
        rows = [row for row in rows if start_date <= row['time_log'].date() <= end_date]
    emails = [row['user_id']['email'] if row['user_id'] and row['user_id']['email'] else 'Unknown' for row in rows]
    email_counts = collections.Counter(emails)
    #print(emails, email_counts)

    results = []
    for email, count in email_counts.items():
        results.append({
            "email": email,
            "pocet": count,
            "suma": count * 0.6  # Cena za jednu kávu
        })
    #print(results)
    return results

# funkcia na generovanie pdf reportu
@anvil.server.callable
def generate_pdf(data, start_date, end_date):
    rows_html = ''.join(
        f"<tr><td>{row['email']}</td><td>{row['pocet']}</td><td>{row['suma']}</td></tr>"
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
            <th>Email</th>
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

    




