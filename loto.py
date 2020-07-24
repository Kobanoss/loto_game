import time
import datetime

import json
import random

from PyQt5 import QtCore
from PyQt5 import QtWidgets

import json_lib
from model import Ui_Form


class Game(QtWidgets.QWidget, Ui_Form):
    """

    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.startTime = time.time()
        self.minute = 0
        self.second = 0
        self.name = ''
        self.all_time = 0

        self.pushButton.pressed.connect(self.start_game)

        self.buttonBox.rejected.connect(self.check_answer_false)
        self.buttonBox.accepted.connect(self.check_answer_true)

        self.buttonBox.setEnabled(False)
        self.pushButton.setEnabled(True)

        self.stats_print()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timer_update)

    '''

    '''

    def name_check(self):
        if not self.lineEdit.text():

            self.log('No input name!')
            return False

        else:
            self.name = self.lineEdit.text()
            return True

    '''

    '''

    def timer_update(self):
        fix = time.time()
        self.minute = int((fix - self.startTime) // 60)
        self.second = int((fix - self.startTime) - self.minute * 60)
        self.QLCDTimer.display(self.timer_str())

    def timer_str(self):
        return ('00' + str(self.minute))[(len(str(self.minute))):] + ':' + \
               ('00' + str(self.second))[(len(str(self.second))):]

    '''
    
    '''

    def check_answer_true(self):
        self.log('take', self.QLCDBarrel.value(), "Player")
        self.bot_game()
        if int(self.QLCDBarrel.value()) in self.player_card_list:

            self.cards_remove('player', int(self.QLCDBarrel.value()))
            self.barrel_out()
            self.cards_print('Player', self.player)
            self.cards_print('Bot', self.bot)
            if self.player_card_list.count('    ') == 27:
                self.end_game(True)
        else:
            self.end_game(False)

    def check_answer_false(self):
        self.log('throw out', self.QLCDBarrel.value(), "Player")
        self.bot_game()
        if int(self.QLCDBarrel.value()) not in self.player_card_list:

            self.barrel_out()
            self.cards_print('Player', self.player)
            self.cards_print('Bot', self.bot)

        else:
            self.end_game(False)

    '''

    '''

    def barrel_new_list(self, size):
        self.log('Barrel pull generating...')
        self.barrel = [i for i in range(size + 1)]
        random.shuffle(self.barrel)
        self.log('Barrel pull generated')

    def barrel_out(self):
        if len(self.barrel) > 0:
            random.shuffle(self.barrel)
            out_barrel = self.barrel.pop(0)
            self.QLCDBarrel.display(out_barrel)
            return ''
        else:
            self.end_game(True)
            return ''

    '''

    '''

    def cards_fill(self):
        self.log('Cards generating...')
        random.shuffle(self.barrel)
        self.player_card_list = [self.barrel[i] for i in range(15)]
        self.bot_card_list = [self.barrel[-i] for i in range(15)]
        random.shuffle(self.barrel)
        self.log('Cards generated\n')
        return ''

    def cards_model(self, card_list):
        self.line1 = [el for el in sorted(card_list[0:5])]
        self.line2 = [el for el in sorted(card_list[5:10])]
        self.line3 = [el for el in sorted(card_list[10:15])]
        run = 5
        for _ in range(4):
            self.line1.insert(random.randint(1, run), '    ')
            self.line2.insert(random.randint(1, run), '    ')
            self.line3.insert(random.randint(1, run), '    ')
            run += 1
        self.card = [self.line1, self.line2, self.line3]
        return self.card

    def cards_remove(self, user_type: str, value):

        if user_type.lower() == "player":

            for line in self.player:
                if value in line:
                    i = line.index(value)
                    line.remove(value)
                    line.insert(i, '    ')

        elif user_type.lower() == "bot":
            for line in self.bot:
                if value in line:
                    i = line.index(value)
                    line.remove(value)
                    line.insert(i, '    ')
        return ''

    def cards_print(self, user_type: str, card):

        all_card = '-' * ((len(self.card[1])) * 6 - 4) + '\n'
        for line in card:
            all_card += '| '
            for el in line:
                if type(el) == int:
                    el = ('0' + str(el))[len(str(el)) - 1:len(str(el)) + 1:]
                all_card += (str(el) + ' | ')
            all_card += '\n'
            all_card += '-' * ((len(card[1])) * 6 - 4) + '\n'

        if user_type.lower() == "player":
            self.textBrowser_player.clear()
            self.textBrowser_player.append(str(all_card))

        elif user_type.lower() == "bot":
            self.textBrowser_bot.clear()
            self.textBrowser_bot.append(str(all_card))

        return ''

    '''

    '''

    def log(self, action, barrel_nu=0, user_type=''):
        if user_type.lower() == "player":
            self.textBrowser_log.append(f'You {str(action)} barrel {str(barrel_nu)} ')
        elif user_type.lower() == "bot":
            self.textBrowser_log.append(f'Bot {str(action)} barrel {str(barrel_nu)}\n')
        else:
            self.textBrowser_log.append(str(action))
        return ''

    '''
    
    '''

    def stats_print(self):
        try:
            f = open("stat.json")
            f.close()
        except FileNotFoundError:
            self.textBrowser.append('Записей о предыдущих играх нет')
            return ''
        self.textBrowser.clear()
        stat_list = json_lib.print_json("stat.json")
        self.textBrowser.append(str(stat_list))
        self.textBrowser.repaint()
        return ''

    def stats_new(self, total_time, name):
        json_lib.add_to_json("stat.json", total_time, name)
        json_lib.sort_json("stat.json")
        return ''

    '''
    
    '''

    def bot_game(self):
        if int(self.QLCDBarrel.value()) in self.bot_card_list:
            self.cards_remove('Bot', int(self.QLCDBarrel.value()))
            self.log('take', self.QLCDBarrel.value(), 'Bot')
        else:
            self.log('throw out', self.QLCDBarrel.value(), 'Bot')
            if self.bot_card_list.count('    ') == 27:
                self.end_game(False)

    '''
    
    '''

    def start_game(self):
        if self.name_check():
            self.timer.start(400)
            self.startTime = time.time()

            self.textBrowser_bot.clear()
            self.textBrowser_player.clear()
            self.textBrowser_log.clear()

            self.log(f'Game started! as <{self.name}>')

            self.pushButton.setEnabled(False)
            self.lineEdit.setReadOnly(True)
            self.buttonBox.setEnabled(True)

            self.barrel_new_list(90)
            self.barrel_out()

            self.cards_fill()

            self.bot = self.cards_model(self.bot_card_list)
            self.player = self.cards_model(self.player_card_list)

            self.cards_print('Player', self.player)
            self.cards_print('Bot', self.bot)

    '''
    
    '''

    def end_game(self, result: bool):
        self.timer.stop()

        total_time = self.timer_str()

        self.pushButton.setEnabled(True)
        self.buttonBox.setEnabled(False)
        self.lineEdit.setReadOnly(False)

        if result:
            self.log("You win!")
            self.stats_new(total_time, str(self.name))
            self.stats_print()
            self.log('Your result was recorded')

        else:
            self.log("You lose!")


app = QtWidgets.QApplication([])
game = Game()
game.show()
exit(app.exec_())
