
class Menu:
    ALLOWED_INPUT = ('1', '2', '3', '4', '9')

    @staticmethod
    def show_main_menu() -> None:
        print('1. Read from file')
        print('2. Write to file')
        print('3. Encode')
        print('4. Decode')
        print('9. Exit')

    @staticmethod
    def user_input() -> str:
        while True:
            user_input = input()
            if user_input in Menu.ALLOWED_INPUT:
                return user_input
