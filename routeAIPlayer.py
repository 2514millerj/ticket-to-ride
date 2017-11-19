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
        tickets = self.getTickets()
        hand = self.getHand()
        print(hand)
        edges = board.getEdges()

        wildCnt = hand['wild']
        count = 0

        # record each edge on the shortest path between cities on ticket
        #   and the percentage of completion of each edge
        edgeWeight = []
        maxWeight = 0
        for route in edges:
            added = False
            weight = board.getEdgeWeight(route[0], route[1])
            if weight > maxWeight:
                maxWeight = weight
            color = board.getEdgeColors(route[0], route[1])
            for cardType in hand:
                numCardsInHand = hand[cardType]
                for c in color:
                    if cardType == c or c == 'grey':
                        pctDone = numCardsInHand / float(weight)
                        routeColor = c
                        added = True

            if added == False:
                routeColor = color[0]
                pctDone = 0

            edgeWeight.append([route[0], route[1], pctDone, weight, routeColor])

        options = []
        for route in edgeWeight:
            if route[3] == maxWeight:
                options.append(route)

        print(options)
        print("")
        return options

    def makeTurnChoice(self, fullBoard, board):
        self.numTurns += 1
        print("Turn number {}".format(self.numTurns))
        paths = self.getPathsInProgress(fullBoard, board)

        for p in paths:
            # if AI has enough cards in hand to play route
            if p[2] >= 1 and p[3] <= self.numTrains:
                return "trains", p

        return "cards", paths

    def AIpickCards(self, board, deck, options):
        print("AI drawing card")
        availableCards = deck.getDrawPile()
        count = 0
        max = 0
        maxOp = None
        print(availableCards)
        print(self.getHand())

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
                    deck.pickFaceUpCard(c)
                    count += 1
                    break

        if count == 0 and 'wild' in availableCards:
            self.addCardToHand('wild')
            deck.pickFaceUpCard('wild')
            count = 2

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
        print(route)
        city1 = route[0]
        city2 = route[1]

        color = route[4]
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
            deck = self.pickAITickets(deck, 2)

        #raw_input("Continue?")
        return board, deck


    def pickAITickets(self, deck, minNumToSelect=1):
        tickets = deck.dealTickets(3)
        tickets = {x[0]: x[1] for x in zip(range(len(tickets)), tickets)}

        choices = self.pickTickets(tickets, 1)

        for ticket in tickets.values():
            if ticket in choices:
                self.addTicket(ticket)
            else:
                deck.addToTicketDiscard(ticket)

        print len(deck.tickets), len(deck.ticketDiscardPile)

        print "All of your tickets: "
        print(self.getTickets())

        return deck