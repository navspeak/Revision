"""
EventBus 101 — a minimal synchronous publish/subscribe broker.

Run this file directly:  python eventbus_demo.py

The pattern in one sentence: publishers emit a named event + a payload,
without knowing who (if anyone) is listening. Subscribers register interest
in a named event, without knowing who (if anyone) will ever publish it.
The bus in the middle is the only thing that knows both sides.
"""

from typing import Callable, Dict, List


class EventBus:
    """
    Tiny in-memory pub/sub broker.

    Two guarantees this implementation makes (both worth knowing, because a
    "real" event bus often relaxes them on purpose):

    1. SYNCHRONOUS: publish() calls each handler directly, inline, and waits
       for it to return before calling the next one. There's no thread pool,
       no queue, no async dispatch.

    2. IN ORDER: handlers for a given event run in the exact order they were
       subscribed, because they're stored in a plain list.

    Trade-off: simple to reason about and debug (you can literally step
    through publish() into each handler) — but one slow handler blocks every
    other subscriber AND the publisher itself, and one handler raising an
    exception stops every handler after it from running.
    """

    def __init__(self) -> None:
        # event_name -> list of handlers, in subscription order
        self._subscribers: Dict[str, List[Callable[[dict], None]]] = {}

    def subscribe(self, event_name: str, handler: Callable[[dict], None]) -> None:
        """Register `handler` to be called whenever `event_name` is published."""
        # setdefault: "give me the list at this key, creating an empty one
        # the first time" — avoids a KeyError on the first subscriber.
        self._subscribers.setdefault(event_name, []).append(handler)

    def publish(self, event_name: str, payload: dict) -> None:
        """Call every handler subscribed to `event_name`, in order, with `payload`."""
        # .get(..., []) rather than [event_name]: publishing an event with
        # zero subscribers is a normal no-op, not an error.
        for handler in self._subscribers.get(event_name, []):
            handler(payload)


# ---------------------------------------------------------------------------
# Demo: a toy "order placed" event with three independent subscribers.
# Each subscriber does ONE job and doesn't know the other two exist — that
# decoupling is the whole point of the pattern.
# ---------------------------------------------------------------------------

def log_order(payload: dict) -> None:
    """Subscriber 1: just logs that something happened."""
    print(f"[log]      order received: {payload['order_id']} (${payload['amount']})")


def send_confirmation_email(payload: dict) -> None:
    """Subscriber 2: pretends to email the customer."""
    print(f"[email]    confirmation sent for {payload['order_id']}")


def update_inventory(payload: dict) -> None:
    """Subscriber 3: pretends to decrement stock."""
    print(f"[inventory] stock decremented for {payload['order_id']}")


def broken_subscriber(payload: dict) -> None:
    """
    Subscriber 4: deliberately raises, to make the 'synchronous, in-order,
    no error isolation' trade-off visible instead of just described.
    Comment out the bus.subscribe(...) line below to see the difference.
    """
    raise RuntimeError(f"something went wrong processing {payload['order_id']}")


if __name__ == "__main__":
    bus = EventBus()

    # Subscription order == dispatch order. Try reordering these three lines
    # and re-running to see the printed order change to match.
    bus.subscribe("ORDER_PLACED", log_order)
    bus.subscribe("ORDER_PLACED", send_confirmation_email)
    bus.subscribe("ORDER_PLACED", update_inventory)

    print("=== publishing ORDER_PLACED (no subscribers fail) ===")
    bus.publish("ORDER_PLACED", {"order_id": "ord-001", "amount": 42.50})

    print("\n=== publishing an event with NO subscribers (silent no-op) ===")
    bus.publish("NOBODY_IS_LISTENING", {"anything": "goes"})
    print("(nothing printed above — that's expected, and that's the point)")

    print("\n=== now add a subscriber that raises, and publish again ===")
    bus.subscribe("ORDER_PLACED", broken_subscriber)
    try:
        bus.publish("ORDER_PLACED", {"order_id": "ord-002", "amount": 17.00})
    except RuntimeError as exc:
        print(f"[caught]   publish() propagated the exception: {exc}")
        print("           notice update_inventory ran fine, but anything")
        print("           subscribed AFTER broken_subscriber never got called.")