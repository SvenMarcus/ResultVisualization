class Event(list):
    def __call__(self, sender, args):
        for callback in self:
            callback(sender, args)
