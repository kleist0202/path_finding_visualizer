from random import randint
from tiles import Tile, Markers


class SidewinderAlgorithm:
    def __init__(self, path_finding):
        self.pf = path_finding

        self.all_odd = [x for x in range(
            self.pf.num_of_squares) if x % 2 == 1 and x < 15]
        self.n_tile = None
        self.all_steps = []

    def generate_maze_init(self):
        self.n_tile = self.pf.get_tile(1, 1)
        for tile in self.pf.tiles:
            row, col = tile.get_pos()
            if row % 2 == 0 or col % 2 == 0:
                tile.set_marker(Markers.OBSTACLE)
        return True

    def generate_maze_process(self):
        step = self.all_odd[randint(1, len(self.all_odd)-1)]
        for _ in range(step):
            c_row, c_col = self.n_tile.get_pos()
            if c_row >= self.pf.num_of_squares-2:
                self.all_steps.append(self.n_tile)
                self.n_tile = self.pf.get_tile(1, c_col+2)
                break
            self.n_tile.set_marker(Markers.NONE)
            self.all_steps.append(self.n_tile)
            self.n_tile = self.pf.get_tile(c_row+1, c_col)
        else:
            if c_col != 1:
                n_row, n_col = self.n_tile.get_pos()
                self.n_tile = self.pf.get_tile(n_row+1, n_col)

        rand = randint(0, len(self.all_steps)-1)
        ii = 0
        for st in self.all_steps:
            up_row, up_col = st.get_pos()
            if up_col != 1:
                st_up = self.pf.get_tile(up_row, up_col-1)
                if ii == rand:
                    st_up_row, st_up_col = st_up.get_pos()
                    if self.pf.get_tile(st_up_row, st_up_col-1).is_obstacle():
                        st_up = self.pf.get_tile(st_up_row-1, st_up_col)
                    st_up.set_marker(Markers.NONE)
            ii += 1
        self.all_steps.clear()

        # end maze generation
        if self.n_tile is None:
            self.pf.proceed_maze_generation = False
            return
