import sys

from src.infrastructure.console_adapter import ConsoleAdapter

def main():
    try:
        app = ConsoleAdapter()
        app.run()
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    main()