
import socket
import threading
import os
import hashlib

class Server:

    def __init__(self, host, port):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.bind((host, port))
        print "Socket binded."
        if not os.path.isfile("data_base.txt"):
            data_base = open("data_base.txt", 'w')
            data_base.close()

        

    def listen(self):
        print "Ready to listen..."
        self.socket.listen(10)

        while True:
            client, address = self.socket.accept()
            print "Client from {} connected.".format(address)
            threading.Thread(target=self.handle_requests, args=(client, address)).start()

    def handle_requests(self, client_socket, address):
        while True:
            client_message = client_socket.recv(1024)

            if client_message:
                client_message_split = client_message.split()

                print client_message_split

                function = client_message_split[0]

                if function == "LOGIN":
                    if len(client_message_split) == 3:
                        username = client_message_split[1]
                        password = client_message_split[2]
                        password = hashlib.sha1(password.encode()).hexdigest()

                        with open("data_base.txt", 'r') as data_base:
                            usernames = get_usernames(data_base)
                        with open("data_base.txt", 'r') as data_base:
                            passwords = get_passwords(data_base)

                        if username not in usernames:
                            client_socket.send("LOGIN LOGIN_ERROR: username doesn't exist")

                        elif username in usernames and password != passwords[usernames.index(username)]:
                            client_socket.send("LOGIN LOGIN_ERROR: password doesn't match to username")

                        elif username in usernames and password == passwords[usernames.index(username)]:
                            client_socket.send("LOGIN OK")

                    else:
                        client_socket.send("LOGIN LOGIN_ERROR: make sure that you fill all the fields")

                elif function == "REGISTER":    # need to check if all data is ok

                    if client_message_split[1] == "0":
                        client_socket.send("REGISTER 1")

                    else:
                        error = ""
                        if len(client_message_split) != 5:
                            error = "REGISTER REGISTER_ERROR: make sure you fill all the fields"

                        client_name = client_message_split[1]
                        if not error and len(client_name) <= 1:
                            error = "REGISTER REGISTER_ERROR: name length can be above two letters"
                        elif " " in client_name:
                            error = "REGSITER REGISTER ERROR: name can't contain space"

                        elif not error and not client_name.isalpha():
                            error = "REGISTER REGISTER_ERROR: name can contain only letters"

                        client_username = client_message_split[2]

                        if not error and len(client_username) < 3:
                            error = "REGISTER REGISTER_ERROR: username length can be above three letters"
                        elif not error and not contains_letters_and_numbers_only(client_username):
                            error = "REGISTER REGISTER_ERROR: username can contain only letters and numbers"
                        elif " " in client_name:
                            error = "REGSITER REGISTER ERROR: username can't contain space"

                        with open("data_base.txt", 'r') as data_base:
                            data = data_base.readlines()
                            for line in data:
                                line_username = line.split()[1]
                                if line_username == client_username.lower():
                                    error = "REGISTER REGISTER_ERROR: username is already exists, try another one"
                                    break

                        client_pass = client_message_split[3]
                        if not error and len(client_pass) < 8:
                            error = "REGISTER REGISTER_ERROR: password length can be above seven letters"
                        elif " " in client_name:
                            error = "REGSITER REGISTER ERROR: password can't contain space"

                        client_confirm_pass = client_message_split[4]
                        if not error and client_confirm_pass != client_pass:
                            error = "REGISTER REGISTER_ERROR: the passwords are not matched"

                        if not error:

                            client_pass = hashlib.sha1(client_pass.encode())
                            client_confirm_pass = hashlib.sha1(client_confirm_pass.encode())

                            data_line = "{} {} {} {}".format(client_name,
                                                             client_username.lower(),
                                                             client_pass.hexdigest(),
                                                             client_confirm_pass.hexdigest())

                            with open("data_base.txt", 'r') as data_base:
                                previous_data = data_base.read()

                            with open("data_base.txt", 'w') as data_base:
                                data_base.write(previous_data + data_line + "\n")

                            data_base.close()

                            client_socket.send("REGISTER OK")

                        else:
                            client_socket.send(error)

              


def get_usernames(data_base):
    usernames = []
    for line in data_base.readlines():
        usernames.append(line.split()[1])
    return usernames


def get_passwords(data_base):
    passwords = []
    for line in data_base.readlines():
        passwords.append(line.split()[2])
    return passwords


def contains_letters_and_numbers_only(str):
    for ch in str:
        if not ch.isalpha() and not ch.isdigit():
            return False
    return True

def main():

    server = Server("0.0.0.0", 195)
    server.listen()


if __name__ == '__main__':
    main()
