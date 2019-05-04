class Result:
    def __init__(self, found_indexes, collisions=0, title=''):
        self.title = title
        self.found_indexes = found_indexes
        self.collisions = collisions
