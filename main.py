from UILayer.MainUi import MainUI
from Fakewindow.FakeWindow import FakeWindow

def make_main_window(window):
    window.add_box(10, 10)
    window.add_header("Hangman")
    window.add_text("Enter your profile name" ,2, 2)

if __name__ == "__main__":
    main_window = FakeWindow()
    make_main_window(main_window)
    main_window.print_window()
    profile_name = input(":")
    main_ui = MainUI(profile_name)
    main_ui.get_input()