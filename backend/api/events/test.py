from api.events.event import Cancelable
from event_manager import Event, EventManager


class MyEvent(Event):
    def __init__(self, data: str):
        self.data = data


class CancelableEvent(Cancelable, Event):
     pass


# def handle_my_event(event: MyEvent):
#     print(f"Received MyEvent: {event.data}")


@EventManager.subscribe()
def handle_my_event(event: MyEvent):
    print(f"Received MyEvent: {event.data}")


event = MyEvent("Hello, world!")
EventManager.post(event)  # 发布 MyEvent
