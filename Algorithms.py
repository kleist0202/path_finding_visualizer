from Tiles import Markers
from math import sqrt
from operator import attrgetter


class BFS:
    def __init__(self, path_finding):
        self.pf = path_finding

        self.neighbours = []

        self.next_value = 1
        self.the_lowest_value = None
        self.end_tile = None

    def start(self):
        for tile in self.pf.tiles:
            if tile.is_start():
                start_tile = tile
                break
        else:
            print("Can not find start tile.")
            return True

        for tile in self.pf.tiles:
            if tile.is_end():
                break
        else:
            print("Can not find end tile.")
            return False

        start_tile.set_value(self.next_value)
        self.next_value += 1
        self.neighbours.append(start_tile)
        print("Start path finding...")
        return True

    def through_maze(self):
        if self.neighbours:
            s_row, s_col = self.neighbours[0].get_pos()
            for i in range(4):  # 4, maximum number of neighbours
                if i == 0:
                    t = self.pf.get_tile(s_row, s_col+1)
                elif i == 1:
                    t = self.pf.get_tile(s_row+1, s_col)
                elif i == 2:
                    t = self.pf.get_tile(s_row, s_col-1)
                elif i == 3:
                    t = self.pf.get_tile(s_row-1, s_col)

                if t is None:
                    continue

                if t.is_end():
                    t.set_value(self.next_value)
                    self.end_tile = t
                    return True

                if t.is_checked() or t.is_start() or t.is_searched():
                    continue

                if not t.is_obstacle():
                    t.set_marker(Markers.CHECKED)
                    self.neighbours.append(t)
                    t.set_value(self.next_value)
                    self.next_value += 1

            if not self.neighbours[0].is_start():
                self.neighbours[0].set_marker(Markers.SEARCHED)
            self.neighbours.pop(0)

            return False

    def show_path(self):
        the_lowest_tile = None
        end_row, end_col = self.end_tile.get_pos()
        if self.the_lowest_value == None:
            self.the_lowest_value = self.end_tile.get_value()
        for i in range(4):  # 4, maximum number of neighbours
            if i == 0:
                coords = (end_row, end_col+1)
            elif i == 1:
                coords = (end_row+1, end_col)
            elif i == 2:
                coords = (end_row, end_col-1)
            elif i == 3:
                coords = (end_row-1, end_col)

            next_tile = self.pf.get_tile(*coords)
            if next_tile is not None:
                val = next_tile.get_value()
                if val < self.the_lowest_value and val != 0:
                    if next_tile.is_start():
                        self.end_tile = None
                        return
                    self.the_lowest_value = val
                    the_lowest_tile = next_tile

        if the_lowest_tile is not None:
            the_lowest_tile.set_marker(Markers.PATH)
            self.end_tile = the_lowest_tile

    def clean_up(self):
        self.neighbours.clear()
        self.next_value = 1
        self.the_lowest_value = None
        self.end_tile = None


# ------------------------------------------------------------


class DFS:
    def __init__(self, path_finding):
        self.pf = path_finding

        self.stack = []
        self.last_tile = None

        self.next_value = 1
        self.the_lowest_value = None
        self.end_tile = None
        pass

    def start(self):
        for tile in self.pf.tiles:
            if tile.is_start():
                start_tile = tile
                break
        else:
            print("Can not find start tile.")
            return False

        for tile in self.pf.tiles:
            if tile.is_end():
                break
        else:
            print("Can not find end tile.")
            return False

        start_tile.set_value(self.next_value)
        self.next_value += 1
        self.stack.append(start_tile)
        print("Start path finding...")
        return True

    def through_maze(self):
        if self.stack:
            s_row, s_col = self.stack[0].get_pos()
            for i in range(4):  # 4, maximum number of neighbours
                if i == 0:
                    t = self.pf.get_tile(s_row, s_col+1)
                elif i == 1:
                    t = self.pf.get_tile(s_row+1, s_col)
                elif i == 2:
                    t = self.pf.get_tile(s_row, s_col-1)
                elif i == 3:
                    t = self.pf.get_tile(s_row-1, s_col)

                if t.is_obstacle() or t.is_checked() or t.is_searched() or t.is_start():
                    continue

                if t is None:
                    continue

                if t.is_end():
                    t.set_value(self.next_value)
                    self.end_tile = t
                    return True

                t.set_marker(Markers.CHECKED)
                self.stack.insert(0, t)
                t.set_value(self.next_value)
                self.next_value += 1
                if self.last_tile is not None:
                    self.last_tile.set_marker(Markers.SEARCHED)

                self.last_tile = t

                return False
            self.stack.pop(0)
        return False

    def show_path(self):
        the_lowest_tile = None
        end_row, end_col = self.end_tile.get_pos()
        if self.the_lowest_value == None:
            self.the_lowest_value = self.end_tile.get_value()
        for i in range(4):  # 4, maximum number of neighbours
            if i == 0:
                coords = (end_row, end_col+1)
            elif i == 1:
                coords = (end_row+1, end_col)
            elif i == 2:
                coords = (end_row, end_col-1)
            elif i == 3:
                coords = (end_row-1, end_col)

            next_tile = self.pf.get_tile(*coords)
            if next_tile is not None:
                val = next_tile.get_value()
                if val < self.the_lowest_value and val != 0:
                    if next_tile.is_start():
                        self.end_tile = None
                        return
                    self.the_lowest_value = val
                    the_lowest_tile = next_tile

        if the_lowest_tile is not None:
            the_lowest_tile.set_marker(Markers.PATH)
            self.end_tile = the_lowest_tile

    def clean_up(self):
        self.stack.clear()
        self.last_tile = None
        self.next_value = 1
        self.the_lowest_value = None
        self.end_tile = None


