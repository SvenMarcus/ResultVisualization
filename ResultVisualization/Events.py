from abc import ABC


class Event(ABC, list):
    """
    Abstract Event class. Allows adding and removing listener functions. Cannot be invoked.
    Provide this type to outside callers instead of InvokableEvent. Use InvokableEvent for classes internally.
    """

    def __init__(self):
        list.__init__(self)


class InvokableEvent(Event):
    """
    InvokableEvent can be invoked to notify listener functions.
    Should only be used by classes internally.
    """

    def __init__(self):
        Event.__init__(self)

    def __call__(self, sender, args=None):
        for callback in self:
            callback(sender, args)
