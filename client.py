import socket
from threading import Thread


class Client:
    DATA_CLUSTER = 1024

    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

        self.__start_chat()

    def __start_chat(self):
        self.__get_server_answer()
        username = input()
        self.client_socket.send(str.encode(username))

        self.__get_server_answer()
        chat_id = input()
        self.client_socket.send(str.encode(chat_id))

        if chat_id == "-1":
            self.__get_server_answer()
            chat_name = input()
            self.client_socket.send(str.encode(chat_name))

        self.__get_server_answer()

        self.__start()

    def __get_server_answer(self):
        server_message = self.client_socket.recv(self.DATA_CLUSTER).decode()
        print(server_message)

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
            self.__get_server_answer()


client = Client("localhost", 5555)
