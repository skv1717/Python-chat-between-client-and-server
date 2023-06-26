import socket
import threading
import os

def receive_messages(sock):

    while True:
        message = ""
        try:
            while True:
                mess = sock.recv(1).decode("utf-8")           
                message += mess
                if mess == '\n':
                    break
           
            if message.startswith("DELIVERY"):
                _, user, msg = message.split(" ", 2)
                print(f"{user}: {msg}")
            elif message.startswith("LIST-OK"):
                _, users = message.split(" ", 1)
                print(f"Online users: {users}")
            elif "BAD-DEST-USER" in message:
                print(f"destination user is not currently logged in")
            elif message.startswith("BAD-REQUEST-HDR"):
                print(f"error in the header")
            elif message.startswith("BAD-REQUEST-BODY"):
                print(f"error in the body")

        except:
            print("An error occurred while receiving messages.")
            break

def user_input(sock):
    while True:
        message = input()
        if message == "!quit":
            string_bytes = f"ADIOS {username}\n".encode("utf-8")
            print(string_bytes)
            bytes_len = len(string_bytes)
            num_bytes_to_send = bytes_len
            while num_bytes_to_send > 0:
                num_bytes_to_send -= sock.send(string_bytes[bytes_len-num_bytes_to_send:])

            sock.close()
            os._exit(os.EX_OK)
        elif message == "!who":
            string_bytes = f"LIST\n".encode("utf-8")
            bytes_len = len(string_bytes)
            num_bytes_to_send = bytes_len
            while num_bytes_to_send > 0:
                num_bytes_to_send -= sock.send(string_bytes[bytes_len-num_bytes_to_send:])
        elif message.startswith("@"):
            
            msg = message.split(" ", 1)
            if len(msg) == 2:
                user = msg[0][1:]
                mess = msg[1]
                string_bytes = f"SEND {user} {mess}\n".encode("utf-8")
                bytes_len = len(string_bytes)
                num_bytes_to_send = bytes_len
                while num_bytes_to_send > 0:
                    num_bytes_to_send -= sock.send(string_bytes[bytes_len-num_bytes_to_send:])
            else:
                print("Invalid command.")
        else:
            print("Invalid command.")
    
            

server_address = ("0.0.0.0", 2185) 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server_address)

while True:
    username = input("Enter your username: ")
    string_bytes = f"HELLO-FROM {username}\n".encode("utf-8")
    bytes_len = len(string_bytes)
    num_bytes_to_send = bytes_len
    while num_bytes_to_send > 0:
        num_bytes_to_send -= sock.send(string_bytes[bytes_len-num_bytes_to_send:])

    
    response = ""
    while True:
        mess = sock.recv(1).decode("utf-8")
        response += mess
        if mess == '\n':
            break

    if response.startswith("HELLO"):
        print(f"Logged in as {username}.")
        break
    elif response == "IN-USE\n":
        print("Username is already taken, please try another.")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_address)
    elif response == "BAD-RQST-BODY\n":
        print("Choose a different username without invalid characters")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_address)
    else:
        print("An error occurred, please try again.")

receive_thread = threading.Thread(target=receive_messages, args=(sock,))
receive_thread.start()


user_input(sock)
receive_thread.join()
