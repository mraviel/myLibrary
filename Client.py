import socket
import select
import sys
import pickle
from queue import Queue
import time


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


def main(q, q1):

    # can log to ip via command line argument
    if len(sys.argv) < 2:
        host = input("Enter host ip address: ")
    else:
        host = sys.argv[1]

    port = 5025
    buffer = 4096
    data_to_send = []

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # connecting host
    try:
        s.connect((host, port))
    except:
        print("\33[31m\33[1m Can't connect to the server \33[0m")
        sys.exit()

    while 1:
        socket_list = [sys.stdin, s]

        # Get the list of sockets which are readable
        rList, wList, error_list = select.select(socket_list, [], [], 0)

        display()

        # The data transfer from the kivyApp - Main thread.
        data_transferred = q.get()
        print(data_transferred)

        data_to_send = data_transferred  # The data to send to the server.
        data_to_send = pickle.dumps(data_to_send)  # Change the format to be able to send via network.

        # Send the data - (list).
        s.send(data_to_send)

        # write here all the repeat code (all the input of the program)

        # If log in than recv from the server if the server found the account.
        if data_transferred[0] == 1:
            # print("Try Log In")
            isFound = s.recv(buffer)  # Recv from server if found.
            s.settimeout(2)

            isFound = eval(isFound.decode())  # --> True / False
            q1.put(isFound)  # Transact the info to the kivy app (another thread).
            print(isFound)


if __name__ == "__main__":
    # main(q)
    pass
