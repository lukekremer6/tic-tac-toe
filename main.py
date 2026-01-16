from gui import Display

if __name__ == "__main__":
    try:
        from ctypes import windll
        # Improve resolution on Windows
        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        display = Display()
        display.mainloop()
