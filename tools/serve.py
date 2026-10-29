"""Serve an explicit local web root with the standard static HTTP handler."""
import argparse, functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

def main():
    """Run until interrupted; test fixtures own and stop their server."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default='dist')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=4173)
    args = parser.parse_args()
    root = Path(args.root).resolve(strict=True)
    handler = functools.partial(SimpleHTTPRequestHandler, directory=str(root))
    with ThreadingHTTPServer((args.host, args.port), handler) as server:
        print(f'Serving {root.name} on port {server.server_port}', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass

if __name__ == '__main__':
    main()