# ------------------------------------------------------------


class AStar:
    def __init__(self, path_finding):
        self.pf = path_finding

        self.open = []
        self.path_tiles = []
        self.last_tile = None

        self.next_value = 1
        self.the_lowest_value = None
        self.end_tile = None

        self.s_tile = None
        self.e_tile = None

    def start(self):
        for tile in self.pf.tiles:
            if tile.is_start():
                self.s_tile = tile
                break
        else:
            print("Can not find start tile.")
            return False

        for tile in self.pf.tiles:
            if tile.is_end():
                self.e_tile = tile
                break
        else:
            print("Can not find end tile.")
            return False

        self.s_tile.set_value(1)
        self.open.append(self.s_tile)
        print("Start path finding...")
        return True

    def calc_g_cost(self, start_node, current_node):
        sn_row, sn_col = start_node.get_pos()
        cn_row, cn_col = current_node.get_pos()

        calc_row, calc_col = cn_row - sn_row, cn_col - sn_col
        g_cost = round(sqrt(calc_row**2 + calc_col**2), 1) * 10
        return g_cost

    def calc_h_cost(self, end_node, current_node):
        en_row, en_col = end_node.get_pos()
        cn_row, cn_col = current_node.get_pos()

        calc_row, calc_col = cn_row - en_row, cn_col - en_col
        h_cost = round(sqrt(calc_row**2 + calc_col**2), 1) * 10
        return h_cost

    def calc_f_cost(self, g_cost, h_cost):
        f_cost = g_cost + h_cost
        return f_cost

    def through_maze(self):
        if self.open:
            current = min(self.open, key=attrgetter("value"))
            self.open.remove(current)

            if not current.is_start():
                current.set_marker(Markers.SEARCHED)

            c_row, c_col = current.get_pos()
            for i in range(4):
                if i == 0:
                    t = self.pf.get_tile(c_row, c_col+1)
                elif i == 1:
                    t = self.pf.get_tile(c_row+1, c_col)
                elif i == 2:
                    t = self.pf.get_tile(c_row, c_col-1)
                elif i == 3:
                    t = self.pf.get_tile(c_row-1, c_col)

                if t is None:
                    continue

                if t.is_obstacle() or t.is_searched() or t.is_checked():
                    continue

                if t.is_end():
                    t.parent = current
                    t.set_value(float("inf"))
                    self.end_tile = t
                    return True

                if t not in self.open:
                    g = self.calc_g_cost(self.s_tile, t)
                    h = self.calc_h_cost(self.e_tile, t)
                    f = self.calc_f_cost(g, h)
                    t.set_value(f)
                    t.parent = current
                    self.path_tiles.append(current)

                    if t not in self.open:
                        self.open.append(t)

                    if not t.is_start():
                        t.set_marker(Markers.CHECKED)

        return False

    def show_path(self):
        self.end_tile = self.end_tile.parent
        if self.end_tile is not None:
            if not self.end_tile.is_start():
                self.end_tile.set_marker(Markers.PATH)

    def clean_up(self):
        self.open.clear()
        self.last_tile = None
        self.next_value = 1
        self.the_lowest_value = None
        self.end_tile = None
