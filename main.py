from threading import Thread
from time import sleep

from Client import Dialogue
from Model import GameState, GameMap, GameActions
from Vehicle import VehicleFactory


class Controller:
    def __init__(self, login_data: dict):
        self.idx = None
        self.login_data = login_data
        self.dialogue = Dialogue()
        self.vehicles_list = None
        self.game_state = None
        self.game_actions = None
        self.map = None

    def play(self):
        self.init_game()
# <---------------------- main loop ---------------------
        while not self.game_state.is_finished:
            sleep(0.1)
            self.refresh_game_state()
            if self.game_state.is_finished:
                break
            if self.game_state.current_player_id != self.idx:
                continue
            for vehicle in self.vehicles_list:
                vehicle_turn = vehicle.make_turn(self.game_state, self.map)
                if not (vehicle_turn is None):
                    self.game_state.update_data(vehicle_turn)
                    self.dialogue.send(*vehicle_turn)
            self.dialogue.send("TURN")
# <-------------------- end of main loop ----------------

        print(f"Game ended, winner: {self.game_state.winner}")
        self.dialogue.send("LOGOUT")

    def refresh_game_state(self):
        self.game_state = GameState(self.dialogue.send("GAME_STATE"), self.idx)

    def refresh_game_actions(self):
        self.game_actions = GameActions(self.dialogue.send("ACTIONS"))

    def init_vehicles(self):
        self.vehicles_list = [VehicleFactory.build(our_vehicle) for our_vehicle in self.game_state.our_tanks.items()]

    def init_game(self):
        self.dialogue.start_dialogue()
        login_answer = self.dialogue.send("LOGIN", self.login_data)
        self.idx = login_answer["idx"]
        self.refresh_game_state()
        self.map = GameMap(self.dialogue.send("MAP"))
        self.init_vehicles()


if __name__ == "__main__":
    login_data_1 = {
        "name": "Sorcerer",
        "password": "123",
        "game": "mygame124",
        "num_turns": 45,
        "num_players": 1,
        "is_observer": False
    }
    player_1 = Controller(login_data_1)
    t1 = Thread(target=player_1.play)
    t1.start()

