import os
import argparse
from utils.config import load_cfg


def write_note(path: str, text: str):
    if not path.endswith(".txt"):
        raise ValueError("Only .txt files are supported")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(text.rstrip() + "\n")

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog='dri-util',
        description='Utilities for Daily Restaurant Insights'
    )
    parser.add_argument(
        '--env',
        choices=('dev', 'prod'),
        help='Override ENV for this run (default comes from .env)'
    )
    parser.add_argument(
        '--echo-cfg',
        action='store_true',
        help='Print resolved configuration and exit'
    )

    parser.add_argument(
        "--write-note", 
        metavar="PATH", 
        help="Append a line of text to a .txt file"
    )
    parser.add_argument(
        "--text", 
        metavar="TEXT", 
        help="Text to append (used with --write-note)"
    )
    
    return parser.parse_args()




def main():
    args = parse_args()

    # Allow CLI to temporarily override ENV
    if args.env:
        os.environ['ENV'] = args.env

    cfg = load_cfg()

    if args.echo_cfg:
        print(f"Resolved config:, {cfg}")
        return
    
    if args.write_note:
        if not args.text:
            raise ValueError(
                "Provide --text when using --write-note")
        write_note(args.write_note, args.text)
        print(f"[dri-util] Wrote 1 line to {args.write_note}")
        return

    print(f'[dri-util] ENV={os.getenv("ENV", "dev")} \
    | project={cfg["project"]} \
    | bucket={cfg["bucket"]}')

if __name__ == '__main__':
    main()

