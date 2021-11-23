import socket
from _thread import start_new_thread


class User:
    def __init__(self, connection, chat_id, username):
        self.connection = connection
        self.chat_id = chat_id
        self.username = username

    def __str__(self):
        return f"{self.username} {self.chat_id}"


class Server:
    CLIENTS_IN_QUEUE = 5
    DATA_CLUSTER = 1024
    WELCOME_MESSAGE = "Вы были подключены к серверу. Введи Ваш username: "
    SELECT_CHAT_MESSAGE = "Выберите чат, к которому хотите подключиться или создайте новый, отправив -1\n" \
                          "Список доступных чатов(для выбора отправьте его номер):\n"
    ENTER_CHAT_NAME = "Введи название нового чата: "
    YOU_CONNECTED_MESSAGE = "Вы успешно подключились к чату"
    NO_CHATS_MESSAGE = "Пока что нет ни одного чата. Введите -1, чтобы создать новый"

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(self.CLIENTS_IN_QUEUE)
        self.all_users = []
        self.all_chats = []

    def __start_communicate_with_client(self, connection):
        connection.send(str.encode(self.WELCOME_MESSAGE))
        username = connection.recv(self.DATA_CLUSTER).decode()

        if not self.all_chats:
            select_chat_mes = self.NO_CHATS_MESSAGE
        else:
            select_chat_mes = self.SELECT_CHAT_MESSAGE + "\n".join(self.all_chats)

        connection.send(str.encode(select_chat_mes))
        chat_id = int(connection.recv(self.DATA_CLUSTER).decode())
        if chat_id == -1:
            connection.send(str.encode(self.ENTER_CHAT_NAME))
            chat_name = connection.recv(self.DATA_CLUSTER).decode()
            chat_id = len(self.all_chats)

            self.all_chats.append(f"{chat_id}. {chat_name}")

        user = User(connection, chat_id, username)
        self.all_users.append(user)
        connection.send(str.encode(self.YOU_CONNECTED_MESSAGE))
        return user

    def __communicate_with_client(self, connection):
        current_user = self.__start_communicate_with_client(connection)
        while True:
            data = connection.recv(self.DATA_CLUSTER).decode()
            print(f"[{current_user.username}]:", data)
            if not data:
                continue

            for user in self.all_users:
                if user.chat_id == current_user.chat_id and user.username != current_user.username:
                    user.connection.send(f"[{current_user.username}]: {data}".encode())

    def start(self):
        while True:
            conn, address = self.server_socket.accept()
            start_new_thread(self.__communicate_with_client, (conn, ))


server = Server("localhost", 5555)
server.start()
