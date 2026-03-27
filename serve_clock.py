"""Serve the realtime clock app locally with the Python standard library."""

from __future__ import annotations

import argparse
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
APP_DIR = Path(__file__).resolve().parent / "clock_app"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Serve the realtime clock app on a local HTTP server."
    )
    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help="host interface to bind to",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help="TCP port for the local server",
    )
    return parser.parse_args(argv)


def resolve_app_dir() -> Path:
    return APP_DIR


def format_url(host: str, port: int) -> str:
    display_host = "127.0.0.1" if host == "0.0.0.0" else host
    return f"http://{display_host}:{port}"


def run_server(host: str, port: int, app_dir: Path) -> int:
    handler = partial(SimpleHTTPRequestHandler, directory=str(app_dir))

    try:
        server = ThreadingHTTPServer((host, port), handler)
    except OSError as exc:
        print(f"unable to start server: {exc}", file=sys.stderr)
        return 1

    url = format_url(host, server.server_port)
    print(f"Realtime clock available at {url}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()

    return 0


def main(argv: list[str]) -> int:
    args = parse_args(argv)

    if not 1 <= args.port <= 65535:
        print("--port must be between 1 and 65535", file=sys.stderr)
        return 1

    app_dir = resolve_app_dir()
    if not app_dir.is_dir():
        print("clock_app directory is missing", file=sys.stderr)
        return 1

    return run_server(args.host, args.port, app_dir)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
