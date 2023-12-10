from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.behaviors import CommonElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.properties import StringProperty
from kivymd.uix.button import MDIconButton
import os

Window.size = (300, 500)


class MenuScreen(Screen):
    pass


class DoToScreen(Screen):
    pass


class ToDoCard(CommonElevationBehavior, MDFloatLayout):
    title = StringProperty()
    description = StringProperty()


class ScrollParameters(CommonElevationBehavior, MDIconButton):
    pass


class NewFileScreen(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class MyApp(MDApp):
    def __init__(self):
        super().__init__()
        self.todo_cards_checkbox = {}
        self.todo_cards_bar = {}
        self.width = None
        self.username = None
        self.notes = None

    def build(self):
        self.theme_cls.primary_palette = "Orange"
        return

    def get_user(self):
        # Get input text
        username = self.root.ids.MenuScreen.ids.data.text
        # WE WANT A NAME
        if username == "":
            return
        # Get the working directory
        parent_dir = os.getcwd()
        path = os.path.join(parent_dir, username)
        # First time connection
        if not os.path.exists(path):
            os.mkdir(path)
            os.chdir(username)
        # Not first time connection
        else:
            os.chdir(username)
            self.charge_data()
        # Changing todolist's name
        self.root.ids.DoToScreen.ids.screenName.text = f"{username} todolist"
        # Changing window
        self.root.current = "DoTo"

    def charge_data(self):
        # Get all task file.txt
        file_list = os.listdir()
        for file in file_list:
            if file.endswith('.txt'):
                title = file.replace(".txt", "")
                with open(file, 'r') as f:
                    notes = f.readlines()
                # Get notes as one str and without the last line
                description = ''.join(notes[:-1])
                self.add_todo(title, description, 1)
                # Check/Uncheck charged data
                if notes[-1] == "0":
                    self.completed(self.todo_cards_checkbox[title], 0, self.todo_cards_bar[title], 1)
                else:
                    self.completed(self.todo_cards_checkbox[title], 1, self.todo_cards_bar[title], 1)
                f.close()

    def add_todo(self, title, description, index):
        # Get all task file.txt
        file_list = os.listdir()
        # index is used to know how I get access to add_todo function (0: click_button 1: charging_data)
        if index == 0:
            # WE ALSO WANT A NAME
            if title != "":
                if title + '.txt' not in file_list:
                    # Create a ToDoCard instance
                    todo_card = ToDoCard(id=title, title=title, description=description)
                    # Add Parameters
                    scroll_parameters = ScrollParameters()
                    # Add the instance to the dictionary with the title as the key
                    self.todo_cards_checkbox[title] = todo_card.ids.checkbox
                    self.todo_cards_bar[title] = todo_card.ids.bar
                    # Add the ToDoCard instance to the todo_list
                    self.root.ids.DoToScreen.ids.todo_list.add_widget(todo_card)
                    self.new_file(title, description)
        else:
            # Create a ToDoCard instance
            todo_card = ToDoCard(id=title, title=title, description=description)
            # Get ToDoCard Widgets address
            self.todo_cards_checkbox[title] = todo_card.ids.checkbox
            self.todo_cards_bar[title] = todo_card.ids.bar
            # Add the ToDoCard instance to the todo_list
            self.root.ids.DoToScreen.ids.todo_list.add_widget(todo_card)
            # Create a file.txt to keep information
            self.new_file(title, description)
        # Reset InputText View
        self.root.ids.NewFileScreen.ids.title.text = ""
        self.root.ids.NewFileScreen.ids.description.text = ""
    def hello(self):
        print('Hello')
    @staticmethod
    def new_file(title, description):
        title = title + '.txt'
        description = description + '\n0'
        file_list = os.listdir()
        if title not in file_list:
            with open(title, 'w') as f:
                f.write(description)
            f.close()

    def completed(self, checkbox, value, bar, index):
        # Checking which checkbox I'm click/charging
        for title, checkbox_instance in self.todo_cards_checkbox.items():
            if checkbox_instance == checkbox:
                files = title + '.txt'
                # I will modify my file.txt by adding/modifying True or False at the end
                with open(files, 'r') as file:
                    lines = file.readlines()
                # Checking the opening methode (add_todo/charging_data)
                if index == 0:
                    # Check/Uncheck ToDoCard
                    if value:
                        bar.md_bg_color = 0, 179 / 255, 0, 1
                        lines[-1] = "1"
                        with open(files, 'w') as file:
                            file.writelines(lines)
                    else:
                        bar.md_bg_color = 1, 170 / 255, 23 / 255, 1
                        lines[-1] = "0"
                        with open(files, 'w') as file:
                            file.writelines(lines)
                # Charged data
                else:
                    # Check the value at the end of the file
                    if lines[-1] == "0":
                        print('H', checkbox.on_active)
                        bar.md_bg_color = 1, 170 / 255, 23 / 255, 1
                    else:
                        print(checkbox.on_active)
                        bar.md_bg_color = 0, 179 / 255, 0, 1


if __name__ == "__main__":
    MyApp().run()
