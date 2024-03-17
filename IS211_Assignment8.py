import random
import time
import argparse

class Die:
    def roll(self):
        return random.randint(1, 6)

class Player:
    def __init__(self, name):
        self.name = name
        self.total_score = 0

    def add_to_score(self, points):
        self.total_score += points

    def decide_action(self, current_score):
        raise NotImplementedError("This method should be overridden by subclasses")

class HumanPlayer(Player):
    def decide_action(self, current_score):
        return input(f"{self.name}, you have {current_score} points so far this turn. Roll (r) or Hold (h)? ").lower()

class ComputerPlayer(Player):
    def decide_action(self, current_score):
        threshold = min(25, 100 - self.total_score)
        return "hold" if current_score >= threshold else "roll"

class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type == "computer":
            return ComputerPlayer(name)
        elif player_type == "human":
            return HumanPlayer(name)
        else:
            raise ValueError("Unknown player type")

class PigGame:
    def __init__(self, players):
        self.players = players
        self.die = Die()

    def play_turn(self, player):
        turn_score = 0
        while True:
            action = player.decide_action(turn_score)
            if action == "h":
                print(f"{player.name} holds with {turn_score} points.")
                player.add_to_score(turn_score)
                break
            roll = self.die.roll()
            print(f"{player.name} rolled a {roll}.")
            if roll == 1:
                print("Oh no, a 1 was rolled. No points this turn.")
                break
            turn_score += roll

    def play_game(self):
        print("Welcome to Pig!")
        player_index = 0
        while all(player.total_score < 100 for player in self.players):
            current_player = self.players[player_index]
            print(f"\n{current_player.name}'s turn:")
            self.play_turn(current_player)
            if current_player.total_score >= 100:
                print(f"{current_player.name} wins with {current_player.total_score} points!")
                return
            player_index = (player_index + 1) % len(self.players)
        print("Game over!")

class TimedGameProxy(PigGame):
    def __init__(self, players, time_limit=60):
        super().__init__(players)
        self.time_limit = time_limit
        self.start_time = time.time()

    def play_game(self):
        self.start_time = time.time()
        super().play_game()
        if time.time() - self.start_time >= self.time_limit:
            print("Time's up!")
            winner = max(self.players, key=lambda player: player.total_score)
            print(f"{winner.name} wins with {winner.total_score} points due to time limit!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play Pig game.")
    parser.add_argument("--player1", choices=["human", "computer"], default="human")
    parser.add_argument("--player2", choices=["human", "computer"], default="human")
    parser.add_argument("--timed", action="store_true")
    args = parser.parse_args()

    player1 = PlayerFactory.create_player(args.player1, "Player 1")
    player2 = PlayerFactory.create_player(args.player2, "Player 2")
    players = [player1, player2]

    if args.timed:
        game = TimedGameProxy(players)
    else:
        game = PigGame(players)

    game.play_game()
