from random import randint, sample, choice
from itertools import combinations, permutations
from time import sleep
from copy import deepcopy


class Card:

    def __init__(self, name = "", left = 1, right = 1, top = 1, bottom = 1):
        self.name = name
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.played = False

    def __repr__(self):
        grid = self.visual(self.name)
        output = ""
        for y in range(9):
            for x in range(17):
                output += grid[x][y][0]
            output += "\n"

        return output

    def visual(self, identifier):
    # This function outputs a 2D grid of lists of length 1, each containing a single character.
    # It aids in the visualization of a given card, with the identifier string in the middle.
    # This may be used to show the name of the card, or the name of the player that controls
    # the card on the board.
    
        #To change any 10 value to 'A' for Ace
        if self.top == 10:
            top = "A"
        else:
            top = str(self.top)
        if self.left == 10:
            left = "A"
        else:
            left = str(self.left)
        if self.right == 10:
            right = "A"
        else:
            right = str(self.right)      
        if self.bottom == 10:
            bottom = "A"
        else:
            bottom = str(self.bottom)
       
        #This helps to ceneter the word on the middle line
        padding = int((11-len(identifier))/2)
        
        #The grid will be 17x9
        grid = [[[" "] for i in range(9)] for j in range(17)]

        for x in range(1, 16):
            grid[x][0] = ["-"]
            grid[x][-1] = ["-"]

        for y in range(1, 8):
            grid[0][y] = ["|"]
            grid[-1][y] = ["|"]

        grid[8][1] = [top]
        grid[8][-2] = [bottom]
        grid[2][4] = [left]
        grid[-3][4] = [right]

        for i in range(len(identifier)):
            grid[3 + padding + i][4] = [identifier[i]]

        return grid



    def visual_2(self, identifier1, identifier2):
    # Works like the visual function, but puts two strings 
    # on the card. This is needed for when the 'Plus'/'Same'/'Combo'
    # rules kick in.
    
        #To change any 10 value to 'A' for Ace
        if self.top == 10:
            top = "A"
        else:
            top = str(self.top)
        if self.left == 10:
            left = "A"
        else:
            left = str(self.left)
        if self.right == 10:
            right = "A"
        else:
            right = str(self.right)      
        if self.bottom == 10:
            bottom = "A"
        else:
            bottom = str(self.bottom)
       
        #This helps to ceneter the word on the middle line
        padding1 = int((11-len(identifier1))/2)
        padding2 = int((11-len(identifier2))/2)
        
        #The grid will be 17x9
        grid = [[[" "] for i in range(9)] for j in range(17)]

        for x in range(1, 16):
            grid[x][0] = ["-"]
            grid[x][-1] = ["-"]

        for y in range(1, 8):
            grid[0][y] = ["|"]
            grid[-1][y] = ["|"]

        grid[8][1] = [top]
        grid[8][-2] = [bottom]
        grid[2][4] = [left]
        grid[-3][4] = [right]

        for i in range(len(identifier1)):
            grid[3 + padding1 + i][3] = [identifier1[i]]

        for i in range(len(identifier2)):
            grid[3 + padding2 + i][5] = [identifier2[i]]

        return grid




class Player:


    counter = 0
    # In case a player doesn't enter a name, this will help to decide if
    # they will be Player 1 or Player 2. This is also used to determine
    # which player's turn it is.

    def __init__(self, name = "", hand = [], points = 5):
        self.name = name
        self.nickname = name
        self.hand = hand
        #A hand is a list of Cards
        self.points = points
        Player.counter += 1
        if self.name == "":
            self.name += "Player {}".format(str(Player.counter))
   
    def __repr__(self):
        if self.hand == []:
            return "{} is a player with {} points, and is out of cards.".format(self.name, self.points)
        else:
            output = "{} is a player with {} points and has the following cards in their hand:\n".format(self.name, self.points)
            for index in range(len(self.hand)):
                if index != (len(self.hand)-1):
                    output += self.hand[index].name + "\n"
                else:
                    output += self.hand[index].name
            return output

    def play_card(self, oponent, card, cell, same, plus):
        # Game will be designed so that it is only possible to play cards from a player's hand.
        # It will also only be possible to play on a non-filled cell.
        self.hand.remove(card)
        cell.filled = True
        cell.controller = self
        cell.card = card
        
        same_and_plus_stack = []
        if plus:
            for direction_1, direction_2 in list(combinations(cell.neighbors, 2)):
                if direction_1 == "left":
                    if direction_2 == "right":
                        left_cell = cell.neighbors[direction_1]
                        right_cell = cell.neighbors[direction_2]
                        if left_cell.filled and right_cell.filled:
                            if (card.left + left_cell.card.right) == (card.right + right_cell.card.left):
                                if left_cell.controller != self:
                                    left_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    left_cell.plus = True
                                    if left_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(left_cell)
                                if right_cell.controller != self:
                                    right_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    right_cell.plus = True
                                    if right_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(right_cell)
                    elif direction_2 == "above":
                        left_cell = cell.neighbors[direction_1]
                        above_cell = cell.neighbors[direction_2]
                        if left_cell.filled and above_cell.filled:
                            if (card.left + left_cell.card.right) == (card.top + above_cell.card.bottom):
                                if left_cell.controller != self:
                                    left_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    left_cell.plus = True
                                    if left_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(left_cell)
                                if above_cell.controller != self:
                                    above_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    above_cell.plus = True
                                    if above_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(above_cell)
                    elif direction_2 == "below":
                        left_cell = cell.neighbors[direction_1]
                        below_cell = cell.neighbors[direction_2]
                        if left_cell.filled and below_cell.filled:
                            if (card.left + left_cell.card.right) == (card.bottom + below_cell.card.top):
                                if left_cell.controller != self:
                                    left_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    left_cell.plus = True
                                    if left_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(left_cell)
                                if below_cell.controller != self:
                                    below_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    below_cell.plus = True
                                    if below_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(below_cell)
                elif direction_1 == "above":
                    if direction_2 == "right":
                        above_cell = cell.neighbors[direction_1]
                        right_cell = cell.neighbors[direction_2]
                        if above_cell.filled and right_cell.filled:
                            if (card.top + above_cell.card.bottom) == (card.right + right_cell.card.left):
                                if above_cell.controller != self:
                                    above_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    above_cell.plus = True
                                    if above_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(above_cell)
                                if right_cell.controller != self:
                                    right_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    right_cell.plus = True
                                    if right_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(right_cell)
                    elif direction_2 == "left":
                        above_cell = cell.neighbors[direction_1]
                        left_cell = cell.neighbors[direction_2]
                        if above_cell.filled and left_cell.filled:
                            if (card.top + above_cell.card.bottom) == (card.left + left_cell.card.right):
                                if above_cell.controller != self:
                                    above_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    above_cell.plus = True
                                    if above_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(above_cell)
                                if left_cell.controller != self:
                                    left_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    left_cell.plus = True
                                    if left_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(left_cell)
                    elif direction_2 == "below":
                        above_cell = cell.neighbors[direction_1]
                        below_cell = cell.neighbors[direction_2]
                        if above_cell.filled and below_cell.filled:
                            if (card.top + above_cell.card.bottom) == (card.bottom + below_cell.card.top):
                                if above_cell.controller != self:
                                    above_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    above_cell.plus = True
                                    if above_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(above_cell)
                                if below_cell.controller != self:
                                    below_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    below_cell.plus = True
                                    if below_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(below_cell)
                elif direction_1 == "right":
                    if direction_2 == "above":
                        right_cell = cell.neighbors[direction_1]
                        above_cell = cell.neighbors[direction_2]
                        if right_cell.filled and above_cell.filled:
                            if (card.right + right_cell.card.left) == (card.top + above_cell.card.bottom):
                                if right_cell.controller != self:
                                    right_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    right_cell.plus = True
                                    if right_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(right_cell)
                                if above_cell.controller != self:
                                    above_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    above_cell.plus = True
                                    if above_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(above_cell)
                    elif direction_2 == "left":
                        right_cell = cell.neighbors[direction_1]
                        left_cell = cell.neighbors[direction_2]
                        if right_cell.filled and left_cell.filled:
                            if (card.right + right_cell.card.left) == (card.left + left_cell.card.right):
                                if right_cell.controller != self:
                                    right_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    right_cell.plus = True
                                    if right_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(right_cell)
                                if left_cell.controller != self:
                                    left_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    left_cell.plus = True
                                    if left_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(left_cell)
                    elif direction_2 == "below":
                        right_cell = cell.neighbors[direction_1]
                        below_cell = cell.neighbors[direction_2]
                        if right_cell.filled and below_cell.filled:
                            if (card.right + right_cell.card.left) == (card.bottom + below_cell.card.top):
                                if right_cell.controller != self:
                                    right_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    right_cell.plus = True
                                    if right_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(right_cell)
                                if below_cell.controller != self:
                                    below_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    below_cell.plus = True
                                    if below_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(below_cell)
                elif direction_1 == "below":
                    if direction_2 == "above":
                        below_cell = cell.neighbors[direction_1]
                        above_cell = cell.neighbors[direction_2]
                        if below_cell.filled and above_cell.filled:
                            if (card.bottom + below_cell.card.top) == (card.top + above_cell.card.bottom):
                                if below_cell.controller != self:
                                    below_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    below_cell.plus = True
                                    if below_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(below_cell)
                                if above_cell.controller != self:
                                    above_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    above_cell.plus = True
                                    if above_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(above_cell)
                    elif direction_2 == "left":
                        below_cell = cell.neighbors[direction_1]
                        left_cell = cell.neighbors[direction_2]
                        if below_cell.filled and left_cell.filled:
                            if (card.bottom + below_cell.card.top) == (card.left + left_cell.card.right):
                                if below_cell.controller != self:
                                    below_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    below_cell.plus = True
                                    if below_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(below_cell)
                                if left_cell.controller != self:
                                    left_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    left_cell.plus = True
                                    if left_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(left_cell)
                    elif direction_2 == "right":
                        below_cell = cell.neighbors[direction_1]
                        right_cell = cell.neighbors[direction_2]
                        if below_cell.filled and right_cell.filled:
                            if (card.bottom + below_cell.card.top) == (card.right + right_cell.card.left):
                                if below_cell.controller != self:
                                    below_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    below_cell.plus = True
                                    if below_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(below_cell)
                                if right_cell.controller != self:
                                    right_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    right_cell.plus = True
                                    if right_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(right_cell)

        if same:
            for direction_1, direction_2 in list(combinations(cell.neighbors, 2)):
                if direction_1 == "left":
                    if direction_2 == "right":
                        left_cell = cell.neighbors[direction_1]
                        right_cell = cell.neighbors[direction_2]
                        if left_cell.filled and right_cell.filled:
                            if (card.left == left_cell.card.right) and (card.right == right_cell.card.left):
                                if left_cell.controller != self:
                                    left_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    left_cell.same = True
                                    if left_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(left_cell)
                                if right_cell.controller != self:
                                    right_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    right_cell.same = True
                                    if right_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(right_cell)
                    elif direction_2 == "above":
                        left_cell = cell.neighbors[direction_1]
                        above_cell = cell.neighbors[direction_2]
                        if left_cell.filled and above_cell.filled:
                            if (card.left == left_cell.card.right) and (card.top == above_cell.card.bottom):
                                if left_cell.controller != self:
                                    left_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    left_cell.same = True
                                    if left_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(left_cell)
                                if above_cell.controller != self:
                                    above_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    above_cell.same = True
                                    if above_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(above_cell)
                    elif direction_2 == "below":
                        left_cell = cell.neighbors[direction_1]
                        below_cell = cell.neighbors[direction_2]
                        if left_cell.filled and below_cell.filled:
                            if (card.left == left_cell.card.right) and (card.bottom == below_cell.card.top):
                                if left_cell.controller != self:
                                    left_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    left_cell.same = True
                                    if left_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(left_cell)
                                if below_cell.controller != self:
                                    below_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    below_cell.same = True
                                    if below_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(below_cell)
                elif direction_1 == "above":
                    if direction_2 == "right":
                        above_cell = cell.neighbors[direction_1]
                        right_cell = cell.neighbors[direction_2]
                        if above_cell.filled and right_cell.filled:
                            if (card.top == above_cell.card.bottom) and (card.right == right_cell.card.left):
                                if above_cell.controller != self:
                                    above_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    above_cell.same = True
                                    if above_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(above_cell)
                                if right_cell.controller != self:
                                    right_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    right_cell.same = True
                                    if right_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(right_cell)
                    elif direction_2 == "left":
                        above_cell = cell.neighbors[direction_1]
                        left_cell = cell.neighbors[direction_2]
                        if above_cell.filled and left_cell.filled:
                            if (card.top == above_cell.card.bottom) and (card.left == left_cell.card.right):
                                if above_cell.controller != self:
                                    above_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    above_cell.same = True
                                    if above_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(above_cell)
                                if left_cell.controller != self:
                                    left_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    left_cell.same = True
                                    if left_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(left_cell)
                    elif direction_2 == "below":
                        above_cell = cell.neighbors[direction_1]
                        below_cell = cell.neighbors[direction_2]
                        if above_cell.filled and below_cell.filled:
                            if (card.top == above_cell.card.bottom) and (card.bottom == below_cell.card.top):
                                if above_cell.controller != self:
                                    above_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    above_cell.same = True
                                    if above_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(above_cell)
                                if below_cell.controller != self:
                                    below_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    below_cell.same = True
                                    if below_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(below_cell)
                elif direction_1 == "right":
                    if direction_2 == "above":
                        right_cell = cell.neighbors[direction_1]
                        above_cell = cell.neighbors[direction_2]
                        if right_cell.filled and above_cell.filled:
                            if (card.right == right_cell.card.left) and (card.top == above_cell.card.bottom):
                                if right_cell.controller != self:
                                    right_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    right_cell.same = True
                                    if right_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(right_cell)
                                if above_cell.controller != self:
                                    above_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    above_cell.same = True
                                    if above_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(above_cell)
                    elif direction_2 == "left":
                        right_cell = cell.neighbors[direction_1]
                        left_cell = cell.neighbors[direction_2]
                        if right_cell.filled and left_cell.filled:
                            if (card.right == right_cell.card.left) and (card.left == left_cell.card.right):
                                if right_cell.controller != self:
                                    right_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    right_cell.same = True
                                    if right_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(right_cell)
                                if left_cell.controller != self:
                                    left_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    left_cell.same = True
                                    if left_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(left_cell)
                    elif direction_2 == "below":
                        right_cell = cell.neighbors[direction_1]
                        below_cell = cell.neighbors[direction_2]
                        if right_cell.filled and below_cell.filled:
                            if (card.right == right_cell.card.left) and (card.bottom == below_cell.card.top):
                                if right_cell.controller != self:
                                    right_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    right_cell.same = True
                                    if right_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(right_cell)
                                if below_cell.controller != self:
                                    below_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    below_cell.same = True
                                    if below_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(below_cell)
                elif direction_1 == "below":
                    if direction_2 == "above":
                        below_cell = cell.neighbors[direction_1]
                        above_cell = cell.neighbors[direction_2]
                        if below_cell.filled and above_cell.filled:
                            if (card.bottom == below_cell.card.top) and (card.top == above_cell.card.bottom):
                                if below_cell.controller != self:
                                    below_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    below_cell.same = True
                                    if below_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(below_cell)
                                if above_cell.controller != self:
                                    above_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    above_cell.same = True
                                    if above_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(above_cell)
                    elif direction_2 == "left":
                        below_cell = cell.neighbors[direction_1]
                        left_cell = cell.neighbors[direction_2]
                        if below_cell.filled and left_cell.filled:
                            if (card.bottom == below_cell.card.top) and (card.left == left_cell.card.right):
                                if below_cell.controller != self:
                                    below_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    below_cell.same = True
                                    if below_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(below_cell)
                                if left_cell.controller != self:
                                    left_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    left_cell.same = True
                                    if left_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(left_cell)
                    elif direction_2 == "right":
                        below_cell = cell.neighbors[direction_1]
                        right_cell = cell.neighbors[direction_2]
                        if below_cell.filled and right_cell.filled:
                            if (card.bottom == below_cell.card.top) and (card.right == right_cell.card.left):
                                if below_cell.controller != self:
                                    below_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    below_cell.same = True
                                    if below_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(below_cell)
                                if right_cell.controller != self:
                                    right_cell.controller = self
                                    self.points += 1
                                    oponent.points -= 1
                                    right_cell.same = True
                                    if right_cell not in same_and_plus_stack:
                                        same_and_plus_stack.append(right_cell)


        if same or plus:
            while same_and_plus_stack != []:
                current_cell = same_and_plus_stack[-1]
                current_card = current_cell.card
                any_card_flipped = False
                for direction, adj_cell in current_cell.neighbors.items():
                    if adj_cell.filled and (adj_cell.controller != self):
                        if direction == "left":
                            if (current_card.left > adj_cell.card.right):
                                any_card_flipped = True
                                adj_cell.controller = self
                                self.points += 1
                                oponent.points -= 1
                                adj_cell.combo = True
                                if adj_cell not in same_and_plus_stack:
                                    same_and_plus_stack.append(adj_cell)
                        elif direction == "above":
                            if current_card.top > adj_cell.card.bottom:
                                any_card_flipped = True
                                adj_cell.controller = self
                                self.points += 1
                                oponent.points -= 1
                                adj_cell.combo = True
                                if adj_cell not in same_and_plus_stack:
                                    same_and_plus_stack.append(adj_cell)
                        elif direction == "right":
                            if current_card.right > adj_cell.card.left:
                                any_card_flipped = True
                                adj_cell.controller = self
                                self.points += 1
                                oponent.points -= 1
                                adj_cell.combo = True
                                if adj_cell not in same_and_plus_stack:
                                    same_and_plus_stack.append(adj_cell)
                        elif direction == "below":
                            if current_card.bottom > adj_cell.card.top:
                                any_card_flipped = True
                                adj_cell.controller = self
                                self.points += 1
                                oponent.points -= 1
                                adj_cell.combo = True
                                if adj_cell not in same_and_plus_stack:
                                    same_and_plus_stack.append(adj_cell)

                if not any_card_flipped:
                    same_and_plus_stack.pop()
                

            
        for direction, adj_cell in cell.neighbors.items():
            if adj_cell.filled and (adj_cell.controller != self):
                if direction == "left":
                    if (card.left > adj_cell.card.right):
                        adj_cell.controller = self
                        self.points += 1
                        oponent.points -= 1
                elif direction == "above":
                    if card.top > adj_cell.card.bottom:
                        adj_cell.controller = self
                        self.points += 1
                        oponent.points -= 1
                elif direction == "right":
                    if card.right > adj_cell.card.left:
                        adj_cell.controller = self
                        self.points += 1
                        oponent.points -= 1
                elif direction == "below":
                    if card.bottom > adj_cell.card.top:
                        adj_cell.controller = self
                        self.points += 1
                        oponent.points -= 1



