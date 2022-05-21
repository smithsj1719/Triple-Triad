from itertools import combinations

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