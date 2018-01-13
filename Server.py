import socket
import SaboteurModel as sm
import threading
import pickle
import os


class Server:
    PORT = 4315

    PLAYER_TEMP_FILE = "Player"
    PLAYER_NAMES_TEMP_FILE = "Player_names"
    BOARD_TEMP_FILE = "Board"

    def __init__(self, nr_of_players):
        self.lock = threading.Lock()

        self.player_names = [None for _ in range(sm.Model.MAX_PLAYERS)]
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(socket.gethostname())
        self.server_socket.bind((socket.gethostname(), Server.PORT))
        self.server_socket.listen(10)
        self.nr_of_players = nr_of_players
        self.client_sockets = [None for _ in range(self.nr_of_players)]
        """:type client_sockets: list[socket.SocketType]"""
        self.wait_for_players()

        while None in self.player_names:
            self.player_names.remove(None)

        self.model = sm.Model(self.player_names)
        print("Model Created")

    def start_game(self):
        print("Starting game")
        # pickle names
        player_names_file = open(Server.PLAYER_NAMES_TEMP_FILE, 'wb')
        pickle.dump(self.model.player_names, player_names_file)
        player_names_file.close()

        # pickle board
        board_file = open(Server.BOARD_TEMP_FILE, 'wb')
        pickle.dump(self.model.board, board_file)
        board_file.close()

        for index in range(len(self.client_sockets)):
            client_socket = self.client_sockets[index]
            # server is ready
            client_socket.send("START".encode())

            # send player object
            player_file = open(Server.PLAYER_TEMP_FILE + str(index), 'wb')
            pickle.dump(self.model.players[index], player_file)
            player_file.close()
            client_socket.send(os.stat(player_file.name).st_size.to_bytes(32, 'big'))  # send size
            player_file = open(Server.PLAYER_TEMP_FILE + str(index), "rb")
            client_socket.sendfile(player_file)
            player_file.close()

            # send player names
            client_socket.send(os.stat(player_names_file.name).st_size.to_bytes(32, 'big'))  # send size
            player_names_file = open(Server.PLAYER_NAMES_TEMP_FILE, "rb")
            client_socket.sendfile(player_names_file)
            player_names_file.close()

            # send board
            client_socket.send(os.stat(board_file.name).st_size.to_bytes(32, 'big'))  # send size
            board_file = open(Server.BOARD_TEMP_FILE, "rb")
            client_socket.sendfile(board_file)
            board_file.close()

            # cleanup
            os.remove(Server.PLAYER_TEMP_FILE + str(index))

        # cleanup
        os.remove(Server.PLAYER_NAMES_TEMP_FILE)
        os.remove(Server.BOARD_TEMP_FILE)

        print("Done Sending")
        while threading.active_count() - 1:
            pass

    def end_listening(self):
        self.server_socket.close()

    def end_game(self):
        for client_socket in self.client_sockets:
            client_socket.send("END".encode())
            client_socket.close()

    def wait_for_players(self):
        enough_players = False
        while not enough_players:
            # accept connections from outside
            (client_socket, address) = self.server_socket.accept()
            name = client_socket.recv(64).decode()
            if name == 0:
                continue
            client_id = self.get_first_available_index(name)
            with self.lock:
                self.player_names[client_id] = name
                self.client_sockets[client_id] = client_socket
            print(name, "connected with id", client_id)
            t = threading.Thread(target=self.client_handler, args=(client_socket, client_id))
            t.daemon = True
            t.start()

            if threading.active_count() - 1 == self.nr_of_players:
                enough_players = True

    def get_first_available_index(self, name):
        i = 0
        with self.lock:
            while self.player_names[i] is not None:
                i += 1
        return i

    def client_handler(self, com_line, client_id):
        assert isinstance(com_line, socket.SocketType)
        try:
            # wait for the client to be set up
            while True:
                ready = com_line.recv(5)
                if not ready:
                    self.remove_client_name(client_id)
                    com_line.close()
                    return
                elif ready.decode() == "READY":
                    break
                else:
                    print(client_id, "sent an unknown message:", ready.decode())

        except socket.error:
            self.remove_client_name(client_id)
            com_line.close()
            return

        print("GAME STARTED FOR ", client_id)

    def remove_client_name(self, client_id):
            print("Connection lost for", client_id)
            with self.lock:
                self.player_names[client_id] = None
                self.client_sockets[client_id] = None
            return


s = Server(3)
s.end_listening()
s.start_game()
