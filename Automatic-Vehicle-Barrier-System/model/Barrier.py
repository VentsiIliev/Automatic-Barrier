class Barrier:
    def __init__(self, state=False):
        self.state = state

    def open(self):
        print("Barrier is open")
        self.state = True

    def close(self):
        print("Barrier is closed")
        self.state = False
