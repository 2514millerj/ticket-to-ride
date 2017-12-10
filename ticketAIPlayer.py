from TTRPlayer import Player
import collections
import TTRBoard
import networkx as nx
import ast
from random import randint

#
# AI that focuses on completing tickets
#
class ticketAIPlayer(Player):

    """
    AI Player Logic
    """

    def pickTickets(self, tickets, minNumToSelect):
        choices = set()
        choices.add(tickets[0])
        choices.add(tickets[1])

        return choices

    def getPathsInProgress(self, fullBoard, board):
        tickets = self.getTickets()
        print(tickets)
        hand = self.getHand()

        wildCnt = hand['wild']
        count = 0

        # record each edge on the shortest path between cities on ticket
        #   and the percentage of completion of each edge
        edgeCompletion = []
        for ticket in tickets.keys():
            count += 1
            if tickets[ticket] == True:
                continue

            try:
                path = nx.shortest_path(board.G, ticket[0], ticket[1])
            except Exception as e:
                print(e)
                #exit()
                #board.showBoard(board.G, 30)
                if count == len(tickets.keys()):
                    return []
                else:
                    continue

            added = False

            numWild = hand['wild']
            print("Number of wild cards in hand: " + str(numWild))
            for city in enumerate(path):
                edgePlayable = True
                try:
                    city1 = path[city[0]]
                    city2 = path[city[0] + 1]
                    if self.playerBoard.hasEdge(city1, city2) or not board.hasEdge(city1, city2):
                        # print("Cannot play on city {} and {}".format(city1, city2))
                        edgePlayable = False
                    weight = board.getEdgeWeight(city1, city2)
                    color = board.getEdgeColors(city1, city2)
                    # print("Cities: {} - {}    weight: {}    color: {}".format(city1, city2, weight,
                    #                                                          color))
                except:
                    break

                if edgePlayable == False:
                    continue

                for cardType in hand:
                    numCardsInHand = hand[cardType]

                    if cardType == 'wild':
                        continue

                    for c in color:
                        if (cardType == c or c == 'grey') and numCardsInHand + wildCnt >= weight:
                            pctDone = (numCardsInHand + numWild) / float(weight)
                            edgeCompletion.append([city1, city2, pctDone, cardType, weight])
                            added = True
                        elif (cardType == c or c == 'grey') and numCardsInHand + wildCnt < weight:
                            pctDone = (numCardsInHand + numWild) / float(weight)
                            edgeCompletion.append([city1, city2, pctDone, cardType, weight])
                            added = True

                if added is False:
                    edgeCompletion.append([city1, city2, numWild / float(board.getEdgeWeight(city1, city2)), color[0], board.getEdgeWeight(city1, city2)])


        print(edgeCompletion)
        print
        ''
        return edgeCompletion

    def getAllPaths(self, fullBoard, board):
        hand = self.getHand()
        wildCnt = hand['wild']
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

        print(edgeCompletion)
        return edgeCompletion

    def makeTurnChoice(self, fullBoard, board, deck):
        pathsTooLong = False
        self.numTurns += 1
        print("Turn number {}".format(self.numTurns))
        paths = self.getPathsInProgress(fullBoard, board)

        if len(paths) == 0 and deck.ticketAvailable() == True:
            return "ticket", []
        elif len(paths) == 0 and deck.ticketAvailable() == False:
            pathsTooLong = True

        for p in paths:
            # if AI has enough cards in hand to play route
            if p[2] >= 1 and p[4] <= self.numTrains:
                return "trains", p
            elif p[2] >= 1 and p[4] > self.numTrains:
                pathsTooLong = True

        if pathsTooLong == True:
            paths = self.getAllPaths(fullBoard, board)
            if len(paths) == 0:
                return "cards", []
            else:
                for i in range(len(paths) * 3):
                    x = randint(0, len(paths) - 1)
                    if paths[x][2] >= 1 and paths[x][4] <= self.numTrains:
                        return "trains", paths[x]

        return "cards", paths

    def pickRandomCards(self, board, deck):
        availableCards = deck.getDrawPile()
        count = 0

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

    def AIpickCards(self, board, deck, options):
        print("AI drawing card")
        availableCards = deck.getDrawPile()
        count = 0
        max = 0
        maxOp = None
        print(availableCards)
        print(self.getHand())
        print(options)

        if len(options) ==  0:
            return self.pickRandomCards(board, deck)

        for op in options:
            availableCards = deck.getDrawPile()
            try:
                routeColor = board.getEdgeColors(op[0], op[1])
            except:
                continue
            if op[2] >= max:
                max = op[0]
                maxOp = op
            for c in routeColor:
                if c in availableCards and count < 2:
                    self.addCardToHand(c)
                    if deck.pickFaceUpCard(c) == None:
                        exit()
                    count += 1
                    break

        availableCards = deck.getDrawPile()
        if count == 0 and 'wild' in availableCards:
            self.addCardToHand('wild')
            if deck.pickFaceUpCard('wild') == None:
                exit()
            count = 2

        chosen = None
        while count < 2:
            availableCards = deck.getDrawPile()
            hand = self.getHand()
            mostCommon = hand.most_common(1)[0][0]
            try:
                colors = board.getEdgeColors(maxOp[0], maxOp[1])
            except:
                continue
            if 'grey' in colors:
                if mostCommon in availableCards:
                    self.addCardToHand(mostCommon)
                    if deck.pickFaceUpCard(mostCommon) == None:
                        exit()
                    count += 1
                else:
                    if chosen == 'grey':
                        print("c6")
                        print(self.getHand())
                        exit()
                    chosen = deck.pickFaceDown()
                    self.addCardToHand(chosen)
                    count += 1
            else:
                chosen = deck.pickFaceDown()
                self.addCardToHand(chosen)
                count += 1
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

        if color == 'grey':
            color = hand.most_common(1)[0][0]

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

        #board.showBoard(self.playerBoard.G, 0.5)
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
            deck = self.pickAITickets(deck, 2)

        #raw_input("Continue?")
        return board, deck

    def pickAITickets(self, deck, minNumToSelect=1):
        tickets = deck.dealTickets(3)
        tickets = {x[0]: x[1] for x in zip(range(len(tickets)), tickets)}

        choices = self.pickTickets(tickets, minNumToSelect)

        for ticket in tickets.values():
            if ticket == None:
                continue
            if ticket in choices:
                self.addTicket(ticket)
            else:
                deck.addToTicketDiscard(ticket)

        print len(deck.tickets), len(deck.ticketDiscardPile)

        print "All of your tickets: "
        print(self.getTickets())

        return deck