import socket
import myfunctions
import numpy 
from cryptography.fernet import Fernet

db_file = "user_db.csv"
global current_user
current_user = ""

host = socket.gethostname()
port = 8080

s = socket.socket()
s.bind((host, port))

s.listen(1)
print ("Server is Running")
client_socket, client_addr = s.accept()
print ("Connection from ", str(client_addr))

# for the new connection, generate the RSA key
p = myfunctions.generate_private()
q = myfunctions.generate_private()
n = p*q
e = myfunctions.generate_e(p,q)

#
#print("p: " + str(p)) 
#print("q: " + str(q)) 
#print("n: " + str(n)) 
#print("e: " + str(e))

# send client the public key (n, e)
public_key = str(n) + ", " + str(e)
client_socket.send(str(public_key).encode('utf-8'))
# recieve confirmation
client_socket.recv(1024).decode('utf-8')

# encrypt using the private key 
lamb_n = numpy.lcm(p-1,q-1)
d = int(myfunctions.mod_inverse(e, lamb_n))
key = Fernet.generate_key()
#print(key)

# send the encrypted fernet key 
e_key = []
for char in key:
    e_key.append(pow(char, d, n))
seperator = ""
e_key = seperator.join(str(e_key))
client_socket.send(str(e_key).encode('utf-8'))

# make the fernet object 
codec = Fernet(key)










def parse(query):
    query_args = query.split(" ")
    #print ("Query split: ", query_args)
    dispatcher = {
        "login"     : login,
        "logout"    : logout,
        "q"         : quitApp,
        "adduser"   : addUser,
        "help"      : helpCommands,
        "delete"    : deleteUser,
        "changepass" : changePass,
        "newentry"  : newEntry,
        "showdata"  : showData,
        "listall"   : listAll,
        "invalid"   : invalid
    }
    dispatch = dispatcher.get(query_args[0], invalid)
    return dispatch(query_args)

admin_commands = """
! admin only !
adduser:    creates a new account
delete:     deletes the specified user's account
listall:    lists all user accounts"""

no_user_commands = """
login:      login to your account
q:          quit the program
help:       lists all commands for the current user"""

user_commands = """
logout:     logout the current user
newentry:   creates a new entry in you mood diary
showdata:   displays all the previous entries in your diary
changepass: change your account password"""

pretty_diary = """
  __  __         __  __                 _     
 |  \/  |       |  \/  |               | |    
 | \  / |_   _  | \  / | ___   ___   __| |___ 
 | |\/| | | | | | |\/| |/ _ \ / _ \ / _` / __|
 | |  | | |_| | | |  | | (_) | (_) | (_| \__ \\
 |_|  |_|\__, | |_|  |_|\___/ \___/ \__,_|___/
          __/ |                               
         |___/    
""" 
def newEntry(args):
    global current_user
    if(current_user == ""):
        msg = "You must login before creating a new entry."
        return msg
    diary_file = current_user + ".txt"
    with open (diary_file, "a+") as output:
        output.write("Your mood on " + args[1] + " " + args[2]
        + " " + args[3] + " at " + args[4] + " was: " )
        for i in range(5, len(args)):
            output.write(args[i] + " ")
        output.write("\n")
    return "New entry created!"

def showData(args):
    global current_user
    if(current_user == ""):
        msg = "You must login before viewing your diary"
        return msg
    diary_file = current_user + ".txt"

    try:
        with open (diary_file, "r") as input:
            msg = input.readlines()
    except:
        msg = "No entries yet! Try 'newentry'"
        return msg

    seperator = ""
    msg = seperator.join(msg)
    msg = "\n" + msg
    msg = pretty_diary + msg
    return msg


def listAll(args):
    global current_user
    if (current_user != "admin"):
        msg = "This function is for admins only."
        return msg
    msg = myfunctions.listAll(db_file)
    return msg

def deleteUser(args):
    global current_user
    if (current_user != "admin"):
        msg = "Only admins can delete users. No changes made."
        return msg
    # trying to delete admin?
    if (args[1] == "admin"):
        msg = "The admin account cannot be deleted."
        return msg
    msg = myfunctions.deleteUser(db_file, args[1])
    if (msg == "") :
        msg = "User not found"
    else: 
        msg = args[1] + " deleted successfully"
    return msg

def changePass(args):
    global current_user
    if (current_user == ""):
        msg = "You must log in before changing your password."
        return msg
    user = current_user
    password = args[1]
    new_pass = args[2]
    new_pass2 = args[3]
    if (myfunctions.changePassword(db_file, user, password, new_pass, new_pass2)):
        msg = "Password changed successfully!"
    else: 
        msg = "Either the password was incorrect or the new passwords did not match."

    return msg

def helpCommands(args):
    global current_user
    msg = no_user_commands
    if (current_user != ""):
        msg += user_commands
    if (current_user == "admin"):
        msg += admin_commands
    return msg


def login(args):
    global current_user
    if (current_user != ""):
        msg = current_user + " is already logged in!"
        return msg
    username = args[1]
    password = args[2]
    ret = myfunctions.login(db_file, username, password)
    if ret == -1:
        ret = -1 # do nothing
    else: 
        current_user = ret
    if current_user == "": msg = ("Username or password incorrect!")
    else: msg = (username + " Logged in successfully!")
    return msg

def logout(args):
    global current_user
    if (current_user == ""):
        return "No user is logged in."
    current_user = ""
    return "Logged out successfully!"

def quitApp(args):
    return "Session Closed"

def addUser(args):
    global current_user
    if (current_user != "admin"):
        msg = "This function is restricted to admins only. New user not added."
        return msg
    username = args[1]
    password = args[2]
    password2 = args[3]
    msg = myfunctions.addUser(db_file, username, password, password2)
    if (msg == -1):
        msg = "The passwords did not match, no new user added."
    else: 
        if (msg == -2):
            msg = "Username already exists!"
        else:
            msg += " added succesfully!"
    return msg

def invalid(args):
    return "Invalid command. \n Type 'help' for a list of commands."










connection = True
data = " "
while connection:
    e_data = (client_socket.recv(1024))
    if e_data: 
        data = codec.decrypt(e_data).decode('utf-8')
        #print ("Client> ", data)
        msg = parse(data)
        
        client_socket.send(codec.encrypt(msg.encode('utf-8')))
    else:
        print ("Server is Closing")
        client_socket.close()
        connection = False
        break


