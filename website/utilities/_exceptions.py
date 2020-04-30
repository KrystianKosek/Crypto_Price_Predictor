class DatabaseError(Exception):
    """Base class for errors"""
    pass


class FilterError(Exception):
    def __init__(self, message, *args):
        super().__init__(message)