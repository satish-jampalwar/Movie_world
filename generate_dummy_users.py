import json

users = [
    {"name": "John", "email": "john@movieworld.com", "password": "#@#@123"},
    {"name": "Jane", "email": "jane@movieworld.com", "password": "#@#@234"},
    {"name": "Bob", "email": "bob@movieworld.com", "password": "#@#@345"}
]

with open('users.json', 'w') as f:
    json.dump(users, f, indent=4)
    print('dummy users creted successfully')
