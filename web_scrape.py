# import requests

# URL = "https://learningsuite.byu.edu/.4YTb/student/top/prioritizer"
# page = requests.get(URL)

# print(page.text)

# # https://learningsuite.byu.edu/.4YTb/student/top/prioritizer
# # https://learningsuite.byu.edu/.Sne2/student/top/prioritizer

from util import *
import json

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def to_json(self):
        return {
            'name': self.name,
            'age': self.age
        }
      
class PersonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Person):
            return obj.to_json()
        return super().default(obj)

# Creating instances of the Person class
dwa = []
for i in range(0,4, 1):
    dwa.append(Person("Alice", 25))

person = Person('Alice', 30)

json_str = json.dumps(dwa, cls=PersonEncoder, indent=2)

print(json_str)

