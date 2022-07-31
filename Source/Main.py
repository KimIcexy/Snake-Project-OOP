from copy import deepcopy
import json
from msvcrt import getch
import random
from re import S
from time import sleep
import pygame
from sympy import false
from pygame import mixer
pygame.init()
mixer.init()

white = [255, 255, 255]
black = [0, 0, 0]
light_brown = [230, 204, 179]
brown = [153, 102, 51]
light_green = [170, 255, 0]
green = [0, 153, 0]
light_blue = [153, 204, 255]
blue = [0, 0, 255]
light_pink = [255, 153, 153]
pink = [255, 51, 153]
red = [255, 0, 0]
dark_red = [179, 36, 0]
color_list1 = [black, brown, dark_red, red]
color_snake = [[light_green, green], [light_blue, blue], [light_pink, pink]]
speed = [1/8, 1/16, 1/4]
game_file = "Data/data.json"
score_file = "Data/score.json"
max_plus_score = 150
plus_part = 3
low_speed = "Image/low_speed.png"
normal_speed = "Image/normal_speed.png"
high_speed = "Image/high_speed.png"
off_music = "Image/off_music.png"
on_music = "Image/on_music.png"
green_snake = "Image/green_snake.png"
blue_snake = "Image/blue_snake.png"
pink_snake = "Image/pink_snake.png"
icon_scale = (256, 256)


class Text:
    def __init__(self, screen, txt, pos, size, color=black, font='cambria'):
        font = pygame.font.SysFont(font, size)
        text = font.render(txt, True, color)
        screen.blit(text, pos)
        pygame.display.update()


class Setting_But:
    def __init__(self, screen, txt, rect, pos, icon_list, i_now):
        # ve button, ghi Text, hien image, danh dau image hien tai
        # gan list
        pygame.draw.rect(screen, brown, rect)
        Text(screen, txt, pos, 30, white)
        self.i_now = i_now  # default icon
        self.txt = txt
        self.pos = pos
        image = pygame.image.load(icon_list[self.i_now])
        image = pygame.transform.scale(image, icon_scale)
        self.image_pos = (pos[0] - icon_scale[0]/4 - 10,
                          pos[1] - 100 - icon_scale[0])
        screen.blit(image, self.image_pos)
        pygame.display.update()

    def change_image(self, icon_list, screen):
        self.i_now += 1
        if self.i_now == len(icon_list):
            self.i_now = 0
        image = pygame.image.load(icon_list[self.i_now])
        image = pygame.transform.scale(image, icon_scale)
        screen.blit(image, self.image_pos)
        pygame.display.update()

    def modify(self, rect, icon_list, screen, on_music, command):
        click = pygame.mouse.get_pressed()
        if rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, white, rect)
            Text(screen, self.txt, self.pos, 30, black)
            if click[0]:
                if on_music == 1:
                    pygame.mixer.Channel(0).play(
                        pygame.mixer.Sound('Sound/click.wav'))
                pygame.event.wait()
                self.change_image(icon_list, screen)
                command()
        else:
            pygame.draw.rect(screen, brown, rect)
            Text(screen, self.txt, self.pos, 30, white)
            pygame.display.update()


class Food:
    def __init__(self, game, mode=0):
        self.w = game.board.get_width()
        self.h = game.board.get_height()
        self.len = 10
        self.pos = [-1, -1]
        self.color = red
        if mode != 0:  # resume
            self.load()

    def load(self):
        with open(game_file, "r") as f:
            data = json.load(f)
            self.pos = data[len(data) - 2]
            self.color = data[len(data) - 1]

    def random_food_pos(self):
        while (self.pos == [-1, -1]):
            new_x = random.randint(2 * self.len, self.w - 2*self.len)
            new_y = random.randint(2 * self.len, self.h - 2*self.len)
            if (new_x != self.pos[0] or new_y != self.pos[1]):  # new pos != old pos
                self.pos = [new_x, new_y]
        return self.pos

    def appear(self, game, screen):  # after check with the snake pos
        if self.color[1] > 0:
            self.len = 20
        pygame.draw.rect(game.board, self.color,
                         (self.pos[0], self.pos[1], self.len, self.len))
        game.update_screen(screen)

    def disappear(self, game, screen):
        if(self.pos != [-1, -1]):
            pygame.draw.rect(game.board, light_brown,
                             (self.pos[0], self.pos[1], self.len, self.len))
            game.update_screen(screen)
            self.pos = [-1, -1]
            self.len = 10


