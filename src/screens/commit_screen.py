from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Label
from textual.containers import Grid

class CommitScreen(Screen):

      def compose(self) -> ComposeResult:
        yield Button("Rollback?")
        yield Button("Commit")

      def on_button_pressed(self):
        self.app.pop_screen()
          
        