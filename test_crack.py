#purpose: password cracker demo
#first commit: 8/10/2025
#updated: 8/10/2025

import subprocess
import os
import getpass
import time

WORDLIST = "/usr/share/wordlists/rockyou.txt"
SALT = "club123"
PASSFILE = "student_passwd.txt"

def loading_animation(text="Cracking", duration=3):
    print()
    for i in range(duration):
        print(f"\r{text}{'.' * (i % 4)}", end="", flush=True)
        time.sleep(0.6)
    print("\n")

def run_cracker():
    print("🔐 Welcome to the Password Cracker Demo!")
    print("⚠️  For education only. Please don't use real passwords.")
    password = getpass.getpass("Enter a test password: ")

    print("\n📡 Hashing your password...")
    hashed_pw = subprocess.check_output(["openssl", "passwd", "-6", "-salt", SALT, password]).decode().strip()

    with open(PASSFILE, "w") as f:
        f.write(f"student:{hashed_pw}\n")

    print("⚙️ Attempting to crack it with a common wordlist...")
    loading_animation("Cracking", 5)

    subprocess.run(["john", PASSFILE, f"--wordlist={WORDLIST}"], stdout=subprocess.DEVNULL)

    output = subprocess.check_output(["john", "--show", PASSFILE]).decode()

    print("\n📊 Result:")
    if "student:" in output:
        cracked_pw = output.strip().split(":")[1]
        print(f"✅ Cracked! Password was: {cracked_pw}")
    else:
        print("❌ Too strong! This password wasn’t in the list.")

    os.remove(PASSFILE)
    print("\n🔁 Press Enter to try another password or Ctrl+C to exit.")
    input()

while True:
    run_cracker()
