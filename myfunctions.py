from random import randint
import sys
import numpy
import hashlib
import csv
import secrets
from getpass import getpass


# generates a 32 bit prime number for an RSA private key
# from a pre generated txt file of prime numbers
def generate_private():
    data = []
    with open("primes2.txt") as prime_list:
        for i in range(0,500):
            line = prime_list.readline()
            for word in line.split():
                data.append(int(word))
    n = data[randint(0, len(data) -1)]
    return n

# Checks if number is prime. Returns true if it is, and false if it is not.
# source: piyush 
def is_prime(n):
    if n == 2 or n == 3: return True
    if n < 2 or n%2 == 0: return False
    if n < 9: return True
    if n%3 == 0: return False
    r = int(n**0.5)
    # since all primes > 3 are of the form 6n ± 1
    # start with f=5 (which is prime)
    # and test f, f+2 for being prime
    # then loop by 6. 
    f = 5
    while f <= r:
        # print('\t',f)
        if n % f == 0: return False
        if n % (f+2) == 0: return False
        f += 6
    return True

# Returns mod multiplicative inverse of a number using the Euclidean method.
def mod_inverse(a, m):
    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = egcd(b % a, a)
            return (g, x - (b // a) * y, y)
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def generate_e(p, q):
    lamb_n = numpy.lcm(p-1,q-1)
    lower = int(lamb_n / randint(3,6))
    upper = lower + 100
    e = 7
    for i in range (lower, upper):
        if (is_prime(i)):
            e = i 
            break
    return e




def addUser(filename, new_user, pass1, pass2):
    if (pass1 != pass2):
        return -1

    salt = secrets.token_hex(4)
    hash_input = new_user + pass1 + salt
    hash_output = hashlib.sha256(hash_input.encode()).hexdigest()

    # is the username already taken?
    db_row = False
    try:
        with open(filename, newline='') as db:
            csv_reader = csv.reader(db)
            for row in csv_reader:
                if new_user == row[0]: 
                    db_row = row
    except:
        print ("ERROR: Unable to open file ", filename)
        return ""
    if db_row: 
        return -2 # already taken

    # write new info to the file
    data = None
    with open(filename) as db:
        csv_file = csv.reader(db)
        data = list(csv_file)

    data.append([new_user, hash_output, salt])

    with open(filename,"w",newline='') as db:
        csv_file = csv.writer(db)
        for row in data:
            csv_file.writerow(row)

    return new_user

def deleteUser(filename, username):
    db_row = False
    try:
        with open(filename, newline='') as db:
            csv_reader = csv.reader(db)
            for row in csv_reader:
                if username == row[0]: 
                    db_row = row
    except:
        print ("ERROR: Unable to open file ", filename)
        return ""
    if not db_row: 
        return "" # user not found
    
    # 1 copy entire db
    data = None
    with open(filename) as db:
        csv_file = csv.reader(db)
        data = list(csv_file)

    # 2 remove the user 
    for row in data:
        if (row[0] == username):
            data.remove(row)

    # 3 write the new list to the csv file
    with open(filename,"w",newline='') as db:
        csv_file = csv.writer(db)
        for row in data:
            csv_file.writerow(row)
    return username


def login(filename, username, password):
    db_row = False
    try:
        with open(filename, newline='') as db:
            csv_reader = csv.reader(db)
            for row in csv_reader:
                if username == row[0]: db_row = row
    except:
        print ("ERROR: Unable to open file ", filename)
        return -1
    if not db_row: return ""
    salt = db_row[2]
    hash_input = username + password + salt
    hash_password = hashlib.sha256(hash_input.encode()).hexdigest()
    if (db_row[1] == hash_password): return username
    else: return ""

def changePassword(filename, username, password, pass1, pass2):
    # 1 copy entire db
    data = None
    with open(filename) as db:
        csv_file = csv.reader(db)
        data = list(csv_file)


    # 3 verify the current password
    db_row = False
    try:
        with open(filename, newline='') as db:
            csv_reader = csv.reader(db)
            for row in csv_reader:
                if username == row[0]: db_row = row
    except:
        print ("ERROR: Unable to open file ", filename)
        return -1
    if not db_row: return ""
    salt = db_row[2]
    hash_input = username + password + salt
    hash_password = hashlib.sha256(hash_input.encode()).hexdigest()
    # 7 if verification fails return false
    if (db_row[1] != hash_password): return False

    
    # 6 if passwords do not match return false
    if (pass1 != pass2):
        return False

    # 8 generate new salt and generate new hash
    salt = secrets.token_hex(4)
    hash_input = username + pass1 + salt
    hashed_password = hashlib.sha256(hash_input.encode()).hexdigest()

    # 9 replace the hash and salt in the list
    for row in data:
        if (row[0] == username):
            row[1] = hashed_password
            row[2] = salt

    # 10 write list to db file
    with open(filename,"w",newline='') as db:
        csv_file = csv.writer(db)
        for row in data:
            csv_file.writerow(row)

    # 11 return true
    return True

def listAll(filename):
    msg = "\n"
    with open(filename, newline='') as db:
        csv_reader = csv.reader(db)
        for i, row in enumerate(csv_reader):
            msg += (row[0]) + "\n"
        msg += ("Total Users:" + str(i+1))
    return msg