#!/usr/bin/env python
import socket
import select
import sys
from threading import * 
from _thread import start_new_thread

def main():
    __server__ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    __server__.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    if len(sys.argv) != 3:
        print("Correct usage ===> $script,  $ip addresses, $port number")
        exit(0)
    else:
        return

    __ip_addresses__ = str(sys.argv[1])
    __port__ = int(sys.argv[2])
    __server__.bind((__ip_addresses__, __port__))
    __server__.listen(100) #Listen for 100 active connections
    __lists_of_clients = []

    def __client_thread(__connections, __address):
        __connections.send("This is a sample of chat room $localhost")
        while True:
            try:
                __message__ = __connections.recv(2048)
                if __message__:
                    print("{" + __address[0] + "}" + __message__)
                    __message__to__be__send = "{" + __address[0] + "}" + __message__
                    __broadcast(__message__to__be__send, __connections)
                else:
                    remove(__connections)
            except:
                continue
    
    def remove(connection):
        if(connection) in __lists_of_clients:
            __lists_of_clients.remove(connection)
    
    def __broadcast(message, connection):
        for clients in __lists_of_clients:
            if clients != connection:
                try:
                    clients.send(message)
                except:
                    clients.close()
                    remove(clients)
    
    while True:
        __connections, __address = __server__.accept()
        __lists_of_clients.append(__connections)
        print(__address[0] + "Connected.")
        start_new_thread(__client_thread, (__connections, __address))
    
    __connections.close()
    __server__.close()

if __name__ == "__main__":
    main()