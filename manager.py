# manager.py
from instrument import Instrument
from communication.serial_comm import SerialCommunication
from communication.tcp_comm import TCPCommunication
from communication.simulated_comm import SimulatedCommunication

class InstrumentManager:
    def __init__(self):
        self.instruments = {}

    def add_instrument(self, name, port, instrument_id):


        if port.startswith("COM"):
            comm = SerialCommunication(port)

        elif "." in port:  # IP
            host, tcp_port = port.split(":")
            comm = TCPCommunication(host, tcp_port, instrument_id)

        else:
            print("Tipo de puerto desconocido")
            comm = SimulatedCommunication(name, port,)
            #return None

        instrument = Instrument(name, comm)
        #self.instruments.append(instrument)
        #return instrument
        self.instruments[name] = Instrument(name, port, instrument_id, comm)
        return self.instruments[name]

    def get_instruments(self):
        return self.instruments.values()

    def remove_instrument(self, instrument):
        for name, inst in list(self.instruments.items()):
            if inst == instrument:
                del self.instruments[name]
                break
