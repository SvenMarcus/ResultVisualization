class Event:
    def __init__(self):
        self.__listeners = []

    def append(self, listener):
        self.__listeners.append(listener)

    def __call__(self, sender, args):
        for callback in self.__listeners:
            callback(sender, args)