# Each square on the board that a card can be put onto is a Cell.
# It will keep track of whether or not it's filled. Once filled, it
# will keep track of the player that controls it, and what card is on it.
# Finally, it encodes which other cells are neighbors.
class Cell:

    def __init__(self, id = "", filled = False, neighbors = {}):
        self.id = id
        self.filled = filled
        self.neighbors = neighbors
        self.card = False
        self.combo = False
        self.plus = False
        self.same = False


class Board:

    def __init__(self):
        self.cell_1 = Cell("1")
        self.cell_2 = Cell("2")
        self.cell_3 = Cell("3")
        self.cell_4 = Cell("4")
        self.cell_5 = Cell("5")
        self.cell_6 = Cell("6")
        self.cell_7 = Cell("7")
        self.cell_8 = Cell("8")
        self.cell_9 = Cell("9")

        self.cell_1.neighbors = {"right":self.cell_2, "below":self.cell_4}
        self.cell_2.neighbors = {"left":self.cell_1, "right":self.cell_3, "below":self.cell_5}
        self.cell_3.neighbors = {"left":self.cell_2, "below":self.cell_6}
        self.cell_4.neighbors = {"above":self.cell_1, "right":self.cell_5, "below":self.cell_7}
        self.cell_5.neighbors = {"left":self.cell_4, "above":self.cell_2, "right":self.cell_6, "below":self.cell_8}
        self.cell_6.neighbors = {"left":self.cell_5, "above":self.cell_3, "below":self.cell_9}
        self.cell_7.neighbors = {"above":self.cell_4, "right":self.cell_8}
        self.cell_8.neighbors = {"left":self.cell_7, "above":self.cell_5, "right":self.cell_9}
        self.cell_9.neighbors = {"left":self.cell_8, "above":self.cell_6}

    def __repr__(self):
        output = ""
        grid = self.board_grid()
        for y in range(31):
            for x in range(67):
                output += grid[x][y][0]
            output += "\n"
        
        return output

    # Outputs a 2D grid of lists, each containing exactly 1 character.
    # This grid contains the information to print the board and any cards
    # that have been played.
    def board_grid(self):
        grid = [[[" "] for i in range(31)] for j in range(67)]

        for x in range(67):
            if (x != 0) and (x != 66):
                grid[x][0] = ["-"]
                grid[x][-1] = ["-"]
                grid[x][10] = ["-"]
                grid[x][20] = ["-"]

        for y in range(31):
            if (y != 0) and (y != 30):
                grid[0][y] = ["|"]
                grid[22][y] = ["|"]
                grid[44][y] = ["|"]
                grid[-1][y] = ["|"]

        if self.cell_1.filled:
            if self.cell_1.plus:
                if self.cell_1.controller.name.lower() == "player 1":
                    subgrid = self.cell_1.card.visual_2("Player1", "PLUS")
                elif self.cell_1.controller.name.lower() == "player 2":
                    subgrid = self.cell_1.card.visual_2("Player2", "PLUS")
                else:
                    subgrid = self.cell_1.card.visual_2(self.cell_1.controller.nickname, "PLUS")
            elif self.cell_1.same:
                if self.cell_1.controller.name.lower() == "player 1":
                    subgrid = self.cell_1.card.visual_2("Player1", "SAME")
                elif self.cell_1.controller.name.lower() == "player 2":
                    subgrid = self.cell_1.card.visual_2("Player2", "SAME")
                else:
                    subgrid = self.cell_1.card.visual_2(self.cell_1.controller.nickname, "SAME")
            elif self.cell_1.combo:
                if self.cell_1.controller.name.lower() == "player 1":
                    subgrid = self.cell_1.card.visual_2("Player1", "COMBO")
                elif self.cell_1.controller.name.lower() == "player 2":
                    subgrid = self.cell_1.card.visual_2("Player2", "COMBO")
                else:
                    subgrid = self.cell_1.card.visual_2(self.cell_1.controller.nickname, "COMBO")
            else:
                if self.cell_1.controller.name.lower() == "player 1":
                    subgrid = self.cell_1.card.visual("Player1")
                elif self.cell_1.controller.name.lower() == "player 2":
                    subgrid = self.cell_1.card.visual("Player2")
                else:
                    subgrid = self.cell_1.card.visual(self.cell_1.controller.nickname)
            for y in range(9):
                for x in range(17):
                    grid[3 + x][1 + y] = subgrid[x][y]
        else:
            #Print a 1 in the top-left corner
            grid[3][1] = ["1"]

        if self.cell_2.filled:
            if self.cell_2.plus:
                if self.cell_2.controller.name.lower() == "player 1":
                    subgrid = self.cell_2.card.visual_2("Player1", "PLUS")
                elif self.cell_2.controller.name.lower() == "player 2":
                    subgrid = self.cell_2.card.visual_2("Player2", "PLUS")
                else:
                    subgrid = self.cell_2.card.visual_2(self.cell_2.controller.nickname, "PLUS")
            elif self.cell_2.same:
                if self.cell_2.controller.name.lower() == "player 1":
                    subgrid = self.cell_2.card.visual_2("Player1", "SAME")
                elif self.cell_2.controller.name.lower() == "player 2":
                    subgrid = self.cell_2.card.visual_2("Player2", "SAME")
                else:
                    subgrid = self.cell_2.card.visual_2(self.cell_2.controller.nickname, "SAME")
            elif self.cell_2.combo:
                if self.cell_2.controller.name.lower() == "player 1":
                    subgrid = self.cell_2.card.visual_2("Player1", "COMBO")
                elif self.cell_2.controller.name.lower() == "player 2":
                    subgrid = self.cell_2.card.visual_2("Player2", "COMBO")
                else:
                    subgrid = self.cell_2.card.visual_2(self.cell_2.controller.nickname, "COMBO")
            else:
                if self.cell_2.controller.name.lower() == "player 1":
                    subgrid = self.cell_2.card.visual("Player1")
                elif self.cell_2.controller.name.lower() == "player 2":
                    subgrid = self.cell_2.card.visual("Player2")
                else:
                    subgrid = self.cell_2.card.visual(self.cell_2.controller.nickname)
            for y in range(9):
                for x in range(17):
                    grid[25 + x][1 + y] = subgrid[x][y]
        else:
            #Print a 2 in the top left corner
            grid[25][1] = ["2"]
            

        if self.cell_3.filled:
            if self.cell_3.plus:
                if self.cell_3.controller.name.lower() == "player 1":
                    subgrid = self.cell_3.card.visual_2("Player1", "PLUS")
                elif self.cell_3.controller.name.lower() == "player 2":
                    subgrid = self.cell_3.card.visual_2("Player2", "PLUS")
                else:
                    subgrid = self.cell_3.card.visual_2(self.cell_3.controller.nickname, "PLUS")
            elif self.cell_3.same:
                if self.cell_3.controller.name.lower() == "player 1":
                    subgrid = self.cell_3.card.visual_2("Player1", "SAME")
                elif self.cell_3.controller.name.lower() == "player 2":
                    subgrid = self.cell_3.card.visual_2("Player2", "SAME")
                else:
                    subgrid = self.cell_3.card.visual_2(self.cell_3.controller.nickname, "SAME")
            elif self.cell_3.combo:
                if self.cell_3.controller.name.lower() == "player 1":
                    subgrid = self.cell_3.card.visual_2("Player1", "COMBO")
                elif self.cell_3.controller.name.lower() == "player 2":
                    subgrid = self.cell_3.card.visual_2("Player2", "COMBO")
                else:
                    subgrid = self.cell_3.card.visual_2(self.cell_3.controller.nickname, "COMBO")
            else:
                if self.cell_3.controller.name.lower() == "player 1":
                    subgrid = self.cell_3.card.visual("Player1")
                elif self.cell_3.controller.name.lower() == "player 2":
                    subgrid = self.cell_3.card.visual("Player2")
                else:
                    subgrid = self.cell_3.card.visual(self.cell_3.controller.nickname)
            for y in range(9):
                for x in range(17):
                    grid[47 + x][1 + y] = subgrid[x][y]
        else:
            #Print a 3 in the top-left corner
            grid[47][1] = ["3"]

        if self.cell_4.filled:
            if self.cell_4.plus:
                if self.cell_4.controller.name.lower() == "player 1":
                    subgrid = self.cell_4.card.visual_2("Player1", "PLUS")
                elif self.cell_4.controller.name.lower() == "player 2":
                    subgrid = self.cell_4.card.visual_2("Player2", "PLUS")
                else:
                    subgrid = self.cell_4.card.visual_2(self.cell_4.controller.nickname, "PLUS")
            elif self.cell_4.same:
                if self.cell_4.controller.name.lower() == "player 1":
                    subgrid = self.cell_4.card.visual_2("Player1", "SAME")
                elif self.cell_4.controller.name.lower() == "player 2":
                    subgrid = self.cell_4.card.visual_2("Player2", "SAME")
                else:
                    subgrid = self.cell_4.card.visual_2(self.cell_4.controller.nickname, "SAME")
            elif self.cell_4.combo:
                if self.cell_4.controller.name.lower() == "player 1":
                    subgrid = self.cell_4.card.visual_2("Player1", "COMBO")
                elif self.cell_4.controller.name.lower() == "player 2":
                    subgrid = self.cell_4.card.visual_2("Player2", "COMBO")
                else:
                    subgrid = self.cell_4.card.visual_2(self.cell_4.controller.nickname, "COMBO")
            else:
                if self.cell_4.controller.name.lower() == "player 1":
                    subgrid = self.cell_4.card.visual("Player1")
                elif self.cell_4.controller.name.lower() == "player 2":
                    subgrid = self.cell_4.card.visual("Player2")
                else:
                    subgrid = self.cell_4.card.visual(self.cell_4.controller.nickname)
            for y in range(9):
                for x in range(17):
                    grid[3 + x][11 + y] = subgrid[x][y]
        else:
            #Print a 4 in the top-left corner
            grid[3][11] = ["4"]

        if self.cell_5.filled:
            if self.cell_5.plus:
                if self.cell_5.controller.name.lower() == "player 1":
                    subgrid = self.cell_5.card.visual_2("Player1", "PLUS")
                elif self.cell_5.controller.name.lower() == "player 2":
                    subgrid = self.cell_5.card.visual_2("Player2", "PLUS")
                else:
                    subgrid = self.cell_5.card.visual_2(self.cell_5.controller.nickname, "PLUS")
            elif self.cell_5.same:
                if self.cell_5.controller.name.lower() == "player 1":
                    subgrid = self.cell_5.card.visual_2("Player1", "SAME")
                elif self.cell_5.controller.name.lower() == "player 2":
                    subgrid = self.cell_5.card.visual_2("Player2", "SAME")
                else:
                    subgrid = self.cell_5.card.visual_2(self.cell_5.controller.nickname, "SAME")
            elif self.cell_5.combo:
                if self.cell_5.controller.name.lower() == "player 1":
                    subgrid = self.cell_5.card.visual_2("Player1", "COMBO")
                elif self.cell_5.controller.name.lower() == "player 2":
                    subgrid = self.cell_5.card.visual_2("Player2", "COMBO")
                else:
                    subgrid = self.cell_5.card.visual_2(self.cell_5.controller.nickname, "COMBO")
            else:
                if self.cell_5.controller.name.lower() == "player 1":
                    subgrid = self.cell_5.card.visual("Player1")
                elif self.cell_5.controller.name.lower() == "player 2":
                    subgrid = self.cell_5.card.visual("Player2")
                else:
                    subgrid = self.cell_5.card.visual(self.cell_5.controller.nickname)
            for y in range(9):
                for x in range(17):
                    grid[25 + x][11 + y] = subgrid[x][y]
        else:
            #Print a 5 in the top-left corner
            grid[25][11] = ["5"]

        if self.cell_6.filled:
            if self.cell_6.plus:
                if self.cell_6.controller.name.lower() == "player 1":
                    subgrid = self.cell_6.card.visual_2("Player1", "PLUS")
                elif self.cell_6.controller.name.lower() == "player 2":
                    subgrid = self.cell_6.card.visual_2("Player2", "PLUS")
                else:
                    subgrid = self.cell_6.card.visual_2(self.cell_6.controller.nickname, "PLUS")
            elif self.cell_6.same:
                if self.cell_6.controller.name.lower() == "player 1":
                    subgrid = self.cell_6.card.visual_2("Player1", "SAME")
                elif self.cell_6.controller.name.lower() == "player 2":
                    subgrid = self.cell_6.card.visual_2("Player2", "SAME")
                else:
                    subgrid = self.cell_6.card.visual_2(self.cell_6.controller.nickname, "SAME")
            elif self.cell_6.combo:
                if self.cell_6.controller.name.lower() == "player 1":
                    subgrid = self.cell_6.card.visual_2("Player1", "COMBO")
                elif self.cell_6.controller.name.lower() == "player 2":
                    subgrid = self.cell_6.card.visual_2("Player2", "COMBO")
                else:
                    subgrid = self.cell_6.card.visual_2(self.cell_6.controller.nickname, "COMBO")
            else:
                if self.cell_6.controller.name.lower() == "player 1":
                    subgrid = self.cell_6.card.visual("Player1")
                elif self.cell_6.controller.name.lower() == "player 2":
                    subgrid = self.cell_6.card.visual("Player2")
                else:
                    subgrid = self.cell_6.card.visual(self.cell_6.controller.nickname)
            for y in range(9):
                for x in range(17):
                    grid[47 + x][11 + y] = subgrid[x][y]
        else:
            #Print a 6 in the top-left corner
            grid[47][11] = ["6"]

        if self.cell_7.filled:
            if self.cell_7.plus:
                if self.cell_7.controller.name.lower() == "player 1":
                    subgrid = self.cell_7.card.visual_2("Player1", "PLUS")
                elif self.cell_7.controller.name.lower() == "player 2":
                    subgrid = self.cell_7.card.visual_2("Player2", "PLUS")
                else:
                    subgrid = self.cell_7.card.visual_2(self.cell_7.controller.nickname, "PLUS")
            elif self.cell_7.same:
                if self.cell_7.controller.name.lower() == "player 1":
                    subgrid = self.cell_7.card.visual_2("Player1", "SAME")
                elif self.cell_7.controller.name.lower() == "player 2":
                    subgrid = self.cell_7.card.visual_2("Player2", "SAME")
                else:
                    subgrid = self.cell_7.card.visual_2(self.cell_7.controller.nickname, "SAME")
            elif self.cell_7.combo:
                if self.cell_7.controller.name.lower() == "player 1":
                    subgrid = self.cell_7.card.visual_2("Player1", "COMBO")
                elif self.cell_7.controller.name.lower() == "player 2":
                    subgrid = self.cell_7.card.visual_2("Player2", "COMBO")
                else:
                    subgrid = self.cell_7.card.visual_2(self.cell_7.controller.nickname, "COMBO")
            else:
                if self.cell_7.controller.name.lower() == "player 1":
                    subgrid = self.cell_7.card.visual("Player1")
                elif self.cell_7.controller.name.lower() == "player 2":
                    subgrid = self.cell_7.card.visual("Player2")
                else:
                    subgrid = self.cell_7.card.visual(self.cell_7.controller.nickname)
            for y in range(9):
                for x in range(17):
                    grid[3 + x][21 + y] = subgrid[x][y]
        else:
            #Print a 7 in the top-left corner
            grid[3][21] = ["7"]

        if self.cell_8.filled:
            if self.cell_8.plus:
                if self.cell_8.controller.name.lower() == "player 1":
                    subgrid = self.cell_8.card.visual_2("Player1", "PLUS")
                elif self.cell_8.controller.name.lower() == "player 2":
                    subgrid = self.cell_8.card.visual_2("Player2", "PLUS")
                else:
                    subgrid = self.cell_8.card.visual_2(self.cell_8.controller.nickname, "PLUS")
            elif self.cell_8.same:
                if self.cell_8.controller.name.lower() == "player 1":
                    subgrid = self.cell_8.card.visual_2("Player1", "SAME")
                elif self.cell_8.controller.name.lower() == "player 2":
                    subgrid = self.cell_8.card.visual_2("Player2", "SAME")
                else:
                    subgrid = self.cell_8.card.visual_2(self.cell_8.controller.nickname, "SAME")
            elif self.cell_8.combo:
                if self.cell_8.controller.name.lower() == "player 1":
                    subgrid = self.cell_8.card.visual_2("Player1", "COMBO")
                elif self.cell_8.controller.name.lower() == "player 2":
                    subgrid = self.cell_8.card.visual_2("Player2", "COMBO")
                else:
                    subgrid = self.cell_8.card.visual_2(self.cell_8.controller.nickname, "COMBO")
            else:
                if self.cell_8.controller.name.lower() == "player 1":
                    subgrid = self.cell_8.card.visual("Player1")
                elif self.cell_8.controller.name.lower() == "player 2":
                    subgrid = self.cell_8.card.visual("Player2")
                else:
                    subgrid = self.cell_8.card.visual(self.cell_8.controller.nickname)
            for y in range(9):
                for x in range(17):
                    grid[25 + x][21 + y] = subgrid[x][y]
        else:
            #Print an 8 in the top-left corner
            grid[25][21] = ["8"]

        if self.cell_9.filled:
            if self.cell_9.plus:
                if self.cell_9.controller.name.lower() == "player 1":
                    subgrid = self.cell_9.card.visual_2("Player1", "PLUS")
                elif self.cell_9.controller.name.lower() == "player 2":
                    subgrid = self.cell_9.card.visual_2("Player2", "PLUS")
                else:
                    subgrid = self.cell_9.card.visual_2(self.cell_9.controller.nickname, "PLUS")
            elif self.cell_9.same:
                if self.cell_9.controller.name.lower() == "player 1":
                    subgrid = self.cell_9.card.visual_2("Player1", "SAME")
                elif self.cell_9.controller.name.lower() == "player 2":
                    subgrid = self.cell_9.card.visual_2("Player2", "SAME")
                else:
                    subgrid = self.cell_9.card.visual_2(self.cell_9.controller.nickname, "SAME")
            elif self.cell_9.combo:
                if self.cell_9.controller.name.lower() == "player 1":
                    subgrid = self.cell_9.card.visual_2("Player1", "COMBO")
                elif self.cell_9.controller.name.lower() == "player 2":
                    subgrid = self.cell_9.card.visual_2("Player2", "COMBO")
                else:
                    subgrid = self.cell_9.card.visual_2(self.cell_9.controller.nickname, "COMBO")
            else:
                if self.cell_9.controller.name.lower() == "player 1":
                    subgrid = self.cell_9.card.visual("Player1")
                elif self.cell_9.controller.name.lower() == "player 2":
                    subgrid = self.cell_9.card.visual("Player2")
                else:
                    subgrid = self.cell_9.card.visual(self.cell_9.controller.nickname)
            for y in range(9):
                for x in range(17):
                    grid[47 + x][21 + y] = subgrid[x][y]
        else:
            #Print a 9 in the top-left corner
            grid[47][21] = ["9"]

        return grid




