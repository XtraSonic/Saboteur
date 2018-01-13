import socket
import SaboteurModel as sm
import threading
import pickle
import time
import os


class Server:
    PORT = 4315

    PLAYER_TEMP_FILE = "Player"
    PLAYER_NAMES_TEMP_FILE = "Player_names"
    BOARD_TEMP_FILE = "Board"
    CARD_TEMP_FILE = "Card"

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
        self.notify_active_player()
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

        # Requests loop
        while not self.model.game_ended:
            command = com_line.recv(64).decode()
            with self.lock:
                if not self.model.turn_index == client_id:
                    print(self.player_names[client_id],client_id, "tried to ", command)
                    com_line.send("NOT YOUR TURN".encode())
                    continue
            assert isinstance(command, str)
            command = command.split(",")
            with self.lock:
                print(self.player_names[client_id], "made this request", command)
                if command[0] == "DISCARD":
                    com_line.send("OK".encode())
                    time.sleep(0.1)
                    hand_index = int(command[1])
                    self.model.play_turn(hand_index, self.model.LOCATION_DISCARD)
                    if len(self.model.players[client_id].hand) == self.model.max_hand_size:
                        self.send_hand_card(self.model.players[client_id].hand[hand_index], client_id)
                    else:
                        self.send_hand_card(None, client_id)
                if self.model.game_ended:  # TODO
                    print("SOMEONE WON", self.model.game_ended)
                self.notify_active_player()

    def notify_active_player(self):
        self.client_sockets[self.model.turn_index].send("YOUR TURN".encode())

    def send_hand_card(self, card, id_to):
        print()
        print("Sending", card, "to", self.player_names[id_to])
        card_file = open(Server.CARD_TEMP_FILE, 'wb')
        pickle.dump(card, card_file)
        card_file.close()
        self.client_sockets[id_to].send(os.stat(card_file.name).st_size.to_bytes(32, 'big'))  # send size
        card_file = open(Server.CARD_TEMP_FILE, "rb")
        self.client_sockets[id_to].sendfile(card_file)
        card_file.close()
        os.remove(self.CARD_TEMP_FILE)

    def remove_client_name(self, client_id):
            print("Connection lost for", client_id)
            with self.lock:
                self.player_names[client_id] = None
                self.client_sockets[client_id] = None
            return


# _s = Server(3)
# _s.end_listening()
# _s.start_game()