class Snake:
    def __init__(self, game, screen, mode=0, color=0):  # mode: 0 (new), 1 (resume)
        self.w = game.board.get_width()
        self.h = game.board.get_height()
        self.r = 10
        self.part = []
        # direction of head and tail: 0: right, 1: left, 2: up, 3: down
        self.head_d = 0
        self.tail_d = 0
        self.color = color_snake[color]
        if mode == 0:  # NEW
            self.default_3 = [self.r, self.h / 2 - self.r]
            self.default_2 = [self.r*3, self.h / 2 - self.r]
            self.default_1 = [self.r*5, self.h / 2 - self.r]
            self.part = [self.default_1, self.default_2, self.default_3]
        else:  # RESUME
            self.load(game)
        if (len(self.part) < 3):
            return
        self.draw(game, screen, self.color[0],
                  self.part[0][0], self.part[0][1])
        for i in range(1, len(self.part)):
            self.draw(game, screen, self.color[1],
                      self.part[i][0], self.part[i][1])
        game.update_screen(screen)

    def load(self, game):
        with open(game_file, "r") as f:
            try:
                data = json.load(f)
                game.counter = data[len(data) - 3]
                game.score = data[len(data) - 4]
                for i in range(len(data[0])):
                    self.part.append(data[0][i])
                if len(self.part) < 3:
                    return
                self.head_direction()
                self.tail_direction()
            except json.JSONDecodeError:
                return

    def head_direction(self):
        self.head_d = self.check_cross_border()
        if self.head_d != -1:
            return

        # NOT cross border:
        # when x_head > x_next_head (RIGHT):
        if self.part[0][0] > self.part[1][0]:
            self.head_d = 0
        # when x_head < x_next_head (LEFT):
        if self.part[0][0] < self.part[1][0]:
            self.head_d = 1
        # when y_head < y_next_head (UP):
        if self.part[0][1] < self.part[1][1]:
            self.head_d = 2
        # when y_head > y_next_head (DOWN):
        if self.part[0][1] > self.part[1][1]:
            self.head_d = 3

    def tail_direction(self):
        old_size = len(self.part)
        old_tail = self.part[old_size - 1]
        old_pre_tail = self.part[old_size - 2]

        # the tail is moving UP or DOWN:
        if(old_tail[0] == old_pre_tail[0]):
            if(old_tail[1] > old_pre_tail[1]):  # up
                self.tail_d = 2
            else:
                self.tail_d = 3

        # the tail is moving LEFT or RIGHT:
        elif(old_tail[1] == old_pre_tail[1]):
            if(old_tail[0] > old_pre_tail[0]):  # left
                self.tail_d = 1
            else:
                self.tail_d = 0

    def draw(self, game, screen, color, x=0, y=0):
        pygame.draw.circle(game.board, color, (x, y), self.r)
        game.update_screen(screen)

    def add_part(self, game, screen, x=0, y=0):
        new_part = [x, y]
        self.check_coordinate(game, new_part)
        self.part.insert(len(self.part), new_part)
        self.draw(game, screen, self.color[1], new_part[0], new_part[1])

    # after touching the boundary, it will reverse path to the opposite one
    def check_coordinate(self, game, pos):
        if (pos[0] < self.r):
            pos[0] = self.w - self.r
        elif (pos[0] > self.w - self.r):
            pos[0] = self.r
        if (pos[1] < self.r):
            pos[1] = self.h - self.r
        elif (pos[1] > self.h - self.r):
            pos[1] = self.r

    def check_cross_border(self):
        for i in range(len(self.part) - 1):
            # cross the right border
            if((self.part[i][0] == self.r)
               and (self.part[i+1][0]+3*self.r > self.w)):
                return 0
            # cross the left border
            if((self.part[i][0] == (self.w - self.r))
               and (self.part[i+1][0]-3*self.r < 0)):
                return 1
            # cross the top border
            if((self.part[i][1] == (self.h - self.r))
               and (self.part[i+1][1]-3*self.r < 0)):
                return 2
            # cross the bottom border
            if((self.part[i][1] == self.r)
               and (self.part[i+1][1]+3*self.r >= self.h)):
                return 3
        return -1

    def move_up(self, game, screen):
        # delete tail
        last_pos = self.part[-1]
        self.draw(game, screen, light_brown, last_pos[0], last_pos[1])
        self.part.pop()

        # draw new parts:
        head_pos = [self.part[0][0], self.part[0][1]-2*self.r]
        self.check_coordinate(game, head_pos)
        self.part.insert(0, head_pos)
        self.draw(game, screen, self.color[0], head_pos[0], head_pos[1])
        for i in range(1, self.part.__len__()):
            self.draw(game, screen, self.color[1],
                      self.part[i][0], self.part[i][1])

    def move_down(self, game, screen):
        # delete tail
        last_pos = self.part[-1]
        self.draw(game, screen, light_brown, last_pos[0], last_pos[1])
        self.part.pop()

        # draw new parts:
        head_pos = [self.part[0][0], self.part[0][1]+2*self.r]
        self.check_coordinate(game, head_pos)
        self.part.insert(0, head_pos)
        self.draw(game, screen, self.color[0], head_pos[0], head_pos[1])
        for i in range(1, self.part.__len__()):
            self.draw(game, screen, self.color[1],
                      self.part[i][0], self.part[i][1])

    def move_left(self, game, screen):
        # delete tail
        last_pos = self.part[-1]
        self.draw(game, screen, light_brown, last_pos[0], last_pos[1])
        self.part.pop()

        # draw new head
        head_pos = [self.part[0][0]-2*self.r, self.part[0][1]]
        self.check_coordinate(game, head_pos)
        self.part.insert(0, head_pos)
        self.draw(game, screen, self.color[0], head_pos[0], head_pos[1])

        for i in range(1, self.part.__len__()):
            self.draw(game, screen, self.color[1],
                      self.part[i][0], self.part[i][1])

    def move_right(self, game, screen):
        # delete tail
        last_pos = self.part[-1]
        self.draw(game, screen, light_brown, last_pos[0], last_pos[1])
        self.part.pop()

        # draw new head
        head_pos = [self.part[0][0]+2*self.r, self.part[0][1]]
        self.check_coordinate(game, head_pos)
        self.part.insert(0, head_pos)
        self.draw(game, screen, self.color[0], head_pos[0], head_pos[1])
        for i in range(1, self.part.__len__()):
            self.draw(game, screen, self.color[1],
                      self.part[i][0], self.part[i][1])

    # moving type (0: right, 1: left, 2: up, 3: down)
    def move(self, game, screen):
        if self.head_d == 1:
            self.move_left(game, screen)
        elif self.head_d == 2:
            self.move_up(game, screen)
        elif self.head_d == 3:
            self.move_down(game, screen)
        else:
            self.move_right(game, screen)

    def check_part_collide_food(self, i, food):
        x = self.part[i][0]
        y = self.part[i][1]
        food_x = food.pos[0]
        food_y = food.pos[1]
        # head_x = [food_x - self.r, food_x + food.len + self.r]
        # head_y = [food_y - self.r, food_y + food.len + self.r]
        if ((food_x - self.r <= x) and (x <= food_x + food.len + self.r)):
            if ((food_y - self.r <= y) and (y <= food_y + food.len + self.r)):
                return True
        return False

    def check_eating(self, game, screen, food):
        # check the HEAD:
        check = self.check_part_collide_food(0, food)
        if check == True:
            return True

        # check if exists other snake PARTS collide to the food:
        for i in range(1, len(self.part)):
            check = self.check_part_collide_food(i, food)
            if check == True:
                food.appear(game, screen)
        return False

    def become_longer(self, game, screen, eat_special):
        n_part = 1  # number of new parts added to the snake
        if eat_special == True:
            n_part = plus_part
        self.tail_direction()

        for i in range(n_part):
            new_tail = [0, 0]
            old_size = len(self.part)
            old_tail = self.part[old_size - 1]
            old_pre_tail = self.part[old_size - 2]

            if self.tail_d == 2:  # up
                new_tail = [old_tail[0], old_tail[1] + self.r]
            elif self.tail_d == 3:  # down
                new_tail = [old_tail[0], old_tail[1] - self.r]
            elif self.tail_d == 1:  # left
                new_tail = [old_tail[0] + self.r, old_tail[1]]
            else:
                new_tail = [old_tail[0] - self.r, old_tail[1]]

            # add:
            self.add_part(game, screen, new_tail[0], new_tail[1])

    def check_appear_food(self, food, game, screen):
        check = True
        food.random_food_pos()
        while(1):
            for i in range(len(self.part)):
                if self.check_part_collide_food(i, food) == True:
                    check = False
                    food.pos = [-1, -1]
                    food.color = red
                    food.random_food_pos()
                    break
            if (check == True):
                food.appear(game, screen)
                break

    def kill(self, game, screen):
        for i in range(1, len(self.part)):
            if (self.part[0] == self.part[i]):
                return True
        return False