class Game:

    def __init__(self, player1, player2, board):
        self.player1 = player1
        self.player2 = player2
        self.board = board

    def __repr__(self):
        grid = [[[" "] for i in range(31)] for j in range(177)]
        subgrid_board = self.board.board_grid()

        #Display current game board
        for y in range(31):
            for x in range(67):
                grid[x][y] = subgrid_board[x][y]

        #Display information for Player 1
        grid[78][2] = ["-"]
        grid[79+len(self.player1.name)][2] = ["-"]
        for i in range(len(self.player1.name)):
            grid[79+i][1] = [self.player1.name[i]]
            grid[79+i][2] = ["-"]

        grid[94+len(self.player1.name)][1] = [str(self.player1.points)]
        grid[96+len(self.player1.name)][1] = ["P"]
        grid[97+len(self.player1.name)][1] = ["o"]
        grid[98+len(self.player1.name)][1] = ["i"]
        grid[99+len(self.player1.name)][1] = ["n"]
        grid[100+len(self.player1.name)][1] = ["t"]
        if self.player1.points != 1:
            grid[101+len(self.player1.name)][1] = ["s"]

        for i in range(len(self.player1.hand)):
            card = self.player1.hand[i]
            subgrid_card = card.visual(card.name)

            #Start at (77, 4)
            for y in range(9):
                for x in range(17):
                    grid[77 + i*18 + x][4 + y] = subgrid_card[x][y]
            
            grid[84 + 18*i][13] = ["("]
            grid[85 + 18*i][13] = [str(i+1)]
            grid[86 + 18*i][13] = [")"]


        #Display informatin for Player 2 
        grid[78][18] = ["-"]
        grid[79+len(self.player2.name)][18] = ["-"]
        for i in range(len(self.player2.name)):
            grid[79+i][17] = [self.player2.name[i]]
            grid[79+i][18] = ["-"]

        grid[94+len(self.player2.name)][17] = [str(self.player2.points)]
        grid[96+len(self.player2.name)][17] = ["P"]
        grid[97+len(self.player2.name)][17] = ["o"]
        grid[98+len(self.player2.name)][17] = ["i"]
        grid[99+len(self.player2.name)][17] = ["n"]
        grid[100+len(self.player2.name)][17] = ["t"]
        if self.player2.points != 1:
            grid[101+len(self.player2.name)][17] = ["s"]

        for i in range(len(self.player2.hand)):
            card = self.player2.hand[i]
            subgrid_card = card.visual(card.name)

            #Start at (77, 19)
            for y in range(9):
                for x in range(17):
                    grid[77 + i*18 + x][20 + y] = subgrid_card[x][y]
                        
            grid[84 + 18*i][29] = ["("]
            grid[85 + 18*i][29] = [str(i+1)]
            grid[86 + 18*i][29] = [")"]


        output = ""
        for y in range(31):
            for x in range(177):
                output += grid[x][y][0]
            output += "\n"

        return output

