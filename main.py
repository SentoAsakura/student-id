import kivy
from kivy.app import App
from kivy.uix.widget import Widget

from scan import test

class MainWidget(Widget):
    def openScanner(self):
        test.Reader.read(self)

class MainApp(App):
    pass


if __name__ == '__main__':
    MainApp().run()