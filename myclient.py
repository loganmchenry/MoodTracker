import socket
import myfunctions
from cryptography.fernet import Fernet
import clientfunctions

prompt = " client> "
host = socket.gethostname()     # Server hostname
port = 8080                     # Server port

s = socket.socket()
s.connect((host, port))

# get the servers public key
public_key = s.recv(1024).decode('utf-8')
n,e = public_key.split(", ")
n = int(n)
e = int(e)
#
# print("recieved n:" + str(n))
# print("recieved e:" + str(e))
#
s.send("Recieved".encode('utf-8'))


# recieve fernet key
e_key = s.recv(1024).decode('utf-8')
key_array = []
key_array = e_key.split(",")

# decrypt the fernet key 
key = []
x = ""
for chunk in key_array:
    x = str(chunk.strip("[]"))
    
    x = pow(int(x), e, n)
    key.append(chr(x))

# format
seperator = ""
d_key = seperator.join(key)
# print(d_key)

# make the fernet object
codec = Fernet(bytes(d_key, 'utf-8'))

print("""
  __  __        __     ___      _               _  
 |  \/  |_   _  \ \   / (_)_ __| |_ _   _  __ _| | 
 | |\/| | | | |  \ \ / /| | '__| __| | | |/ _` | | 
 | |  | | |_| |   \ V / | | |  | |_| |_| | (_| | | 
 |_|__|_|\__, |    \_/  |_|_|   \__|\__,_|\__,_|_| 
 |  _ \(_)___/_ _ __ _   _                         
 | | | | |/ _` | '__| | | |                        
 | |_| | | (_| | |  | |_| |                        
 |____/|_|\__,_|_|   \__, |                        
                     |___/   
                    
""")
print("Welcome to your virtual mood tracker!")


msg = ""
print("Enter 'help' for a list of commands.")
while (msg != 'q'):
    msg = input(prompt)

    # get the correct args
    if (msg ==  "login"):
        msg = clientfunctions.generate_login(prompt)
        if (msg != "invalid"):
            args = msg.split(" ")
            prompt = " " + args[1] + "> "
    else:
        if (msg == "adduser"):
            msg = clientfunctions.generate_new_user(prompt)
        else:
            if (msg == "changepass"):
                msg = clientfunctions.generate_change_pass(prompt) 
            else:
                if (msg == "delete"):
                    msg = clientfunctions.generate_delete_user(prompt)
                else:
                    if (msg == "newentry"):
                        msg = clientfunctions.generate_new_entry(prompt)

    s.send(codec.encrypt(msg.encode('utf-8')))
    reply = codec.decrypt(s.recv(1024)).decode('utf-8')
    

    # change prompt if a new user logged in
    if(reply == "Logged out successfully!" 
     or reply == "Username or Password Incorrect!"):
        prompt = " client> "
    

    print ("Server says: ", reply)
s.close()