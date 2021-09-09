import pygame
from gui import Color
from Tiles import Tile, Markers, Algorithms
from gui import Frame


class PathFinding:
    def __init__(self, square_size, num_of_squares):
        self.square_size = square_size
        self.num_of_squares = num_of_squares

        self.furthest = square_size*num_of_squares+num_of_squares-1

        self.main_surface = None

        self.tiles = []

        self.prev_start_tile = None
        self.prev_end_tile = None

        self.chosen_marker = Markers.NONE
        self.chosen_algorithm = Algorithms.DFS

        self.time_elapsed = 0

        # bool vars for algorithm
        self.start_algorithm = False
        self.stop_algorithm = True

        # maze generation
        self.init_maze_generation = False
        self.proceed_maze_generation = False

        # gui
        self.gui_width = 125

    def get_screen_size(self):
        return self.furthest+self.gui_width, self.furthest

    def get_gui_width(self):
        return self.gui_width

    def get_gui_height(self):
        return self.furthest

    def initial_render(self):
        self.main_surface = pygame.Surface(
            (self.furthest, self.furthest), pygame.HWSURFACE)

        for row in range(self.num_of_squares):
            for col in range(self.num_of_squares):
                new_tile = Tile(row, col)
                if row == 0 or col == 0 or row == self.num_of_squares-1 or col == self.num_of_squares-1:
                    # set borders
                    new_tile.set_marker(Markers.OBSTACLE)
                self.tiles.append(new_tile)

        for tile in self.tiles:
            row, col = tile.get_pos()
            x = row*self.square_size
            y = col*self.square_size
            if tile.get_marker() == Markers.OBSTACLE:
                pygame.draw.rect(
                    self.main_surface, Color.Black, (x+row+1, y+col+1, self.square_size, self.square_size))
            else:
                pygame.draw.rect(
                    self.main_surface, Color.White, (x+row+1, y+col+1, self.square_size, self.square_size))

            # drawing grid
            pygame.draw.line(
                self.main_surface, Color.DarkGray, (x+row, y+col), (x+row, self.furthest))
            pygame.draw.line(
                self.main_surface, Color.DarkGray, (x+row, y+col), (self.furthest, y+col))

    def draw_markers(self):
        for tile in self.tiles:
            row, col = tile.get_pos()
            x = row*self.square_size
            y = col*self.square_size
            coords = (x+row+1, y+col+1)
            if tile.is_start():
                pygame.draw.rect(self.main_surface, Color.Red,
                                 (*coords, self.square_size, self.square_size))

            elif tile.is_end():
                pygame.draw.rect(self.main_surface, Color.Green,
                                 (*coords, self.square_size, self.square_size))

            elif tile.is_obstacle():
                pygame.draw.rect(self.main_surface, Color.Black,
                                 (*coords, self.square_size, self.square_size))

            elif tile.is_none():
                pygame.draw.rect(self.main_surface, Color.White,
                                 (*coords, self.square_size, self.square_size))

            elif tile.is_searched():
                pygame.draw.rect(self.main_surface, Color.Orange,
                                 (*coords, self.square_size, self.square_size))

            elif tile.is_checked():
                pygame.draw.rect(self.main_surface, Color.Yellow,
                                 (*coords, self.square_size, self.square_size))
            elif tile.is_path():
                pygame.draw.rect(self.main_surface, Color.Purple,
                                 (*coords, self.square_size, self.square_size))
            else:
                raise Exception

    def place_markers(self, mouse_pos, mouse_button):
        for tile in self.tiles:
            row, col = tile.get_pos()
            x = row*self.square_size
            y = col*self.square_size
            gui_w = self.get_gui_width()
            coords = (x+row+1+gui_w, y+col+1)
            if mouse_pos[0] > coords[0] and mouse_pos[0] < coords[0] + self.square_size \
                    and mouse_pos[1] > coords[1] and mouse_pos[1] < coords[1] + self.square_size:

                if mouse_button[0]:
                    if self.chosen_marker == Markers.START:
                        if self.prev_start_tile != None:
                            self.prev_start_tile.set_marker(Markers.NONE)
                        tile.set_marker(Markers.START)
                        self.prev_start_tile = tile

                    elif self.chosen_marker == Markers.END:
                        if self.prev_end_tile != None:
                            self.prev_end_tile.set_marker(Markers.NONE)
                        tile.set_marker(Markers.END)
                        self.prev_end_tile = tile

                    elif self.chosen_marker == Markers.OBSTACLE:
                        if tile.is_end():
                            self.prev_end_tile = None
                        if tile.is_start():
                            self.prev_start_tile = None
                        tile.set_marker(Markers.OBSTACLE)

                    elif self.chosen_marker == Markers.NONE:
                        tile.set_marker(Markers.NONE)

    def get_tile(self, r, c):
        for tile in self.tiles:
            row, col = tile.get_pos()
            if row == r and col == c:
                return tile
        return None

    def render_scene(self, screen):
        screen.blit(self.main_surface, (self.get_gui_width(), 0))

    def clear_all_tiles(self):
        for tile in self.tiles:
            row, col = tile.get_pos()
            if row != 0 and col != 0 and row != self.num_of_squares-1 and col != self.num_of_squares-1:
                tile.set_marker(Markers.NONE)
                tile.set_value(0)
            else:
                tile.set_marker(Markers.OBSTACLE)
        self.clean_up()

    def clear_searched(self):
        for tile in self.tiles:
            if tile.is_searched() or tile.is_checked() or tile.is_path():
                tile.set_marker(Markers.NONE)
                tile.set_value(0)
        self.clean_up()

    def clean_up(self):
        self.proceed_maze_generation = False
        self.start_algorithm = False
        self.stop_algorithm = True
        self.time_elapsed = 0
