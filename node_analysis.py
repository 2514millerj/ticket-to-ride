import TTRBoard
import networkx as nx

B = TTRBoard.Board()

games = [["mixed", "tickets"],
         ["mixed", "mixed"]]

def getGraph(game):
    edgeLabels = []
    G1 = nx.Graph()
    G2 = nx.Graph()

    with open("TTR_edges_" + game[0] + "_" + game[1] + ".csv") as file:
        for line in file:
            splitLine = line.split(":")
            playerName = splitLine[0]

            data = splitLine[1]
            nodes = data.split("-")
            for node in nodes:
                nodeList = node.split(",")

                if len(nodeList) == 2:
                    if playerName == "p1" and G1.has_edge(nodeList[0], nodeList[1]):
                        G1.get_edge_data(nodeList[0], nodeList[1])['count'] += 1
                    elif playerName == "p1" and not G1.has_edge(nodeList[0], nodeList[1]):
                        G1.add_edge(nodeList[0], nodeList[1],
                                    count=1)
                    elif playerName == "p2" and G2.has_edge(nodeList[0], nodeList[1]):
                        G2.get_edge_data(nodeList[0], nodeList[1])['count'] += 1
                    elif playerName == "p2" and not G2.has_edge(nodeList[0], nodeList[1]):
                        G2.add_edge(nodeList[0], nodeList[1],
                                    count=1)
                else:
                    continue


    edgeList1 = G1.edges()
    counts1 = []
    for edge in edgeList1:
        counts1.append(G1.get_edge_data(edge[0],edge[1])["count"])

    edgeList2 = G2.edges()
    counts2 = []
    for edge in edgeList2:
        counts2.append(G2.get_edge_data(edge[0], edge[1])["count"])

    print("\n\nGAME: p1 -> " + game[0] + " VS p2 -> " + game[1])
    print("Top 5 routes for p1:")
    for i in range(0,5):
        print(str(edgeList1[counts1.index(max(counts1))]) + "   Count: " + str(counts1[counts1.index(max(counts1))]))
        edgeList1.pop(counts1.index(max(counts1)))
        counts1.pop(counts1.index(max(counts1)))

    print("\nTop 5 routes for p2:")
    for i in range(0,5):
        print(str(edgeList2[counts2.index(max(counts2))]) + "   Count: " + str(counts2[counts2.index(max(counts2))]))
        edgeList2.pop(counts2.index(max(counts2)))
        counts2.pop(counts2.index(max(counts2)))

for game in games:
    getGraph(game)