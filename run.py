import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py [cli|gui|web]")
        return
        
    platform = sys.argv[1].lower()
    
    if platform == "cli":
        from platforms.cli.main import run_cli
        run_cli()
    elif platform == "gui":
        from platforms.gui.main import run_gui
        run_gui()
    elif platform == "web":
        from platforms.web.main import run_web
        run_web()
    else:
        print("Choose: cli, gui, or web")

if __name__ == "__main__":
    main()