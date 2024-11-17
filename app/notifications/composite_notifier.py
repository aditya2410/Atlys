from app.notifications.notifier import Notifier

class CompositeNotifier(Notifier):
    def __init__(self, notifiers: list[Notifier]):
        self.notifiers = notifiers

    def notify(self, message: str):
        for notifier in self.notifiers:
            notifier.notify(message)