class Game:
    def __init__(self, screen, on_music=1):
        if on_music == 1:
            mixer.music.load('Sound/play.mp3')
            mixer.music.play(-1)  # play indefinitely
        self.w = screen.get_width()
        self.h = screen.get_height()
        self.score = 0
        self.counter = 0  # count times of appear new food (0->3)
        self.high_score = [0, 0, 0, 0, 0]

        # draw board:
        self.edge = pygame.Surface((self.w, self.h*0.9))
        self.edge.fill(brown)
        self.board = pygame.Surface((self.w - 100, self.h*0.9 - 100))
        self.board.fill(light_brown)
        self.update_screen(screen)

    def update_screen(self, screen):
        self.edge.blit(self.board, (50, self.h/10 - 35))
        screen.blit(self.edge, (0, self.h/10))
        pygame.display.update()

    def update_score(self, screen, is_special, special_color):
        # erase old score:
        pygame.draw.rect(screen, white, (self.w / 30, self.h / 35, self.w, 50))
        pygame.display.update()
        if is_special == False:
            self.score += 3
        else:
            self.score = int(self.score + (max_plus_score - special_color) / 3)
        text = 'Your score: ' + str(self.score)
        Text(screen, text, (self.w / 30, self.h / 35), 36)
        pygame.display.update()

    def update_eat(self, snake, food, screen, on_music):
        is_special = (divmod(self.counter, 3)[1] == 0 and self.counter != 0)
        if(snake.check_eating(self, screen, food) == True):
            food.disappear(self, screen)
            if on_music == 1:
                pygame.mixer.Channel(0).play(
                    pygame.mixer.Sound('Sound/eat.mp3'))
            # if eat special, + 3
            snake.become_longer(self, screen, is_special)
            # if eat special, plus more if eat faster!
            self.update_score(screen, is_special, food.color[1])
            if is_special == True:  # previous eating is special!
                food.color[1] = 0  # return to normal food
                self.counter = 0  # restore to 0
                snake.check_appear_food(food, self, screen)
                return
            self.counter += 1

            # special food appears after 3 eatting
            if (divmod(self.counter, 3)[1] == 0):
                food.color[1] += 3  # lightening red color
            snake.check_appear_food(food, self, screen)

        elif is_special == True:  # update new color for special food
            food.color[1] += 3
            if food.color[1] > max_plus_score:  # return to normal food
                food.disappear(self, screen)
                food.color[1] = 0
                self.counter = 0  # restore
            snake.check_appear_food(food, self, screen)

    def save_game_data(self, snake, food):
        with open(game_file, "w") as f:
            data = []
            data.append(deepcopy(snake.part))
            data.append(self.score)
            data.append(self.counter)
            data.append(food.pos)
            data.append(food.color)
            json.dump(data, f)

    def save_high_score(self):
        with open(score_file, "r") as f:
            try:
                data = json.load(f)
                for i in range(len(data)):
                    self.high_score[i] = data[i]
            except json.JSONDecodeError:
                pass

        for k in range(len(self.high_score) - 1):
            if self.score > self.high_score[k]:
                for i in range(4 - k):  # just save 5 high score
                    self.high_score[4-i] = self.high_score[4-i-1]
                self.high_score[k] = self.score
                break
        with open(score_file, "w") as f:
            json.dump(self.high_score, f)

    def run(self, screen, mode, on_music, color_snake, level):  # mode: 0: NEW, 1: RESUME
        quit_game = False
        snake = Snake(self, screen, mode, color_snake)

        # no saved data for last game
        if len(snake.part) == 0:
            if on_music == 1:
                pygame.mixer.Channel(0).play(
                    pygame.mixer.Sound('Sound/wrong_select.mp3'))
            return

        food = Food(self, mode)
        text = 'Your score: ' + str(self.score)
        Text(screen, text, (self.w / 30, self.h / 35), 36)
        snake.check_appear_food(food, self, screen)
        food.appear(self, screen)

        while not quit_game:
            clock = pygame.time.Clock()
            snake.move(self, screen)
            self.update_eat(snake, food, screen, on_music)
            if(snake.kill(self, screen) == True):
                quit_game = True
                if on_music == 1:
                    mixer.music.load('Sound/fail.wav')
                    mixer.music.play()
                # empty the game file, save high score:
                with open(game_file, "w") as f:
                    pass
                self.save_high_score()
                sleep(2)
            for event in pygame.event.get():
                # event: pause, restart
                if event.type == pygame.QUIT:
                    quit_game = True
                    self.save_game_data(snake, food)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if snake.head_d != 1:  # not change to wrong direction
                            snake.head_d = 0
                    elif event.key == pygame.K_LEFT:
                        if snake.head_d != 0:
                            snake.head_d = 1
                    elif event.key == pygame.K_UP:
                        if snake.head_d != 3:
                            snake.head_d = 2
                    elif event.key == pygame.K_DOWN:
                        if snake.head_d != 2:
                            snake.head_d = 3
            sleep(speed[level])
            clock.tick(60)


