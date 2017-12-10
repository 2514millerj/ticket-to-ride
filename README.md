TicketToRide
============
Ticket to Ride AI implementations are based off of the framework here: https://github.com/CodeProgress/TicketToRide

How to run: python AIGame.py --num_ai 2 --num_human 0 --ai_strategies tickets,route

Current AI Supported:
- ticket focused ==> AI will work to complete tickets and draw new ones when finished
- route focused ==> AI completes available routes with the heaviest weights assigned to them
- random ==> AI lays down trains as soon as possible and selects cards randomly from the deck

================================================================
Python simulation of the original Ticket To Ride board game.

Python 2.7.3

Package used:
NetworkX 1.8.1

For further information about Ticket To Ride:  http://en.wikipedia.org/wiki/Ticket_to_Ride_(board_game)

