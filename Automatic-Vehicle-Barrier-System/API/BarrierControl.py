class BarrierControl:
    def __init__(self, barrier):
        self.barrier = barrier

    def open(self):
        self.barrier.open()

    def close(self):
        self.barrier.close()

    def deny_access(self):
        print("Access denied")
        if self.barrier.state:
            self.barrier.close()

    def get_status(self):
        return self.barrier.state
