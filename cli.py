import argparse
import sys
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from core import analyze_code, debug_code

console = Console()


def main():
    parser = argparse.ArgumentParser(
        description="AI Code Assistant CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py review myfile.py
  python cli.py debug myfile.py --log "NameError: name 'x' is not defined"
  python cli.py debug myfile.py --logfile error.log
"""
    )
    subparsers = parser.add_subparsers(dest="command")


    review_parser = subparsers.add_parser(
        "review", help="Review a file for bugs and improvements"
    )
    review_parser.add_argument("file", type=str, help="Path to the file to review")
    review_parser.add_argument(
        "--model", type=str, default="codellama",
        help="Ollama model to use (default: codellama)"
    )

    debug_parser = subparsers.add_parser(
        "debug",
        help="Correlate an error traceback with your source file and get a patch plan"
    )
    debug_parser.add_argument("file", type=str, help="Path to the source file with the bug")
    debug_parser.add_argument(
        "--model", type=str, default="codellama",
        help="Ollama model to use (default: codellama)"
    )
    log_group = debug_parser.add_mutually_exclusive_group(required=True)
    log_group.add_argument(
        "--log", type=str, metavar="TRACEBACK",
        help="Paste the error traceback/log directly as a string"
    )
    log_group.add_argument(
        "--logfile", type=str, metavar="FILE",
        help="Path to a log file containing the error traceback"
    )

    args = parser.parse_args()

    if args.command == "review":
        console.print(Panel(
            f"Reading and analyzing [bold cyan]{args.file}[/bold cyan]...",
            title="Code Assistant — Review Mode",
            border_style="green"
        ))
        source = _read_file(args.file)
        with console.status(
            "[bold yellow]Analyzing code with Ollama...[/bold yellow]", spinner="dots"
        ):
            response = analyze_code(source, model=args.model)
        console.print("\n")
        console.print(Panel(Markdown(response), title="Review Results", border_style="blue"))
        console.print("\n[bold green]✓ Review Complete![/bold green]")

    elif args.command == "debug":
        console.print(Panel(
            f"🐛 Correlating traceback with [bold cyan]{args.file}[/bold cyan]...",
            title="Code Assistant — Debug Session",
            border_style="red"
        ))
        source = _read_file(args.file)

        if args.logfile:
            traceback_log = _read_file(args.logfile)
        else:
            traceback_log = args.log

        with console.status(
            "[bold yellow]Running root-cause analysis with Ollama...[/bold yellow]",
            spinner="dots"
        ):
            response = debug_code(source, traceback_log, model=args.model)

        console.print("\n")
        console.print(Panel(
            Markdown(response),
            title="🔍 Debug Report — Root Cause & Patch Plan",
            border_style="red"
        ))
        console.print("\n[bold green]✓ Debug Session Complete![/bold green]")

    else:
        parser.print_help()


def _read_file(path: str) -> str:
    """Read a file and return its content, exiting cleanly on error."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        console.print(f"[bold red]Error:[/bold red] File '{path}' not found.")
        sys.exit(1)
    except OSError as e:
        console.print(f"[bold red]Error reading '{path}':[/bold red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
