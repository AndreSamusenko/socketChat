import socket
from threading import Thread


class Client:
    DATA_CLUSTER = 1024

    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

        self.__start_chat()

    def __start_chat(self):
        server_message = self.client_socket.recv(self.DATA_CLUSTER).decode()
        print(server_message)
        username = input()
        self.client_socket.send(str.encode(username))

        server_message = self.client_socket.recv(self.DATA_CLUSTER).decode()
        print(server_message)
        chat_id = input()
        self.client_socket.send(str.encode(chat_id))

        if chat_id == "-1":
            server_message = self.client_socket.recv(self.DATA_CLUSTER).decode()
            print(server_message)
            chat_name = input()
            self.client_socket.send(str.encode(chat_name))

        server_message = self.client_socket.recv(self.DATA_CLUSTER).decode()
        print(server_message)

        self.__start()

    def __start(self):
        thread1 = Thread(target=self.__receive_messages)
        thread2 = Thread(target=self.__send_messages)

        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()

        self.client_socket.close()

    def __send_messages(self):
        while True:
            message = input()
            if not message:
                break

            self.client_socket.send(str.encode(message))

    def __receive_messages(self):
        while True:
            response = self.client_socket.recv(self.DATA_CLUSTER)
            print(response.decode())


client = Client("localhost", 5555)
