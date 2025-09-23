from textual import on
from textual.app import ComposeResult
from textual.widgets import TextArea, Button
from textual.widget import Widget
from textual.containers import Vertical

class QueryAreaWidget(Widget):
    BORDER_TITLE = "Query"

    def compose(self) -> ComposeResult:
        yield TextArea(placeholder="Write your SQL here...", id="query-editor", language="sql")
        with Vertical(id="query-area-buttons"):
            yield Button("Run Query", id="run-query")
            yield Button("Analyze Query", id="analyze-query")
        