from textual.app import ComposeResult, on
from textual.screen import Screen
from textual.widgets import Button, Static
from textual.containers import Horizontal

class CommitScreen(Screen):

      def compose(self) -> ComposeResult:
        yield Static("Would You Like to commit or rollback this query?", id="confirm-transaction-label")
        with Horizontal(id="btn-holders"):
          yield Button("Rollback?", id="rollback-btn")
          yield Button("Commit", id="commit-btn")

      @on(Button.Pressed, "#rollback-btn")
      def handle_rollback(self) -> None:
        self.dismiss(False)

      @on(Button.Pressed, "#commit-btn")
      def handle_yes(self) -> None:
        self.dismiss(True)  