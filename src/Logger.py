from datetime import datetime

class Logger:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def __init__(self, name):
        self.name = name

    def log_info(self, message):
        print(f"{Logger.BOLD}[{self.name}: {datetime.now()}]{Logger.ENDC} {message}")

    def log_warning(self, message):
        print(f"{Logger.WARNING}{Logger.BOLD}[{self.name}: {datetime.now()}]{Logger.ENDC}{Logger.WARNING} {message}{Logger.ENDC}")

    def log_error(self, message):
        print(f"{Logger.FAIL}{Logger.BOLD}[{self.name}: {datetime.now()}]{Logger.ENDC}{Logger.FAIL} {message}{Logger.ENDC}")

    def log_success(self, message):
        print(f"{Logger.OKGREEN}{Logger.BOLD}[{self.name}: {datetime.now()}]{Logger.ENDC}{Logger.OKGREEN} {message}{Logger.ENDC}")