# Determines how the computer will play its cards. This AI only uses
# minor heuristics.
def normal_AI(game, same, plus):
    card_to_play = choice(game.player2.hand)
    empty_cells = []
    if not game.board.cell_1.filled:
        empty_cells.append(game.board.cell_1)
    if not game.board.cell_2.filled:
        empty_cells.append(game.board.cell_2)    
    if not game.board.cell_3.filled:
        empty_cells.append(game.board.cell_3)
    if not game.board.cell_4.filled:
        empty_cells.append(game.board.cell_4)
    if not game.board.cell_5.filled:
        empty_cells.append(game.board.cell_5)
    if not game.board.cell_6.filled:
        empty_cells.append(game.board.cell_6)    
    if not game.board.cell_7.filled:
        empty_cells.append(game.board.cell_7)
    if not game.board.cell_8.filled:
        empty_cells.append(game.board.cell_8)
    if not game.board.cell_9.filled:
        empty_cells.append(game.board.cell_9)  
    
    cell_to_fill = choice(empty_cells)
    
    # Heuristic to determine placement of the first card.
    
    # Try to pick a corner card first
    if len(game.player1.hand) + len(game.player2.hand) in [9,10]:
        for i in range(1, 6):
            card = game.player2.hand[-i]
            if card.right >= 8 and card.bottom >= 8:
                if not game.board.cell_1.filled:
                    print("\nThe computer played the {} card in cell 1.".format(card.name))
                    game.player2.play_card(game.player1, card, game.board.cell_1, same, plus)
                    return
                else:
                    if card.left > game.board.cell_1.card.right:
                        print("\nThe computer played the {} card in cell 2.".format(card.name))
                        game.player2.play_card(game.player1, card, game.board.cell_2, same, plus)
                        return
                    elif card.top > game.board.cell_1.card.bottom:
                        print("\nThe computer played the {} card in cell 4.".format(card.name))
                        game.player2.play_card(game.player1, card, game.board.cell_4, same, plus)
                        return
                    else:
                        card_to_play = card
                        cell_to_fill = game.board.cell_2
            elif card.right >= 8 and card.top >= 8:
                if not game.board.cell_7.filled:
                    print("\nThe computer played the {} card in cell 7.".format(card.name))
                    game.player2.play_card(game.player1, card, game.board.cell_7, same, plus)
                    return
                else:
                    if card.left > game.board.cell_7.card.right:
                        print("\nThe computer played the {} card in cell 8.".format(card.name))
                        game.player2.play_card(game.player1, card, game.board.cell_8, same, plus)
                        return
                    elif card.bottom > game.board.cell_7.card.top:
                        print("\nThe computer played the {} card in cell 4.".format(card.name))
                        game.player2.play_card(game.player1, card, game.board.cell_4, same, plus)
                        return
                    else:
                        card_to_play = card
                        cell_to_fill = game.board.cell_8
            elif card.left >= 8 and card.top >= 8:
                if not game.board.cell_9.filled:
                    print("\nThe computer played the {} card in cell 9.".format(card.name))
                    game.player2.play_card(game.player1, card, game.board.cell_9, same, plus)
                    return
                else:
                    if card.right > game.board.cell_9.card.left:
                        print("\nThe computer played the {} card in cell 8.".format(card.name))
                        game.player2.play_card(game.player1, card, game.board.cell_8, same, plus)
                        return
                    elif card.bottom > game.board.cell_9.card.top:
                        print("\nThe computer played the {} card in cell 6.".format(card.name))
                        game.player2.play_card(game.player1, card, game.board.cell_6, same, plus)
                        return
                    else:
                        card_to_play = card
                        cell_to_fill = game.board.cell_8
            elif card.left >= 8 and card.bottom >= 8:
                if not game.board.cell_3.filled:
                    print("\nThe computer played the {} card in cell 3.".format(card.name))
                    game.player2.play_card(game.player1, card, game.board.cell_3, same, plus)
                    return
                else:
                    if card.right > game.board.cell_3.card.left:
                        print("\nThe computer played the {} card in cell 2.".format(card.name))
                        game.player2.play_card(game.player1, card, game.board.cell_2, same, plus)
                        return
                    elif card.top > game.board.cell_3.card.bottom:
                        print("\nThe computer played the {} card in cell 6.".format(card.name))
                        game.player2.play_card(game.player1, card, game.board.cell_6, same, plus)
                        return
                    else:
                        card_to_play = card
                        cell_to_fill = game.board.cell_8
        # If we get to this point, then we are trying to play our first card and haven't found
        # a corner card. We'll just play whichever card and cell are currently chosen.
        print("\nThe computer played the {} card in cell {}.".format(card_to_play.name, cell_to_fill.id))
        game.player2.play_card(game.player1, card_to_play, cell_to_fill, same, plus)
        return
    
    # For the rest of the turns, the computer will attempt to flip cards greedily. If it can't, it will
    # attempt to protect the lowest exposed side of any current card on the board.
    for i in range(len(empty_cells)):
        for j in range(len(game.player2.hand)):
            game_copy = deepcopy(game)
            empty_cells_copy = []
            if not game_copy.board.cell_1.filled:
                empty_cells_copy.append(game_copy.board.cell_1)
            if not game_copy.board.cell_2.filled:
                empty_cells_copy.append(game_copy.board.cell_2)    
            if not game_copy.board.cell_3.filled:
                empty_cells_copy.append(game_copy.board.cell_3)
            if not game_copy.board.cell_4.filled:
                empty_cells_copy.append(game_copy.board.cell_4)
            if not game_copy.board.cell_5.filled:
                empty_cells_copy.append(game_copy.board.cell_5)
            if not game_copy.board.cell_6.filled:
                empty_cells_copy.append(game_copy.board.cell_6)    
            if not game_copy.board.cell_7.filled:
                empty_cells_copy.append(game_copy.board.cell_7)
            if not game_copy.board.cell_8.filled:
                empty_cells_copy.append(game_copy.board.cell_8)
            if not game_copy.board.cell_9.filled:
                empty_cells_copy.append(game_copy.board.cell_9)

            game_copy.player2.play_card(game_copy.player1, game_copy.player2.hand[j], empty_cells_copy[i], same, plus)
            if game_copy.player2.points > game.player2.points:
                print("\nThe computer played the {} card in cell {}.".format(game.player2.hand[j].name, empty_cells[i].id))
                game.player2.play_card(game.player1, game.player2.hand[j], empty_cells[i], same, plus)
                return

    # If we make it here, then there were no cards to flip.
    num_to_cell = {
        1 : game.board.cell_1,
        2 : game.board.cell_2,
        3 : game.board.cell_3,
        4 : game.board.cell_4,
        5 : game.board.cell_5,
        6 : game.board.cell_6,
        7 : game.board.cell_7,
        8 : game.board.cell_8,
        9 : game.board.cell_9}

    lowest_value = 10
    for i in range(1, 10):
        if num_to_cell[i].filled:
            if num_to_cell[i].controller == game.player2:
                for direction, adj_cell in num_to_cell[i].neighbors.items():
                    if not adj_cell.filled:
                        if direction == "right":
                            if num_to_cell[i].card.right < lowest_value:
                                lowest_value = num_to_cell[i].card.right
                                cell_to_fill = adj_cell
                        if direction == "left":
                            if num_to_cell[i].card.left < lowest_value:
                                lowest_value = num_to_cell[i].card.left
                                cell_to_fill = adj_cell
                        if direction == "above":
                            if num_to_cell[i].card.top < lowest_value:
                                lowest_value = num_to_cell[i].card.top
                                cell_to_fill = adj_cell
                        if direction == "below":
                            if num_to_cell[i].card.bottom < lowest_value:
                                lowest_value = num_to_cell[i].card.bottom
                                cell_to_fill = adj_cell

    
    print("\nThe computer played the {} card in cell {}.".format(card_to_play.name, cell_to_fill.id))
    game.player2.play_card(game.player1, card_to_play, cell_to_fill, same, plus)

def hard_AI(game, same, plus):
    # We  want to pick the move that could reulst in the highest
    # number of points for the computer

    card_to_play = choice(game.player2.hand)

    empty_cells = []
    if not game.board.cell_1.filled:
        empty_cells.append(game.board.cell_1)
    if not game.board.cell_2.filled:
        empty_cells.append(game.board.cell_2)    
    if not game.board.cell_3.filled:
        empty_cells.append(game.board.cell_3)
    if not game.board.cell_4.filled:
        empty_cells.append(game.board.cell_4)
    if not game.board.cell_5.filled:
        empty_cells.append(game.board.cell_5)
    if not game.board.cell_6.filled:
        empty_cells.append(game.board.cell_6)    
    if not game.board.cell_7.filled:
        empty_cells.append(game.board.cell_7)
    if not game.board.cell_8.filled:
        empty_cells.append(game.board.cell_8)
    if not game.board.cell_9.filled:
        empty_cells.append(game.board.cell_9)
    
    cell_to_fill = choice(empty_cells)


    num_to_cell = {
        1 : game.board.cell_1,
        2 : game.board.cell_2,
        3 : game.board.cell_3,
        4 : game.board.cell_4,
        5 : game.board.cell_5,
        6 : game.board.cell_6,
        7 : game.board.cell_7,
        8 : game.board.cell_8,
        9 : game.board.cell_9}


    # There are still too many game combinations on the second move. The AI will only look x moves into
    # the future and try to pick a good move with that knowledge.
    if len(game.player1.hand) + len(game.player2.hand) in [7, 8, 9, 10]:
        next_plays = partial_simulate(game, same, plus, 2, 2)
        decisions = []
        for play in next_plays:
            already_there = False
            for decision in decisions:
                if decision[0] == play[0]:
                    already_there = True
                    decision[1].append(play[-1])
            if not already_there:
                decisions.append([play[0], [play[-1]]])

        best_move = decisions[0][0]
        current_average = sum(decisions[0][1])/len(decisions[0][1])
        for i in range(len(decisions)):
            next_average = sum(decisions[i][1])/len(decisions[i][1])
            if next_average > current_average:
                current_average = next_average
                best_move = decisions[i][0]

        print("\nThe computer played the {} card in cell {}.".format(game.player2.hand[best_move[1]].name, best_move[2]))
        game.player2.play_card(game.player1, game.player2.hand[best_move[1]], num_to_cell[best_move[2]], same, plus)
        return


    # We want to choose the next play by looking far into the future.
    moves_left = len(game.player1.hand) + len(game.player2.hand) - 1
    next_plays = partial_simulate(game, same, plus, 2, moves_left)
    decisions = []
    # We add any next move to the list of possible move for which
    # there is any sequence of further moves that results in a win.
    for play in next_plays:
        already_there = False
        if play[-1] >= 6:
            for decision in decisions:
                if decision[0] == play[0]:
                    already_there = True
                    decision[1] += 1 # Our next move will be the one with the most ways to win afterwords
            if not already_there:
                decisions.append([play[0], 1])
    
    # If decisions is empty, then there's no way to win. Try to draw instead.
    if decisions == []:
        for play in next_plays:
            already_there = False
            if play[-1] == 5:
                for decision in decisions:
                    if decision[0] == play[0]:
                        already_there = True
                        decision[1] += 1
                if not already_there:
                    decisions.append([play[0], 1])

    # If decisions is still empty, then we lose regardless. Just place a random card in a
    # random cell.
    if decisions == []:
        print("\nThe computer played the {} card in cell {}.".format(card_to_play.name, cell_to_fill.id))
        game.player2.play_card(game.player1, card_to_play, cell_to_fill, same, plus)
        return

    # We want to pick the next move with the largest number of wins following it.
    largest_number = 0
    best_choice = False
    for decision in decisions:
        if decision[1] > largest_number:
            best_choice = decision[0]


    print("\nThe computer played the {} card in cell {}.".format(game.player2.hand[best_choice[1]].name, best_choice[2]))
    game.player2.play_card(game.player1, game.player2.hand[best_choice[1]], num_to_cell[best_choice[2]], same, plus)



