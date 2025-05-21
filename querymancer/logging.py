from rich.console import Console
from rich.panel import Panel
from rich.style import Style

blue_border_style = Style(color="#0EA5E9")
green_border_style = Style(color="#10B981")

console = Console()


def log(content: str):
    console.log(content)


def log_panel(
    title: str,
    content: str,
    border_style: Style = blue_border_style,
):
    console.log(
        Panel(
            content,
            title=title,
            border_style=border_style,
        )
    )
