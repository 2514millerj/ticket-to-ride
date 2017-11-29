import pandas

games = [["tickets", "random"],
         ["route", "random"],
         ["route", "route"],
         ["random", "random"],
         ["tickets", "route"],
         ["tickets", "tickets"],
         ["route", "tickets"],
         ["random", "route"],
         ["random", "tickets"]]

def getStats(game):
    data_df = pandas.read_csv("TTR_log_" + game[0] + "_" + game[1] + ".csv")
    cols = data_df.columns

    points1 = data_df['points1']
    points2 = data_df['points2']

    print("GAME --- " + data_df['strategy1'][0] + "  VS  " + data_df['strategy2'][0])
    print("Strategy 1: " + data_df['strategy1'][0])
    print(points1.describe())
    print("Strategy 2: " + data_df['strategy2'][0])
    print(points2.describe())

    wins1 = 0
    wins2 = 0
    ties = 0
    total = 0

    for s1, s2 in zip(points1, points2):
        total += 1
        if s1 > s2:
            wins1 += 1
        elif s2 > s1:
            wins2 += 1
        else:
            ties += 1

    print("Win percentage for " + data_df['strategy1'][0] + ": " + str(wins1/float(total)))
    print("Win percentage for " + data_df['strategy2'][0] + ": " + str(wins2 / float(total)))

for game in games:
    getStats(game)
    print("")