# Tieu chi: giao dien don gian, than thien, truc quan, de choi, gioi han thoi gian choi <60p !

import random
from time import sleep
import pygame
from sympy import false
from pygame import mixer
pygame.init()
mixer.init()

white = (255, 255, 255)
black = (0, 0, 0)
purple = (172, 172, 255)
light_brown = (230, 204, 179)
brown = (153, 102, 51)
light_green = (170, 255, 0)
green = (0, 153, 0)
red = (255, 0, 0)
dark_red = (179, 36, 0)
color_list1 = [black, brown]
default_screen = (1720, 760)


class Text:
    def __init__(self, screen, txt, x, y, size, color=black, font='cambria'):
        font = pygame.font.SysFont(font, size)
        text = font.render(txt, True, color)
        screen.blit(text, (x, y))
        pygame.display.update()


class Surface:
    pass


class Snake:
    def __init__(self, game, screen):
        # draw snake with 3 circle:
        __w = game.board.get_width()
        __h = game.board.get_height()
        self.n_part = 3
        self.r = 10
        self.part = [(__w/10, __h/5), (__w/10 -
                                       2*self.r, __h/5), (__w/10 -
                                                          4*self.r, __h/5)]

        self.draw(game, screen, green, self.part[0][0], self.part[0][1])
        self.draw(game, screen, green, self.part[1][0], self.part[1][1])
        self.draw(game, screen, green, self.part[2][0], self.part[2][1])
        game.Update(screen)

    def draw(self, game, screen, color, x=0, y=0):
        pygame.draw.circle(game.board, color, (x, y), self.r)
        game.Update(screen)

    def move_up(self, game, screen):
        # only when y_head <= y_next_head
        if (self.part[0][1] <= self.part[1][1]):
            # draw new head
            head_pos = (self.part[0][0], self.part[0][1]-2*self.r)
            self.part.insert(0, head_pos)
            self.draw(game, screen, green, head_pos[0], head_pos[1])

            # delete tail
            last_pos = self.part[-1]
            self.draw(game, screen, light_brown, last_pos[0], last_pos[1])
            self.part.pop()

        # check collide to board:

    def move_down(self, game, screen):
        # only when y_head >= y_next_head
        if (self.part[0][1] >= self.part[1][1]):
            # draw new head
            head_pos = (self.part[0][0], self.part[0][1]+2*self.r)
            self.part.insert(0, head_pos)
            self.draw(game, screen, green, head_pos[0], head_pos[1])

            # delete tail
            last_pos = self.part[-1]
            self.draw(game, screen, light_brown, last_pos[0], last_pos[1])
            self.part.pop()

        # check collide to board:

    def move_left(self, game, screen):
        # only when x_head <= x_next_head
        if (self.part[0][0] <= self.part[1][0]):
            # draw new head
            head_pos = (self.part[0][0]-2*self.r, self.part[0][1])
            self.part.insert(0, head_pos)
            self.draw(game, screen, green, head_pos[0], head_pos[1])

            # delete tail
            last_pos = self.part[-1]
            self.draw(game, screen, light_brown, last_pos[0], last_pos[1])
            self.part.pop()

        # check collide to board:

    def move_right(self, game, screen):
        # only when x_head >= x_next_head
        if (self.part[0][0] >= self.part[1][0]):
            # draw new head
            head_pos = (self.part[0][0]+2*self.r, self.part[0][1])
            self.part.insert(0, head_pos)
            self.draw(game, screen, green, head_pos[0], head_pos[1])

            # delete tail
            last_pos = self.part[-1]
            self.draw(game, screen, light_brown, last_pos[0], last_pos[1])
            self.part.pop()

        # check collide to board:


class Game:
    def __init__(self, screen):
        # music, score:
        mixer.music.load('Sound/play.mp3')
        mixer.music.play()
        self.__w = screen.get_width()
        self.__h = screen.get_height()
        Text(screen, 'Your score: ', self.__w / 30, self.__h / 35, 36)

        # draw board:
        self.edge = pygame.Surface((self.__w, self.__h*0.9))
        self.edge.fill(brown)
        self.board = pygame.Surface((self.__w - 100, self.__h*0.9 - 100))
        self.board.fill(light_brown)
        self.edge.blit(self.board, (50, self.__h/10 - 35))
        screen.blit(self.edge, (0, self.__h/10))
        pygame.display.update()

    def Update(self, screen):
        self.edge.blit(self.board, (50, self.__h/10 - 35))
        screen.blit(self.edge, (0, self.__h/10))
        pygame.display.update()

    def Run(self, screen):
        # init the state of game (snake, score, food, heart)
        # open file, load game,
        quit_game = False
        snake = Snake(self, screen)
        while not quit_game:
            clock = pygame.time.Clock()
            for event in pygame.event.get():
                # event: pause, restart
                if event.type == pygame.QUIT:
                    quit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        snake.move_left(self, screen)
                    elif event.key == pygame.K_RIGHT:
                        snake.move_right(self, screen)
                    elif event.key == pygame.K_UP:
                        snake.move_up(self, screen)
                    elif event.key == pygame.K_DOWN:
                        snake.move_down(self, screen)
            clock.tick(90)
        # nhan biet phim mui ten con cham ?????
        

