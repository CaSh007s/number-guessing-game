import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py [cli|gui]")
        return
        
    platform = sys.argv[1].lower()
    
    if platform == "cli":
        from platforms.cli.main import run_cli
        run_cli()
    elif platform == "gui":
        from platforms.gui.main import run_gui
        run_gui()
    else:
        print("Choose: cli or gui")

if __name__ == "__main__":
    main()