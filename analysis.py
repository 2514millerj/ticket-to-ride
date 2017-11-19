import pandas

games = [["tickets", "random"],
         ["route", "random"],
         ["route", "route"],
         ["random", "random"],
         ["tickets", "route"]]

def getStats(game):
    data_df = pandas.read_csv("TTR_log_" + game[0] + "_" + game[1] + ".csv")
    cols = data_df.columns

    points1 = data_df['points1']
    points2 = data_df['points2']

    print("Strategy 1: " + data_df['strategy1'][0])
    print("Strategy 2: " + data_df['strategy2'][0])
    print("Average points for strategy 1: " + str(sum(points1) / float(len(points1))))
    print("Average points for strategy 2: " + str(sum(points2) / float(len(points2))))

for game in games:
    getStats(game)
    print("")