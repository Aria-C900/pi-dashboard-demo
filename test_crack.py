#purpose: password cracker demo
#first commit: 8/10/2025
#updated: 6/30/2026

import subprocess
import os
import getpass
import time

WORDLIST = "/usr/share/wordlists/rockyou-5k.txt"
SALT = "club123"
PASSFILE = "student_passwd.txt"
TEMPFILE = "temp_passwd.txt"
#EDIT: the program automatically makes these files

def loading_animation(text="Cracking", duration=3):
    print()
    for i in range(duration):
        print(f"\r{text}{'.' * (i % 4)}", end="", flush=True)
        time.sleep(0.6)
    print("\n")

# WELCOME
def run_cracker():
    print("Welcome to the Password Cracker Demo!")
    print("For educational use only. Please don't use real passwords.")
    password = getpass.getpass("Enter a password: ")

# ENTER PASSWORD
    print("\n Hashing your password...")
    hashed_pw = subprocess.check_output(["openssl", "passwd", "-1", "-salt", SALT, password]).decode().strip()
# NOTE: Depending on your version of Johntheripper, you may be able to change the "-1" to different hashes, 
# such as -6 to change to sha512crypt
  
    with open(PASSFILE, "w") as f:
        f.write(f"student:{hashed_pw}\n")

    with open(TEMPFILE, "w") as tf:
        tf.write(f"student:{hashed_pw}\n")
        
    print("Attempting to crack it with a common wordlist...")
    loading_animation("Cracking", 5)

# CRACK (options first, then file; add format for $6$ hashes)
result = subprocess.run(
    ["john", f"--wordlist={WORDLIST}", TEMPFILE],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
    output=subprocess.check_output(["john", "--show", TEMPFILE]).decode()

line = next((ln for ln in output.splitlines() if ln.startswith("student:")), None)
if line:
    cracked_pw = line.split(":", 1)[1]
    print(f"Cracked! Password was: {cracked_pw}")
else:
    print("Too strong! This password wasn’t in the list.")

# clean only the temp file; keep your PASSFILE history
try:
    os.remove(TEMPFILE)
except FileNotFoundError:
    pass

input("\n Press Enter to try another password.")

### end of new
while True:
    run_cracker()
    again = input("\nTry another password? y/n: ").lower()

    if again != "y":
        print("Goodbye!")
        break
