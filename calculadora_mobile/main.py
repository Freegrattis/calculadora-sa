from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.animation import Animation
import kivy.utils
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
            ['C', '( )', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['+/-', '0', ',', '='],
            ['Histórico','DEL','ANS']
        ]

        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                if label:
                    button = Button(text=label, font_size=24, on_press=self.on_button_press)
                    button.background_normal = ''
                    
                    if label in ['/', '*', '-', '+','( )','%','/','+/-',',']:
                        button.background_color = kivy.utils.get_color_from_hex("#2B3133")
                        button.color = kivy.utils.get_color_from_hex("#41B6DD")
                    elif label in ['C']:
                        button.background_color = kivy.utils.get_color_from_hex("#2B3133")
                        button.color = kivy.utils.get_color_from_hex("#b32110")
                    elif label in ['=']:
                        button.background_color = kivy.utils.get_color_from_hex("#557B88")
                    elif label in ['Histórico','DEL', 'ANS']:
                        button.background_color = kivy.utils.get_color_from_hex("#262E33")
                    else:
                        button.background_color = kivy.utils.get_color_from_hex("#2B3033") 
                    
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
            elif button_text == '=':
                result = eval(self.input_box.text)
                self.add_to_history(self.input_box.text, result) 
                self.input_box.text = str(result)
                self.last_result = result
            elif button_text == 'ANS':
                self.input_box.text += str(self.last_result)
            elif button_text == '( )':
                cursor_index = self.input_box.cursor_index()
                # Se já houver um número ou expressão selecionada, coloca entre parênteses
                if current_text and current_text[cursor_index:].strip():
                    new_text = f"{current_text[:cursor_index]}({current_text[cursor_index:]})"
                    self.input_box.text = new_text
                    self.input_box.cursor = (cursor_index + 1, 0)
                else:
                    # Caso contrário, adiciona parênteses vazios na posição do cursor
                    new_text = f"{current_text[:cursor_index]}(){current_text[cursor_index:]}"
                    self.input_box.text = new_text
                    self.input_box.cursor = (cursor_index + 1, 0)
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

