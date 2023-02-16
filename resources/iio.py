import csv
import json
import os
import pickle
import subprocess
from dataclasses import dataclass, field

Any = object()

@dataclass
class BaseData:
    file: str
    path: str = "data"
    value: Any = field(init=False, default=None)

    def __post_init__(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        self.path = os.path.join(self.path, self.file)
    
    def read(self) -> Any:
        return self.value
    
    def write(self, value: Any):
        with open(self.path, 'w') as f:
            f.write(str(value))

    def delete(self):
        os.remove(self.path)

    def extension(self) -> str:
        return self.file.split('.')[-1]


class JSONData(BaseData):
    value: dict|list|None

    def load(self):
        try:
            with open(self.path, 'r') as f:
                self.value = json.load(f)
        except FileNotFoundError:
            self.save()
    
    def write(self, value: dict|list):
        with open(self.path, 'w') as f:
            json.dump(value, f, indent=4)
        
    def save(self):
        self.write(self.value)


class PickleData(BaseData):

    def load(self):
        try:
            with open(self.path, 'rb') as f:
                self.value = pickle.load(f)
        except FileNotFoundError:
            self.write(self.value)

    def write(self, value: object):
        with open(self.path, 'wb') as f:
            pickle.dump(value, f)

    def save(self):
        self.write(value=self.value)

if __name__ == '__main__':
    person = JSONData(file='person.json')
    person.load() # Load the data
    person.value = {'name': 'John', 'age': 30} # Change the value
    person.save() # Save the data
    print(person.read()) # Read the data

    # Pause the program natively
    subprocess.call('pause', shell=True)