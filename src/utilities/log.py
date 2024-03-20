def display_code_via_panel(code: str):
    from rich.panel import Panel
    from rich.console import Console

    console = Console()
    console.print(Panel(code, title="Content"))
