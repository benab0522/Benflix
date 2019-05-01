
import socket
import threading
import os
import client_gui
import wx
import cv2


class Client:

    def __init__(self, ip_address, port):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip_address, port))

        self.graphics_folder = ""

    def recv(self):

        threading.Thread(target=client_gui.LoginFrame, args=(self.socket, "")).start()

        while True:
            server_response = self.socket.recv(175428)
            server_response_split = server_response.split()

            if server_response_split[0] == "LOGIN":
                if server_response_split[1] == "OK":
                    threading.Thread(target=client_gui.MainFrame, args=(self.socket,)).start()
                else:
                    print server_response[5:]    # create info window (with gui) with the error
                    threading.Thread(target=client_gui.LoginFrame, args=(self.socket, server_response[5:])).start()

            elif server_response_split[0] == "REGISTER":
                if server_response_split[1] == "1":
                    threading.Thread(target=client_gui.RegisterFrame, args=(self.socket, "")).start()

                elif server_response_split[1] == "OK":
                    threading.Thread(target=client_gui.LoginFrame, args=(self.socket, "")).start()

                else:
                    print server_response[9:]
                    threading.Thread(target=client_gui.RegisterFrame, args=(self.socket, server_response[9:])).start()

            elif server_response_split[0] == "PLAY":
                print "1"


def main():

    client = Client("127.0.0.1", 195)
    threading.Thread(target=client.recv).start()

if __name__ == '__main__':
    main()