# Python Chat between client and server
 Based on two separated programs: Chat client and Chat server
 
 These programs utilize Python programming language, socket programming, and the Transmission Control Protocol (TCP) to develop a straightforward chat application that enables users to communicate by sending messages to each other.


# Chat Client 

The chat client allows users to connect to the chat server and exchange messages with other users. It provides a user-friendly text-based interface for chatting.

# Features

<br / 1.Connects to the chat server and lets the user log in using a unique name.>
<br / 2.Asks for another name if the chosen name is already taken.>
<br / 3.Lets the user shutdown the client by typing !quit.>
<br / 4.Lets the user list all currently logged-in users by typing !who.>
<br / 5.Lets the user send messages to other users by typing @username message.>
<br / 6.Receives messages from other users and displays them to the user.>

# Usage


To run the chat client, execute the following command:

python client.py <server_address> <server_port>
Replace <server_address> and <server_port> with the appropriate values for your chat server.

Chat Server (server.py) The chat server connects multiple clients and forwards messages between them using the same chat protocol as the client.

Supports at least 64 simultaneous clients. Usage To run the chat server, execute the following command:

python server.py <server_port>
Replace <server_port> with the desired port for your chat server.