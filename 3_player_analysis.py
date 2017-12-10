import pandas
import os
from itertools import product
from scipy.stats import rankdata

strategies = ["tickets", "random", "route"]

def getStats(game):
    data_df = pandas.read_csv("3_players/TTR_log_" + game[0] + "_" + game[1] + "_" + game[2] + ".csv")

    points1 = data_df['points1']
    points2 = data_df['points2']
    points3 = data_df['points3']

    print("GAME --- " + data_df['strategy1'][0] + "  VS  " + data_df['strategy2'][0] + "  VS  " + data_df['strategy3'][0])
    print("Strategy 1: " + data_df['strategy1'][0])
    print(points1.describe())
    print("Strategy 2: " + data_df['strategy2'][0])
    print(points2.describe())
    print("Strategy 3: " + data_df['strategy3'][0])
    print(points3.describe())

    wins1 = 0
    wins2 = 0
    wins3 = 0
    total = 0

    for s1, s2, s3 in zip(points1, points2, points3):
        total += 1
        ranked = rankdata([s1, s2, s3])
        print(ranked)
        wins1 += ranked[0]
        wins2 += ranked[1]
        wins3 += ranked[2]

    print("Average rank for " + data_df['strategy1'][0] + ": " + str(wins1/float(total)))
    print("Average rank for " + data_df['strategy2'][0] + ": " + str(wins2 / float(total)))
    print("Average rank for " + data_df['strategy3'][0] + ": " + str(wins3 / float(total)))

def playGame(strategies):
    os.system('python2 AIGame.py --num_ai 3 --num_human 0 --ai_strategies ' + strategies)
    pass

games_to_play = list(product(strategies, repeat=3))

#run all possible games and build data
'''for game in games_to_play:
    strategy_string = ",".join(game)
    print(strategy_string)
    playGame(strategy_string)'''

#analyze data for all possible games
for game in games_to_play:
    getStats(game)
    break