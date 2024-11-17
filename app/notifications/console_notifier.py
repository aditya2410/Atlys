from app.notifications.notifier import Notifier

class ConsoleNotifier(Notifier):
    def notify(self, message: str):
        print(message)
