from textual.widgets import Tree
from textual.reactive import reactive


class TableTree(Tree):
    def __init__(self, label, data=None, **kwargs):
        super().__init__(label, data, **kwargs)
        self.root.expand()

    def set_tables(self, table_dict: list) -> None:
        for table_name in table_dict:
            self.root.add(table_name)
    
    def set_schema(self, node_id: int, schema: list) -> None:
        table_node = self.get_node_by_id(node_id)
        for column in schema:
            table_node.add_leaf(f"{column[0]} - {column[1]}")