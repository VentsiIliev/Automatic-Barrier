from shared.Database import Database


class SingletonDatabase:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SingletonDatabase, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.instance = Database("database/access_events_logs.csv")

    def getInstance(self):
        return self.instance
