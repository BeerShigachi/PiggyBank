import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty


class MyGrid(Widget):
    """Style in kivy lang."""
    objective = ObjectProperty(None)
    budget = ObjectProperty(None)

    def btn(self):
        print(self.objective, self.objective.text, self.budget, self.budget.text)  # todo delete later.
        self.objective.text = ''
        self.budget.text = ''

# class MyGrid(GridLayout):
#     """Style in kivy python."""
#     def __init__(self, **kwargs):
#         super(MyGrid, self).__init__(**kwargs)
#         self.cols = 1
#         self.inside = GridLayout()
#         self.inside.cols = 2
#         self.inside.add_widget(Label(text="Name: "))
#         self.name = TextInput(multiline=False)
#         self.inside.add_widget(self.name)
#
#         self.inside.add_widget(Label(text="Deposit: "))
#         self.deposit = TextInput(multiline=False, input_filter='int')
#         self.inside.add_widget(self.deposit)
#
#         self.add_widget(self.inside)
#
#         self.submit = Button(text="Submit", font_size=40)
#         self.submit.bind(on_press=self.some_events)
#         self.add_widget(self.submit)
#
#     def some_events(self, instance):
#         print("YOUR NAME", self.name.text, "Deposit", self.deposit.text)
#         self.name.text = ""
#         self.deposit.text = ""


class MyApp(App):
    def build(self):
        return MyGrid()


if __name__ == "__main__":
    MyApp().run()
