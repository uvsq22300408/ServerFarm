from eventType import EventType

class Event:

    def __init__(self, eventType, temps, fin=0.0):
        self.eventType = eventType
        self.temps = temps
        self.fin = fin