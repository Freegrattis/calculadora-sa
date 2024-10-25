from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.animation import Animation
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
import math


class CalculatorScreen(Screen):
    memory = 0
    last_result = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.calc_layout = BoxLayout(orientation='vertical')

        self.input_box = TextInput(font_size=32, halign='right', multiline=False,
                                   background_color=(0, 0, 0, 1), foreground_color=(1, 1, 1, 1))
        self.calc_layout.add_widget(self.input_box)

        buttons = [
            ['7', '8', '9', '/', 'M+'],
            ['4', '5', '6', '*', 'M-'],
            ['1', '2', '3', '-', 'MR'],
            ['.', '0', 'C', '+', 'ANS'],
            ['(', ')', '^', '√', 'Dec'],
            ['%', 'DEL', '=', 'Histórico']
        ]

        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                if label:
                    button = Button(text=label, font_size=24, on_press=self.on_button_press)
                    button.background_normal = ''
                    
                    if label in ['/', '*', '-', '+', 'ANS', 'M+', 'M-', 'MR', 'Dec', '√']:
                        button.background_color = [0.2, 0.6, 0.8, 1]
                    elif label in ['=']:
                        button.background_color = (1, 0.5, 0, 1)
                    elif label in ['Histórico']:
                        button.background_color = (0.1, 0.3, 0.9, 1)
                    else:
                        button.background_color = [0.4, 0.4, 0.4, 1]  
                    
                    button.bind(on_press=self.animate_button)  
                    h_layout.add_widget(button)
            self.calc_layout.add_widget(h_layout)

        self.add_widget(self.calc_layout)

    def on_button_press(self, instance):
        current_text = self.input_box.text
        button_text = instance.text

        try:
            if button_text == 'C':
                self.input_box.text = ''
            elif button_text == 'DEL':
                self.input_box.text = current_text[:-1]
            elif button_text == '√':
                self.input_box.text = str(math.sqrt(float(current_text)))
            elif button_text == '^':
                self.input_box.text += '**'
            elif button_text == '=':
                result = eval(self.input_box.text)
                self.add_to_history(self.input_box.text, result) 
                self.input_box.text = str(result)
                self.last_result = result
            elif button_text == 'ANS':
                self.input_box.text += str(self.last_result)
            elif button_text == 'M+':
                self.memory += float(self.input_box.text)
            elif button_text == 'M-':
                self.memory -= float(self.input_box.text)
            elif button_text == 'MR':
                self.input_box.text = str(self.memory)
            elif button_text == 'Dec':
                self.input_box.text = str(round(float(self.input_box.text), 2)) 
            elif button_text == 'Histórico':
                self.manager.current = 'history' 
            else:
                self.input_box.text += button_text
        except ZeroDivisionError:
            self.input_box.text = 'Erro: Divisão por zero'
        except Exception as e:
            self.input_box.text = f'Erro: {str(e)}'

    def add_to_history(self, expression, result):
        """Adiciona o cálculo ao histórico"""
        self.manager.get_screen('history').add_to_history(f'{expression} = {result}')

    def animate_button(self, instance):
        anim = Animation(size=(instance.width + 10, instance.height + 10), duration=0.1) + Animation(
            size=(instance.width, instance.height), duration=0.1)
        anim.start(instance)


class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.history_layout = GridLayout(cols=1, size_hint_y=None)
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))

        self.scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=True, do_scroll_y=True)
        self.scroll_view.add_widget(self.history_layout)
        self.add_widget(self.scroll_view)

        self.back_button = Button(text="Voltar", size_hint=(1, 0.1), on_press=self.go_back,
                                  font_size=24, background_color=(0.2, 0.6, 0.8, 1)) 
        self.add_widget(self.back_button)

    def add_to_history(self, text):
        """Adiciona o cálculo ao histórico"""
        history_item = Label(
            text=text,
            font_size=24,  
            color=(1, 1, 1, 1),  
            size_hint_y=None,
            height=50,
            text_size=(self.width, None),  
            halign='left',
            valign='middle'
        )
        history_item.bind(size=self.adjust_text_size)  
        self.history_layout.add_widget(history_item)
        self.scroll_view.scroll_to(history_item)  

    def go_back(self, instance):
        """Retorna para a tela da calculadora"""
        self.manager.current = 'calculator'

    def adjust_text_size(self, instance, size):
        """Ajusta a fonte dependendo do tamanho do texto"""
        instance.text_size = (instance.width, None)


class CalculadoraApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(CalculatorScreen(name='calculator'))
        sm.add_widget(HistoryScreen(name='history'))
        return sm


if __name__ == '__main__':
    CalculadoraApp().run()

