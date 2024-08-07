"""
Project for learning Pyxel. This game simulates Conway's Way Of Life.

Game rules: https://www.wikiwand.com/en/Conway%27s_Game_of_Life
 - Any live cell with fewer than two live neighbours dies, as if by underpopulation.
 - Any live cell with two or three live neighbours lives on to the next generation.
 - Any live cell with more than three live neighbours dies, as if by overpopulation.
 - Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
"""

import pyxel
from time import time

class App:
    SPACE_WIDTH = 160
    SPACE_HEIGHT = 120

    def __init__(self):
        pyxel.init(App.SPACE_WIDTH, App.SPACE_HEIGHT, "Conway's Game Of Life")
        
        # Update interval in milliseconds
        self.update_interval = 1000
        # Timestamp in milliseconds
        self.prev_update_time = 0

        # TODO: Diffent hardcoded start states e.g. Beehive, Pulsar
        self.cells = App._new_empty_cells(App.SPACE_WIDTH, App.SPACE_HEIGHT, 6400)

        pyxel.run(self.update, self.draw)

    def update(self):
        # Adjust update speed
        if pyxel.btn(pyxel.KEY_UP):
            self.update_interval -= 100
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.update_interval += 100

        now = int(time() * 1000)
        if now - self.prev_update_time < self.update_interval:
            return

        self._update_cells()
        
        self.prev_update_time = int(time() * 1000)

    def draw(self):
        pyxel.cls(0)

        for x in range(len(self.cells)):
            for y in range(len(self.cells[x])):
                if self.cells[x][y] == 1:
                    pyxel.pset(x, y, pyxel.COLOR_LIME)
    
    def _new_empty_cells(width, height, population = 0):
        """Create new state with random living cells
        
        Args:
            width (int): Width of the space
            height (int): Height of the space
            population (int): Initial population count, default 100

        Returns:
            list: 2D list of cells
        """

        # Prevent stupid mistake
        #population = min(population, width * height)

        cells = [[0 for i in range(height)] for j in range(width)]
        while population > 0:
            x = pyxel.rndi(0, width - 1)
            y = pyxel.rndi(0, height - 1)
            if cells[x][y] == 0:
                cells[x][y] = 1
                population -= 1

        return cells
    
    def _update_cells(self):
        """Update cells for new iteration"""

        new_cells = App._new_empty_cells(App.SPACE_WIDTH, App.SPACE_HEIGHT)
        
        for x in range(len(self.cells)):
            for y in range(len(self.cells[x])):
                if self.cells[x][y] == 1:
                    # Live cell
                    neighbors = self._count_neighbors(x, y)
                    if neighbors < 2 or neighbors > 3:
                        # Die due to (over/under)popluation
                        new_cells[x][y] = 0
                    else:
                        # Live on
                        new_cells[x][y] = 1
                else:
                    # Empty cell
                    neighbors = self._count_neighbors(x, y)
                    if neighbors == 3:
                        new_cells[x][y] = 1

        self.cells = new_cells

    def _count_neighbors(self, x, y):
        """Count number of living neighbours"""

        count = 0
        for offset_x in range(-1, 2):
            if x + offset_x < 0 or x + offset_x >= App.SPACE_WIDTH:
                continue

            for offset_y in range(-1, 2):
                if offset_x == 0 and offset_y == 0:
                    # This is not neighbour
                    continue
                elif y + offset_y < 0 or y + offset_y >= App.SPACE_HEIGHT:
                    continue

                if self.cells[x + offset_x][y + offset_y] == 1:
                    count += 1

        return count

App()