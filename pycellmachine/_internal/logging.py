import sys, os
import time

class log_file:
    def __init__(self, file_name, file_path=os.path.dirname(os.path.abspath(__file__)), level="INFO", format="%Y-%m-%d %H:%M:%S"):
        self.file_path = os.path.join(file_path, file_name)
        self.log_file = open(self.file_path, "w")
        self.level = level
        self.format = format
    
    def now(self, format=None):
        return time.strftime(self.format if format == None else format, time.localtime())

    def clear(self):
        self.log_file.truncate(0)

    def write(self, message, level=None):
        self.log_file.write(f"[{self.level if level == None else level}] " + f"{self.now()} " + message + f"\n")