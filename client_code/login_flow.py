from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.js
from LoginDialog import LoginDialog
from SignupDialog import SignupDialog
from ForgottenPasswordDialog import ForgottenPasswordDialog
from PasswordResetSetupDialog import PasswordResetSetupDialog
from NewUserDialog import NewUserDialog
from .NewIntake import NewIntake

#allow_cancel=True
def login_with_form():
  """Log in by popping up the custom LoginDialog"""
  d = LoginDialog()

  BUTTONS = [("Log in", "login", "primary"), ("Cancel", None)]
  #if allow_cancel:
    #BUTTONS += [("Cancel", None)]
  
  while anvil.users.get_user() is None:
    choice = alert(d, title="Log In",  buttons=BUTTONS)
    #dismissible=allow_cancel,
    if choice == 'login':
      try:
        anvil.users.login_with_email(d.email_box.text, d.password_box.text, remember=True)
        #print("12.3")
        try:
          anvil.js.call('location.reload()')
        except Exception as e:
          print(f"Error occurred: {e}")
          pass

      except anvil.users.EmailNotConfirmed:
        d.confirm_lnk.visible = True
      except anvil.users.AuthenticationFailed as e:
        #print("12.32")
        d.login_err_lbl.visible = True
        d.login_err_lbl.text = str(e.args[0])
        #d.refresh_data_bindings()  # Ak používate dátové väzby

        
    elif choice == 'reset_password':
      fp = ForgottenPasswordDialog(d.email_box.text)
      
      if alert(fp, title='Forgot Password', buttons=[("Reset password", True, "primary"), ("Cancel", False)]):
        
        if anvil.server.call('_send_password_reset', fp.email_box.text):
          alert(f"A password reset email has been sent to {fp.email_box.text}.")
        else:
          alert("That username does not exist in our records.")
        
    elif choice == 'confirm_email':
      if anvil.server.call('_send_email_confirm_link', d.email_box.text):
        alert(f"A new confirmation email has been sent to {d.email_box.text}.")
      else:
        alert(f"'{d.email_box.text}' is not an unconfirmed user account.")
      d.confirm_lnk.visible = False
    
    elif choice is None:
      #and allow_cancel
      break
    anvil.server.call('get_user_role')
    

      
def signup_with_form():
  d = SignupDialog()

  while True:
    if not alert(d, title="Sign Up", buttons=[("Sign Up", True, 'primary'), ("Cancel", False)]):
      return
    
    if d.password_box.text != d.password_repeat_box.text:
      d.signup_err_lbl.text = 'Passwords do not match. Try again.'
      d.signup_err_lbl.visible = True
      continue
    
    err = anvil.server.call('_do_signup', d.email_box.text, d.name_box.text, d.password_box.text)
    if err is not None:
      d.signup_err_lbl.text = err
      d.signup_err_lbl.visible = True
    else:
      alert(f"We have sent a confirmation email to {d.email_box.text}.\n\nCheck your email, and click on the link.")
      return
  
    
def do_email_confirm_or_reset():
  print('som tu0')
  """Check whether the user has arrived from an email-confirmation link or a password reset, and pop up any necessary dialogs.
     Call this function from the 'show' event on your startup form.
  """
  h = anvil.get_url_hash()
  if isinstance(h, dict) and 'email' in h:
    print('som tu reset')
    if 'pwreset' in h:
      if not anvil.server.call('_is_password_key_correct', h['email'], h['pwreset']):
        alert("This is not a valid password reset link")
        return

      while True:
        pwr = PasswordResetSetupDialog()
        if not alert(pwr, title="Reset Your Password", buttons=[("Reset password", True, 'primary'), ("Cancel", False)]):
          return
        if pwr.pw_box.text != pwr.pw_repeat_box.text:
          alert("Passwords did not match. Try again.")
        else:
          break
  
      if anvil.server.call('_perform_password_reset', h['email'], h['pwreset'], pwr.pw_box.text):
        alert("Your password has been reset. You are now logged in.")
      else:
        alert("This is not a valid password reset link")

        
    elif isinstance(h, dict) and 'email' in h:
      if 'setup' in h:
        if not anvil.server.call('_is_password_key_correct', h['email'], h['setup']):
          print('som tu setup')
          alert("This is not a valid password setup link")
          return

        while True:
          pwr = PasswordResetSetupDialog()
          print('som tu2')
          if not alert(pwr, title="Setup Your Password", buttons=[("Setup password", True, 'primary'), ("Cancel", False)]):
            return
          if pwr.pw_box.text != pwr.pw_repeat_box.text:
            alert("Passwords did not match. Try again.")
          else:
            break
  
        if anvil.server.call('_perform_password_reset', h['email'], h['setup'], pwr.pw_box.text):
          alert("Your password has been setup. You are now logged in.")
        else:
          alert("This is not a valid password setup link")
        
    elif 'confirm' in h:
      if anvil.server.call('_confirm_email_address', h['email'], h['confirm']):
        alert("Thanks for confirming your email address. You are now logged in.")
      else:
        alert("This confirmation link is not valid. Perhaps you have already confirmed your address?\n\nTry logging in normally.")
 
     
def add_new_user(allow_cancel=True):
  d = NewUserDialog()
  BUTTONS = [("Submit", "submit", "primary"), ("Cancel", None)]
  choice = alert(d, title="Add new user",  buttons=BUTTONS)
  if choice == 'submit':
    try:
      anvil.server.call('add_user',d.name_box.text, d.email_box.text, d.role_box.text)
      #wait()
      anvil.server.call('_send_password_setup_link', d.email_box.text)
      
    except Exception as e:
      d.err_lbl.text = "Velky spatny"
      print(e)

def addRowCofLogs():
  d = NewIntake()
  BUTTONS = [("Submit", "submit", "primary"), ("Cancel", None)]
  choice = alert(d, title="Add new intake",  buttons=BUTTONS)
  if choice == 'submit':
    try:
      anvil.server.call('newIntake',d.text_box_user_id.text, d.text_box_timelog.text)
    except Exception as e:
        print(e)
    #anvil.tables.coffe_logs.add_row(id=newID,user_id=d.text_box_user_id.text, timelog=d.text_box_timelog.text)
    #anvil.tables.coffee_logs.add_row()