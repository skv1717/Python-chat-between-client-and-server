import socket
import threading

clients = {}

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
                if username[0] in invalid_characters:
                    raise ValueError("BAD-RQST-BODY")
                if username.strip() in clients:
                    raise ValueError("IN-USE")
                else:
                    clients[username.strip()] = conn
                    conn.send(f"HELLO {username}\n".encode("utf-8"))

            elif msg.startswith("SEND"):
                _, user, message = msg.split(" ", 2)
                mess = msg.split(" ", 2)
                user = mess[1].strip()
                message = mess[2].strip()
                if user in clients:
                    clients[user].send(f"DELIVERY {user} {message}\n".encode("utf-8"))
                    conn.send("SEND-OK\n".encode("utf-8"))
                elif user == "" or message == "":
                    raise ValueError("BAD-RQST-BODY")
                else:
                    raise ValueError("BAD-DEST-USER")

            elif msg.startswith("LIST"):
                users_list = ", ".join(clients.keys())
                conn.send(f"LIST-OK {users_list}\n".encode("utf-8"))

            elif msg.startswith("BYE"):
                _, user = msg.split(" ", 1)
                username = user.strip()
                if username in clients:
                    del clients[username]
                else:
                    raise ValueError("ERROR") 
            else:
                raise ValueError("BAD-RQST-HDR")

        except ValueError as e:
            conn.send(f"{e}\n".encode("utf-8"))
        except Exception as e:
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
            conn.send("BUSY\n".encode("utf-8"))
            conn.close()
        else:
            print(f"New connection from {addr[0]}:{addr[1]}")
            t = threading.Thread(target=client_thread, args=(conn, addr))
            t.start()

if __name__ == "__main__":
    main()
