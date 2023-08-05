from re import findall
from subprocess import Popen, PIPE, CREATE_NO_WINDOW, check_output
import time
import datetime
import socket


def ping(host, ping_count):
    # Get name of system
    system = socket.gethostname()

    # Get name of wifi

    network = input("What is the name of the network you want to "
                      "keep record of?\n"
                    "'SpectrumSetup-66'? [Y/n] ")
    if network == "" or network.capitalize() == "Y":
        network = "SpectrumSetup-66"
    else:
        network = input("Please specify the name of the network:\n")

    OS = input("Is system a Windows OS? [Y/n] ")
    if OS == "" or OS[0].capitalize() == "Y":
        OS = "-n"
    elif OS[0].capitalize() == "N":
        OS = "-c"
    else:
        print("Improper response")
        return "Ending program"

    # seconds = int(input("How often should the ping be performed? ("
    #                     "in seconds)\n"))
    seconds = 60  # Set timer to loop every 60 seconds

    # Minute counter
    minutes_counter = 0

    # if input == ""
    default_timer = 2628000  # Default timer is 5 years
    timer = input("How many min would you like it to run? "
                      "Press enter for 5 years. Otherwise enter the "
                      "number of minutes.\n")
    if timer == "":  # If they hit enter, use the 5-year timer
        timer = default_timer
    else:
        timer = int(timer)

    pass_counter = 0

    # Set the length of time to run the test
    while minutes_counter < timer:
        for ip in host:
            data = ""
            output = Popen(f"ping {ip} {OS} {ping_count}",
                            stdout=PIPE, creationflags=CREATE_NO_WINDOW,
                           encoding="utf-8")

            for line in output.stdout:
                data = data + line
                ping_test = findall("TTL", data)

            if ping_test:
                result = f"{system} - {ip} - Successful Ping " \
                          f"{datetime.datetime.now()}"
            else:
                result = f"{system} - {ip} - Failed Ping {datetime.datetime.now()}"

        # Set frequency of ping test, based on the input
        if timer > 1:
            time.sleep(seconds)

        minutes_counter += 1

        # with open(r"C:\Users\ftbbo\OneDrive\Development\Python_dev"
        #           "\Surface_Pro_8\Ping\ping_log.txt", 'w') as f:
        #     f.write(r"C:\Users\ftbbo\OneDrive\Development\Python_dev"
        #             r"\Surface_Pro_8\Ping\ping_log.txt")

        print(result)

        # If the internet is down, and has not already been recorded
        # as being down, record the event. If it has been recorded as
        # being down, skip logging anything further until a change.
        # If the internet comes back up, record it's back up for the
        # first change of circumstances. After that, don't record
        # anything further until a change of circumstances.
        is_up = False
        is_down = False
        if "Failed" in result:
            if is_down == False:
                with open('Workbook_ping_log.txt', 'a') as f:
                    f.write(f"{network} : {result}")
                    f.write("\n")
                pass_counter = 0  # Reset pass_counter if ping failed
                is_down = True
                is_up = False
        else:
            if is_up == False:
                with open('Workbook_ping_log.txt', 'a') as f:
                    f.write(f"{network} : {result}")
                    f.write("\n")
                is_up = True
                is_down = False


            # # Every time it passes, (about every min) it'll
            # increment - This has been commented out bc of
            # establishing change-of-state logic above.
            # pass_counter += 1
            # print("Pass")

        # # Every interval it's successful, record that it's still up
        # interval = 15
        # if pass_counter == 1 or pass_counter % interval == 0:
        #     with open('Workbook_ping_log.txt', 'a') as f:
        #         f.write(f"Update {network} : {result}")
        #         f.write("\n")


nodes = ["8.8.8.8", "20.20.20.50", "facebook.com", "192.168.1.20"]
google = ["8.8.8.8"]

ping(google, 3)
