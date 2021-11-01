from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import ListProperty
from kivy.properties import StringProperty
from utils import get_settings
from kivy.lang import Builder

Builder.load_string('''
<CalculatorKeyPadButton>
    size_hint_y:
        (1/6) - (((1/200) / 6) * 5)
    font_size:
        self.width / 3
    markup:
        True
    color:
        root.text_color
    canvas.before:
        Color:
            rgba:
                root.down_color if self.state == 'down' else self.normal_color
        RoundedRectangle:
            pos:
                root.pos
            size:
                root.size
            radius:
                [10]

<CalculatorDisplay>
    size_hint_y:
        .3
    pos_hint:
        {'y': .7}
    margin:
        self.width / 180, self.height / 30
    canvas:
        Color:
            rgba:
                root.bg_color
        RoundedRectangle:
            pos:
                root.margin
            size:
                root.width - root.margin[0] * 2, root.height - root.margin[1] * 2
    Label:
        size_hint:
            None, None
        pos_hint:
            {'x': (root.margin[0] / root.width)*4, 'y': (root.margin[1] / root.height)*1.5}
        font_size:
            root.width / 10
        text_size:
            root.width - root.margin[0] * 6, root.height - root.margin[1] * 2
        size:
            self.texture_size
        valign:
            'bottom'
        halign:
            'center'
        markup:
            True
        text:
            root.text
        color:
            root.text_color

<CalculatorKeyPad>
    size_hint_y:
        .7
    padding:
        root.width / 180, 0, root.width / 180, root.height / 100
    spacing:
        root.width / 200, root.height / 200
''')

    
button_labels = [
    '(',   ')',   'del', 'C',
    'π',   'X[sup]2[/sup]',  '√',   '×',
    '7',   '8',   '9',   '÷',
    '4',   '5',   '6',   '+',
    '1',   '2',   '3',   '−',
    '.',   '0',   '='
]   

settings = get_settings()


class CalculatorKeyPadButton(ButtonBehavior, Label):
    
    normal_color = ListProperty(settings['color']['background']['button_normal'])
    down_color = ListProperty(settings['color']['background']['button_down'])
    text_color = ListProperty(settings['color']['text']['button'])

    def reload(self):
        settings = get_settings()
        self.normal_color = settings['color']['background']['button_normal']
        self.down_color = settings['color']['background']['button_down']
        self.text_color = settings['color']['text']['button']


class CalculatorDisplay(RelativeLayout):

    margin = ListProperty([0, 0])
    text = StringProperty()
    bg_color = ListProperty(settings['color']['background']['display'])
    text_color = ListProperty(settings['color']['text']['display'])

    def update(self, text):
        self.text = text
        
    def reload(self):
        settings = get_settings()
        bg_color = settings['color']['background']['display']
        text_color = settings['color']['text']['display']


class CalculatorKeyPad(StackLayout):
    
    def __init__(self, callback):
        super().__init__()
        for label in button_labels:
            self.add_widget(CalculatorKeyPadButton(
                text=label,
                size_hint_x=.5 if label == '=' else .25,
                on_release=callback))


__all__ = ['CalculatorDisplay', 'CalculatorKeyPad']