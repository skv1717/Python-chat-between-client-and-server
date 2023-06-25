import socket
import threading

clients = {}
# clients = []

def client_thread(conn, addr):
    username = None
    while True:
        try:
            msg = ""
            while True:
                mess = conn.recv(1).decode("utf-8")            
                msg += mess
                if mess == '\n':
                    break
            msg.strip()
            print(msg)
            if msg.startswith("HELLO-FROM"):
                username = msg.split(" ")[1]
                invalid_characters ={'!', '@', '#', '\n', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '[', ']', '{', '}', ';', ':', '"', '<', ',', '.', '>', '/', '?', '|'}
                # print(list(clients.keys()))
                # print(username)

                if username[0] in invalid_characters:
                    string_bytes = "BAD-RQST-BODY\n".encode("utf-8")
                    bytes_len = len(string_bytes)
                    num_bytes_to_send = bytes_len
                    while num_bytes_to_send > 0:
                        num_bytes_to_send -= conn.send(string_bytes[bytes_len-num_bytes_to_send:])
                # print(f"username: {username}, list: {list(clients.keys())}")
                if username.strip() in list(clients.keys()):
                    string_bytes = f"IN-USE\n".encode("utf-8")
                    bytes_len = len(string_bytes)
                    num_bytes_to_send = bytes_len
                    while num_bytes_to_send > 0:
                        num_bytes_to_send -= conn.send(string_bytes[bytes_len-num_bytes_to_send:])
                else:
                    clients[username.strip()] = conn
                    string_bytes = f"HELLO {username}\n".encode("utf-8")
                    bytes_len = len(string_bytes)
                    num_bytes_to_send = bytes_len
                    while num_bytes_to_send > 0:
                        num_bytes_to_send -= conn.send(string_bytes[bytes_len-num_bytes_to_send:])

            elif msg.startswith("SEND"):
                _, user, message = msg.split(" ", 2)
                mess = msg.split(" ", 2)
                user = mess[1].strip()
                message = mess[2].strip()
                if user in clients:
                    string_bytes = f"DELIVERY {user} {message}\n".encode("utf-8")
                    bytes_len = len(string_bytes)
                    num_bytes_to_send = bytes_len
                    while num_bytes_to_send > 0:
                        num_bytes_to_send -= clients[user].send(string_bytes[bytes_len-num_bytes_to_send:])

                    string_bytes = f"SEND-OK\n".encode("utf-8")
                    bytes_len = len(string_bytes)
                    num_bytes_to_send = bytes_len
                    while num_bytes_to_send > 0:
                        num_bytes_to_send -= conn.send(string_bytes[bytes_len-num_bytes_to_send:])
                
                elif user == "" or message == "":
                    string_bytes = "BAD-RQST-BODY\n".encode("utf-8")
                    bytes_len = len(string_bytes)
                    num_bytes_to_send = bytes_len
                    while num_bytes_to_send > 0:
                        num_bytes_to_send -= conn.send(string_bytes[bytes_len-num_bytes_to_send:])
                else:
                    string_bytes = f"BAD-DEST-USER\n".encode("utf-8")
                    bytes_len = len(string_bytes)
                    num_bytes_to_send = bytes_len
                    while num_bytes_to_send > 0:
                        num_bytes_to_send -= conn.send(string_bytes[bytes_len-num_bytes_to_send:])

            elif msg.startswith("LIST"):
                users_list = ""
                for element in clients.keys():
                    users_list += element.strip() + ", " 
                string_bytes = f"LIST-OK {users_list}\n".encode("utf-8")
                bytes_len = len(string_bytes)
                num_bytes_to_send = bytes_len
                while num_bytes_to_send > 0:
                    num_bytes_to_send -= conn.send(string_bytes[bytes_len-num_bytes_to_send:])
            elif msg.startswith("ADIOS"):
                print("AAAAAAAAAAAAAAAAAAAAAA")
                _, user = msg.split(" ", 1)
                print(f"user: {user} aaaaaa")
                username = user.strip()
                print(f"{username}, aaa")
                if username in clients:
                    del clients[username]
                    print(f"LISTA TERAZ: {list(clients.keys())}")
                else:
                    print(f"CHUJ: {username}, lista: {list(clients.keys())}")
            else:
                string_bytes = f"BAD-RQST-HDR\n".encode("utf-8")
                bytes_len = len(string_bytes)
                num_bytes_to_send = bytes_len
                while num_bytes_to_send > 0:
                    num_bytes_to_send -= conn.send(string_bytes[bytes_len-num_bytes_to_send:])

        except:
            if username in clients:
                del clients[username]
            conn.close()
            break

def main():
    server_address = ("0.0.0.0", 2185)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(server_address)
    server_socket.listen(64)
    print(f"Chat server started on {server_address[0]}:{server_address[1]}")
    
    while True:
        conn, addr = server_socket.accept()
        if len(clients) >= 64:
            string_bytes = f"BUSY\n".encode("utf-8")
            bytes_len = len(string_bytes)
            num_bytes_to_send = bytes_len
            while num_bytes_to_send > 0:
                num_bytes_to_send -= conn.send(string_bytes[bytes_len-num_bytes_to_send:])

            conn.close()
        else:
            print(f"New connection from {addr[0]}:{addr[1]}")

            t = threading.Thread(target=client_thread, args=(conn, addr))
            t.start()

if __name__ == "__main__":
    main()