class Menu:
    def __init__(self):
        scr_size = pygame.display.get_desktop_sizes()
        x = scr_size[0][0] - 60
        y = scr_size[0][1] - 60
        self.screen = pygame.display.set_mode((x, y))
        # setting state (music, speed, color): index in list (def setting)
        self.state_now = [1, 0, 0]
        self.refresh()

    def refresh(self):
        self.screen.fill(light_brown)
        pygame.display.update()
        pygame.display.set_caption('SNAKE GAME')
        if self.state_now[0] == 1:
            mixer.music.load('Sound/openning.mp3')
            mixer.music.play(-1)

    def button(self, elip, rect, command=None):
        click = pygame.mouse.get_pressed()
        if elip.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.ellipse(self.screen, brown, rect)
            if click[0] and command != None:
                if self.state_now[0] == True:
                    pygame.mixer.Channel(0).play(
                        pygame.mixer.Sound('Sound/click.wav'))
                pygame.event.wait()
                command()
                self.refresh()
        else:
            pygame.draw.ellipse(self.screen, white, rect)

    def show(self):
        w = self.screen.get_width()
        h = self.screen.get_height()
        Text(self.screen, 'SNAKE GAME', (w/3 + 70,
             h/10), 60, random.choice(color_list1))

        rect = (w/8, h/4, 300, 100)
        btn = pygame.draw.ellipse(self.screen, white, rect)
        self.button(btn, rect, self.new)
        Text(self.screen, '    START', (rect[0] + rect[2]/4,
             rect[1] + rect[3]/3), 30, random.choice(black))

        rect = (w/8, h/2, 300, 100)
        btn = pygame.draw.ellipse(self.screen, white, rect)
        self.button(btn, rect, self.setting)
        Text(self.screen, '  SETTING', (rect[0] + rect[2] /
             4, rect[1] + rect[3]/3), 30, black)

        rect = (w/8, h / 4 * 3, 300, 100)
        btn = pygame.draw.ellipse(self.screen, white, rect)
        self.button(btn, rect, self.highscore)
        Text(self.screen, 'HIGH SCORES', (rect[0] + rect[2] /
             5, rect[1] + rect[3]/3), 30, black)

        rect = (w/2 + 270, h/4, 300, 100)
        btn = pygame.draw.ellipse(self.screen, white, rect)
        self.button(btn, rect, self.resume)
        Text(self.screen, '   RESUME', (rect[0] + rect[2] /
             4, rect[1] + rect[3]/3), 30, black)

        rect = (w/2 + 270, h/2, 300, 100)
        btn = pygame.draw.ellipse(self.screen, white, rect)
        self.button(btn, rect, self.how_to)
        Text(self.screen, 'HOW TO PLAY', (rect[0] + rect[2] /
             6, rect[1] + rect[3]/3), 30, black)

        rect = (w/2 + 270, h/4*3, 300, 100)
        btn = pygame.draw.ellipse(self.screen, white, rect)
        self.button(btn, rect, self.quit)
        Text(self.screen, '  QUIT', (rect[0] + rect[2] /
             3, rect[1] + rect[3]/3), 30, black)
        pygame.display.update()

    def new(self):
        self.screen.fill(white)
        pygame.display.update()
        G = Game(self.screen, self.state_now[0])
        G.run(self.screen, 0, self.state_now[0],
              self.state_now[2], self.state_now[1])

    def resume(self):
        self.screen.fill(white)
        pygame.display.update()
        G = Game(self.screen, self.state_now[0])
        G.run(self.screen, 1, self.state_now[0],
              self.state_now[2], self.state_now[1])

    def highscore(self):
        # load 5 highest scores
        high_score = [0, 0, 0, 0, 0]
        with open(score_file, "r") as f:
            try:
                data = json.load(f)
                for i in range(len(data)):
                    high_score[i] = data[i]

            except json.JSONDecodeError:
                return

        # show
        w = self.screen.get_width()
        h = self.screen.get_height()
        self.screen.fill(light_brown)
        board = pygame.Surface((w / 2, h*0.8))
        board.fill(brown)
        for i in range(5):
            txt = '#' + str(i + 1) + ' .                 ' + str(high_score[i])
            Text(board, txt, (w/8,
                 h/5 + i*90), 45, white)
        self.screen.blit(board, (w / 4, h/10))
        Text(self.screen, 'HIGHEST SCORES', (w/3,
             h/6), 65, white)
        pygame.display.update()

        quit_board = False
        while (quit_board == False):
            clock = pygame.time.Clock()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_board = True
                    self.refresh()
            clock.tick(60)

    def how_to(self):
        w = self.screen.get_width()
        h = self.screen.get_height()
        self.screen.fill(light_brown)
        board = pygame.Surface((w * 0.8, h*0.8))
        board.fill(white)
        x = w/9
        y = h/10 + 50
        delta = 50
        txt = 'Use arrow keys to move your snake.'
        Text(board, txt, (x, y), 20)
        txt = 'If the snake touches a border, it will move to another opposite one!'
        Text(board, txt, (x, y+delta), 20)
        txt = 'Let the snake eat more food for increasing your score.'
        Text(board, txt, (x, y+delta*2), 20)
        txt = 'There are NORMAL food and SPECIAL food.'
        Text(board, txt, (x, y+delta*3), 20)

        txt = 'The special food help you develop more faster!'
        Text(board, txt, (x, y+delta*4), 20)
        txt = 'Try your best to eat it as soon as possible for having more score!'
        Text(board, txt, (x, y+delta*5), 20)
        txt = 'By the way, do not make the snake eat itself then the game will be over!'
        Text(board, txt, (x, y+delta*6), 20)
        txt = 'Tips: You can turn on/off the music, modify the speed and color of your snake in the SETTING menu.'
        Text(board, txt, (x, y+delta*7), 20)
        txt = 'Hope you enjoy this simple game! ^^'
        Text(board, txt, (x, y+delta*8), 20)
        
        self.screen.blit(board, (w / 10, h/10))
        Text(self.screen, 'HOW TO PLAY', (x + 130, y - 25), 65, red)
        pygame.display.update()

        quit_board = False
        while (quit_board == False):
            clock = pygame.time.Clock()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_board = True
                    self.refresh()
            clock.tick(60)

    def set_music(self):
        self.state_now[0] = not self.state_now[0]
        if self.state_now[0] == 1:
            mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()

    def set_speed(self):
        self.state_now[1] += 1
        if self.state_now[1] == len(speed):
            self.state_now[1] = 0

    def set_color(self):
        self.state_now[2] += 1
        if self.state_now[2] == len(color_snake):
            self.state_now[1] = 0

    def setting(self):
        # sound, speed, color
        w = self.screen.get_width()
        h = self.screen.get_height()
        self.screen.fill(light_brown)
        pygame.display.update()
        quit = False

        music_rect = pygame.Rect(w/8, h * 0.8, 100, 50)
        music_pos = [music_rect[0] + 10, music_rect[1] + 5]
        music_icon_list = [off_music, on_music]
        music_set = Setting_But(
            self.screen, "Music", music_rect, music_pos, music_icon_list, self.state_now[0])

        speed_rect = pygame.Rect(w/8 + 2 * icon_scale[0], h * 0.8, 100, 50)
        speed_pos = [speed_rect[0] + 10, speed_rect[1] + 5]
        speed_icon_list = [normal_speed, high_speed, low_speed]
        speed_set = Setting_But(
            self.screen, "Speed", speed_rect, speed_pos, speed_icon_list, self.state_now[1])

        color_rect = pygame.Rect(w/8 + 4 * icon_scale[0], h * 0.8, 100, 50)
        color_pos = [color_rect[0] + 10, color_rect[1] + 5]
        color_icon_list = [green_snake, blue_snake, pink_snake]
        color_set = Setting_But(
            self.screen, "Color", color_rect, color_pos, color_icon_list, self.state_now[2])

        while (quit == False):
            clock = pygame.time.Clock()
            Text(self.screen, 'SETTING', (w/3 + 100,
                                          h/10), 60, random.choice(color_list1))
            music_set.modify(music_rect, music_icon_list,
                             self.screen, self.state_now[0], self.set_music)
            speed_set.modify(speed_rect, speed_icon_list,
                             self.screen, self.state_now[0], self.set_speed)
            color_set.modify(color_rect, color_icon_list,
                             self.screen, self.state_now[0], self.set_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit = True
                    self.refresh()

            clock.tick(60)

    def quit(self):
        exit()


def main():
    menu = Menu()
    quit_game = False
    while not quit_game:
        clock = pygame.time.Clock()
        menu.show()
        # place 'menu.Show' here
        # because after execute the command,
        # we can go to the next loop instead of waiting for the next game event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game = True
                menu.refresh()

        clock.tick(60)
    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
