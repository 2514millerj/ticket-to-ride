from TTRPlayer import Player
import collections
import TTRBoard
import networkx as nx
import ast
from random import *

#
# AI that focuses on completing longest routes
#
class randomAIPlayer(Player):

    """
    AI Player Logic
    """

    def pickTickets(self, tickets, minNumToSelect):
        choices = set()
        choices.add(tickets[0])
        choices.add(tickets[1])

        return choices

    def getPathsInProgress(self, fullBoard, board):
        hand=self.getHand()
        wildCnt=hand['wild']
        edgeCompletion = []
        
        for edge in board.getEdges():
            color = board.getEdgeColors(edge[0], edge[1])
            weight = board.getEdgeWeight(edge[0], edge[1])
            for cardType in hand:
                        numCardsInHand = hand[cardType]

                        for c in color:
                            pctDone = numCardsInHand / float(weight)
                            if (cardType == c or c == 'grey') and pctDone >= 1:
                                edgeCompletion.append([edge[0], edge[1], pctDone, cardType, weight])
                                added = True

        return edgeCompletion

    def makeTurnChoice(self, fullBoard, board):
        self.numTurns += 1
        print("Turn number {}".format(self.numTurns))
        paths = self.getPathsInProgress(fullBoard, board)

        if len(paths) == 0:
            return "cards", []
        else:
            x=randint(0, len(paths) - 1)
            return "trains", paths[x]
        

    def AIpickCards(self, board, deck, options):
        print("AI drawing card")
        availableCards = deck.getDrawPile()
        count = 0
        max = 0
        maxOp = None
        print(availableCards)
        print(self.getHand())

        while count < 2:
            availableCards = deck.getDrawPile()
            choice = randint(0, len(availableCards) -1)
            print(availableCards[choice])
            if availableCards[choice] == "wild" and count == 0:
                chosen = deck.pickFaceUpCard(availableCards[choice])
                count = 2
            else:
                chosen = deck.pickFaceUpCard(availableCards[choice])
                count += 1
            self.addCardToHand(chosen)

        print(self.getHand())

        return board, deck

    def AIplaceTrains(self, board, deck, route, routeValues):
        city1 = route[0]
        city2 = route[1]

        color = route[3]
        routeDist = board.getEdgeWeight(city1, city2)

        hand = self.getHand()
        print(hand)
        numWild = hand['wild']

        numColor = routeDist - numWild

        # remove route from main board
        board.removeEdge(city1, city2, color)

        # calculate points
        self.addPoints(routeValues[routeDist])

        # remove cards from player's hand
        self.removeCardsFromHand(color, numColor)
        self.removeCardsFromHand('wild', numWild)

        # add cards to discard pile
        deck.addToDiscard([color for x in range(numColor)]
                               + ['wild' for x in range(numWild)]
                               )

        # remove trains from players numTrains
        self.playNumTrains(routeDist)

        #
        # claim route for player (see dedicated method within Game class)
        self.playerBoard.addEdge(city1, city2, routeDist, color)

        board.showBoard(self.playerBoard.G, 0.5)
        #self.board.showBoard(self.board.G, 2)

        print "Number of trains left to play: " + str(self.getNumTrains())

        count = 0
        completed = 0
        for ticket in self.getTickets():
            count += 1
            try:
                if self.playerBoard.hasPath(ticket[0], ticket[1]) and not self.getTickets()[ticket]:
                    print("***Ticket Completed***")
                    self.completeTicket(ticket)
                    completed += 1
                elif self.playerBoard.hasPath(ticket[0], ticket[1]):
                    completed += 1
            except:
                continue

        if count == completed:
            print("***All tickets completed, drawing new ones***")
            deck = self.pickAITickets(2)

        #raw_input("Continue?")
        return board, deck

    def pickAITickets(self, deck, minNumToSelect=1):
        tickets = deck.dealTickets(3)
        tickets = {x[0]: x[1] for x in zip(range(len(tickets)), tickets)}

        choices = self.pickTickets(tickets, minNumToSelect)

        for ticket in tickets.values():
            if ticket in choices:
                self.addTicket(ticket)
            else:
                deck.addToTicketDiscard(ticket)

        print len(deck.tickets), len(deck.ticketDiscardPile)

        print "All of your tickets: "
        print(self.getTickets())

        return deck
