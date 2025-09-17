## Python Native Imports
import sys

## Library imports
from textual import on, work
from textual.app import App, ComposeResult
from textual.widgets import Static, Header, Button, TextArea, DataTable
from textual.containers import Container, Horizontal, VerticalScroll

## Self Imports
from db import DbClient
from widgets.TableTree import TableTree
from widgets.QueryArea import QueryAreaWidget
from widgets.QueryResults import QueryResultsWidget
from screens.commit_screen import CommitScreen
from screens.explain_plan_screen import ExplainPlanScreen

class MainApp(App):
    CSS_PATH = "grid_layout1.tcss"

    ## extend init to take in db_path
    def __init__(self, db_path, **kwargs):
        super().__init__(**kwargs)
        self.db = DbClient(db_path)

    def compose(self) -> ComposeResult:
        yield Header(name="LiteView")
        with Container(id="app-grid"):
            with Container(id="table-tree-container"):
                yield TableTree(label="Tables",id="table-view")
            yield QueryAreaWidget(id="query-area")
            yield QueryResultsWidget(id="data-view")
        yield Button("Click me to quit", id="quit-button")
           
    
    def on_mount(self) -> None:
        self.title = "LiteView"
        tables = self.db.get_tables()
        table_tree = self.query_one(TableTree)
        table_tree.set_tables(tables)

    @on(Button.Pressed, "#quit-button")
    def quit_button_pressed(self) -> None:
        self.exit()    

    @on(TableTree.mount)
    def get_tables(self):
        print("Getting Tables")
        tables = self.db.get_tables()
        table_tree = self.query_one(TableTree)
        table_tree.set_tables(tables)
    
    @on(TableTree.NodeExpanded)
    def table_tree_node_expanded(self, message: TableTree.NodeExpanded) -> None:
        #get necessary info from message and TableTree
        table_tree = self.query_one(TableTree)
        node_expanded = message.node
        ## check if we already added the schema - note this will probably have to be changed if we want to be able to change the schema in the viewer
        if(len(node_expanded.children) == 0):
            table_name = node_expanded.label
            table_schema = self.db.get_table_schema(table_name)
            #convert schema to list of tuples with column name and type
            schema = list(map(lambda ts: (ts[1], ts[2]),table_schema))
            ##set the schema
            table_tree.set_schema(node_expanded.id,schema)
    
    @work
    async def push_commit_screen(self):
        if await self.push_screen_wait(CommitScreen()):
            print("Commiting")
            self.db.conn.commit()
        else:
            self.db.conn.rollback()
    

    @on(Button.Pressed, "#analyze-query")
    def handle_analyze_query(self) -> None:
        text_area_widget = self.query_one("#query-editor", TextArea)
        query_text = text_area_widget.text.strip()
        data = self.db.explain_query(query_text)
        if(data == None):
            #Eventually push error screen here
            return
        else:
            self.push_screen(ExplainPlanScreen(data))
            print(data)

        

    @on(Button.Pressed, "#run-query")
    async def handle_run_query(self, event: Button.Pressed) -> None:
        # Get the query editor and the data
        text_area_widget = self.query_one("#query-editor", TextArea)
        data_table_widget = self.query_one("#data-view", QueryResultsWidget)
        # Get SQL String and run the query
        query_text = text_area_widget.text.strip()
        data = self.db.run_query(query_text)
        ## Not a select statment
        if(data == None):
            self.push_commit_screen()
            
        else:
            returned_data = data[0]
            column_names = tuple(map(lambda desc: str(desc[0]),data[1]))
            #clear data_table and add columns and rows
            data_table_widget.clear(columns=True)
            data_table_widget.add_columns(*column_names)
            data_table_widget.add_rows(returned_data)
        
    

def main():
    print("Hello from liteview!")



if __name__ == "__main__":
    num_args = len(sys.argv)
    if(num_args == 2):
        path = sys.argv[1]        
        app = MainApp(path)
        app.run()
        
    else:
        print("Please pass in path to your SQLite Database")
