import pygame
import sys
import argparse
from fps import Fps
from path_finding import PathFinding, Markers, Algorithms
from maze_generation import SidewinderAlgorithm
from algorithms import BFS, DFS, AStar
from gui import Frame, TextFrame, Button, VLayout, HLayout, GridLayout
from gui import Color


p = argparse.ArgumentParser(formatter_class=argparse.MetavarTypeHelpFormatter)
p.add_argument("--tile-size", "-s", type=int,
               help="set size of single tile", default=16)
p.add_argument("--tiles-number", "-n", type=int,
               help="set number of tiles in a row", default=35)


class Main:
    """
    Main program class, it creates pygame window and it contains main loop
        where you are supposed to place all program logic, objects etc.
    """

    def __init__(self, **args):
        caption = "PATH FINDING"
        fullscreen = 0
        tile_size, tiles_number = args["tile_size"], args["tiles_number"]

        if tiles_number % 2 == 0:
            raise Exception("Number of tiles should be odd.")

        self.path = PathFinding(tile_size, tiles_number)
        self.window_size = self.path.get_screen_size()

        x_size, y_size = self.window_size

        if y_size < 356:
            raise Exception("Such small maze is not allowed.")

        info = pygame.display.Info()
        if x_size > info.current_w or y_size > info.current_h:
            raise Exception("Such big maze is not allowed.")

        # window operations

        options = pygame.HWSURFACE | pygame.DOUBLEBUF
        if fullscreen:
            options |= pygame.FULLSCREEN

        self.screen = pygame.display.set_mode(self.window_size, options)
        pygame.display.set_caption(caption)
        self.running = True
        self.screen_color = (0, 0, 0)

        self.clock = pygame.time.Clock()

        # variables

        self.delta_time = 0
        self.last_frame_time = pygame.time.get_ticks()

        # fps class init

        self.fps = Fps(14, x=42, y=7)

        # main render class init

        self.path.initial_render()

        # maze_generation init

        self.maze_gen = SidewinderAlgorithm(self.path)

        # path finding algorithm

        self.bfs = BFS(self.path)
        self.dfs = DFS(self.path)
        self.astar = AStar(self.path)
        self.num_of_algorithms = 3

        self.algo = None
        self.algorithm_index = 0

        # gui
        self.fr = Frame(w=self.path.get_gui_width(),
                        h=self.path.get_gui_height(),
                        fill=Color.SliderColorBg,
                        border=True,
                        borderthickness=3,
                        bordercolor=Color.DarkGray)

        self.main_v = VLayout(self.screen, orientation="W")
        self.main_v.add_widget(self.fr)

        self.fps_frame = TextFrame(w=110,
                                   h=20,
                                   fill=Color.SliderColorBg,
                                   text="Fps:",
                                   fontcolor=Color.Yellow,
                                   anchor="W")

        self.selected_marker_frame = TextFrame(w=110,
                                               h=20,
                                               fontsize=10,
                                               fill=Color.SliderColorBg,
                                               text="Marker: ---",
                                               anchor="W")

        self.selected_algorithm_frame = TextFrame(w=110,
                                                  h=20,
                                                  fontsize=10,
                                                  fill=Color.SliderColorBg,
                                                  text="Algorithm: ---",
                                                  anchor="W")

        self.clear_button = Button(w=110,
                                   h=20,
                                   fontsize=10,
                                   fill=Color.White,
                                   text="Clear path (c)",
                                   func=self.clear_path,
                                   bordercolor=Color.DarkGray,
                                   borderthickness=1)

        self.clear_all_button = Button(w=110,
                                       h=20,
                                       fontsize=10,
                                       fill=Color.White,
                                       text="Clear all (x)",
                                       func=self.clear_all,
                                       bordercolor=Color.DarkGray,
                                       borderthickness=1)

        self.gen_maze_button = Button(w=110,
                                      h=20,
                                      fontsize=10,
                                      fill=Color.White,
                                      text="Generate maze (g)",
                                      func=self.gen_maze,
                                      bordercolor=Color.DarkGray,
                                      borderthickness=1)

        self.run_button = Button(w=110,
                                 h=20,
                                 fontsize=10,
                                 fill=Color.White,
                                 text="Run (space)",
                                 func=self.run,
                                 bordercolor=Color.DarkGray,
                                 borderthickness=1)

        self.time_frame = TextFrame(w=110,
                                    h=20,
                                    fontsize=10,
                                    fill=Color.SliderColorBg,
                                    text="Time: ---",
                                    anchor="W")

        self.gui_frames_layout = VLayout(
            self.screen, orientation="NW", x_start=7, y_start=7)

        self.gui_frames_layout.add_widget(self.fps_frame)
        self.gui_frames_layout.add_widget(self.selected_marker_frame)
        self.gui_frames_layout.add_widget(self.selected_algorithm_frame, 10)
        self.gui_frames_layout.add_widget(self.clear_button, 5)
        self.gui_frames_layout.add_widget(self.clear_all_button, 5)
        self.gui_frames_layout.add_widget(self.gen_maze_button, 10)

        self.run_button_layout = VLayout(
            self.screen, orientation="SW", x_start=7, y_start=-7)
        self.run_button_layout.add_widget(self.time_frame)
        self.run_button_layout.add_widget(self.run_button)

        self.choose_marker_layout = GridLayout(
            self.screen, orientation="NW", x_start=6, y_start=160)

        # choose marker

        self.start_marker_button = Button(
            w=20, h=20, borderthickness=1, fill=Color.Red, pressedcolor=Color.LightRed, func=self.set_marker_start, bordercolor=Color.DarkGray)
        self.end_marker_button = Button(
            w=20, h=20, borderthickness=1, fill=Color.Green, pressedcolor=Color.LightGreen, func=self.set_marker_end, bordercolor=Color.DarkGray)
        self.obstacle_marker_button = Button(
            w=20, h=20, borderthickness=1, fill=Color.Black, pressedcolor=Color.DarkGray, func=self.set_marker_obstacle, bordercolor=Color.DarkGray)
        self.none_marker_button = Button(
            w=20, h=20, borderthickness=1, fill=Color.White, pressedcolor=Color.White, func=self.set_marker_none, bordercolor=Color.DarkGray)

        self.start_marker_button_text = TextFrame(w=80,
                                                  h=20,
                                                  fontsize=10,
                                                  fill=Color.SliderColorBg,
                                                  text="Start (1)",
                                                  anchor="W")
        self.end_marker_button_text = TextFrame(w=80,
                                                h=20,
                                                fontsize=10,
                                                fill=Color.SliderColorBg,
                                                text="End (2)",
                                                anchor="W")
        self.obstacle_marker_button_text = TextFrame(w=80,
                                                     h=20,
                                                     fontsize=10,
                                                     fill=Color.SliderColorBg,
                                                     text="Obstacle (3)",
                                                     anchor="W")
        self.none_marker_button_text = TextFrame(w=80,
                                                 h=20,
                                                 fontsize=10,
                                                 fill=Color.SliderColorBg,
                                                 text="None (4)",
                                                 anchor="W")

        self.choose_marker_layout.add_widget(
            self.start_marker_button, 0, 0, 1, 5)
        self.choose_marker_layout.add_widget(
            self.start_marker_button_text, 0, 1, 0, 5)

        self.choose_marker_layout.add_widget(
            self.end_marker_button, 1, 0, 1, 5)
        self.choose_marker_layout.add_widget(
            self.end_marker_button_text, 1, 1, 0, 5)

        self.choose_marker_layout.add_widget(
            self.obstacle_marker_button, 2, 0, 1, 5)
        self.choose_marker_layout.add_widget(
            self.obstacle_marker_button_text, 2, 1, 0, 5)

        self.choose_marker_layout.add_widget(
            self.none_marker_button, 3, 0, 1, 5)
        self.choose_marker_layout.add_widget(
            self.none_marker_button_text, 3, 1, 0, 5)

        # choose algorithm

        self.choose_algorithm_layout = HLayout(
            self.screen, orientation="NW", x_start=6, y_start=270)

        self.choose_algo_left_button = Button(
            w=15, h=20, func=self.prev_algorithm, borderthickness=1, bordercolor=Color.DarkGray, text="<")
        self.chosen_algorithm_frame = TextFrame(
            w=80, h=20, border=True, text=self.path.chosen_algorithm.name, borderthickness=1, bordercolor=Color.DarkGray)
        self.choose_algo_right_button = Button(
            w=15, h=20, func=self.next_algorithm, borderthickness=1, bordercolor=Color.DarkGray, text=">")

        self.choose_algorithm_layout.add_widget(self.choose_algo_left_button)
        self.choose_algorithm_layout.add_widget(self.chosen_algorithm_frame)
        self.choose_algorithm_layout.add_widget(self.choose_algo_right_button)

    def main_loop(self):
        self.set_screen_color(100, 100, 200)

        while self.running:
            self.events()
            self.screen.fill(self.screen_color)

            # ------------ scene ------------- #

            # get mouse input
            mouse_button = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            keys = pygame.key.get_pressed()
            self.path.place_markers(mouse_pos, mouse_button)

            self.path.render_scene(self.screen)
            self.main_v.draw(self.screen.get_size(), mouse_pos,
                             mouse_button, keys, self.delta_time)
            self.gui_frames_layout.draw(self.screen.get_size(), mouse_pos,
                                        mouse_button, keys, self.delta_time)
            self.run_button_layout.draw(self.screen.get_size(), mouse_pos,
                                        mouse_button, keys, self.delta_time)
            self.choose_marker_layout.draw(self.screen.get_size(), mouse_pos,
                                           mouse_button, keys, self.delta_time)
            self.choose_algorithm_layout.draw(self.screen.get_size(), mouse_pos,
                                              mouse_button, keys, self.delta_time)

            self.selected_marker_frame.set_text(
                f"Marker: {self.path.chosen_marker.name}")
            self.selected_algorithm_frame.set_text(
                f"Algorithm: {self.path.chosen_algorithm.name}")
            self.chosen_algorithm_frame.set_text(
                f"{self.path.chosen_algorithm.name}")
            self.time_frame.set_text(
                f"Time: {self.path.time_elapsed:.2f}")
            self.path.draw_markers()

            # generate maze when 'g' key is pressed

            if self.path.init_maze_generation:
                if self.maze_gen.generate_maze_init():
                    self.path.init_maze_generation = False
                    self.path.proceed_maze_generation = True

            if self.path.proceed_maze_generation:
                self.maze_gen.generate_maze_process()

            # -------------------------------------

            if self.path.chosen_algorithm == Algorithms.DFS:
                self.algo = self.dfs
            elif self.path.chosen_algorithm == Algorithms.BFS:
                self.algo = self.bfs
            elif self.path.chosen_algorithm == Algorithms.AStar:
                self.algo = self.astar

            self.run_algorithm()
            # -------------------------------- #

            # fps management
            self.fps.fps()
            self.fps.show_fps(self.screen)

            # flip screen at the end of scene
            pygame.display.flip()

            # delta time calcualtions
            current_frame_time = pygame.time.get_ticks()
            self.delta_time = (current_frame_time -
                               self.last_frame_time) / 1000.0
            self.last_frame_time = current_frame_time
            # self.clock.tick(60)

        self.kill()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_g:
                    self.gen_maze()
                elif event.key == pygame.K_1:
                    self.path.chosen_marker = Markers.START
                elif event.key == pygame.K_2:
                    self.path.chosen_marker = Markers.END
                elif event.key == pygame.K_3:
                    self.path.chosen_marker = Markers.OBSTACLE
                elif event.key == pygame.K_4:
                    self.path.chosen_marker = Markers.NONE
                elif event.key == pygame.K_SPACE:
                    self.run()
                elif event.key == pygame.K_x:
                    self.clear_all()
                elif event.key == pygame.K_c:
                    self.clear_path()
                elif event.key == pygame.K_n:
                    self.next_algorithm()
                elif event.key == pygame.K_p:
                    self.prev_algorithm()

    def run_algorithm(self):
        if self.path.start_algorithm:
            if self.algo.start():
                self.path.stop_algorithm = False
            self.path.start_algorithm = False

        if not self.path.stop_algorithm:
            self.path.time_elapsed += self.delta_time
            if self.algo.through_maze():
                self.path.stop_algorithm = True

        if self.algo.end_tile != None:
            self.algo.show_path()

    def next_algorithm(self):
        self.algorithm_index += 1
        self.path.chosen_algorithm = Algorithms(
            self.algorithm_index % self.num_of_algorithms)
        self.clear_path()

    def prev_algorithm(self):
        self.algorithm_index -= 1
        self.path.chosen_algorithm = Algorithms(
            self.algorithm_index % self.num_of_algorithms)
        self.clear_path()

    def run(self):
        self.path.start_algorithm = True

    def clear_all(self):
        self.path.clear_all_tiles()
        self.algo.clean_up()

    def clear_path(self):
        self.path.clear_searched()
        self.algo.clean_up()

    def gen_maze(self):
        self.path.clear_all_tiles()
        self.algo.clean_up()
        self.path.init_maze_generation = True

    def set_marker_start(self):
        self.path.chosen_marker = Markers.START

    def set_marker_end(self):
        self.path.chosen_marker = Markers.END

    def set_marker_obstacle(self):
        self.path.chosen_marker = Markers.OBSTACLE

    def set_marker_none(self):
        self.path.chosen_marker = Markers.NONE

    def set_screen_color(self, r, g, b):
        self.screen_color = (r, g, b)

    @ staticmethod
    def kill():
        pygame.quit()


if __name__ == "__main__":
    pygame.init()
    args = p.parse_args()
    Main(**vars(args)).main_loop()
