import json

def get_settings():
    with open('settings.json', 'r') as f:
        return json.load(f)


def set_settings(dict):
    with open('settings.json', 'w') as f:
        json.dump(dict, f)


def get_atlas(name):
    with open(f'img/{name}.atlas', 'r') as f:
        return json.load(f)


def set_atlas(name, dict):
    with open(f'img/{name}.atlas', 'w') as f:
        json.dump(dict, f)