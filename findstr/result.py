def __init__(self, found_indexes, collisions=0, time=0.0, title=''):
    self.title = title
    self.found_indexes = found_indexes
    self.collisions = collisions
    self.time = time


def log(self):
    print(f'       method {self.title}')
    print(f'     found on {self.found_indexes}')
    print(f'indexes count {len(self.found_indexes)}')
    print(f'   collisions {self.collisions}')
    print(f'         time {self.time}')
    print()
