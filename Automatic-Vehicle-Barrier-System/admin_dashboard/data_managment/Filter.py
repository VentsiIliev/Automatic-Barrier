class Filter:
    def __init__(self, **kwargs):
        """Initialize the filter with arbitrary keyword arguments."""
        self.filters = kwargs

    def to_dict(self):
        """Convert the filter attributes to a dictionary."""
        return {key: value for key, value in self.filters.items() if value is not None}

    def __getitem__(self, item):
        """Allow access to filters using item access (e.g., filter['key'])."""
        return self.filters.get(item, None)
