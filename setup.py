import os
import sys
from getpass import getpass


def setup():
    # check if .env exists, if not create it
    if not os.path.exists(".env"):
        print("Creating .env file. ")
        f = open(".env", "w")
        f.close()

    # prompt user for ip, user, pass
    ip = input("Enter iLO IP address: ")
    user = input("Enter iLO username: ")
    password = getpass("Enter iLO password: ")
    # write to .env
    f = open(".env", "w")
    f.write(f"IP={ip}\nUSER={user}\nPASS={password}\n")
    f.close()
    print("Setup complete. ")
    sys.exit(0)
