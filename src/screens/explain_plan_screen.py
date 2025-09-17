from textual.app import ComposeResult, on
from textual.screen import Screen
from textual.widgets import Button, Static, Markdown
from textual.containers import Vertical

class ExplainPlanScreen(Screen):
      def __init__(self, plan, name = None, id = None, classes = None):
         super().__init__(name, id, classes)
         self.plan = plan


      def compose(self):
        with Vertical():
            # Markdown widget for nicely formatted EXPLAIN
            yield Markdown(f"```sql\n{self.plan}\n```")
            
            # Done button to close the screen
            yield Button("Done", id="done-btn")

      def on_button_pressed(self, event):
        if event.button.id == "done-btn":
            self.app.pop_screen()