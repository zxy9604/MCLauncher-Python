import threading
import time
import socket
import json
import sys
import os
import datetime

port = 7777
mutex = threading.Lock()
server_name = "SyncMods"
modpath = "."

expires = datetime.timedelta(days=1)

class Req(threading.Thread):
    def __init__(self, sock):
        #Status: ON : 0, OFF : 1, BOOM : 2
        threading.Thread.__init__(self)
        self.client = sock                          #set socket for communication
    def run(self):
        if mutex.acquire(1):                        #thread lock
            print("\n--------------------------------------------------------------")
            print("Thread is created. Now connection start...")
            GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
            content = json.dumps(os.listdir(modpath)).encode()
            print("Request Header:")
            print(self.client.recv(1024).decode())
            now = datetime.datetime.utcnow()
            response = '''HTTP/1.1 200 OK
            Server: %s
            Date: %s
            Expires: %s
            Content-Type: text/html
            Content-Length: %s
            Connection: keep-alive\n
            %s''' % (
            server_name,
            now.strftime(GMT_FORMAT),
            (now + expires).strftime(GMT_FORMAT),
            len(content),
            content
            )
            self.client.send(response)
            self.client.close()                         #close the socket for changing a status
            print("Exiting...")
            print("--------------------------------------------------------------\n")
            mutex.release()



def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', port)) #port
    server.listen(5) #backlog
    print("Server Start...\n")
    while True:
        client, name = server.accept()
        Req(client).start()
    server.close()


if __name__ == "__main__":
    main()
