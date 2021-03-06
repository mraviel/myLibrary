import queue
import socket
import select
import sys
import pickle
from queue import Queue
import time
import threading


# Helper function (formatting)
def display():
    you = "\33[33m\33[1m"+" You: "+"\33[0m"
    sys.stdout.write(you)
    sys.stdout.flush()


def main(q, q1, q2, q3, q5):

    # Can log to ip via command line argument.
    if len(sys.argv) < 2:
        host = input("Enter host ip address: ")
    else:
        host = sys.argv[1]

    port = 5044
    buffer = 4096
    data_to_send = []
    username = str()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # connecting host
    try:
        s.connect((host, port))
    except:
        print("\33[31m\33[1m Can't connect to the server \33[0m")
        sys.exit()

    while 1:
        # socket_list = [sys.stdin, s]  -- before.
        socket_list = [s]

        # Get the list of sockets which are readable
        rList, wList, error_list = select.select(socket_list, [], [], 1)

        print(rList)
        for sock in rList:
            if sock == s:
                print("Data accepted")
                data = s.recv(buffer)
                q3.put(pickle.loads(data))
            else:
                pass

        display()

        # Data from kivy app.
        try:
            data_transferred = q.get_nowait()
            data_transferred.append(username)
        except queue.Empty:
            data_transferred = [0, []]

        data_to_send = pickle.dumps(data_transferred)  # Change to binary.

        # Send to server - (list).
        s.send(data_to_send)

        # Login
        if data_transferred[0] == 1:
            isFound = s.recv(buffer)  # Recv if found.
            s.settimeout(2)

            # Send data to kivy app.
            print(isFound)
            isFound = eval(isFound.decode())  # True / False
            q1.put(isFound)

            # Recv all books in WishList.
            if isFound:
                username = data_transferred[1]["USERNAME"]
                books = b''
                while True:
                    data_recv = s.recv(buffer)
                    books += data_recv
                    if len(data_recv) < buffer:
                        break

                # Send data to kivy app. [(), (), ...]
                books = pickle.loads(books)

                q2.put(books['wish_list'])
                q5.put(books['books_read'])


if __name__ == "__main__":
    pass
