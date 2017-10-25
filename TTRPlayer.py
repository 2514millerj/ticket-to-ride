import collections
from networkx import nx

class Player(object):
    
    def __init__(self, 
                 startingHand, 
                 startingTickets, 
                 playerBoard, 
                 playerPosition, 
                 numTrains,
                 type
                 ):
        """orderNumber: int
        startingHand: list
        startingTickets: list
        playerBoard: PlayerBoard object from the TTRBoard module
        playerPosition: int
        """
        self.name           = '' #ask for them to enter it on first turn
        
        #implimented as a collection to avoid O(n) hand.remove(x)
        self.hand           = collections.Counter(startingHand)
        
        self.tickets        = {x:False for x in startingTickets}
        self.numTrains      = numTrains
        self.points         = 0
        self.playerPosition = playerPosition
        
        #custom board to represent
        self.playerBoard    = playerBoard

        #Human or AI player
        self.type           = type
                    
    def removeCardsFromHand(self, color, numColor):
        """removes one ore more cards from hand
        assumes all cards are in hand, error if not
        cards: list
        """
        assert self.hand[color] >= numColor
        self.hand[color] -= numColor
        
    #add card to hand
    def addCardToHand(self, card):
        """adds a single card to hand
        assumes card is a valid choice
        card: String
        """
        if card != None:
            self.hand[card] += 1
    
    #add ticket to hand
    def addTicket(self, ticket):
        """adds a single ticket to tickets
        ticket: tuple(city1, city2, value)
        """
        self.tickets[ticket] = False
    
    def completeTicket(self, ticket):
        """updates the value in the tickets dict to True for key: ticket
        ticket: tuple(city1, city2, value)
        """
        assert ticket in self.tickets
        self.tickets = True
    
    def getHand(self):
        return self.hand
    
    def addPoints(self, numPoints):
        self.points += numPoints
    
    def subtractPoints(self, numPoints):
        self.points -= numPoints
        
    def getPoints(self):
        return self.points
        
    def getTickets(self):
        return self.tickets
    
    def getNumTrains(self):
        return self.numTrains
    
    def playNumTrains(self, numTrains):
        assert numTrains <= self.numTrains
        self.numTrains -= numTrains
        
    def setPlayerName(self, name):
        """sets playerName to name
        name: string
        """
        self.name = name
    
    def getName(self):
        return self.name


    """
        AI Player Logic
    """
    def pickTickets(self, tickets, minNumToSelect):
        choices = set()
        choices.add(tickets[0])
        choices.add(tickets[1])

        return choices

    def getPathsInProgress(self, fullBoard):
        tickets = self.getTickets()
        hand = self.getHand()

        print(tickets)
        print(hand)

        # record each edge on the shortest path between cities on ticket
        #   and the percentage of completion of each edge
        edgeCompletion = []
        for ticket in tickets.keys():
            path = nx.shortest_path(fullBoard.returnGraph(), ticket[0], ticket[1])
            for city in enumerate(path):
                try:
                    city1 = path[city[0]]
                    city2 = path[city[0] + 1]
                    weight = fullBoard.getEdgeWeight(city1, city2)
                    color = fullBoard.getEdgeColors(city1, city2)
                    print("Cities: {} - {}    weight: {}    color: {}".format(city1, city2, weight,
                                                                              color))
                except:
                    continue

                for cardType in hand:
                    numCardsInHand = hand[cardType]
                    if cardType == 'wild':
                        wildCnt = numCardsInHand
                    else:
                        wildCnt = 0

                    for c in color:
                        if cardType == c and numCardsInHand + wildCnt >= weight:
                            pctDone = numCardsInHand / float(weight)
                            edgeCompletion.append((city1, city2, pctDone, 1))
                        elif cardType == c and numCardsInHand + wildCnt < weight:
                            pctDone = numCardsInHand / float(weight)
                            edgeCompletion.append((city1, city2, pctDone, 1))

            # check for duplicates
            # TODO: add a weight to tuple
            edgeCompletion.append(edgeCompletion[0])
            duplicates = [k for k, v in collections.Counter(edgeCompletion).items() if v > 1]

            print("Duplicate Paths: " + str(duplicates))
            print("Percent towards edge completion: " + str(edgeCompletion))

            print ''
            return edgeCompletion

    def makeTurnChoice(self, fullBoard):
        self.getPathsInProgress(fullBoard)
        return "cards"
        

        
        
        