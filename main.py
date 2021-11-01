from kivy.config import Config
Config.read('config.ini')
from kivy.core.window import Window
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager
from screens import *
from math import sqrt

operators = {
    '×': '*', '÷': '/', '+': '+', '−': '-', 
    '[sup]2[/sup]': '** 2'}

symbols = {'π': '3.14159265358'}

def replace_operators(e):
    for key, val in operators.items():
        e = e.replace(key, val)
    return e


def replace_symbols(e):
    for key, val in symbols.items():
        elems = e.split(key)
        for i, elem in enumerate(elems):
            if i > 0:
                try:
                    if elems[i-1][-1] not in ('*', '/', '+', '-', '√'):
                        elems[i-1] += '*'
                except:
                    pass
                finally:
                    elems[i-1] += val
                try:
                    if elems[i+1][0] not in ('*', '/', '+', '-'):
                        elems[i-1] += '*'
                except:
                    pass
    return ''.join(elems)


def replace_square_roots(e):
    elems = e.split('√')
    for i, elem in enumerate(elems[1:]):
        if elem[0] == '(':
            elems[i+1] = ''.join(elem.partition(')')[0:2]) + '** .5'
        else:
            e = ''
            elem = iter(elem)
            for char in elem:
                if not char.isdigit() and char != '.':
                    break
                else:
                    e += char
                    char = ''
            e += '**.5' + char + ''.join(elem)
            elems[i+1] = e
    return ''.join(elems)


def parse(e):
    e = replace_operators(e)
    e = replace_symbols(e)
    return replace_square_roots(e)
    

class CalculatorApp(App):

    offset_is_set = False
    equation = StringProperty()
    error = StringProperty()
    waiting = False

    def build(self):
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(
            CalculatorMainScreen(
                self.key_pressed,
                self.goto_settings_screen))
        self.screen_manager.add_widget(
            CalculatorSettingsScreen())
        return self.screen_manager

    @property
    def main_screen(self):
        if self.screen_manager.current == 'Main':
            return self.screen_manager.current_screen

    def goto_settings_screen(self):
        self.screen_manager.current = 'Settings'
        Clock.schedule_once(self.return_to_main, .5)

    def return_to_main(self, _):
        self.screen_manager.current = 'Main'

    def key_pressed(self, key):
        if self.waiting:
            return
        val = key.text
        if val == 'del':
            self.delete()
        elif val == 'C':
            self.cancel()
        elif val == '=':
            self.solve()
        else:
            self.append(val)
        self.wait()

    def wait(self):
        self.waiting = True
        Clock.schedule_once(self.stop_waiting, .1)

    def stop_waiting(self, _):
        self.waiting = False

    def append(self, val):
        if val == 'X[sup]2[/sup]':
            val = val[1:]
        self.equation += val

    def delete(self):
        if self.equation[-1] == ']':
            self.equation = self.equation[:-12]
        else:
            self.equation = self.equation[:-1]

    def cancel(self):
        self.equation = ''
        self.error = ''

    def solve(self):
        equation = parse(self.equation)
        try:
            answer = round(eval(equation), 12)
            answer = answer if answer % 1 else int(answer)
            answer = str(answer)
            error = None
        except ZeroDivisionError:
            answer = ''
            error = 'Division by zero'
        except Exception as e:
            answer = ''
            error = 'Malformed Expression'
        self.update(answer, error)

    def update(self, answer, error):
        self.error = ''
        self.equation = answer
        if error:
            self.error = error

    def on_equation(self, _, text):
        self.main_screen.display.update(text)

    def on_error(self, _, text):
        self.main_screen.display.update(text)


if __name__ == '__main__':
    CalculatorApp().run()