from cell import Cell

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