import pygame
from pygame.locals import *
import sys


class Level:
    def __init__(self, level_name, map_name):
        self.clock = pygame.time.Clock()
        pygame.init()

        pygame.display.set_caption(level_name)

        with open('screen_size.txt') as f:
            size = f.read().split('x')
            self.WINDOW_SIZE = (int(size[0]), int(size[1]) - 60)

        with open('buttons.txt') as f:
            self.buttons_list = f.read().split()

        self.screen = pygame.display.set_mode(self.WINDOW_SIZE, 0, 32)
        self.display = pygame.Surface((576, 324))
        self.display_x = 576
        self.display_y = 324

        self.moving_right = False
        self.moving_left = False
        self.vertical_momentum = 0
        self.air_timer = 0

        self.true_scroll = [0, 0]

        self.game_map = self.load_map(map_name)

        self.bushes = self.load_bushes()
        self.willows = self.load_willows()
        self.grass = self.load_grass()
        self.ridges = self.load_ridges()
        self.pointers = self.load_pointers()
        self.trees = self.load_trees()

        self.dict_tiles = self.load_tiles()
        self.animation_frames = {}

        self.animation_database = dict()

        with open('character.txt') as f:
            self.character = f.read()

        if self.character == 'owlet':
            self.animation_database['run'] = self.load_animation('player_animations_owlet/run', [10, 10, 10, 10, 10, 10])
            self.animation_database['idle'] = self.load_animation('player_animations_owlet/idle', [10, 10, 10, 10])
            self.player_rect = pygame.Rect(24, 200, 20, 27)
        elif self.character == 'dude':
            self.animation_database['run'] = self.load_animation('player_animations_dude/run', [10, 10, 10, 10, 10, 10])
            self.animation_database['idle'] = self.load_animation('player_animations_dude/idle', [10, 10, 10, 10])
            self.player_rect = pygame.Rect(24, 200, 17, 27)
        else:
            self.animation_database['run'] = self.load_animation('player_animations/run', [10, 10, 10, 10, 10, 10])
            self.animation_database['idle'] = self.load_animation('player_animations/idle', [10, 10, 10, 10])
            self.player_rect = pygame.Rect(24, 200, 17, 28)
        
        self.player_action = 'idle'
        self.player_frame = 0
        self.player_flip = False

        self.coin_touched = 0

        self.coin_frame = 0
        self.coin_dict = self.load_coin_animation()

        self.coin_coords = self.get_coins_coords()

        self.coin_list = list()
        for i in range(4):
            for _ in range(10):
                self.coin_list.append(self.coin_dict[i])

        self.coin_animation_dict = dict()
        for i in range(len(self.coin_coords)):
            self.coin_animation_dict[i] = self.coin_list

        self.coin_sound = pygame.mixer.Sound(r'sounds\coin_sound.ogg')
        self.coin_sound.set_volume(0.1)
        self.jump_sound = pygame.mixer.Sound(r'sounds\sound_jump.mp3')
        self.jump_sound.set_volume(0.7)

        pygame.mixer.music.load(r'sounds\main_sound.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)

        self.jump_flag = False
        self.flag = True
        self.jump_counter = 0

        if level_name == 'First Level':
            self.file_name = 'level1_coins.txt'
            self.all_coins = '104'
        elif level_name == 'Second Level':
            self.file_name = 'level2_coins.txt'
            self.all_coins = '110'
        if level_name == 'Third Level':
            self.file_name = 'level3_coins.txt'
            self.all_coins = '119'

        self.level_name = level_name

        self.coins_flag = False
        if self.coin_touched == self.all_coins:
            self.coins_flag = True

        self.image_coin = pygame.image.load(r'tiles\coins\Tile_coin3.png')

        self.list_background = self.load_background()

    def game_loop(self):
        while self.flag:
            self.display.fill((146, 244, 255))

            # self.true_scroll[0] += (self.player_rect.x - self.true_scroll[0] - 343) / 20
            # self.true_scroll[1] += (self.player_rect.y - self.true_scroll[1] - 184) / 20

            self.true_scroll[0] += (self.player_rect.x - self.true_scroll[0] - 272) / 20
            self.true_scroll[1] += (self.player_rect.y - self.true_scroll[1] - 152) / 20

            scroll = self.true_scroll.copy()
            scroll[0] = int(scroll[0])
            scroll[1] = int(scroll[1])

            self.display.blit(self.list_background[0], (0, 0))
            self.display.blit(self.list_background[1], (0, 0))
            self.display.blit(self.list_background[4], (0, 0))

            tile_rects = []

            y = 0
            for layer in self.game_map:
                x = 0
                for tile in layer:
                    if tile != '-1':
                        tile = str(int(tile) + 1)
                        self.display.blit(self.dict_tiles[tile], (x * 32 - scroll[0], y * 32 - scroll[1]))
                        tile_rects.append(pygame.Rect(x * 32, y * 32, 32, 32))
                        self.display.blit(self.dict_tiles[tile], (x * 32 - scroll[0], y * 32 - scroll[1]))
                    x += 1
                y += 1

            player_movement = [0, 0]
            if self.moving_right:
                player_movement[0] += 2
            if self.moving_left:
                player_movement[0] -= 2
            player_movement[1] += self.vertical_momentum
            self.vertical_momentum += 0.185
            if self.vertical_momentum > 3:
                self.vertical_momentum = 3

            if player_movement[0] == 0:
                self.player_action, self.player_frame = self.change_action(self.player_action, self.player_frame,
                                                                           'idle')
            if player_movement[0] > 0:
                self.player_flip = False
                self.player_action, self.player_frame = self.change_action(self.player_action, self.player_frame, 'run')
            if player_movement[0] < 0:
                self.player_flip = True
                self.player_action, self.player_frame = self.change_action(self.player_action, self.player_frame, 'run')

            # ----------------------------------DECORATIONS-------------------------------------------------------------

            if self.level_name == 'First Level':
                willows1 = [[0, 6 * 32 - 6], [34 * 32, 10 * 32 - 6], [60 * 32, -32 - 6], [91 * 32, 8 * 32 - 6]]
                for i in range(len(willows1)):
                    self.display.blit(self.willows[0], (willows1[i][0] - scroll[0], willows1[i][1] - scroll[1]))

                willows2 = [[15 * 32, 2 * 32 - 7], [48 * 32, 4 * 32 - 7], [63 * 32, 9 * 32 - 7]]
                for i in range(len(willows2)):
                    self.display.blit(self.willows[1], (willows2[i][0] - scroll[0], willows2[i][1] - scroll[1]))

                willows3 = [[24 * 32, 4 * 32 + 10], [78 * 32, 3 * 32 + 10], [94 * 32, 6 * 32 + 10]]
                for i in range(len(willows3)):
                    self.display.blit(self.willows[2], (willows3[i][0] - scroll[0], willows3[i][1] - scroll[1]))

                ridges_coords = [[19 * 32, 6 * 32 + 7], [31 * 32, 13 * 32 + 7], [93 * 32, 11 * 32 + 7],
                                 [35 * 32, 2 * 32 + 4], [50 * 32, 5], [57 * 32, 2 * 32 - 8]]
                for i in range(3):
                    self.display.blit(self.ridges[0], (ridges_coords[i][0] - scroll[0], ridges_coords[i][1] - scroll[1]))

                self.display.blit(self.ridges[3], (ridges_coords[3][0] - scroll[0], ridges_coords[3][1] - scroll[1]))
                self.display.blit(self.ridges[1], (ridges_coords[4][0] - scroll[0], ridges_coords[4][1] - scroll[1]))
                self.display.blit(self.ridges[2], (ridges_coords[5][0] - scroll[0], ridges_coords[5][1] - scroll[1]))

                trees1_coords = [[65 * 32, 3 * 32 - 6]]
                self.display.blit(self.trees[0], (trees1_coords[0][0] - scroll[0], trees1_coords[0][1] - scroll[1]))

                trees2_coords = [[6 * 32, -2 * 32 - 3], [41 * 32, 8 * 32 - 3]]
                for i in range(len(trees2_coords)):
                    self.display.blit(self.trees[1], (trees2_coords[i][0] - scroll[0], trees2_coords[i][1] - scroll[1]))

                trees3_coords = [[75 * 32, 7 * 32 + 11]]
                self.display.blit(self.trees[2], (trees3_coords[0][0] - scroll[0], trees3_coords[0][1] - scroll[1]))

                bushes5_coords = [[19 * 32, 11 * 32 + 5], [60 * 32, 8 * 32 + 5], [73 * 32, 11 * 32 + 5], [79 * 32, 5]]
                for i in range(len(bushes5_coords)):
                    self.display.blit(self.bushes[4], (bushes5_coords[i][0] - scroll[0], bushes5_coords[i][1] - scroll[1]))

                bushes7_coords = [[29 * 32, 9], [72 * 32, 2 * 32 + 9], [98 * 32, 2 * 32 + 9]]
                for i in range(len(bushes7_coords)):
                    self.display.blit(self.bushes[6], (bushes7_coords[i][0] - scroll[0], bushes7_coords[i][1] - scroll[1]))

                bushes8_coords = [[11 * 32, 4 * 32 + 6], [42 * 32, 6 * 32 + 6], [55 * 32, 11 * 32 + 6]]
                for i in range(len(bushes8_coords)):
                    self.display.blit(self.bushes[7], (bushes8_coords[i][0] - scroll[0], bushes8_coords[i][1] - scroll[1]))

                grass6_coords = [[2 * 32, 4 * 32 + 24], [8 * 32, 7 * 32 + 24], [13 * 32, 4 * 32 + 24],
                                 [18 * 32, 6 * 32 + 24], [26 * 32, 3 * 32 + 24], [21 * 32, 11 * 32 + 24],
                                 [37 * 32, 3 * 32 + 24], [30 * 32, 9 * 32 + 24], [43 * 32, 11 * 32 + 24],
                                 [49 * 32, 8 * 32 + 24], [81 * 32, 24], [81 * 32, 8 * 32 + 24],
                                 [62 * 32, 8 * 32 + 24], [68 * 32, 10 * 32 + 24], [64 * 32, 13 * 32 + 24],
                                 [75 * 32, 11 * 32 + 24], [91 * 32, 11 * 32 + 24], [97 * 32, 11 * 32 + 24]]
                for i in range(len(grass6_coords)):
                    self.display.blit(self.grass[5], (grass6_coords[i][0] - scroll[0], grass6_coords[i][1] - scroll[1]))

                grass5_coords = [[36 * 32, 3 * 32 + 20], [43 * 32, 6 * 32 + 20], [61 * 32, 2 * 32 + 20],
                                 [67 * 32, 5 * 32 + 20], [65 * 32, 13 * 32 + 20], [77 * 32, 11 * 32 + 20],
                                 [83 * 32, 8 * 32 + 20], [95 * 32, 11 * 32 + 20]]
                for i in range(len(grass5_coords)):
                    self.display.blit(self.grass[4], (grass5_coords[i][0] - scroll[0], grass5_coords[i][1] - scroll[1]))

                grass1_coords = [[8 * 32, 32 + 15], [17 * 32, 6 * 32 + 15], [32 * 32, 13 * 32 + 15]]
                for i in range(len(grass1_coords)):
                    self.display.blit(self.grass[0], (grass1_coords[i][0] - scroll[0], grass1_coords[i][1] - scroll[1]))

                grass3_coords = [[50 * 32, 8 * 32 + 17], [99 * 32, 11 * 32 + 17]]
                for i in range(len(grass3_coords)):
                    self.display.blit(self.grass[2], (grass3_coords[i][0] - scroll[0], grass3_coords[i][1] - scroll[1]))

                grass4_coords = [[20 * 32, 6 * 32 + 21], [33 * 32, 13 * 32 + 21], [51 * 32, 21],
                                 [58 * 32, 2 * 32 + 21], [93 * 32, 11 * 32 + 21], [74 * 32, 11 * 32 + 21],
                                 [56 * 32, 11 * 32 + 21], [73 * 32, 2 * 32 + 21]]
                for i in range(len(grass4_coords)):
                    self.display.blit(self.grass[3], (grass4_coords[i][0] - scroll[0], grass4_coords[i][1] - scroll[1]))

            # -------------------------------------COINS----------------------------------------------------------------

            for i in range(len(self.coin_coords)):
                if 0 < (self.coin_coords[i][0] - self.player_rect[0]) <= 17 and \
                        0 < (self.coin_coords[i][1] - self.player_rect[1]) <= 28 and self.coin_animation_dict[i]:
                    self.coin_touched += 1
                    self.coin_animation_dict[i] = None
                    self.coin_sound.play()

            if self.coin_frame >= len(self.coin_list) - 1:
                self.coin_frame = 0
            else:
                self.coin_frame += 1

            for i in range(len(self.coin_coords)):
                if self.coin_animation_dict.get(i):
                    self.display.blit(self.coin_animation_dict.get(i)[self.coin_frame],
                                      (self.coin_coords[i][0] - scroll[0], self.coin_coords[i][1] - scroll[1]))

            # -------------------------------------COINS----------------------------------------------------------------

            self.create_text(str(self.coin_touched), str(len(self.coin_coords)))

            player_rect, collisions = self.move(self.player_rect, player_movement, tile_rects)

            if collisions['bottom']:
                self.air_timer = 0
                self.vertical_momentum = 0
                self.jump_counter = 0
            else:
                self.air_timer += 1

            self.player_frame += 1
            if self.player_frame >= len(self.animation_database[self.player_action]):
                self.player_frame = 0

            player_img_id = self.animation_database[self.player_action][self.player_frame]
            player_img = self.animation_frames[player_img_id]
            self.display.blit(pygame.transform.flip(player_img, self.player_flip, False),
                              (player_rect.x - scroll[0], player_rect.y - scroll[1]))

            if player_rect[1] >= 500:
                with open(self.file_name, 'w') as f:
                    f.write(str(self.coin_touched) + ' ' + self.all_coins)
                self.flag = False

            if str(self.coin_touched) == self.all_coins:
                with open(self.file_name, 'w') as f:
                    f.write(str(self.coin_touched) + ' ' + self.all_coins)
                self.flag = False

            for event in pygame.event.get():
                if event.type == QUIT:
                    with open(self.file_name, 'w') as f:
                        f.write(str(self.coin_touched) + ' ' + self.all_coins)
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if self.buttons_list[2] == 'right':
                        if event.key == K_RIGHT:
                            self.moving_right = True
                    elif self.buttons_list[2] == 'd':
                        if event.key == K_d:
                            self.moving_right = True

                    if self.buttons_list[1] == 'left':
                        if event.key == K_LEFT:
                            self.moving_left = True
                    elif self.buttons_list[1] == 'a':
                        if event.key == K_a:
                            self.moving_left = True

                    if self.buttons_list[0] == 'up':
                        if event.key == K_UP:
                            if self.jump_counter < 2:
                                self.jump_sound.play()
                                self.vertical_momentum = -4.2
                                self.jump_counter += 1

                    elif self.buttons_list[0] == 'w':
                        if event.key == K_w:
                            if self.jump_counter < 2:
                                self.jump_sound.play()
                                self.vertical_momentum = -4.2
                                self.jump_counter += 1

                if event.type == KEYUP:
                    if self.buttons_list[2] == 'right':
                        if event.key == K_RIGHT:
                            self.moving_right = False
                    elif self.buttons_list[2] == 'd':
                        if event.key == K_d:
                            self.moving_right = False

                if event.type == KEYUP:
                    if self.buttons_list[1] == 'left':
                        if event.key == K_LEFT:
                            self.moving_left = False
                    elif self.buttons_list[1] == 'a':
                        if event.key == K_a:
                            self.moving_left = False

            self.screen.blit(pygame.transform.scale(self.display, self.WINDOW_SIZE), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()

    def load_map(self, path):
        f = open(path + '.txt', 'r')
        data = f.read()
        f.close()
        data = data.split('\n')
        game_map = []
        for row in data:
            game_map.append(row.split(','))
        return game_map

    def create_text(self, num, length):
        font = pygame.font.Font(None, 16)
        text = font.render(num + ' / ' + length, False, (255, 213, 105))
        self.display.blit(text, (17, 5))
        self.display.blit(self.image_coin, (5, 5))

    def get_coins_coords(self):
        coin_coords = list()
        y = 0
        for layer in self.game_map:
            x = 0
            for tile in layer:
                if tile != '-1':
                    if self.game_map[(self.game_map.index(layer)) - 1][layer.index(tile)] == '-1':
                        coin_coords.append(list([x * 32 + 12, (y - 1) * 32 + 15]))
                x += 1
            y += 1
        return coin_coords

    def load_tiles(self):
        dict_tiles = {}
        for layer in self.game_map:
            for tile in layer:
                if tile != '-1':
                    tile = str(int(tile) + 1)
                    if len(tile) == 1:
                        dict_tiles[tile] = pygame.image.load(r'tiles\Tile_0' + tile + '.png')
                    if len(tile) >= 2:
                        dict_tiles[tile] = pygame.image.load(r'tiles\Tile_' + tile + '.png')
        return dict_tiles

    def load_coin_animation(self):
        coin_dict = dict()
        for i in range(4):
            coin_dict[i] = pygame.image.load(r'tiles\coins\Tile_coin' + str(i) + '.png')

        return coin_dict

    def load_background(self):
        layer1 = pygame.image.load(r'background_layers\layer1.png')
        layer2 = pygame.image.load(r'background_layers\layer2.png')
        layer3 = pygame.image.load(r'background_layers\layer3.png')
        layer4 = pygame.image.load(r'background_layers\layer4.png')
        layer5 = pygame.image.load(r'background_layers\layer5.png')

        return list([layer1, layer2, layer3, layer4, layer5])

    def load_bushes(self):
        bush1 = pygame.image.load(r'tiles\bushes\Tile_bush1.png')
        bush2 = pygame.image.load(r'tiles\bushes\Tile_bush2.png')
        bush3 = pygame.image.load(r'tiles\bushes\Tile_bush3.png')
        bush4 = pygame.image.load(r'tiles\bushes\Tile_bush4.png')
        bush5 = pygame.image.load(r'tiles\bushes\Tile_bush5.png')
        bush6 = pygame.image.load(r'tiles\bushes\Tile_bush6.png')
        bush7 = pygame.image.load(r'tiles\bushes\Tile_bush7.png')
        bush8 = pygame.image.load(r'tiles\bushes\Tile_bush8.png')
        bush9 = pygame.image.load(r'tiles\bushes\Tile_bush9.png')

        return list([bush1, bush2, bush3, bush4, bush5, bush6, bush7, bush8, bush9])

    def load_trees(self):
        tree1 = pygame.image.load(r'tiles\trees\Tile_tree1.png')
        tree2 = pygame.image.load(r'tiles\trees\Tile_tree2.png')
        tree3 = pygame.image.load(r'tiles\trees\Tile_tree3.png')

        return list([tree1, tree2, tree3])

    def load_willows(self):
        willow1 = pygame.image.load(r'tiles\willows\Tile_willow1.png')
        willow2 = pygame.image.load(r'tiles\willows\Tile_willow2.png')
        willow3 = pygame.image.load(r'tiles\willows\Tile_willow3.png')

        return list([willow1, willow2, willow3])

    def load_grass(self):
        grass1 = pygame.image.load(r'tiles\grass\Tile_grass1.png')
        grass2 = pygame.image.load(r'tiles\grass\Tile_grass2.png')
        grass3 = pygame.image.load(r'tiles\grass\Tile_grass3.png')
        grass4 = pygame.image.load(r'tiles\grass\Tile_grass4.png')
        grass5 = pygame.image.load(r'tiles\grass\Tile_grass5.png')
        grass6 = pygame.image.load(r'tiles\grass\Tile_grass6.png')
        grass7 = pygame.image.load(r'tiles\grass\Tile_grass7.png')
        grass8 = pygame.image.load(r'tiles\grass\Tile_grass8.png')
        grass9 = pygame.image.load(r'tiles\grass\Tile_grass9.png')
        grass10 = pygame.image.load(r'tiles\grass\Tile_grass10.png')

        return list([grass1, grass2, grass3, grass4, grass5, grass6, grass7, grass8, grass9, grass10])

    def load_ridges(self):
        ridge1 = pygame.image.load(r'tiles\ridges\Tile_ridge1.png')
        ridge2 = pygame.image.load(r'tiles\ridges\Tile_ridge2.png')
        ridge3 = pygame.image.load(r'tiles\ridges\Tile_ridge3.png')
        ridge4 = pygame.image.load(r'tiles\ridges\Tile_ridge4.png')
        ridge5 = pygame.image.load(r'tiles\ridges\Tile_ridge5.png')
        ridge6 = pygame.image.load(r'tiles\ridges\Tile_ridge6.png')

        return list([ridge1, ridge2, ridge3, ridge4, ridge5, ridge6])

    def load_pointers(self):
        pointer1 = pygame.image.load(r'tiles\pointers\Tile_pointer1.png')
        pointer2 = pygame.image.load(r'tiles\pointers\Tile_pointer2.png')
        pointer3 = pygame.image.load(r'tiles\pointers\Tile_pointer3.png')
        pointer4 = pygame.image.load(r'tiles\pointers\Tile_pointer4.png')
        pointer5 = pygame.image.load(r'tiles\pointers\Tile_pointer5.png')
        pointer6 = pygame.image.load(r'tiles\pointers\Tile_pointer6.png')
        pointer7 = pygame.image.load(r'tiles\pointers\Tile_pointer7.png')
        pointer8 = pygame.image.load(r'tiles\pointers\Tile_pointer8.png')

        return list([pointer1, pointer2, pointer3, pointer4, pointer5, pointer6, pointer7, pointer8])

    def load_animation(self, path, frame_durations):
        animation_name = path.split('/')[-1]
        animation_frame_data = []
        n = 0
        for frame in frame_durations:
            animation_frame_id = animation_name + '_' + str(n)
            img_loc = path + '/' + animation_frame_id + '.png'
            animation_image = pygame.image.load(img_loc).convert()
            animation_image.set_colorkey((0, 0, 0))
            self.animation_frames[animation_frame_id] = animation_image.copy()

            for i in range(frame):
                animation_frame_data.append(animation_frame_id)
            n += 1

        return animation_frame_data

    def change_action(self, action_var, frame, new_value):
        if action_var != new_value:
            action_var = new_value
            frame = 0
        return action_var, frame

    def collision_test(self, rect, tiles):
        hit_list = []
        for tile in tiles:
            if rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move(self, rect, movement, tiles):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        rect.x += movement[0]
        hit_list = self.collision_test(rect, tiles)
        for tile in hit_list:
            if movement[0] > 0:
                rect.right = tile.left
                collision_types['right'] = True
            elif movement[0] < 0:
                rect.left = tile.right
                collision_types['left'] = True

        rect.y += movement[1]
        hit_list = self.collision_test(rect, tiles)

        for tile in hit_list:
            if movement[1] > 0:
                rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                rect.top = tile.bottom
                collision_types['top'] = True
        return rect, collision_types


class FirstLevel(Level):
    def __init__(self):
        super().__init__('First Level', 'level1')


class SecondLevel(Level):
    def __init__(self):
        super().__init__('Second Level', 'level2')


class ThirdLevel(Level):
    def __init__(self):
        super().__init__('Third Level', 'level3')
