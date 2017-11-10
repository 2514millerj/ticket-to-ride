from TTRPlayer import Player
import collections
import TTRBoard
import networkx as nx
import ast

#
# AI that focuses on completing longest routes
#
class routeAIPlayer(Player):

    """
    AI Player Logic
    """

    def pickTickets(self, tickets, minNumToSelect):
        choices = set()
        choices.add(tickets[0])
        choices.add(tickets[1])

        return choices

    def getPathsInProgress(self, fullBoard, board):
        return

    def makeTurnChoice(self, fullBoard, board):
        self.numTurns += 1
        print("Turn number {}".format(self.numTurns))

        return

    def AIpickCards(self, board, deck, options):
        return

    def AIplaceTrains(self, board, deck, route, routeValues):
        return

    def pickAITickets(self, deck, minNumToSelect=1):
        return