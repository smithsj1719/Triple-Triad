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