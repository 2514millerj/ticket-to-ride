# this version no longer takes input from user.
# Designed for computer OR human player (mainly comp v comp sim)

# All values and methods associated with the Original Ticket to Ride board game
from TTRGame import Game
import collections
import pprint
import argparse

def playTTR(num_ai, num_human, ai_strategies):
    # before first turn, select 1, 2 or 3 destination tickets

    if len(ai_strategies) != num_ai:
        print("ERROR: Number of AI do not match number of AI strategies")
        exit()

    print("\n Welcome to Ticket to Ride! \n")
    print("Version 0.2 -- One Human vs One AI Player")

    game = Game(numAIPlayers=num_ai, numHumanPlayers=num_human, aiStrategies=ai_strategies)

    game.initialize()

    player = game.players[game.posToMove]

    # main game loop
    while True:
        print("\n_________________NEW PLAYER'S TURN_________________ \n")
        print("It's your turn " + str(player.getName()) + "! ")

        if player.type == 'Human':
            game.playHumanTurn(player)
        elif player.type == 'AI':
            game.playAITurn(player)

        # condition to break out of loop
        if game.checkEndingCondition(player):
            game.advanceOnePlayer()
            player = game.getCurrentPlayer()
            break
        game.advanceOnePlayer()
        player = game.getCurrentPlayer()

    print("\n This is the last round!  Everyone has one more turn! \n")

    for i in range(len(game.players)):
        print("\n_________________NEW PLAYER'S TURN_________________ \n")
        print("This is your LAST TURN " + str(player.getName()) + "! ")
        if player.type == 'Human':
            game.playHumanTurn(player)
        elif player.type == 'AI':
            game.playAITurn(player)
        game.advanceOnePlayer()
        player = game.getCurrentPlayer()

    for player in game.players:
        game.scorePlayerTickets(player)

    game.scoreLongestPath()

    scores = []
    for player in game.players:
        print(str(player.getName())
              + " had "
              + str(player.getPoints())
              + " points!"
              )
        score = player.getPoints()
        scores.append(score)

    winners = [x.getName() for x in game.players
               if x.getPoints() == max(scores)]

    if len(winners) == 1:
        print("The winner is " + str(winners[0]))
    else:
        print("The winners are " + ' and '.join(winners))

    print
    "\n =========== Data =========== \n"

    game.printAllPlayerData()

    print
    "\n =========== fin =========== \n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MCTS research code')
    parser.add_argument('--num_ai', action="store", required=True, type=int)
    parser.add_argument('--num_human', action="store", required=True, type=int)
    parser.add_argument('--ai_strategies', action="store", required=True, type=str)
    args = parser.parse_args()

    playTTR(args.num_ai, args.num_human, args.ai_strategies.split(','))

