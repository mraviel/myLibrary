import pickle
import socket
import sys
import select
from Database.DatabaseFile import Database
from Bot import bot
import threading
from os import path
from queue import Queue


def send_to_all(sock, message):

    # Message not forwarded to server and sender itself
    try:
        sock.sendall(message)
    except:
        # if connection not available
        sock.close()
        connected_list.remove(sock)


# Find the chromedriver.
Bot_path = path.abspath("Bot")
driver_path = path.join(Bot_path, "chromedriver")


def bot_activate(book_name, user_name, sock_d):
    database = Database()

    while True:
        # Block until get info.
        book = book_name.get()
        username = user_name.get()
        sockd = sock_d.get()
        (i, p) = sockd.getpeername()

        print("Client ({0}) ({1}) Looking for book...".format((i, p), username))

        book_details = bot.find_book(book, driver_path)

        if book_details is None:
            pass
        else:
            database.add_new_book(book_details)
            database.add_book_to_table(book_details[0], username, "WishList")

        print("Client ({0}) ({1}) Send Info".format((i, p), username))
        send_to_all(sockd, pickle.dumps(book_details))


if __name__ == "__main__":

    # List to keep track of socket descriptors
    connected_list = []
    buffer = 4096
    port = 5044

    database = Database()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(10)  # Listen at most 10 connection at one time

    # Add server socket to the list of readable connections
    connected_list.append(server_socket)

    print("\33[32m \t\t\t\tSERVER WORKING \33[0m")
    name = ""

    # Queue's for bot thread.
    book_name_q = Queue()
    username_q = Queue()
    sock_q = Queue()

    while 1:
        # Get the list sockets which are ready to be read through select
        rList, wList, error_sockets = select.select(connected_list, [], [])
        for sock in rList:
            # New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()

                print("Client ({0}, {1}) is Online".format(addr[0], addr[1]))

                # Recv list. Ex: [2, {dictionary}]
                connected_list.append(sockfd)

                # Bot thread, each client has it's own thread.
                x = threading.Thread(target=bot_activate, args=(book_name_q, username_q, sock_q, ))
                x.start()

            # Some incoming message from a client
            else:

                # Data from client
                try:
                    # Handle all recv data

                    data1 = sock.recv(buffer)
                    try:
                        data1 = pickle.loads(data1)
                    except EOFError:
                        continue
                    data = data1

                    # get addr of client sending the message
                    (i, p) = sock.getpeername()
                    if data == "tata":
                        print("Client (%s, %s) is offline (error)" % (i, p), " [", name, "]\n")
                        connected_list.remove(sock)
                        sock.close()
                        continue
                    else:
                        # What to do with the data recv?
                        # print(data)

                        # Insert the data into the database.
                        if data[0] == 1:
                            user = [tuple(data[1][k] for k in ['USERNAME', 'PASSWORD']) for d in data[1]][0]  # (USERNAME, PASSWORD)
                            found = database.login(user)
                            send_to_all(sock, str(found).encode())
                            name = user[0]

                            # Send the wish list books to show in the app.
                            if found:
                                d = {}
                                print("Client ({0}) Login Successfully ({1})".format((i, p), name))
                                d['wish_list'] = database.all_wish_list_books(user)
                                d['books_read'] = database.all_books_read(user)
                                send_to_all(sock, pickle.dumps(d))

                                # Need to send also BooksRead.
                            else:
                                print("Client ({0}) Login Failed".format((i, p)))

                        elif data[0] == 2:
                            user = [tuple(data[1][k] for k in ['USERNAME', 'PASSWORD', 'EMAIL']) for d in data[1]][0]  # (USERNAME, PASSWORD, EMAIL)
                            database.add_user_signup(user)

                        elif data[0] == 3:
                            # Put the values for the Thread.
                            book_name_q.put(data[1][0])
                            username_q.put(data[1][1])
                            sock_q.put(sock)

                        elif data[0] == 4:
                            # Delete book from WishList.
                            book_name = data[1][0]
                            username = data[2]
                            database.delete_book_from_table(book_name, username, "WishList")

                        elif data[0] == 5:
                            # Delete book from BooksRead.
                            book_name = data[1][0]
                            username = data[2]
                            database.delete_book_from_table(book_name, username, "BooksRead")

                        elif data[0] == 6:
                            # Mark book as read.
                            book_name = data[1][0]
                            username = data[2]
                            database.transfer_book(book_name, username, "WishList", "BooksRead")

                        elif data[0] == 7:
                            # Back to wish list.
                            book_name = data[1][0]
                            username = data[2]
                            database.transfer_book(book_name, username, "BooksRead", "WishList")

                        else:
                            pass

                # Abrupt user exit
                except:
                    (i, p) = sock.getpeername()
                    print("Client (%s, %s) is offline (error)" % (i, p), " [", name, "]\n")
                    connected_list.remove(sock)
                    sock.close()
                    continue

    # server_socket.close()
