import os


def init_base_dir_path():
    base_dir = os.path.dirname(__file__)

    while 'main.py' not in os.listdir(base_dir):
        base_dir = os.path.abspath(os.path.join(base_dir, '../'))

    return base_dir


