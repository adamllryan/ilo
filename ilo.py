from hpilo import Ilo, IloCommunicationError
import sys
from dotenv import dotenv_values
from setup import setup
from time import sleep
import logging

TIMEOUT = 15


def power(want_status):
    # Try to get power status and check if valid connection.

    curr_status = "OFF"
    try:
        print("Connecting to iLO. ")
        curr_status = ilo.get_host_power_status()
    except IloCommunicationError:
        print("Could not connect. ")
        sys.exit(1)

    # Cast to string (match output and return value)

    if type(want_status) == bool:
        want_status = "ON" if want_status else "OFF"

    # Press virtual power button if needed

    if not curr_status == want_status:
        ilo.press_pwr_btn()
    else:
        print("System is already {}.".format(want_status.lower()))
        sys.exit(0)

    # run TIMEOUT times

    print()  # newline

    for second in range(1, TIMEOUT):
        # check if status is met

        if ilo.get_host_power_status() == want_status:
            print("Computer has powered {}.".format(want_status.lower()))
            logging.info(want_status)
            sys.exit(0)

        # Log and sleep

        print("\033[FRetry {}/{}.".format(second, TIMEOUT))
        sleep(1)

    # Timeout expired case

    print(
        "Computer did not power {} before timeout {}s was reached".format(
            want_status.lower(), TIMEOUT
        )
    )
    logging.info(curr_status)
    sys.exit(0)


if __name__ == "__main__":
    # ensure only one arg
    if len(sys.argv) != 2:
        print("Usage: python ilostartup.py [on|off]")
        sys.exit(1)
    else:
        config = dotenv_values(".env")
        if len(config) == 0:
            setup()
        ilo = Ilo(config["IP"], config["USER"], config["PASS"])
        if sys.argv[1] == "on" or sys.argv[1] == "off":
            power(sys.argv[1].upper())
        elif sys.argv[1] == "setup":
            setup()
        else:
            print("Usage: python ilostartup.py [on|off]")
            sys.exit(1)