# Player is the player (1 or 2) whose turn it is when this function is called.
# Moves is the number of moves I want to project into the future.
def partial_simulate(game, same, plus, player, moves):
    # plays will keep track of all game possibilities. It is a list of 'games', where
    # each 'game' is a list of 'plays'. Each play is a list [#, card, cell], where # is the
    # player, card refers to the card being played from the player's hand, and cell refers
    # to the empty cell where the card is being played.
    plays = []
    empty_cells = []
    if not game.board.cell_1.filled:
        empty_cells.append(1)
    if not game.board.cell_2.filled:
        empty_cells.append(2)    
    if not game.board.cell_3.filled:
        empty_cells.append(3)
    if not game.board.cell_4.filled:
        empty_cells.append(4)
    if not game.board.cell_5.filled:
        empty_cells.append(5)
    if not game.board.cell_6.filled:
        empty_cells.append(6)    
    if not game.board.cell_7.filled:
        empty_cells.append(7)
    if not game.board.cell_8.filled:
        empty_cells.append(8)
    if not game.board.cell_9.filled:
        empty_cells.append(9)

    counter = -1

    # In this case, Player 2 went first and it is currently Player 2's turn.
    if (player == 2) and (moves % 2 == 1):
        for cell_orders in list(permutations(empty_cells, moves)):
            for player2_card_orders in list(permutations(range(len(game.player2.hand)),int((moves+1)/2))):
                for player1_card_orders in list(permutations(range(len(game.player1.hand)),int((moves-1)/2))):
                    plays.append([])
                    counter += 1
                    for i in range(len(player2_card_orders)):
                        plays[counter].append([2, player2_card_orders[i], cell_orders[2*i]])
                        if i < len(player2_card_orders)-1:
                            plays[counter].append([1, player1_card_orders[i], cell_orders[2*i+1]])
    # In this case, Player 1 went first and it is currently Player 2's turn.
    elif (player == 2) and (moves % 2 == 0):
        for cell_orders in list(permutations(empty_cells, moves)):
            for player2_card_orders in list(permutations(range(len(game.player2.hand)),int(moves/2))):
                for player1_card_orders in list(permutations(range(len(game.player1.hand)),int(moves/2))):
                    plays.append([])
                    counter += 1
                    for i in range(len(player1_card_orders)):
                        plays[counter].append([2, player2_card_orders[i], cell_orders[2*i]])
                        plays[counter].append([1, player1_card_orders[i], cell_orders[2*i+1]])
    # In this case, Player 1 went first and it is currently Player 1's turn.
    elif (player == 1) and (moves % 2 == 1):
        for cell_orders in list(permutations(empty_cells, moves)):
            for player2_card_orders in list(permutations(range(len(game.player2.hand)),int((moves-1)/2))):
                for player1_card_orders in list(permutations(range(len(game.player1.hand)),int((moves+1)/2))):
                    plays.append([])
                    counter += 1
                    for i in range(len(player1_card_orders)):
                        plays[counter].append([1, player1_card_orders[i], cell_orders[2*i]])
                        if i < len(player1_card_orders)-1:
                            plays[counter].append([2, player2_card_orders[i], cell_orders[2*i+1]])
    # In this case, Player 2 went first and it is currently Player 1's turn.
    elif (player == 1) and (moves % 2 == 0):
        for cell_orders in list(permutations(empty_cells, moves)):
            for player2_card_orders in list(permutations(range(len(game.player2.hand)),int(moves/2))):
                for player1_card_orders in list(permutations(range(len(game.player1.hand)),int(moves/2))):
                    plays.append([])
                    counter += 1
                    for i in range(len(player2_card_orders)):
                        plays[counter].append([1, player1_card_orders[i], cell_orders[2*i]])
                        plays[counter].append([2, player2_card_orders[i], cell_orders[2*i+1]])
                    
    # There is an indexing issue with the plays because the cards in player's hand are constantly
    # changing index. For example, if the first card in the hand is played, then
    # card 5 becomes card 4 afterwords. This needs to be carefully fixed.

    for playthrough in plays:
        if moves % 2 == 0:
            for i in range(int(moves/2)-1):
                for j in range(i+1, int(moves/2)):
                    if playthrough[2*j][1] > playthrough[2*i][1]:
                        playthrough[2*j][1] -= 1
                    if playthrough[2*j+1][1] > playthrough[2*i+1][1]:
                        playthrough[2*j+1][1] -= 1
        else:
            for i in range(int((moves-1)/2)):
                for j in range(i+1, int((moves+1)/2)):
                    if playthrough[2*j][1] > playthrough[2*i][1]:
                        playthrough[2*j][1] -= 1
                    if j < int((moves-1)/2):
                        if playthrough[2*j+1][1] > playthrough[2*i+1][1]:
                            playthrough[2*j+1][1] -= 1
            
    # Now that plays is fixed, I will use it to simulate the next few rounds.

    for playthrough in plays:
        game_copy = deepcopy(game)
        num_to_cell = {
            1 : game_copy.board.cell_1,
            2 : game_copy.board.cell_2,
            3 : game_copy.board.cell_3,
            4 : game_copy.board.cell_4,
            5 : game_copy.board.cell_5,
            6 : game_copy.board.cell_6,
            7 : game_copy.board.cell_7,
            8 : game_copy.board.cell_8,
            9 : game_copy.board.cell_9}

        for play in playthrough:
            if play[0] == 1:
                player = game_copy.player1
                opponent = game_copy.player2
            else:
                player = game_copy.player2
                opponent = game_copy.player1
            player.play_card(opponent, player.hand[play[1]], num_to_cell[play[2]], same, plus)

        #The AI is Player 2, so I want to know how many points it has after these moves
        playthrough.append(game_copy.player2.points)
    
    return plays
    



# Takes in a list of exactly 3 cards and returns a string to
# print the cards in the list in an organized fashion.
def show_3_choices(possible_cards):
    choice_grid = [[[" "] for i in range(10)] for j in range(60)]

    for i in range(3):
        for y in range(9):
            for x in range(17):
                choice_grid[18*i + x][y] = possible_cards[i].visual(possible_cards[i].name)[x][y]

        choice_grid[7 + 18*i][9] = ["("]
        choice_grid[8 + 18*i][9] = [str(i+1)]
        choice_grid[9 + 18*i][9] = [")"]

    card_choice = ""
    for y in range(10):
        for x in range(60):
            card_choice += choice_grid[x][y][0]
        card_choice += "\n"

    return card_choice


# Takes in a list of exactly 11 cards and returns a string to
# print the cards in the list in an organized fashion.
def show_11_choices(possible_cards):
    choice_grid = [[[" "] for i in range(21)] for j in range(170)]

    topcards = [possible_cards[i] for i in range(5)]
    bottomcards = [possible_cards[i] for i in range(5, 10)]
    
    for i in range(5):
        for y in range(9):
            for x in range(17):
                choice_grid[18*i + x][y] = topcards[i].visual(topcards[i].name)[x][y]
        
        choice_grid[7 + 18*i][9] = ["("]
        choice_grid[8 + 18*i][9] = [str(i+1)]
        choice_grid[9 + 18*i][9] = [")"]

        for y in range(9):
            for x in range(17):
                choice_grid[18*i + x][11 + y] = bottomcards[i].visual(bottomcards[i].name)[x][y]
        
        choice_grid[7 + 18*i][20] = ["("]
        choice_grid[8 + 18*i][20] = [str(i+6)]
        choice_grid[9 + 18*i][20] = [")"]

    for y in range(9):
        for x in range(17):
            choice_grid[90 + x][5 + y] = possible_cards[10].visual(possible_cards[10].name)[x][y]

    choice_grid[97][14] = ["("]
    choice_grid[98][14] = ["11"]
    choice_grid[99][14] = [")"]


    card_choice = ""
    for y in range(21):
        for x in range(170):
            card_choice += choice_grid[x][y][0]
        card_choice += "\n"

    return card_choice

# Subroutine to have a player choose 5 cards out of 11 cards that are shown.
# Takes in a string and list of exactly 11 cards. Returns a list of cards.
def choose_5_of_11(player_name, possible_cards, single_player):
    choices = [str(i) for i in range(1, 12)]
    num_to_card = {}
    for i in range(11):
        num_to_card[str(i+1)] = possible_cards[i]

    good_to_go = False
    while not good_to_go:
        player_card_list = []
        while len(player_card_list) != 5:
            if len(player_card_list) == 0:
                if single_player:
                    card_input = input("Please choose 5 cards to play with. Enter the numbers for the cards you want separated by commas. ").split(",")
                else:
                    card_input = input("{}, please choose 5 cards to play with. Enter the numbers for the cards you want separated by commas. ".format(player_name)).split(",")
                for card in card_input:
                    if card.strip() in choices:
                        player_card_list.append(card)
            elif len(player_card_list) < 5:
                print("{}, you currently have the following cards in your hand:\n".format(player_name))
                for card in player_card_list:
                    print(num_to_card[card.strip()].name)
                print("\n")
                num_left = 5-len(player_card_list)
                if num_left == 1:
                    card_input = input("Please select " + str(num_left) + " more card. ").split(",")
                else:
                    card_input =  input("Please select " + str(num_left) + " more cards. ").split(",")

                for card in card_input:
                    if card.strip() in choices:
                        player_card_list.append(card)
            else:
                print("You can only select 5 cards.")
                player_card_list = []

        current_cards = "You have the following cards in your hand: "
        for i in range(5):
            if i != 4:
                current_cards += num_to_card[player_card_list[i].strip()].name + ", "
            else:
                current_cards += num_to_card[player_card_list[i].strip()].name + "."
        print(current_cards)
        check_on_check = False
        while not check_on_check:
            check = input("Is this good? (y/n) ")
            if check.lower() in ["y", "yes", "n", "no"]:
                check_on_check = True
                if check.lower() in ["y", "yes"]:
                    good_to_go = True
                    hand = [num_to_card[player_card_list[i].strip()] for i in range(5)]
                    return hand

# Prints the 11 cards of the possible_cards list.
# Asks the user to select 5.
# Returns a list of these 5 cards.
def choose_5(player_name, possible_cards, single_player):
    print(show_11_choices(possible_cards))
    print("\n\nThe card choices are shown above.")
    return choose_5_of_11(player_name, possible_cards, single_player)

# Prints the 3 cards of the possible_cards list.
# Asks the user to select the one card they don't want.
# Returns a list of the 2 selected cards.
def choose_2_of_3(player_name, possible_cards, single_player):
    print(show_3_choices(possible_cards))
    choices = [str(i) for i in range(1, 4)]

    good_to_go = False
    while not good_to_go:
        expected = False
        while not expected:
            if single_player:
                card_to_remove = input("Two of these cards will be added to your hand. Enter the number for the card that you don't want. ")
            else:
                card_to_remove = input("{}, two of these cards will be added to your hand. Enter the number for the card that you don't want. ".format(player_name))
            if card_to_remove.strip() in choices:
                expected = True
                hand = [possible_cards[i] for i in range(3) if str(i+1) != card_to_remove.strip()]
                check = False
                while not check:
                    check_input = input("You are adding the {} and {} cards to your hand. Is this ok? (y/n) ".format(hand[0].name, hand[1].name))
                    if check_input.lower() in ["y", "yes", "n", "no"]:
                        check = True
                        if check_input.lower() in ["y", "yes"]:
                            good_to_go = True
                            return hand

# Shows all 11 cards of the possible_cards list.
# Asks the user which card they want to add to their hand.
# Returns a list of length 1 with exactly that card.
def choose_1_of_11(player_name, possible_cards, single_player):
    print(show_11_choices(possible_cards))
    choices = [str(i) for i in range(1, 12)]

    good_to_go = False
    while not good_to_go:
        expected = False
        while not expected:
            if single_player:
                card_to_add = input("Select one of these 11 cards to add to your hand. Enter the number for the card that you want. ")
            else:
                card_to_add = input("{}, select one of these 11 cards to add to your hand. Enter the number for the card that you want. ".format(player_name))
            if card_to_add.strip() in choices:
                expected = True
                hand = [possible_cards[int(card_to_add.strip()) - 1]]
                check = False
                while not check:
                    check_input = input("You are adding the {} card to your hand. Is this ok? (y/n) ".format(hand[0].name))
                    if check_input.lower() in ["y", "yes", "n", "no"]:
                        check = True
                        if check_input.lower() in ["y", "yes"]:
                            good_to_go = True
                            return hand
    


