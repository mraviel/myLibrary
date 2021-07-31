import pickle
import socket
import sys
import select
from Database.DatabaseFile import Database


if __name__ == "__main__":

    # List to keep track of socket descriptors
    connected_list = []
    buffer = 4096
    port = 5021

    database = Database()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind(("localhost", port))
    server_socket.listen(10)  # Listen at most 10 connection at one time

    # Add server socket to the list of readable connections
    connected_list.append(server_socket)

    print("\33[32m \t\t\t\tSERVER WORKING \33[0m")
    name = ""

    while 1:
        # Get the list sockets which are ready to be read through select
        rList, wList, error_sockets = select.select(connected_list, [], [])
        for sock in rList:
            # New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()

                print("GOOD")
                """
                # Recv list. Ex: [2, {dictionary}]
                data_recv = sockfd.recv(4096)
                try:
                    data_recv = pickle.loads(data_recv)
                except EOFError:
                    continue
                print(data_recv)

                a = [tuple(data_recv[1][k] for k in ['USERNAME', 'PASSWORD', 'EMAIL']) for d in data_recv[1]][0]  # (USERNAME, PASSWORD)
                if data_recv[0] == 1:
                    database.login(a)
                elif data_recv[0] == 2:
                    database.add_user_signup(a)
                else:
                    pass
                """
                connected_list.append(sockfd)

            # Some incoming message from a client
            else:

                # Data from client
                try:
                    # Handle all the recv code

                    data1 = sock.recv(buffer)
                    try:
                        data1 = pickle.loads(data1)
                    except EOFError:
                        continue
                    data = data1
                    # print "sock is: ",sock
                    # data = data1[:data1.index("\n")]
                    # print "\n data received: ",data

                    # get addr of client sending the message
                    (i, p) = sock.getpeername()
                    if data == "tata":
                        print("Client (%s, %s) is offline (error)" % (i, p), " [", name, "]\n")
                        connected_list.remove(sock)
                        sock.close()
                        continue
                    else:
                        # What to do with the data recv?
                        print(data)  # Write the data on the screen.

                        # Insert the data into the database.
                        a = [tuple(data[1][k] for k in ['USERNAME', 'PASSWORD', 'EMAIL']) for d in data[1]][0]  # (USERNAME, PASSWORD, EMAIL)
                        if data[0] == 1:
                            database.login(a)
                        elif data[0] == 2:
                            database.add_user_signup(a)
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
