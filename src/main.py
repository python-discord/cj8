from src.frontend.core import CoreFrontend

if __name__ == "__main__":
    frontend = CoreFrontend()
    frontend.backend.new_level()
    frontend.start_loop()