def play():
    draw_option = 0
    plus = False
    same = False
    AI_normal = True
    player1_name = ""
    player1_nickname = ""
    player2_name = ""
    player2_nickname = ""

    good_to_go = False
    print("----------------")
    print("  Triple Triad  ")
    print("----------------")
    print("Written by Stephen Smith, 2022.\n")
    
    while not good_to_go:
        expected = False
        while not expected:
            print("Welcome! At any point during the game setup, type 'help' to see the instructions.\n")
            game_type = input("Would you like to play a one or two player game? ")
            if game_type.strip().lower() in ["1", "2", "one", "two", "x", "exit", "one player", "1 player", "two player", "2 player", "h", "help", "instructions"]:
                expected = True
                if game_type.strip().lower() in ["h", "help", "instructions"]:
                    instructions()
                    play()
                    return

                if game_type.strip().lower() in ["x", "exit"]:
                    print("See you next time!")
                    good_to_go = True
                    break

                expected_2 = False
                print("\nThere are four options for drawing hands:")
                print("  (1) Each player may choose 5 high-level cards.")
                print("  (2) Through a draft system, both players will choose 2 low-level cards, 2 mid-level cards, and 1 high-level card.")
                print("  (3) Each player will randomly be given 2 low-level cards, 2 mid-level cards, and 1 high-level card.")
                print("  (4) Each player will be given 5 random cards of any level.\n")
                while not expected_2:
                    
                    draw_choice = input("Which draw option would you like to use? Enter the number of your choice. ")
                    if draw_choice.strip().lower() in ["1", "one", "option 1", "option one",\
                        "2", "two", "option 2", "option two", "3", "three", "option 3", "option three", "4", "four", "option 4", "option four", "h", "help", "instructions"]:
                    
                        expected_2 = True

                        if draw_choice.strip().lower() in ["h", "help", "instructions"]:
                            instructions()
                            play()
                            return
                    
                        if draw_choice.strip().lower() in ["1", "one", "option 1", "option one"]:
                            draw_option = 1
                        elif draw_choice.strip().lower() in ["2", "two", "option 2", "option two"]:
                            draw_option = 2
                        elif draw_choice.strip().lower() in ["3", "three", "option 3", "option three"]:
                            draw_option = 3
                        elif draw_choice.strip().lower() in ["4", "four", "option 4", "option four"]:
                            draw_option = 4

                        expected_3 = False
                        while not expected_3:
                            same_option = input("Would you like to add the 'Same' rule to the gameplay? (y/n) ")
                            if same_option.strip().lower() in ["y", "yes", "n", "no", "h", "help", "instructions"]:
                                expected_3 = True

                                if same_option.strip().lower() in ["h", "help", "instructions"]:
                                    instructions()
                                    play()
                                    return

                                if same_option.strip().lower() in ["yes", "y"]:
                                    same = True
                            
                                expected_4 = False
                                while not expected_4:
                                    plus_option = input("Would you like to add the 'Plus' rule to the gameplay? (y/n) ")
                                    if plus_option.strip().lower() in ["y", "yes", "n", "no", "h", "help", "instructions"]:
                                        
                                        expected_4 = True

                                        if plus_option.strip().lower() in ["h", "help", "instructions"]:
                                            instructions()
                                            play()
                                            return

                                        if plus_option.strip().lower() in ["yes", "y"]:
                                            plus = True

                                        if game_type.strip().lower() in ["1", "one", "one player", "1 player"]:
                                            expected_5 = False
                                            print("\nThere are two distinct AI's to choose from:")
                                            print("  (1) Aggressive AI")
                                            print("  (2) Defensive AI\n")
                                            while not expected_5:
                                                ai_option = input("Which AI would you like to play against? Enter the number of your choice. ")
                                                if ai_option.lower().strip() in ["1", "one", "2", "two", "h", "help", "instructions"]:
                                                    
                                                    expected_5 = True
                                                    
                                                    if ai_option.strip().lower() in ["h", "help", "instructions"]:
                                                        instructions()
                                                        play()
                                                        return

                                                    if ai_option.lower().strip() in ["2", "two"]:
                                                        AI_normal = False

                                                    check = False
                                                    while not check:
                                                        if (not same) and (not plus):
                                                            if AI_normal:
                                                                check_input = input("You have chosen to play single-player against the aggressive AI with no additional rules and draw option {}. Is this okay? (y/n) ".format(str(draw_option)))
                                                            else:
                                                                check_input = input("You have chosen to play single-player against the defensive AI with no additional rules and draw option {}. Is this okay? (y/n) ".format(str(draw_option)))
                                                            if check_input.strip().lower() in ["y", "yes", "n", "no",  "h", "help", "instructions"]:
                                                                check = True
                                                                if check_input.strip().lower() in ["h", "help", "instructions"]:
                                                                    instructions()
                                                                    play()
                                                                    return
                                                                if check_input.strip().lower() in ["yes", "y"]:
                                                                    good_to_go = True
                                                                    play_type1(draw_option, same, plus, AI_normal, player1_name, player1_nickname)
                                                        elif same and (not plus):
                                                            if AI_normal:
                                                                check_input = input("You have chosen to play single-player against the aggressive AI with the 'Same' rule and draw option {}. Is this okay? (y/n) ".format(str(draw_option)))
                                                            else:
                                                                check_input = input("You have chosen to play single-player against the defensive AI with the 'Same' rule and draw option {}. Is this okay? (y/n) ".format(str(draw_option)))
                                                            if check_input.strip().lower() in ["y", "yes", "n", "no",  "h", "help", "instructions"]:
                                                                check = True
                                                                if check_input.strip().lower() in ["h", "help", "instructions"]:
                                                                    instructions()
                                                                    play()
                                                                    return
                                                                if check_input.strip().lower() in ["yes", "y"]:
                                                                    good_to_go = True
                                                                    play_type1(draw_option, same, plus, AI_normal, player1_name, player1_nickname)
                                                        elif (not same) and plus:
                                                            if AI_normal:
                                                                check_input = input("You have chosen to play single-player against the aggressive AI with the 'Plus' rule and draw option {}. Is this okay? (y/n) ".format(str(draw_option)))
                                                            else:
                                                                check_input = input("You have chosen to play single-player against the defensive AI with the 'Plus' rule and draw option {}. Is this okay? (y/n) ".format(str(draw_option)))
                                                            if check_input.strip().lower() in ["y", "yes", "n", "no",  "h", "help", "instructions"]:
                                                                check = True
                                                                if check_input.strip().lower() in ["h", "help", "instructions"]:
                                                                    instructions()
                                                                    play()
                                                                    return
                                                                if check_input.strip().lower() in ["yes", "y"]:
                                                                    good_to_go = True
                                                                    play_type1(draw_option, same, plus, AI_normal, player1_name, player1_nickname)
                                                        elif same and plus:
                                                            if AI_normal:
                                                                check_input = input("You have chosen to play single-player against the aggressive AI with the 'Same' and 'Plus' rules and draw option {}. Is this okay? (y/n) ".format(str(draw_option)))
                                                            else:
                                                                check_input = input("You have chosen to play single-player against the defensive AI with the 'Same' and 'Plus' rules and draw option {}. Is this okay? (y/n) ".format(str(draw_option)))
                                                            if check_input.strip().lower() in ["y", "yes", "n", "no",  "h", "help", "instructions"]:
                                                                check = True
                                                                if check_input.strip().lower() in ["h", "help", "instructions"]:
                                                                    instructions()
                                                                    play()
                                                                    return
                                                                if check_input.strip().lower() in ["yes", "y"]:
                                                                    good_to_go = True
                                                                    play_type1(draw_option, same, plus, AI_normal, player1_name, player1_nickname)        
                                        else:
                                            check = False
                                            while not check:
                                                if (not same) and (not plus):
                                                    check_input = input("You have chosen to play two-player with no additional rules and draw option {}. Is this okay? (y/n) ".format(str(draw_option)))
                                                    if check_input.strip().lower() in ["y", "yes", "n", "no",  "h", "help", "instructions"]:
                                                        check = True
                                                        if check_input.strip().lower() in ["h", "help", "instructions"]:
                                                            instructions()
                                                            play()
                                                            return
                                                        if check_input.strip().lower() in ["yes", "y"]:
                                                            good_to_go = True
                                                            play_type2(draw_option, same, plus, player1_name, player1_nickname, player2_name, player2_nickname)
                                                elif same and (not plus):
                                                    check_input = input("You have chosen to play two-player with the 'Same' rule and draw option {}. Is this okay? (y/n) ".format(str(draw_option)))
                                                    if check_input.strip().lower() in ["y", "yes", "n", "no",  "h", "help", "instructions"]:
                                                        check = True
                                                        if check_input.strip().lower() in ["h", "help", "instructions"]:
                                                            instructions()
                                                            play()
                                                            return
                                                        if check_input.strip().lower() in ["yes", "y"]:
                                                            good_to_go = True
                                                            play_type2(draw_option, same, plus, player1_name, player1_nickname, player2_name, player2_nickname)
                                                elif (not same) and plus:
                                                    check_input = input("You have chosen to play two-player with the 'Plus' rule and draw option {}. Is this okay? (y/n) ".format(str(draw_option)))
                                                    if check_input.strip().lower() in ["y", "yes", "n", "no",  "h", "help", "instructions"]:
                                                        check = True
                                                        if check_input.strip().lower() in ["h", "help", "instructions"]:
                                                            instructions()
                                                            play()
                                                            return
                                                        if check_input.strip().lower() in ["yes", "y"]:
                                                            good_to_go = True
                                                            play_type2(draw_option, same, plus, player1_name, player1_nickname, player2_name, player2_nickname)
                                                elif same and plus:
                                                    check_input = input("You have chosen to play two-player with the 'Same' and 'Plus' rules and draw option {}. Is this okay? (y/n) ".format(str(draw_option)))
                                                    if check_input.strip().lower() in ["y", "yes", "n", "no",  "h", "help", "instructions"]:
                                                        check = True
                                                        if check_input.strip().lower() in ["h", "help", "instructions"]:
                                                            instructions()
                                                            play()
                                                            return
                                                        if check_input.strip().lower() in ["yes", "y"]:
                                                            good_to_go = True
                                                            play_type2(draw_option, same, plus, player1_name, player1_nickname, player2_name, player2_nickname)

#Instructions
def instructions():
    print("------------")
    print("INSTRUCTIONS")
    print("------------")

    print("\nAt any point during the instructions, type 'exit' to return to game setup.\n")

    check = input("Press enter to continue. ")
    if check.strip().lower() in ["x", "exit"]:
        return

    example_player1_1 = Player("Player 1", [buel, ochu, tripoint, chimera, rinoa])
    example_player2_1 = Player("Player 2", [creeps, tonberry, behemoth, iguion, squall])
    example_board_1 = Board()
    example_game_1 = Game(example_player1_1, example_player2_1, example_board_1)
    print("\nTriple Triad is a mini-game that was developed by Squaresoft and introduced in Final Fantasy VIII.\n")
    print("It is a two-player card game in which both players are given five cards, and every card has a value on each of it's four sides.\n")
    print("The values range from 1 to 10, with 'A' being 10.\n")
    print("See an example card below.\n")
    print(seifer)
    check = input("Press enter to continue. ")
    if check.strip().lower() in ["x", "exit"]:
        return

    print("\nThroughout the game, each player will take turns placing a card from their hand onto the board.\n")
    print("The starting player is chosen randomly.\n")
    check = input("Press enter to see the board below. ")
    if check.strip().lower() in ["x", "exit"]:
        return
    print(example_board_1)
    check = input("Press enter to continue. ")
    if check.strip().lower() in ["x", "exit"]:
        return

    print("\nEach player starts off by 'controlling' the five cards in their hand.")
    print("A player's points is equal to the number of cards that they currently control.\n")
    print("The goal of the game is to control more cards than your opponent, and thus have more points.\n")
    print("When placing a card onto the board, if your opponent controls an adjacent cell and the card that you're")
    print("placing has a higher value between the two sides that are touching, the opponent's card is captured.\n")
    print("Multiple cards can be captured at once.\n")

    check = input("Press enter to see an example. ")
    if check.strip().lower() in ["x", "exit"]:
        return

    example_player1_1.play_card(example_player2_1, buel, example_board_1.cell_8, False, False)
    example_player2_1.play_card(example_player1_1, tonberry, example_board_1.cell_1, False, False)

    print(example_game_1)
    print("\nIt's currently Player 1's turn. If Player 1 plays the Ochu card in cell 4, then it's top")
    print("value of 5 is being compared against the bottom value of 4 from the card in cell 1.\n")

    print("Since 5 > 4, the top card is captured and now controlled by Player 1. As a result,")
    print("Player 1 gains a point, while Player 2 loses a point.\n")
    
    check = input("Press enter to see the Ochu card get played. ")
    if check.strip().lower() in ["x", "exit"]:
        return
    example_player1_1.play_card(example_player2_1, ochu, example_board_1.cell_4, False, False)
    print(example_game_1)
    check = input("Press enter to continue. ")
    if check.strip().lower() in ["x", "exit"]:
        return

    print("\nIn the game setup, you can decide to play two-player against a friend, or")
    print("single-player against the AI.\n")

    print("For single-player mode, there are two distinct AI's:\n")
    print("The first AI is aggressive and prioritizes capturing cards when it can.\n")
    print("The second AI is more defensive and will try to outmaneuver you.\n")

    check = input("Press enter to continue. ")
    if check.strip().lower() in ["x", "exit"]:
        return

    print("\nIn addition to the normal rules for capturing cards, you may choose to have")
    print("the additional rules of 'Same' and/or 'Plus' active.\n")

    check = input("Press enter to continue. ")
    if check.strip().lower() in ["x", "exit"]:
        return

    print("\nIf the 'Same' rule is active, then any time you place a card on the board, all pairs of cells")
    print("adjacent to that card are checked. When the played card is touching two cards already on the board,")
    print("and the touching sides have the same value (separately for both cards), those cards are")
    print("captured. If one of the two cards is already controlled by you, then you still capture the")
    print("other card. If both cards are already controlled by you, then nothing happens.\n")

    print("Any cards captured via the 'Same' rule are treated as if you just played them. They are")
    print("able to capture adjacent cards, but only with the normal capturing rules. Any cards captured")
    print("thusly are also treated as if you had just played them. This can cause a chain reaction")
    print("called a 'Combo'.\n")

    check = input("Press enter to see an example. ")
    if check.strip().lower() in ["x", "exit"]:
        return

    example_player1_2 = Player("Player 1", [malboro, behemoth, iguion, cactuar, edea])
    example_player2_2 = Player("Player 2", [zell, irvine, grendel, abadon, creeps])
    example_board_2 = Board()
    example_game_2 = Game(example_player1_2, example_player2_2, example_board_2)
    example_player2_2.play_card(example_player1_2, grendel, example_board_2.cell_4, True, False)
    example_player1_2.play_card(example_player2_2, behemoth, example_board_2.cell_2, True, False)
    example_player2_2.play_card(example_player1_2, irvine, example_board_2.cell_7, True, False)
    example_player1_2.play_card(example_player2_2, iguion, example_board_2.cell_8, True, False)
    example_player2_2.play_card(example_player1_2, zell, example_board_2.cell_5, True, False)
    example_player1_2.play_card(example_player2_2, edea, example_board_2.cell_6, True, False)
    example_player2_2.play_card(example_player1_2, creeps, example_board_2.cell_9, True, False)

    print(example_game_2)
    print("\nIt's currently Player 1's turn and Player 1 wants to play the Malboro card in Cell 1.\n")
    print("The bottom value of the Malboro card is equal to the top value of the card in Cell 4 AND the")
    print("right value of the Malboro card is equal to the left value of the card in Cell 2. Thus, the")
    print("'Same' rule will apply, and the cards in both Cells 2 and 4 are captured by Player 1.\n")

    print("Furthermore, the newly controled card in Cell 4 is strong enough to capture the card")
    print("in Cell 7, which is strong enough to capture the card in Cell 8. The chain reaction ends")
    print("at that point.\n")

    check = input("Press enter to see the Malboro card get played. ")
    if check.strip().lower() in ["x", "exit"]:
        return
    example_player1_2.play_card(example_player2_2, malboro, example_board_2.cell_1, True, False)
    print(example_game_2)
    
    check = input("Press enter to continue. ")
    if check.strip().lower() in ["x", "exit"]:
        return

    print("\nIf the 'Plus' rule is active, then any time you place a card on the board, all pairs of cells")
    print("adjacent to that card are checked. When the played card is touching two cards already on the board,")
    print("and the two touching sides sum to the same value, those cards are captured. If one of the")
    print("two cards is already controlled by you, then you still capture the other card. If both cards")
    print("are already controlled by you, then nothing happens.\n")

    print("Any cards captured via the 'Plus' rule can trigger a 'Combo' in the same way as the 'Same' rule.\n")

    check = input("Press enter to see an example. ")
    if check.strip().lower() in ["x", "exit"]:
        return

    example_player1_3 = Player("Player 1", [abadon, laguna, chimera, elnoyle, blobra])
    example_player2_3 = Player("Player 2", [cactuar, ward, jelleye, tiamat, tonberry])
    example_board_3 = Board()
    example_game_3 = Game(example_player1_3, example_player2_3, example_board_3)
    example_player1_3.play_card(example_player2_3, abadon, example_board_3.cell_1, False, True)
    example_player2_3.play_card(example_player1_3, tonberry, example_board_3.cell_4, False, True)
    example_player1_3.play_card(example_player2_3, laguna, example_board_3.cell_5, False, True)
    example_player2_3.play_card(example_player1_3, tiamat, example_board_3.cell_6, False, True)
    example_player1_3.play_card(example_player2_3, chimera, example_board_3.cell_9, False, True)
    example_player2_3.play_card(example_player1_3, jelleye, example_board_3.cell_7, False, True)
    example_player1_3.play_card(example_player2_3, blobra, example_board_3.cell_8, False, True)

    print(example_game_3)

    print("\nIt's currently Player 2's turn and Player 2 wants to play the Cactuar card in Cell 2.\n")
    print("The bottom value of the Cactuar card plus the top value of the card in Cell 5 sum to 11.")
    print("The left value of the Cactuar card plus to right value of the card in Cell 1 also sum to 11.")
    print("The 'Plus' rule will capture both cards in Cells 1 and 5.\n")
    print("Either of these newly controlled cards are strong enough to capture the card in Cell 4, which")
    print("is strong enough to capture the card in Cell 7.\n")
    print("The card in Cell 5 is also strong enough to capture the cards in Cells 6 and 8. The chain")
    print("reaction ends there.\n")

    check = input("Press enter to see the Cactuar card get played. ")
    if check.strip().lower() in ["x", "exit"]:
        return
    example_player2_3.play_card(example_player1_3, cactuar, example_board_3.cell_2, False, True)
    print(example_game_3)
    
    check = input("Press enter to continue. ")
    if check.strip().lower() in ["x", "exit"]:
        return

    print("\nThat's it for the rules. Have fun!\n")
    print("-----------------------------------------\n")




