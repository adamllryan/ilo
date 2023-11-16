from hpilo import Ilo
import sys
from dotenv import dotenv_values
from setup import setup


def power_on():
    if ilo.get_host_power_status() == "ON":
        print("Server is already on. ")
        sys.exit(0)
    else:
        print("Booting server. ")
        ilo.press_pwr_btn()


def power_off():
    if ilo.get_host_power_status() == "ON":
        print("Shutting down server. ")
        ilo.press_pwr_btn()
    else:
        print("Server is already off. ")
        sys.exit(0)


if __name__ == "__main__":
    # ensure only one arg
    if len(sys.argv) != 2:
        print("Usage: python ilostartup.py [on|off]")
        sys.exit(1)
    else:
        config = dotenv_values(".env")
        ilo = Ilo(config["IP"], config["USER"], config["PASS"])
        if sys.argv[1] == "on":
            power_on()
        elif sys.argv[1] == "off":
            power_off()
        elif sys.argv[1] == "setup":
            setup()

        else:
            print("Usage: python ilostartup.py [on|off]")
            sys.exit(1)
