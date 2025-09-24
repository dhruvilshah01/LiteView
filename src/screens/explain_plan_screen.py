from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Button, Markdown, Static, Header, Footer
from textual.containers import Vertical, VerticalScroll, Horizontal


class ExplainPlanScreen(Screen):
    def __init__(self, plan, query_str, **kwargs):
        super().__init__(**kwargs)
        self.plan = plan
        self.query_str = query_str
        print(plan)

    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical(id="explain-layout"):
            # Scrollable content
            with VerticalScroll(id="content-box"):
                yield Static("Query:", id="query-box")
                yield Static(self.query_str, id="query-str")
                yield Static("\nQuery Plan:", id="query-plan-label")
                yield Static(self.convert_plan(self.plan), id="plan-box")

            # Sticky buttons at bottom
            with Horizontal(id="button-row"):
                yield Button("⬅ Back", id="back-btn", variant="primary")
                yield Button("Export Plan", id="export-btn", variant="default")

            yield Footer()

      

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "back-btn":
            self.app.pop_screen()
        elif event.button.id == "export-btn":
            with open("explain_plan.txt", "w") as f:
                f.write(self.convert_plan(self.plan))
            self.notify("Exported explain plan to explain_plan.txt")

    def convert_plan(self, plan: list) -> str:
        plans_arr = [f"{i + 1}. {plan[i][3]}" for i in range(len(plan))]
        print("\n".join(plans_arr))
        return "\n".join(plans_arr)