#A single-player game.
def play_type1(draw_option, same, plus, AI_normal, player1_name, player1_nickname):
    print("\nOK!")
    while len(player1_name) == 0:
        player1_name = input("Please enter your name. ")
    if len(player1_name) > 7 and len(player1_nickname) == 0:
        player1_nickname = player1_name
        while len(player1_nickname) > 7 or len(player1_nickname) == 0:
            player1_nickname = input("Please enter a nickname of at most 7 characters. This will appear on cards that you control on the board. ")
    
    if draw_option == 1:
        hand1 = choose_5(player1_name, high_levels, True)
        CPU_hand = sample(high_levels, 5)
    elif draw_option == 2:
        hand1 = []
        hand1 += choose_2_of_3(player1_name, sample(low_levels, 3), True)
        hand1 += choose_2_of_3(player1_name, sample(mid_levels, 3), True)
        hand1 += choose_1_of_11(player1_name, high_levels, True)
        CPU_hand = sample(low_levels, 2) + sample(mid_levels, 2) + sample(high_levels, 1)
    elif draw_option == 3:
        hand1 = sample(low_levels, 2) + sample(mid_levels, 2) + sample(high_levels, 1)
        CPU_hand = sample(low_levels, 2) + sample(mid_levels, 2) + sample(high_levels, 1)
    else:
        hand1 = sample(full_deck, 5)
        CPU_hand = sample(full_deck, 5)

    print("\n")
    print("Perfect. Let's get started!")
    player1 = Player(player1_name, hand1)
    if len(player1.name) > 7:
        player1.nickname = player1_nickname

    player2 = Player("The computer", CPU_hand)
    player2.nickname = "CPU"

    board = Board()
    game = Game(player1, player2, board)

    num_to_cell = {
        "1": board.cell_1,
        "2": board.cell_2,
        "3": board.cell_3,
        "4": board.cell_4,
        "5": board.cell_5,
        "6": board.cell_6,
        "7": board.cell_7,
        "8": board.cell_8,
        "9": board.cell_9}
    
    starter = randint(1, 2)
    if starter == 1:
        print("This time, you will go first.")

        for i in range(9):
            if i % 2 == 0:
                good_to_go = False
                print(game)
                # Keeps track of cards flipped by 'Same', 'Plus', or 'Combo'
                # on the previous turn. After it displays that game state,
                # we want the cards to display as normal on the next round.
                board.cell_1.combo = False
                board.cell_2.combo = False
                board.cell_3.combo = False
                board.cell_4.combo = False
                board.cell_5.combo = False
                board.cell_6.combo = False
                board.cell_7.combo = False
                board.cell_8.combo = False
                board.cell_9.combo = False
                
                board.cell_1.plus = False
                board.cell_2.plus = False
                board.cell_3.plus = False
                board.cell_4.plus = False
                board.cell_5.plus = False
                board.cell_6.plus = False
                board.cell_7.plus = False
                board.cell_8.plus = False
                board.cell_9.plus = False
                
                board.cell_1.same = False
                board.cell_2.same = False
                board.cell_3.same = False
                board.cell_4.same = False
                board.cell_5.same = False
                board.cell_6.same = False
                board.cell_7.same = False
                board.cell_8.same = False
                board.cell_9.same = False
                
                while not good_to_go:
                    num_check = False
                    while not num_check:
                        if len(player1.hand) > 1:
                            print("{}, choose a card to play from your hand.".format(player1.name))
                            card_to_play = input("Select the number under the card that you want to play. ")
                        else:
                            card_to_play = "1"
                        if card_to_play.strip() in [str(i+1) for i in range(len(player1.hand))]:
                            num_check = True
                            card_to_play = player1.hand[int(card_to_play) - 1]
                            cell_check = False
                            while not cell_check:
                                cell_to_fill = input("Please select an empty cell to place the {} card into. ".format(card_to_play.name))
                                if (cell_to_fill.strip() in [str(i+1) for i in range(9)]) and (not num_to_cell[cell_to_fill.strip()].filled):
                                    cell_check = True
                                    cell_to_fill = num_to_cell[cell_to_fill.strip()]
                                    check_on_check = False
                                    while not check_on_check:
                                        check = input("You have selected to play the {} card in cell {}. Is this ok? (y/n) ".format(card_to_play.name, cell_to_fill.id))
                                        if check.lower() in ['y', 'yes', 'n', 'no']:
                                            check_on_check = True
                                            if check.lower() in ['y', 'yes']:
                                                good_to_go = True
                                                player1.play_card(player2, card_to_play, cell_to_fill, same, plus)
            else:
                print(game)
                # Keeps track of cards flipped by 'Same', 'Plus', or 'Combo'
                # on the previous turn. After it displays that game state,
                # we want the cards to display as normal on the next round.
                board.cell_1.combo = False
                board.cell_2.combo = False
                board.cell_3.combo = False
                board.cell_4.combo = False
                board.cell_5.combo = False
                board.cell_6.combo = False
                board.cell_7.combo = False
                board.cell_8.combo = False
                board.cell_9.combo = False
                
                board.cell_1.plus = False
                board.cell_2.plus = False
                board.cell_3.plus = False
                board.cell_4.plus = False
                board.cell_5.plus = False
                board.cell_6.plus = False
                board.cell_7.plus = False
                board.cell_8.plus = False
                board.cell_9.plus = False
                
                board.cell_1.same = False
                board.cell_2.same = False
                board.cell_3.same = False
                board.cell_4.same = False
                board.cell_5.same = False
                board.cell_6.same = False
                board.cell_7.same = False
                board.cell_8.same = False
                board.cell_9.same = False

                sleep(3)
                if AI_normal:
                    normal_AI(game, same, plus)
                else:
                    hard_AI(game, same, plus)
    else:
        print("This time, the computer will go first.")

        for i in range(9):
            if i % 2 == 1:
                good_to_go = False
                print(game)
                # Keeps track of cards flipped by 'Same', 'Plus', or 'Combo'
                # on the previous turn. After it displays that game state,
                # we want the cards to display as normal on the next round.
                board.cell_1.combo = False
                board.cell_2.combo = False
                board.cell_3.combo = False
                board.cell_4.combo = False
                board.cell_5.combo = False
                board.cell_6.combo = False
                board.cell_7.combo = False
                board.cell_8.combo = False
                board.cell_9.combo = False
                
                board.cell_1.plus = False
                board.cell_2.plus = False
                board.cell_3.plus = False
                board.cell_4.plus = False
                board.cell_5.plus = False
                board.cell_6.plus = False
                board.cell_7.plus = False
                board.cell_8.plus = False
                board.cell_9.plus = False
                
                board.cell_1.same = False
                board.cell_2.same = False
                board.cell_3.same = False
                board.cell_4.same = False
                board.cell_5.same = False
                board.cell_6.same = False
                board.cell_7.same = False
                board.cell_8.same = False
                board.cell_9.same = False
                
                while not good_to_go:
                    num_check = False
                    while not num_check:
                        if len(player1.hand) > 1:
                            print("{}, choose a card to play from your hand.".format(player1.name))
                            card_to_play = input("Select the number under the card that you want to play. ")
                        else:
                            card_to_play = "1"
                        if card_to_play.strip() in [str(i+1) for i in range(len(player1.hand))]:
                            num_check = True
                            card_to_play = player1.hand[int(card_to_play) - 1]
                            cell_check = False
                            while not cell_check:
                                cell_to_fill = input("Please select an empty cell to place the {} card into. ".format(card_to_play.name))
                                if (cell_to_fill.strip() in [str(i+1) for i in range(9)]) and (not num_to_cell[cell_to_fill.strip()].filled):
                                    cell_check = True
                                    cell_to_fill = num_to_cell[cell_to_fill.strip()]
                                    check_on_check = False
                                    while not check_on_check:
                                        check = input("You have selected to play the {} card in cell {}. Is this ok? (y/n) ".format(card_to_play.name, cell_to_fill.id))
                                        if check.lower() in ['y', 'yes', 'n', 'no']:
                                            check_on_check = True
                                            if check.lower() in ['y', 'yes']:
                                                good_to_go = True
                                                player1.play_card(player2, card_to_play, cell_to_fill, same, plus)
            else:
                print(game)
                # Keeps track of cards flipped by 'Same', 'Plus', or 'Combo'
                # on the previous turn. After it displays that game state,
                # we want the cards to display as normal on the next round.
                board.cell_1.combo = False
                board.cell_2.combo = False
                board.cell_3.combo = False
                board.cell_4.combo = False
                board.cell_5.combo = False
                board.cell_6.combo = False
                board.cell_7.combo = False
                board.cell_8.combo = False
                board.cell_9.combo = False
                
                board.cell_1.plus = False
                board.cell_2.plus = False
                board.cell_3.plus = False
                board.cell_4.plus = False
                board.cell_5.plus = False
                board.cell_6.plus = False
                board.cell_7.plus = False
                board.cell_8.plus = False
                board.cell_9.plus = False
                
                board.cell_1.same = False
                board.cell_2.same = False
                board.cell_3.same = False
                board.cell_4.same = False
                board.cell_5.same = False
                board.cell_6.same = False
                board.cell_7.same = False
                board.cell_8.same = False
                board.cell_9.same = False

                sleep(3)
                if AI_normal:
                    normal_AI(game, same, plus)
                else:
                    hard_AI(game, same, plus)

    print(game)
    if player1.points > player2.points:
        print("You win!\n")
    elif player2.points > player1.points:
        print("You lose.\n")
    else:
        print("It's a draw!\n")

    new_game_check = False
    while not new_game_check:
        new_game_option = input("Type 'replay' to play again with the same settings, 'new' to reset your settings, or 'exit' to quit the program. ")
        if new_game_option.lower().strip() in ["replay", "exit", "new"]:
            new_game_check = True
            if new_game_option.lower().strip() == "replay":
                play_type1(draw_option, same, plus, AI_normal, player1_name, player1_nickname)
            elif new_game_option.lower().strip() == "new":
                play()
            else:
                return


