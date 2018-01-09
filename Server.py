import socket
import SaboteurModel as sm
import threading


class Server:
    PORT = 4315

    def __init__(self, nr_of_players):
        self.lock = threading.Lock()

        self.player_names = [None for _ in range(sm.Model.MAX_PLAYERS)]
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(socket.gethostname())
        self.server_socket.bind((socket.gethostname(), Server.PORT))
        self.server_socket.listen(10)
        self.game_started = False
        self.nr_of_players = nr_of_players

    def start(self):
        while not self.game_started:
            # accept connections from outside
            (client_socket, address) = self.server_socket.accept()
            name = client_socket.recv(64).decode()
            if name == 0:
                continue
            client_id = self.get_first_available_index(name)
            print(name, "connected with id", client_id)
            t = threading.Thread(target=self.client_listener, args=(client_socket, client_id))
            t.daemon = True
            t.start()

            if threading.active_count() - 1 == self.nr_of_players:
                self.game_started = True

        while None in self.player_names:
            self.player_names.remove(None)

        self.model = sm.Model(self.player_names)
        # todo
        print("ALL GOOD YOU BASTARTD ;)")
        self.server_socket.close()

    def get_first_available_index(self, name):
        i = 0
        with self.lock:
            while self.player_names[i] is not None:
                i += 1
            self.player_names[i] = name

        return i

    def client_listener(self, com_line, client_id):
        assert isinstance(com_line, socket.SocketType)
        ready = com_line.recv(1)
        if ready == 0:
            with self.lock:
                self.player_names[client_id] = None
            return

        print("GAME STARTED FOR ", client_id)

# s = Server(3)
# s.start()
