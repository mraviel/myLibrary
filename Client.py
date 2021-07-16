import socket
import select
import sys
import pickle
from kivyApp import LibraryApp, SignupWindow


# Helper function (formatting)
def display():
    you = "\33[33m\33[1m"+" You: "+"\33[0m"
    sys.stdout.write(you)
    sys.stdout.flush()


def sign_up():
    d = {}
    print("\33[34m\33[1m\n SIGN UP: \33[0m")
    d["USERNAME"] = input("\33[34m\33[1m Username: \33[0m")
    d["PASSWORD"] = input("\33[34m\33[1m Password: \33[0m")
    d["VALID_PASSWORD"] = input("\33[34m\33[1m Valid password: \33[0m")
    return d


def log_in():
    d = {}
    print("\33[34m\33[1m\n LOGIN: \33[0m")
    d["USERNAME"] = input("\33[34m\33[1m Username: \33[0m")
    d["PASSWORD"] = input("\33[34m\33[1m Password: \33[0m")
    return d


def main():

    # can log to ip via command line argument
    if len(sys.argv) < 2:
        host = input("Enter host ip address: ")
    else:
        host = sys.argv[1]

    port = 5021
    buffer = 4096
    data_to_send = []

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # Start here the kivy application:
    LibraryApp().run()
    print(SignupWindow().signup())

    # connecting host
    try:
        s.connect((host, port))
    except:
        print("\33[31m\33[1m Can't connect to the server \33[0m")
        sys.exit()

    while True:
        try:
            choice = int(input("\33[34m\33[1m\n Hallo, press\n 1: LOGIN\n 2: SIGNUP  \33[0m"))
            if choice == 1:  # LOGIN.
                data_to_send.append(choice)
                data_to_send.append(log_in())
                break
            elif choice == 2:  # SIGNUP.
                data_to_send.append(choice)
                data_to_send.append(sign_up())
                if data_to_send[1]["VALID_PASSWORD"] == data_to_send[1]["PASSWORD"]:  # Valid password
                    del data_to_send[1]["VALID_PASSWORD"]  # Send the data without valid password
                    break
                else:
                    data_to_send = []  # Reset the data to send.
                    print("Valid password is not equal to password ")

            # Incorrect input, Try again.
            else:
                print("Only number: 1 or 2")
        except ValueError as e:
            print("Only number: 1 or 2 ", e)

    data_to_send = pickle.dumps(data_to_send)
    s.send(data_to_send)
    display()
    while 1:
        socket_list = [sys.stdin, s]

        # Get the list of sockets which are readable
        rList, wList, error_list = select.select(socket_list, [], [])

        for sock in rList:
            # incoming message from server (recv data)
            if sock == s:
                data = sock.recv(buffer).decode()
                if not data:
                    print('\33[31m\33[1m \rDISCONNECTED!!\n \33[0m')
                    sys.exit()
                else:
                    sys.stdout.write(data)
                    display()

            # user entered a message (send data)
            else:
                display()
                msg = sys.stdin.readline()
                s.send(msg.encode())
                # write here all the repeat code (all the input of the program)


if __name__ == "__main__":
    main()
