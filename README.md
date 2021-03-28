# Chat-app

In this project we create a chat program to communicate. There are two scripts for this communication. 
One of them for server, the other one for client. While client send request to join the chat room, server provide a connection to this incoming requests.

The second part is file transfer functionality. When we send a file, we divide the file into small pieces (1000 bytes) and assign a sequence number to each piece. 
Then we send each piece in a single packet. On the receiving end we combine these pieces to reconstruct the file. With TCP we have not any lost packets and packets 
will be received in correct order. We report the upload/download rate(bits/seconds) over time.

Lastly, in our program we have upload, download and cancel button. We also scan the file for safe transfer.

Ahmet Harun Tokyer & Alperen Kağan Kara