# A 2-player game.
def play_type2(draw_option, same, plus, player1_name, player1_nickname, player2_name, player2_nickname):
    print("\nOK!")
    while len(player1_name) == 0:
        player1_name = input("Please enter a name for Player 1. ")
    if len(player1_name) > 7 and len(player1_nickname) == 0:
        player1_nickname = player1_name
        while len(player1_nickname) > 7 or len(player1_nickname) == 0:
            player1_nickname = input("Please enter a nickname of at most 7 characters. This will appear on cards that you control on the board. ")

    while len(player2_name) == 0:
        player2_name = input("Please enter a name for Player 2. ")
    if len(player2_name) > 7 and len(player2_nickname) == 0:
        player2_nickname = player2_name
        while len(player2_nickname) > 7 or len(player2_nickname) == 0:
            player2_nickname = input("Please enter a nickname of at most 7 characters. This will appear on cards that you control on the board. ")

    
    if draw_option == 1:
        hand1 = choose_5(player1_name, high_levels, False)
        hand2 = choose_5(player2_name, high_levels, False)
    elif draw_option == 2:
        hand1 = []
        hand1 += choose_2_of_3(player1_name, sample(low_levels, 3), False)
        hand1 += choose_2_of_3(player1_name, sample(mid_levels, 3), False)
        hand1 += choose_1_of_11(player1_name, high_levels, False)
        hand2 = []
        hand2 += choose_2_of_3(player2_name, sample(low_levels, 3), False)
        hand2 += choose_2_of_3(player2_name, sample(mid_levels, 3), False)
        hand2 += choose_1_of_11(player2_name, high_levels, False)
    elif draw_option == 3:
        hand1 = sample(low_levels, 2) + sample(mid_levels, 2) + sample(high_levels, 1)
        hand2 = sample(low_levels, 2) + sample(mid_levels, 2) + sample(high_levels, 1)
    else:
        hand1 = sample(full_deck, 5)
        hand2 = sample(full_deck, 5)
    
    print("\n")
    print("Perfect. Let's get started!")
    player1 = Player(player1_name, hand1)
    if len(player1.name) > 7:
        player1.nickname = player1_nickname

    player2 = Player(player2_name, hand2)
    if len(player2.name) > 7:
        player2.nickname = player2_nickname

    board = Board()
    game = Game(player1, player2, board)

    num_to_cell = {
        "1": board.cell_1,
        "2": board.cell_2,
        "3": board.cell_3,
        "4": board.cell_4,
        "5": board.cell_5,
        "6": board.cell_6,
        "7": board.cell_7,
        "8": board.cell_8,
        "9": board.cell_9}
    
    starter = randint(1, 2)
    if starter == 1:
        print("This time, {} will go first.".format(player1.name))

        for i in range(9):
            if i % 2 == 0:
                good_to_go = False
                print(game)
                # Keeps track of cards flipped by 'Same', 'Plus', or 'Combo'
                # on the previous turn. After it displays that game state,
                # we want the cards to display as normal on the next round.
                board.cell_1.combo = False
                board.cell_2.combo = False
                board.cell_3.combo = False
                board.cell_4.combo = False
                board.cell_5.combo = False
                board.cell_6.combo = False
                board.cell_7.combo = False
                board.cell_8.combo = False
                board.cell_9.combo = False
                
                board.cell_1.plus = False
                board.cell_2.plus = False
                board.cell_3.plus = False
                board.cell_4.plus = False
                board.cell_5.plus = False
                board.cell_6.plus = False
                board.cell_7.plus = False
                board.cell_8.plus = False
                board.cell_9.plus = False
                
                board.cell_1.same = False
                board.cell_2.same = False
                board.cell_3.same = False
                board.cell_4.same = False
                board.cell_5.same = False
                board.cell_6.same = False
                board.cell_7.same = False
                board.cell_8.same = False
                board.cell_9.same = False
                
                while not good_to_go:
                    num_check = False
                    while not num_check:
                        if len(player1.hand) > 1:
                            print("{}, choose a card to play from your hand.".format(player1.name))
                            card_to_play = input("Select the number under the card that you want to play. ")
                        else:
                            card_to_play = "1"
                        if card_to_play.strip() in [str(i+1) for i in range(len(player1.hand))]:
                            num_check = True
                            card_to_play = player1.hand[int(card_to_play) - 1]
                            cell_check = False
                            while not cell_check:
                                cell_to_fill = input("Please select an empty cell to place the {} card into. ".format(card_to_play.name))
                                if (cell_to_fill.strip() in [str(i+1) for i in range(9)]) and (not num_to_cell[cell_to_fill.strip()].filled):
                                    cell_check = True
                                    cell_to_fill = num_to_cell[cell_to_fill.strip()]
                                    check_on_check = False
                                    while not check_on_check:
                                        check = input("You have selected to play the {} card in cell {}. Is this ok? (y/n) ".format(card_to_play.name, cell_to_fill.id))
                                        if check.lower() in ['y', 'yes', 'n', 'no']:
                                            check_on_check = True
                                            if check.lower() in ['y', 'yes']:
                                                good_to_go = True
                                                player1.play_card(player2, card_to_play, cell_to_fill, same, plus)
            else:
                good_to_go = False
                print(game)
                # Keeps track of cards flipped by 'Same', 'Plus', or 'Combo'
                # on the previous turn. After it displays that game state,
                # we want the cards to display as normal on the next round.
                board.cell_1.combo = False
                board.cell_2.combo = False
                board.cell_3.combo = False
                board.cell_4.combo = False
                board.cell_5.combo = False
                board.cell_6.combo = False
                board.cell_7.combo = False
                board.cell_8.combo = False
                board.cell_9.combo = False
                
                board.cell_1.plus = False
                board.cell_2.plus = False
                board.cell_3.plus = False
                board.cell_4.plus = False
                board.cell_5.plus = False
                board.cell_6.plus = False
                board.cell_7.plus = False
                board.cell_8.plus = False
                board.cell_9.plus = False
                
                board.cell_1.same = False
                board.cell_2.same = False
                board.cell_3.same = False
                board.cell_4.same = False
                board.cell_5.same = False
                board.cell_6.same = False
                board.cell_7.same = False
                board.cell_8.same = False
                board.cell_9.same = False
                
                while not good_to_go:
                    num_check = False
                    while not num_check:
                        if len(player2.hand) > 1:
                            print("{}, choose a card to play from your hand.".format(player2.name))
                            card_to_play = input("Select the number under the card that you want to play. ")
                        else:
                            card_to_play = "1"
                        if card_to_play.strip() in [str(i+1) for i in range(len(player2.hand))]:
                            num_check = True
                            card_to_play = player2.hand[int(card_to_play) - 1]
                            cell_check = False
                            while not cell_check:
                                cell_to_fill = input("Please select an empty cell to place the {} card into. ".format(card_to_play.name))
                                if (cell_to_fill.strip() in [str(i+1) for i in range(9)]) and (not num_to_cell[cell_to_fill.strip()].filled):
                                    cell_check = True
                                    cell_to_fill = num_to_cell[cell_to_fill.strip()]
                                    check_on_check = False
                                    while not check_on_check:
                                        check = input("You have selected to play the {} card in cell {}. Is this ok? (y/n) ".format(card_to_play.name, cell_to_fill.id))
                                        if check.lower() in ['y', 'yes', 'n', 'no']:
                                            check_on_check = True
                                            if check.lower() in ['y', 'yes']:
                                                good_to_go = True
                                                player2.play_card(player1, card_to_play, cell_to_fill, same, plus)


    else:
        print("This time, {} will go first.".format(player2.name))
        for i in range(9):
            if i % 2 == 1:
                good_to_go = False
                print(game)
                # Keeps track of cards flipped by 'Same', 'Plus', or 'Combo'
                # on the previous turn. After it displays that game state,
                # we want the cards to display as normal on the next round.
                board.cell_1.combo = False
                board.cell_2.combo = False
                board.cell_3.combo = False
                board.cell_4.combo = False
                board.cell_5.combo = False
                board.cell_6.combo = False
                board.cell_7.combo = False
                board.cell_8.combo = False
                board.cell_9.combo = False
                
                board.cell_1.plus = False
                board.cell_2.plus = False
                board.cell_3.plus = False
                board.cell_4.plus = False
                board.cell_5.plus = False
                board.cell_6.plus = False
                board.cell_7.plus = False
                board.cell_8.plus = False
                board.cell_9.plus = False
                
                board.cell_1.same = False
                board.cell_2.same = False
                board.cell_3.same = False
                board.cell_4.same = False
                board.cell_5.same = False
                board.cell_6.same = False
                board.cell_7.same = False
                board.cell_8.same = False
                board.cell_9.same = False
                
                while not good_to_go:
                    num_check = False
                    while not num_check:
                        if len(player1.hand) > 1:
                            print("{}, choose a card to play from your hand.".format(player1.name))
                            card_to_play = input("Select the number under the card that you want to play. ")
                        else:
                            card_to_play = "1"
                        if card_to_play.strip() in [str(i+1) for i in range(len(player1.hand))]:
                            num_check = True
                            card_to_play = player1.hand[int(card_to_play) - 1]
                            cell_check = False
                            while not cell_check:
                                cell_to_fill = input("Please select an empty cell to place the {} card into. ".format(card_to_play.name))
                                if (cell_to_fill.strip() in [str(i+1) for i in range(9)]) and (not num_to_cell[cell_to_fill.strip()].filled):
                                    cell_check = True
                                    cell_to_fill = num_to_cell[cell_to_fill.strip()]
                                    check_on_check = False
                                    while not check_on_check:
                                        check = input("You have selected to play the {} card in cell {}. Is this ok? (y/n) ".format(card_to_play.name, cell_to_fill.id))
                                        if check.lower() in ['y', 'yes', 'n', 'no']:
                                            check_on_check = True
                                            if check.lower() in ['y', 'yes']:
                                                good_to_go = True
                                                player1.play_card(player2, card_to_play, cell_to_fill, same, plus)
            else:
                good_to_go = False
                print(game)
                # Keeps track of cards flipped by 'Same', 'Plus', or 'Combo'
                # on the previous turn. After it displays that game state,
                # we want the cards to display as normal on the next round.
                board.cell_1.combo = False
                board.cell_2.combo = False
                board.cell_3.combo = False
                board.cell_4.combo = False
                board.cell_5.combo = False
                board.cell_6.combo = False
                board.cell_7.combo = False
                board.cell_8.combo = False
                board.cell_9.combo = False
                
                board.cell_1.plus = False
                board.cell_2.plus = False
                board.cell_3.plus = False
                board.cell_4.plus = False
                board.cell_5.plus = False
                board.cell_6.plus = False
                board.cell_7.plus = False
                board.cell_8.plus = False
                board.cell_9.plus = False
                
                board.cell_1.same = False
                board.cell_2.same = False
                board.cell_3.same = False
                board.cell_4.same = False
                board.cell_5.same = False
                board.cell_6.same = False
                board.cell_7.same = False
                board.cell_8.same = False
                board.cell_9.same = False
                
                while not good_to_go:
                    num_check = False
                    while not num_check:
                        if len(player2.hand) > 1:
                            print("{}, choose a card to play from your hand.".format(player2.name))
                            card_to_play = input("Select the number under the card that you want to play. ")
                        else:
                            card_to_play = "1"
                        if card_to_play.strip() in [str(i+1) for i in range(len(player2.hand))]:
                            num_check = True
                            card_to_play = player2.hand[int(card_to_play) - 1]
                            cell_check = False
                            while not cell_check:
                                cell_to_fill = input("Please select an empty cell to place the {} card into. ".format(card_to_play.name))
                                if (cell_to_fill.strip() in [str(i+1) for i in range(9)]) and (not num_to_cell[cell_to_fill.strip()].filled):
                                    cell_check = True
                                    cell_to_fill = num_to_cell[cell_to_fill.strip()]
                                    check_on_check = False
                                    while not check_on_check:
                                        check = input("You have selected to play the {} card in cell {}. Is this ok? (y/n) ".format(card_to_play.name, cell_to_fill.id))
                                        if check.lower() in ['y', 'yes', 'n', 'no']:
                                            check_on_check = True
                                            if check.lower() in ['y', 'yes']:
                                                good_to_go = True
                                                player2.play_card(player1, card_to_play, cell_to_fill, same, plus)

    print(game)
    if player1.points > player2.points:
        print("{} wins!".format(player1.name))
    elif player2.points > player1.points:
        print("{} wins!".format(player2.name))
    else:
        print("It's a draw!")

    new_game_check = False
    while not new_game_check:
        new_game_option = input("Type 'replay' to play again with the same settings, 'new' to reset your settings, or 'exit' to quit the program. ")
        if new_game_option.lower().strip() in ["replay", "exit", "new"]:
            new_game_check = True
            if new_game_option.lower().strip() == "replay":
                play_type2(draw_option, same, plus, player1_name, player1_nickname, player2_name, player2_nickname)
            elif new_game_option.lower().strip() == "new":
                play()
            else:
                return


buel = Card("Buel", 3, 2, 6, 2)
grat = Card("Grat", 1, 1, 7, 3)
creeps = Card("Creeps", 2, 2, 5, 5)
grendel = Card("Grendel", 2, 4, 4, 5)
jelleye = Card("Jelleye", 7, 2, 3, 1)
ochu = Card("Ochu", 3, 6, 5, 3)
sam08g = Card("SAM08G", 4, 6, 5, 2)
cactuar = Card("Cactuar", 3, 2, 6, 6)
tonberry = Card("Tonberry", 4, 6, 3, 4)
blobra = Card("Blobra", 5, 3, 2, 1)
gesper = Card("Gesper", 1, 5, 1, 4)

low_levels = [buel, grat, creeps, grendel, jelleye, ochu, sam08g, cactuar, tonberry, blobra, gesper]

behemoth = Card("Behemoth", 7, 6, 3, 5)
chimera = Card("Chimera", 3, 6, 7, 5)
malboro = Card("Malboro", 2, 7, 7, 4)
elnoyle = Card("Elnoyle", 6, 3, 5, 7)
xatm092 = Card("X-ATM92", 3, 8, 4, 7)
gerogero = Card("Gerogero", 3, 8, 1, 8)
iguion = Card("Iguion", 2, 2, 8, 8)
abadon = Card("Abadon", 5, 8, 6, 4)
krysta = Card("Krysta", 1, 5, 7, 8)
tripoint = Card("Tri-Point", 8, 5, 8, 2)
tiamat = Card("Tiamat", 4, 8, 8, 5)

mid_levels = [behemoth, chimera, malboro, elnoyle, xatm092, gerogero, iguion, abadon, krysta, tripoint, tiamat]


ward = Card("Ward", 8, 7, 10, 2)
kiros = Card("Kiros", 10, 7, 6, 6)
laguna = Card("Laguna", 9, 10, 5, 3)
selphie = Card("Selphie", 4, 8, 10, 6)
quistis = Card("Quistis", 2, 6, 9, 10)
irvine = Card("Irvine", 10, 6, 2, 9)
zell = Card("Zell", 6, 5, 8, 10)
rinoa = Card("Rinoa", 10, 10, 4, 2)
edea = Card("Edea", 3, 10, 10, 3)
seifer = Card("Seifer", 4, 9, 6, 10)
squall = Card("Squall", 9, 4, 10, 6)

high_levels = [ward, kiros, laguna, selphie, quistis, irvine, zell, rinoa, edea, seifer, squall]

full_deck = low_levels + mid_levels + high_levels


play()

