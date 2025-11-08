# Launcher: python run.py [cli|gui|web|mp]
import sys
from platforms.cli.main import run_cli

def main():
    if len(sys.argv) < 2 or sys.argv[1] == "cli":
        run_cli()
    else:
        print("Usage: python run.py cli")
        print("Other platforms coming soon...")

if __name__ == "__main__":
    main()