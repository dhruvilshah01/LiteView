## Python Native Imports
import sys

## Library imports
from textual import on, work
from textual.app import App, ComposeResult
from textual.widgets import Header, Button, TextArea, DataTable
from textual.containers import Container

## Self Imports
from db import DbClient
from widgets.TableTree import TableTree
from widgets.QueryArea import QueryAreaWidget
from widgets.QueryResults import QueryResultsWidget
from screens.commit_screen import CommitScreen
from screens.explain_plan_screen import ExplainPlanScreen

class MainApp(App):
    CSS_PATH = ["grid_layout1.tcss", "./widgets/query_area_layout.tcss", "./widgets/query_results.tcss", "./screens/explain_plan_screen.tcss"]
    PAGE_SIZE = 100
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
            self.db.conn.commit()
        else:
            self.db.conn.rollback()
    

    @on(Button.Pressed, "#analyze-query")
    def handle_analyze_query(self) -> None:
        text_area_widget = self.query_one("#query-editor", TextArea)
        query_text = text_area_widget.text.strip()
        plan = self.db.explain_query(query_text)
        print(type(plan))
        if isinstance(plan, Exception):
            self.notify(f"SQL Error! \n {plan}\n", severity="error", timeout=5)
        else:
            self.push_screen(ExplainPlanScreen(plan = plan, query_str=query_text))

    @on(Button.Pressed, "#run-query")
    async def handle_run_query(self, event: Button.Pressed) -> None:
        text_area_widget = self.query_one("#query-editor", TextArea)
        query_results_widget = self.query_one("#data-view", QueryResultsWidget)
        query_text = text_area_widget.text.strip()
        data = self.db.run_query(query_text)
        ## Not a select statment
        if(data == None):
            self.push_commit_screen()
        ## Incorrect statement, some error
        elif isinstance(data,Exception):
            self.notify(f"SQL Error! \n {data}\n", severity="error", timeout=3)
        else:
            returned_data = data["data"]
            column_names = tuple(map(lambda desc: str(desc[0]),data["desc"]))
            if(not data["is_limit"]):
                query_results_widget.display_pagination()
                query_results_widget.page = 1
                query_results_widget.query_str = query_text
            else:
                query_results_widget.undisplay_pagination()
            query_results_widget.set_table(data = returned_data, columns = column_names, page_size = MainApp.PAGE_SIZE)

    @on(Button.Pressed, "#next-page")
    def handle_next_pagination(self) -> None: 
         query_results_widget = self.query_one("#data-view", QueryResultsWidget)
         query_results_widget.page += 1
         data = self.db.run_query(query_results_widget.query_str, page = query_results_widget.page, page_size = MainApp.PAGE_SIZE)
         returned_data = data['data']
         column_names = tuple(map(lambda desc: str(desc[0]),data["desc"]))
         query_results_widget.set_table(data = returned_data, columns = column_names, page_size = MainApp.PAGE_SIZE)
    
    @on(Button.Pressed, "#prev-page")
    def handle_prev_pagination(self) -> None:
         query_results_widget = self.query_one("#data-view", QueryResultsWidget)
         query_results_widget.page -= 1
         data = self.db.run_query(query_results_widget.query_str, page = query_results_widget.page, page_size = MainApp.PAGE_SIZE)
         returned_data = data['data']
         column_names = tuple(map(lambda desc: str(desc[0]),data["desc"]))
         query_results_widget.set_table(data = returned_data, columns = column_names, page_size = MainApp.PAGE_SIZE)
         
if __name__ == "__main__":
    num_args = len(sys.argv)
    if(num_args == 2):
        path = sys.argv[1]        
        app = MainApp(path)
        app.run()
        
    else:
        print("Please pass in path to your SQLite Database")
