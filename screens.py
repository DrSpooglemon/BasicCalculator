from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from kivy.clock import Clock
from widgets import *
from utils import get_settings
from kivy.lang import Builder

Builder.load_string('''
<CalculatorScreen>
    canvas.before:
        Rectangle:
            source:
                root.bg_image
            size:
                root.size
        Color:
            rgba:
                root.bg_color
        Rectangle:
            size:
                root.size

<CalculatorSettingsScreen>
''')

settings = get_settings()


class CalculatorScreen(Screen):

    bg_image = StringProperty(settings['image']['background'])
    bg_color = ListProperty(settings['color']['background']['screen'])

    def reload(self):
        settings = get_settings()
        self.bg_image = settings['image']['background']
        self.bg_color,disable_on_activity = settings['color']['background']['screen']
        for child in self.children:
            child.reload()


class CalculatorMainScreen(CalculatorScreen):

    def __init__(self, keypad_callback, goto_settings):
        super().__init__(name='Main')
        self.display = CalculatorDisplay()
        self.add_widget(self.display)
        self.key_pad = CalculatorKeyPad(keypad_callback)
        self.add_widget(self.key_pad)


class CalculatorSettingsScreen(CalculatorScreen):
    
    def __init__(self):
        super().__init__(name='Settings')
        self.add_widget(Label(
            color=(0, 0, 0, 1),
            font_size=30,
            halign='center',
            text='Nothing\nto\nsee\nhere'))


__all__ = ['CalculatorMainScreen', 'CalculatorSettingsScreen']