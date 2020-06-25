import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget


class TouchScreen(FloatLayout):
    def on_touch_down(self, touch):
        print("touch down", touch)

    def on_touch_up(self, touch):
        print("touch up")

    def on_touch_move(self, touch):
        print("touch moving", touch)


class MyApp(App):
    def build(self):
        return TouchScreen()


if __name__ == "__main__":
    MyApp().run()
