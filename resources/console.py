"""
VOTE BRENT PETERSON FOR PRESIDENT
"""

import datetime
import os
import zipfile

INFO = 0
WARNING = 1
ERROR = 2
DEBUG = 3

class Console:
    def __init__(self):
        self.configured = False

    def configure(self, title: str = "latest.log", folder: str = "logs", limit: int = 10, layout: str = "[%(asctime)s] %(levelname)s: %(message)s", time_format: str = "%Y-%m-%d %H:%M:%S", compress: bool = False, zipfile: str = "logs.zip", debug: bool = False):
        if self.configured != False:
            return
            
        self.start_time = datetime.datetime.now() # Time when the console instance was created

        self.title = title
        self.folder = folder
        self.limit = limit
        self.layout = layout
        self.time_format = time_format
        self.compress = compress
        self.zip = zipfile
        self.debugging = debug

        PATH = os.path.join(self.folder, self.title) # Path of the log file
        
        self.configured = True
        self.writer = open(PATH, 'a') # Open the log file
        
        if os.path.getsize(PATH) > 0:
            self.writer.truncate(0) # Clear the file if it is not empty

        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

        if self.compress:
            # Get the logs that are older than the folder capacity
            LOGS: list[str] = []

            for file in os.listdir(self.folder):
                if file.endswith(self.title):
                    continue # Probably the current log file

                if not file.endswith(".log"):
                    continue

                LOGS.append(file) # Add the file to the list
            
            LOGS.sort(key=lambda x: os.path.getmtime(os.path.join(self.folder, x))) # Sort the logs by their creation date
            if len(LOGS) >= self.limit:
                self._compress(LOGS, self.zip)
            
        self.print_properties()

    def __del__(self):
        self.close()

    def printf(self, level: int, *output: str) -> None:
        """
        Print a message to the console and the log file
        """
        if not self.configured:
            raise Exception("Console instance is not configured.")

        if self.writer.closed or self.writer is None:
            return

        level = max(INFO, min(DEBUG, level)) # Make sure the level is between 0 and 3
        if level == DEBUG and not self.debugging:
            return
        
        for line in output:
            levelname = {INFO: 'INFO', WARNING: 'WARNING', ERROR: 'ERROR', DEBUG: 'DEBUG'}.get(level, 'INFO') # get the level name
            time = datetime.datetime.now().strftime(self.time_format) # get the current time

            
            line = str(line).encode('ascii', 'ignore').decode('ascii') # Remove non-ascii characters
            if line.startswith("\n"):
                line = line[1:]
            line = self.layout % {'asctime': time, 'levelname': levelname, 'message': line}

            self.writer.write(line + "\n")
            self.writer.flush()

            print(line)

    def info(self, *output: str) -> None:
        """
        Print an info message
        """
        self.printf(INFO, *output)
    
    def warning(self, *output: str) -> None:
        """
        Print a warning message
        """
        self.printf(WARNING, *output)
    
    def error(self, *output: str) -> None:
        """
        Print an error message
        """
        self.printf(ERROR, *output)

    def debug(self, *output: str) -> None:
        """
        Print a debug message
        """
        self.printf(DEBUG, *output)
    
    def print_properties(self) -> None:
        """
        Print the properties of the console instance
        """
        if not self.configured:
            raise Exception("Console instance is not configured.")

        attributes = dir(self)
        attributes.sort(key=lambda x: x.lower())
        
        for attribute in attributes:
            if attribute.startswith("__"):
                continue

            value = getattr(self, attribute)
            if callable(value):
                continue

            self.debug(f"{attribute}: {value}")

    def close(self) -> None:
        """
        Close the log file
        """
        if not self.configured:
            return

        PATH = os.path.join(self.folder, self.title) # Path of the log file

        self.info("adios o7 :)")
        
        os.rename(PATH, os.path.join(self.folder, "old.log"))
        self.writer.close()


    def _compress(self, logs: list[str], zip: str) -> None:
        """
        Compress files into a zip archive
        """
        if not self.configured:
            raise Exception("Console instance is not configured.")

        if not self.compress:
            return

        for file in logs:
            path = os.path.join(self.folder, file)
            
            if not os.path.exists(path):
                continue # Somehow the file doesn't exist

            try:
                with zipfile.ZipFile(os.path.join(self.folder, zip), 'a') as z:
                    z.write(path, file)
                
                self.debug(f"Compressed \"{file}\"")
                os.remove(os.path.join(self.folder, file))
            except:
                self.error(f"Failed to compress \"{file}\"")

if __name__ == '__main__':
    console = Console()
    console.configure(limit=15, compress=True, zipfile='logs.zip', debug=True)

    console.info("info")
    console.warning("warning")
    console.error("error")
    console.debug("debug")
    
    while True:
        user_input = input("$ ")

        if user_input in ['exit', 'quit', 'stop']:
            console.close()
            break

        console.info(user_input)
        continue
