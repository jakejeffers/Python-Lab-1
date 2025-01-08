from socket import *
import sys  # In order to terminate the program

# Prepare a server socket
serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 6789
serverSocket.bind(("", serverPort))  # Bind to all interfaces on the specified port
serverSocket.listen(1)  # Listen for incoming connections

print("The server is ready to receive on port", serverPort)

while True:
    print("Ready to serve...")
    connectionSocket, addr = serverSocket.accept()  # Accept incoming connection
    try:
        message = connectionSocket.recv(1024).decode()  # Receive the HTTP request
        if not message:
            continue  # Handle empty message edge case

        print("Message received:", message)

        filename = message.split()[1]  # Get the requested file name
        filepath = filename[1:]  # Remove the leading '/'

        try:
            with open(filepath, "r") as f:
                outputdata = f.read()  # Read the content of the file

            # Send HTTP header line for success
            connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())

            # Send the content of the file
            connectionSocket.send(outputdata.encode())

        except FileNotFoundError:
            # Send response message for file not found
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
            connectionSocket.send("<html><body><h1>404 Not Found</h1></body></html>".encode())

        connectionSocket.close()  # Close the client socket

    except Exception as e:
        print("An error occurred:", e)
        connectionSocket.close()  # Ensure the client socket is closed

serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data
