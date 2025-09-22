from textual.app import ComposeResult, on
from textual.screen import Screen
from textual.widgets import Button, Static
from textual.containers import Horizontal

class ErrorScreen(Screen):
    def __init__(self, error ,name = None, id = None, classes = None):
        super().__init__(name, id, classes)
        self.error = f"{error}"

    def compose(self) -> ComposeResult:
        yield Static("ERROR")
        yield Static(self.error)
        yield Button("⬅ Back", id="error_screen_back_button", variant="primary")

    @on(Button.Pressed, "#error_screen_back_button")
    def handle_rollback(self) -> None:
        self.app.pop_screen()
