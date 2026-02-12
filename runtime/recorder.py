"""
Execution Recorder - Tracks execution for time travel
Works with TimeEngine to provide complete observability
"""

from typing import Optional, Any, Callable, List
from datetime import datetime


class ExecutionRecorder:
    """
    Records execution events for playback and analysis
    Decorates runtime execution with observability hooks
    """

    def __init__(self):
        self.recording = True
        self.events: List[dict] = []
        self.listeners: List[Callable] = []

    def record_event(self, event_type: str, data: dict) -> None:
        """Record an execution event"""
        if not self.recording:
            return

        event = {
            'type': event_type,
            'timestamp': datetime.now().timestamp(),
            'data': data
        }

        self.events.append(event)

        # Notify listeners
        for listener in self.listeners:
            try:
                listener(event)
            except Exception as e:
                print(f"⚠️ Listener error: {e}")

    def add_listener(self, callback: Callable) -> None:
        """Add event listener for live updates"""
        self.listeners.append(callback)

    def remove_listener(self, callback: Callable) -> None:
        """Remove event listener"""
        if callback in self.listeners:
            self.listeners.remove(callback)

    def start_recording(self) -> None:
        """Start recording events"""
        self.recording = True

    def stop_recording(self) -> None:
        """Stop recording events"""
        self.recording = False

    def clear_events(self) -> None:
        """Clear recorded events"""
        self.events.clear()

    def get_events(self, event_type: Optional[str] = None) -> List[dict]:
        """Get recorded events, optionally filtered by type"""
        if event_type:
            return [e for e in self.events if e['type'] == event_type]
        return self.events.copy()

    def get_event_types(self) -> List[str]:
        """Get unique event types"""
        return list(set(e['type'] for e in self.events))

    def __repr__(self) -> str:
        status = "Recording" if self.recording else "Paused"
        return f"<ExecutionRecorder: {len(self.events)} events, {status}>"


# Event type constants
EVENT_EXECUTION_START = "execution_start"
EVENT_EXECUTION_END = "execution_end"
EVENT_STATEMENT_EXECUTE = "statement_execute"
EVENT_VARIABLE_SET = "variable_set"
EVENT_VARIABLE_GET = "variable_get"
EVENT_FUNCTION_CALL = "function_call"
EVENT_FUNCTION_RETURN = "function_return"
EVENT_ERROR = "error"
EVENT_STATE_CHANGE = "state_change"
