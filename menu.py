from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from level import *


def set_level_coins(file_name):
    file_name = file_name + '.txt'
    with open(file_name) as f:
        touched_c, all_c = f.read().split()

    return touched_c, all_c


class Menu(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('main_menu.ui', self)

        self.selected_buttons = dict()

        self.widget_settings.hide()
        self.widget_play.hide()
        self.widget_passed_level.hide()
        self.widget_characters.hide()
        self.widget_screen_size.hide()
        self.widget_buttons.hide()

        self.initUI()

    def initUI(self):
        self.button_settings.clicked.connect(self.open_settings)
        self.button_back_settings.clicked.connect(self.close_settings)

        # ----------------------------------------------PLAY------------------------------------------------------------
        self.button_play.clicked.connect(self.open_play)
        self.button_back_play.clicked.connect(self.close_play)

        # COINS
        level_coins = set_level_coins('level1_coins')
        self.level1_coins.setText(level_coins[0] + ' / ' + level_coins[1])

        level_coins = set_level_coins('level2_coins')
        self.level2_coins.setText(level_coins[0] + ' / ' + level_coins[1])

        level_coins = set_level_coins('level3_coins')
        self.level3_coins.setText(level_coins[0] + ' / ' + level_coins[1])

        # LOAD LEVELS
        self.button_level1.clicked.connect(self.open_level1)
        self.button_level2.clicked.connect(self.open_level2)
        self.button_level3.clicked.connect(self.open_level3)

        # CLEAR
        self.button_clear.clicked.connect(self.clear_touched_coins)

        self.button_back_passed_level.clicked.connect(self.close_passed_level)

        # ----------------------------------------------CHARACTERS------------------------------------------------------
        self.button_characters.clicked.connect(self.open_characters)
        self.button_back_characters.clicked.connect(self.close_characters)

        # PICK CHARACTER
        self.button_dude_monster.clicked.connect(self.pick_dude_monster)
        self.button_pink_monster.clicked.connect(self.pick_pink_monster)
        self.button_owlet_monster.clicked.connect(self.pick_owlet_monster)

        # ----------------------------------------------SCREEN SIZE-----------------------------------------------------
        self.button_screen_size.clicked.connect(self.open_screen_size)
        self.button_back_screen_size.clicked.connect(self.close_screen_size)

        # CHANGE SCREEN SIZE
        self.button_size1.clicked.connect(self.set_screen_size1)
        self.button_size2.clicked.connect(self.set_screen_size2)
        self.button_size3.clicked.connect(self.set_screen_size3)
        self.button_size4.clicked.connect(self.set_screen_size4)
        self.button_size5.clicked.connect(self.set_screen_size5)
        self.button_size6.clicked.connect(self.set_screen_size6)

        # --------------------------------------------BUTTONS-----------------------------------------------------------
        self.button_buttons.clicked.connect(self.open_buttons)
        self.button_back_buttons.clicked.connect(self.close_buttons)

        # BUTTONS UP
        self.button_w.clicked.connect(self.select_button_w)
        self.button_up.clicked.connect(self.select_button_up)

        # BUTTONS LEFT
        self.button_a.clicked.connect(self.select_button_a)
        self.button_left.clicked.connect(self.select_button_left)

        # BUTTONS RIGHT
        self.button_d.clicked.connect(self.select_button_d)
        self.button_right.clicked.connect(self.select_button_right)

    def change_selected_buttons(self):
        text = f"{self.selected_buttons.get('up')} {self.selected_buttons.get('left')} " \
               f"{self.selected_buttons.get('right')}"
        with open('buttons.txt', 'w') as f:
            f.write(text)

    def select_button_w(self):
        self.selected_buttons['up'] = 'w'
        self.change_selected_buttons()

    def select_button_up(self):
        self.selected_buttons['up'] = 'up'
        self.change_selected_buttons()

    def select_button_a(self):
        self.selected_buttons['left'] = 'a'
        self.change_selected_buttons()

    def select_button_left(self):
        self.selected_buttons['left'] = 'left'
        self.change_selected_buttons()

    def select_button_d(self):
        self.selected_buttons['right'] = 'd'
        self.change_selected_buttons()

    def select_button_right(self):
        self.selected_buttons['right'] = 'right'
        self.change_selected_buttons()

    def set_screen_size1(self):
        with open('screen_size.txt', 'w') as f:
            f.write('1920x1080')

    def set_screen_size2(self):
        with open('screen_size.txt', 'w') as f:
            f.write('1366x768')

    def set_screen_size3(self):
        with open('screen_size.txt', 'w') as f:
            f.write('1600x900')

    def set_screen_size4(self):
        with open('screen_size.txt', 'w') as f:
            f.write('1536x864')

    def set_screen_size5(self):
        with open('screen_size.txt', 'w') as f:
            f.write('1440x900')

    def set_screen_size6(self):
        with open('screen_size.txt', 'w') as f:
            f.write('1280x720')

    def clear_touched_coins(self):
        with open('level1_coins.txt', 'w') as f:
            f.write('0 104')
            self.level1_coins.setText('0 / 104')
        with open('level2_coins.txt', 'w') as f:
            f.write('0 110')
            self.level2_coins.setText('0 / 110')
        with open('level3_coins.txt', 'w') as f:
            f.write('0 119')
            self.level3_coins.setText('0 / 119')

    def pick_dude_monster(self):
        with open('character.txt', 'w') as f:
            f.write('dude')

    def pick_pink_monster(self):
        with open('character.txt', 'w') as f:
            f.write('pink')

    def pick_owlet_monster(self):
        with open('character.txt', 'w') as f:
            f.write('owlet')

    def open_level1(self):
        level = FirstLevel()
        level.game_loop()

        level_coins = set_level_coins('level1_coins')
        self.level1_coins.setText(level_coins[0] + ' / ' + level_coins[1])

        if level_coins[0] == level_coins[1]:
            self.widget_passed_level.show()

    def open_level2(self):
        level = SecondLevel()
        level.game_loop()

        level_coins = set_level_coins('level2_coins')
        self.level2_coins.setText(level_coins[0] + ' / ' + level_coins[1])

        if level_coins[0] == level_coins[1]:
            self.widget_passed_level.show()

    def open_level3(self):
        level = ThirdLevel()
        level.game_loop()

        level_coins = set_level_coins('level3_coins')
        self.level3_coins.setText(level_coins[0] + ' / ' + level_coins[1])

        if level_coins[0] == level_coins[1]:
            self.widget_passed_level.show()

    def open_settings(self):
        self.widget_settings.show()

    def close_settings(self):
        self.widget_settings.hide()

    def open_play(self):
        self.widget_play.show()

    def close_play(self):
        self.widget_play.hide()

    def close_passed_level(self):
        self.widget_passed_level.hide()

    def open_characters(self):
        self.widget_characters.show()

    def close_characters(self):
        self.widget_characters.hide()

    def open_screen_size(self):
        self.widget_screen_size.show()

    def close_screen_size(self):
        self.widget_screen_size.hide()

    def open_buttons(self):
        self.widget_buttons.show()

    def close_buttons(self):
        self.widget_buttons.hide()