class Menu:
    def __init__(self):
        scr_size = pygame.display.get_desktop_sizes()
        x = scr_size[0][0] - 60
        y = scr_size[0][1] - 60
        self.screen = pygame.display.set_mode((x, y))
        self.screen.fill(light_brown)
        pygame.display.update()
        pygame.display.set_caption('SNAKE GAME')
        mixer.music.load('Sound/openning.mp3')
        mixer.music.play()

    def button(self, elip, rect, command=None):
        click = pygame.mouse.get_pressed()
        if elip.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.ellipse(self.screen, brown, rect)
            if click[0] and command != None:
                mixer.music.load('Sound/click.wav')
                mixer.music.play()
                pygame.event.wait()
                command()
        else:
            pygame.draw.ellipse(self.screen, white, rect)

    def Show(self):
        w = self.screen.get_width()
        h = self.screen.get_height()
        Text(self.screen, 'SNAKE GAME', w/3 + 70,
             h/10, 60, random.choice(color_list1))

        rect = (w/8, h/4, 300, 100)
        btn = pygame.draw.ellipse(self.screen, white, rect)
        self.button(btn, rect, self.New)
        Text(self.screen, '    START', rect[0] + rect[2]/4,
             rect[1] + rect[3]/3, 30, random.choice(black))

        rect = (w/8, h/2, 300, 100)
        btn = pygame.draw.ellipse(self.screen, white, rect)
        self.button(btn, rect)
        Text(self.screen, '  SETTING', rect[0] + rect[2] /
             4, rect[1] + rect[3]/3, 30, black)

        rect = (w/8, h / 4 * 3, 300, 100)
        btn = pygame.draw.ellipse(self.screen, white, rect)
        self.button(btn, rect)
        Text(self.screen, 'HIGH SCORES', rect[0] + rect[2] /
             5, rect[1] + rect[3]/3, 30, black)

        rect = (w/2 + 270, h/4, 300, 100)
        btn = pygame.draw.ellipse(self.screen, white, rect)
        self.button(btn, rect)
        Text(self.screen, '   RESUME', rect[0] + rect[2] /
             4, rect[1] + rect[3]/3, 30, black)

        rect = (w/2 + 270, h/2, 300, 100)
        btn = pygame.draw.ellipse(self.screen, white, rect)
        self.button(btn, rect)
        Text(self.screen, 'HOW TO PLAY', rect[0] + rect[2] /
             6, rect[1] + rect[3]/3, 30, black)

        rect = (w/2 + 270, h/4*3, 300, 100)
        btn = pygame.draw.ellipse(self.screen, white, rect)
        self.button(btn, rect, self.Quit)
        Text(self.screen, '  QUIT', rect[0] + rect[2] /
             3, rect[1] + rect[3]/3, 30, black)
        pygame.display.update()

    def New(self):
        # khoi tao game:
        # chay game + luu trang thai game (neu ko bi thua), luu diem cao nhat (neu co)
        self.screen.fill(white)
        pygame.display.update()
        G = Game(self.screen)
        G.Run(self.screen)

    def Resume(self):
        # khoi phuc trang thai game
        # chay game + luu trang thai game (neu ko bi thua)
        pass

    def HighScore(self):
        # show 5 highest score, day time and scores
        print('')

    def HowTo(self):
        # easy to understand tutorial
        print('')

    def Setting(self):
        # che do sang toi, am thanh...
        pass

    def Quit(self):
        exit()


def main():
    menu = Menu()
    quit_game = False
    while not quit_game:
        clock = pygame.time.Clock()
        for event in pygame.event.get():
            menu.Show()
            if event.type == pygame.QUIT:
                quit_game = True
            clock.tick(90)
    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
