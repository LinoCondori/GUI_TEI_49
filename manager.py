# manager.py
from instrument import Instrument

class InstrumentManager:
    def __init__(self):
        self.instruments = {}

    def add_instrument(self, name, port, instrument_id):

        if name in self.instruments:
            return None

        if name not in self.instruments:
            self.instruments[name] = Instrument(name, port, instrument_id)
        return self.instruments[name]


    def get_instruments(self):
        return self.instruments.values()

    def remove_instrument(self, instrument):
        for name, inst in list(self.instruments.items()):
            if inst == instrument:
                del self.instruments[name]
                break
