"""
Event System - FIFO event queue and dispatcher
Handles event registration, emission, and processing
"""

from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass
from collections import deque
import time


@dataclass
class Event:
    """Represents an event in the system"""
    name: str
    data: Dict[str, Any]
    timestamp: float = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = time.time()


class EventQueue:
    """
    FIFO event queue with handler registration
    Supports custom events, timers, and file watching
    """

    def __init__(self):
        self.queue: deque = deque()
        self.handlers: Dict[str, List[Callable]] = {}
        self.processed_count = 0

    def register(self, event_name: str, handler: Callable) -> None:
        """Register a handler for an event type"""
        if event_name not in self.handlers:
            self.handlers[event_name] = []
        self.handlers[event_name].append(handler)

    def unregister(self, event_name: str, handler: Optional[Callable] = None) -> None:
        """Unregister handler(s) for an event type"""
        if event_name not in self.handlers:
            return

        if handler is None:
            # Remove all handlers for this event
            del self.handlers[event_name]
        else:
            # Remove specific handler
            if handler in self.handlers[event_name]:
                self.handlers[event_name].remove(handler)

    def emit(self, event_name: str, data: Optional[Dict[str, Any]] = None) -> None:
        """Emit an event (add to queue)"""
        event = Event(name=event_name, data=data or {})
        self.queue.append(event)

    def process_one(self) -> bool:
        """
        Process one event from the queue
        Returns True if event was processed, False if queue empty
        """
        if not self.queue:
            return False

        event = self.queue.popleft()

        # Get handlers for this event type
        handlers = self.handlers.get(event.name, [])

        # Execute all handlers
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                print(f"⚠️ Event handler error ({event.name}): {e}")

        self.processed_count += 1
        return True

    def process_all(self) -> int:
        """
        Process all events in queue
        Returns number of events processed
        """
        count = 0
        while self.process_one():
            count += 1
        return count

    def pending_count(self) -> int:
        """Get number of pending events"""
        return len(self.queue)

    def has_handlers(self, event_name: str) -> bool:
        """Check if any handlers registered for event"""
        return event_name in self.handlers and len(self.handlers[event_name]) > 0

    def clear(self) -> None:
        """Clear all events and handlers"""
        self.queue.clear()
        self.handlers.clear()
        self.processed_count = 0

    def __repr__(self) -> str:
        pending = len(self.queue)
        handlers = sum(len(h) for h in self.handlers.values())
        return f"<EventQueue: {pending} pending, {handlers} handlers, {self.processed_count} processed>"


class EventScheduler:
    """
    Schedules events to fire after delays or at intervals
    """

    def __init__(self, event_queue: EventQueue):
        self.event_queue = event_queue
        self.scheduled: List[Dict[str, Any]] = []

    def schedule_once(self, event_name: str, delay_seconds: float, data: Optional[Dict] = None) -> None:
        """Schedule event to fire once after delay"""
        fire_time = time.time() + delay_seconds
        self.scheduled.append({
            'event_name': event_name,
            'fire_time': fire_time,
            'data': data or {},
            'interval': None
        })

    def schedule_interval(self, event_name: str, interval_seconds: float, data: Optional[Dict] = None) -> None:
        """Schedule event to fire repeatedly at interval"""
        fire_time = time.time() + interval_seconds
        self.scheduled.append({
            'event_name': event_name,
            'fire_time': fire_time,
            'data': data or {},
            'interval': interval_seconds
        })

    def tick(self) -> int:
        """
        Process scheduled events (call this in runtime loop)
        Returns number of events fired
        """
        now = time.time()
        fired_count = 0

        # Check each scheduled event
        to_remove = []
        for i, scheduled in enumerate(self.scheduled):
            if now >= scheduled['fire_time']:
                # Fire the event
                self.event_queue.emit(
                    scheduled['event_name'], scheduled['data'])
                fired_count += 1

                # If interval, reschedule
                if scheduled['interval']:
                    scheduled['fire_time'] = now + scheduled['interval']
                else:
                    # One-shot, remove it
                    to_remove.append(i)

        # Remove one-shot events
        for i in reversed(to_remove):
            self.scheduled.pop(i)

        return fired_count

    def clear(self) -> None:
        """Clear all scheduled events"""
        self.scheduled.clear()
