from textual.app import ComposeResult, on
from textual.screen import Screen
from textual.widgets import Button, Static
from textual.containers import Horizontal

class CommitScreen(Screen):

      def compose(self) -> ComposeResult:
        yield Static("Would You Like to commit or rollback this query?")
        with Horizontal():
          yield Button("Rollback?", id="rollback")
          yield Button("Commit", id="commit")

      @on(Button.Pressed, "#rollback")
      def handle_rollback(self) -> None:
        self.dismiss(False)

      @on(Button.Pressed, "#commit")
      def handle_yes(self) -> None:
        self.dismiss(True)  