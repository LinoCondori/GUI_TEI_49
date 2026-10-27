
class BaseCommunication:
    type = "base"

    def connect(self):
        pass

    def read(self):
        pass

    def close(self):
        pass

    def recover_data(self, start, end, path):
        pass