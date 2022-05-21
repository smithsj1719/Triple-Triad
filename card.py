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