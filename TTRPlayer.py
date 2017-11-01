import collections
from networkx import nx
import ast
import TTRBoard

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
        self.fullBoard      = TTRBoard.Board()

        #Human or AI player
        self.type           = type
        self.numTurns       = 0
                    
    def removeCardsFromHand(self, color, numColor):
        """removes one ore more cards from hand
        assumes all cards are in hand, error if not
        cards: list
        """
        #assert self.hand[color] >= numColor
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
        self.tickets[ticket] = True
    
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
        

        
        
        