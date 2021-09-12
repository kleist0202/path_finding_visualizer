from enum import Enum


class Markers(Enum):
    START = 1
    END = 2
    OBSTACLE = 3
    NONE = 4
    CHECKED = 5
    SEARCHED = 6
    PATH = 7


class Algorithms(Enum):
    DFS = 0
    BFS = 1
    AStar = 2


def ntimes(n):
    def inner(f):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                rv = f(*args, **kwargs)
            return rv
        return wrapper
    return inner


class Tile:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.marker = Markers.NONE
        self.value = 0
        self.parent = None

    def __repr__(self):
        return f"Tile({self.row}, {self.col}, {self.marker}, {self.value})"

    def get_pos(self):
        return (self.row, self.col)

    def set_marker(self, marker):
        self.marker = marker

    def get_marker(self):
        return self.marker

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def is_start(self):
        if self.get_marker() == Markers.START:
            return True
        return False

    def is_end(self):
        if self.get_marker() == Markers.END:
            return True
        return False

    def is_obstacle(self):
        if self.get_marker() == Markers.OBSTACLE:
            return True
        return False

    def is_checked(self):
        if self.get_marker() == Markers.CHECKED:
            return True
        return False

    def is_searched(self):
        if self.get_marker() == Markers.SEARCHED:
            return True
        return False

    def is_path(self):
        if self.get_marker() == Markers.PATH:
            return True
        return False

    def is_none(self):
        if self.get_marker() == Markers.NONE:
            return True
        return False
