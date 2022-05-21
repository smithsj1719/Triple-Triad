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