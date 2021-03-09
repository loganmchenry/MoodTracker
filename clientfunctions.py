from getpass import getpass
from datetime import datetime
from datetime import date

def generate_login(prompt):
    if (prompt != " client> "):
        print ("Already logged in!")
        return "invalid"
    username = input("Enter your username \n" + prompt)
    password = getpass("Enter your password \n" + prompt)
    return "login " + username + " " + password

def generate_new_user(prompt):
    username = input("Enter the new username \n" + prompt)
    password = getpass("Enter the new password \n" + prompt)
    password2 = getpass("Reenter the password \n" + prompt)
    return "adduser " + username + " " + password + " " + password2

def generate_change_pass(prompt):
    password = getpass("Enter your current password \n" + prompt)
    pass1 = getpass("Enter your new password \n" + prompt)
    pass2 = getpass("Reenter your new password \n" + prompt)
    return "changepass " + password + " " + pass1 + " " + pass2


def generate_delete_user(prompt):
    username = input("Enter the username you would like to delete \n" + prompt)
    return "delete " + username

def generate_new_entry(prompt):
    entry = input("What's your mood today? \n" + prompt)
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    today = date.today()
    today_date = today.strftime("%B %d, %Y")
    return "newentry " + today_date + " " + time + " " + entry