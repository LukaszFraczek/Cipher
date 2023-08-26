import pytest

from src.menu import MenuMsg, MenuItem, DialogItem, Menu, Dialog
from src.exceptions import MenuUniqueOptionError


class TestMenu:
    @pytest.fixture(
        params=[
            (
                "MenuName",
                [
                    MenuItem("1", "OPTION 1", lambda: 1),
                    MenuItem("2", "OPTION 2", lambda: 2),
                ],
            ),
            (
                "AnotherMenuName",
                [
                    MenuItem("-1", "This", lambda: 1),
                    MenuItem("0", "Is", lambda: 2),
                    MenuItem("-3", "A test", lambda: 3),
                    MenuItem("1", "For", lambda: 4),
                    MenuItem("A", "Multiple Choices", lambda: 5),
                ],
            ),
        ]
    )
    def valid_menu(self, request):
        yield request.param[0], request.param[1]

    @pytest.fixture(
        params=[
            (
                "MenuName",
                [
                    MenuItem("1", "OPTION 1", lambda: 1),
                    MenuItem("1", "OPTION 2", lambda: 2),
                ],
            ),
            (
                "AnotherMenuName",
                [
                    MenuItem("a", "OPTION 1", lambda: 1),
                    MenuItem("2", "OPTION 2", lambda: 2),
                    MenuItem("a", "OPTION 3", lambda: 3),
                ],
            ),
        ]
    )
    def not_valid_menu(self, request):
        yield request.param[0], request.param[1]

    def test_should_print_text_with_proper_formatting(self, capsys, valid_menu):
        name, items = valid_menu

        # Generate string from parameters for assertion
        expected_string = name
        for item in items:
            tmp = "\n" + item.option + ". " + item.description
            expected_string += tmp
            del tmp

        menu = Menu(name, *items)
        menu.display()
        text_capture = capsys.readouterr()

        assert text_capture.out.strip() == expected_string

    def test_should_raise_error_when_provided_with_the_same_inputs(
        self, not_valid_menu
    ):
        name, items = not_valid_menu

        with pytest.raises(MenuUniqueOptionError):
            Menu(name, *items)

    def test_when_option_is_selected_correct_function_should_be_called(
        self, mocker, valid_menu
    ):
        name, items = valid_menu

        menu = Menu(name, *items)

        # check every option in provided menu
        for menu_item in items:
            mock_input = menu_item.option
            mocker.patch("builtins.input", return_value=mock_input)
            assert menu.select() is menu_item.function()

    @pytest.mark.parametrize("mock_input", ["a", "b", ";", "900"])
    def test_should_display_invalid_selection_msg_when_input_is_not_valid(
        self, capsys, mocker, mock_input, valid_menu
    ):
        name, items = valid_menu

        menu = Menu(name, *items)

        mocker.patch("builtins.input", return_value=mock_input)

        menu.select()
        text_capture = capsys.readouterr()

        assert text_capture.out.strip() == MenuMsg.INVALID_SELECTION


class TestDialog:
    @pytest.fixture(
        params=[
            ("DialogName", [DialogItem("1", lambda: 1), DialogItem("2", lambda: 2)]),
            (
                "AnotherDialogName",
                [
                    DialogItem("A", lambda: 1),
                    DialogItem("B", lambda: 2),
                    DialogItem("C", lambda: 3),
                ],
            ),
        ]
    )
    def valid_dialog(self, request):
        yield request.param[0], request.param[1]

    @pytest.fixture(
        params=[
            ("DialogName", [DialogItem("2", lambda: 1), DialogItem("2", lambda: 2)]),
            (
                "AnotherDialogName",
                [
                    DialogItem("A", lambda: 1),
                    DialogItem("B", lambda: 2),
                    DialogItem("B", lambda: 3),
                ],
            ),
        ]
    )
    def not_valid_dialog(self, request):
        yield request.param[0], request.param[1]

    def test_should_print_text_with_proper_formatting(self, capsys, valid_dialog):
        title, items = valid_dialog

        # Generate string from parameters for assertion
        expected_string = title + " ["
        for dialog_item in items:
            expected_string += dialog_item.option
            if dialog_item != items[-1]:
                expected_string += "/"
            else:
                expected_string += "]"

        dialog = Dialog(title, *items)
        dialog.display()
        text_capture = capsys.readouterr()

        assert text_capture.out.strip() == expected_string

    def test_should_raise_error_when_provided_with_the_same_inputs(
        self, not_valid_dialog
    ):
        title, items = not_valid_dialog

        with pytest.raises(MenuUniqueOptionError):
            Menu(title, *items)

    def test_when_option_is_selected_correct_function_should_be_called(
        self, mocker, valid_dialog
    ):
        title, items = valid_dialog

        dialog = Dialog(title, *items)

        # check every option in provided menu
        for dialog_item in items:
            mock_input = dialog_item.option
            mocker.patch("builtins.input", return_value=mock_input)
            assert dialog.select() is dialog_item.function()

    @pytest.mark.parametrize("mock_input", ["x", "b", ";", "900"])
    def test_should_display_invalid_selection_msg_when_input_is_not_valid(
        self, capsys, mocker, mock_input, valid_dialog
    ):
        title, items = valid_dialog

        dialog = Dialog(title, *items)

        mocker.patch("builtins.input", return_value=mock_input)

        dialog.select()
        text_capture = capsys.readouterr()

        assert text_capture.out.strip() == MenuMsg.INVALID_SELECTION
