from textual import on
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import DataTable, Button, Label
from textual.containers import Vertical, Horizontal
from textual.message import Message


class QueryResultsWidget(Widget):
    BORDER_TITLE = "Data"
    page = reactive(1)


    def __init__(self, query_str ="", **kwargs):
        super().__init__(**kwargs)
        self.query_str = query_str
        

    def compose(self) -> ComposeResult:
        with Vertical(id="query-results-container"):
            # Table itself
            yield DataTable(id="data-table")

            # Pagination controls at bottom
            with Horizontal(id="pagination-controls"):
                yield Button("< Prev", id="prev-page")
                yield Label(f"Page 1", id="page-label")
                yield Button("Next >", id="next-page")
    
    def set_table(self, data, columns, page_size):
        data_table_widget = self.app.query_one("#data-table", DataTable)
        #clear and add columns
        data_table_widget.clear(columns=True)
        data_table_widget.add_columns(*columns)
        data_table_widget.add_rows(data)
        self.set_pagination_styles(len(data),page_size)
    
    def display_pagination(self):
        controls = self.app.query_one("#pagination-controls")
        controls.styles.display = "block"
    
    def undisplay_pagination(self):
        controls = self.app.query_one("#pagination-controls")
        controls.styles.display = "none"
    
    def set_pagination_styles(self, data_len, page_size):
        prev_button = self.query_one("#prev-page")
        next_button = self.query_one("#next-page")
        #this works since we always fetch an extra row in our DB
        prev_button.disabled = self.page == 1
        
        if data_len > page_size:
            next_button.disabled = False
        else:
            next_button.disabled = True
    
    
    def watch_page(self, old_page, new_page) -> None:
        self.query_one("#page-label").update(f"Page {new_page}")