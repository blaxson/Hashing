import bcrypt, os, sys, time
import os
import sys
import time

def main():
    users = get_users()
    crack_user_passwords(users)
    print("All Passwords:")
    for user in users:
        print("User: {0}, Password: {1}".format(user['user'], user['password']))
    #verify_password(users[0], "test")
     
def crack_user_passwords(users):
    from nltk.corpus import words
    wordlist = words.words()
    for user in users:
        start = time.time()
        stop = 0
        for word in wordlist:
            if len(word) >= 6 and len(word) <= 10:
                if verify_password(user, word):
                    stop = time.time()
                    break
        if stop == 0:
            print("password not found")
        else:
            print("took {} seconds".format(stop-start))
        print("{0}'s password: {1}".format(user['user'], user['password']))

""" returns true if password is correct, false otherwise;
    if password is correct, updates user["password"] """
def verify_password(user, word):
    salt = "${0}${1}${2}".format(user['prefix'], user['wf'], user['salt'])
    correct_hash = salt + user['hash_val']
    salt = bytes(salt, 'utf-8')
    correct_hash = bytes(correct_hash, 'utf-8')
    hashed = bcrypt.hashpw(bytes(word, 'utf-8'), salt)
    if hashed == correct_hash:
        user['password'] = word
        print("{0}'s password: {1}".format(user['user'], word))
        return True
    else:
        return False

""" returns a list of json users """
def get_users():
    file = open("shadow.txt", "r")
    users = []
    for line in file:
        user = get_user_data(line)
        users.append(user)
        line = file.readline()
    file.close()
    return users

""" Takes a line from the file and builds a user json """
def get_user_data(line):
    username = ""
    algorithm = ""
    workfactor = 0
    salt = ""
    hash_val = ""
    line = line.split(":")
    
    username = line[0]
    line = line[1].split("$")
    line = line[1:]
    algorithm = line[0]
    workfactor = line[1]
    salt = line[2][:22]
    hash_val = line[2][22:]
    user = {
        "user" : username,
        "prefix" : algorithm,
        "wf" : workfactor,
        "salt" : salt,
        "hash_val" : hash_val.strip('\n'),
        "password" : "",
    }
    return user

if __name__ == "__main__":
    main()
