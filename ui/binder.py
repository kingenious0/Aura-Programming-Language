"""
UI Binding Layer - Connects Aura State to UI Frameworks
Provides reactive state subscription and auto-updates
"""

from typing import Dict, List, Callable, Any, Optional
from dataclasses import dataclass


@dataclass
class Subscription:
    """Represents a UI subscription to a state variable"""
    var_name: str
    callback: Callable
    active: bool = True


class UIBinder:
    """
    Manages bindings between Aura state and UI frameworks
    Implements observer pattern for reactive updates
    """

    def __init__(self, runtime):
        self.runtime = runtime
        self.subscriptions: Dict[str, List[Subscription]] = {}
        self.global_listeners: List[Callable] = []

    def subscribe(self, var_name: str, callback: Callable) -> Subscription:
        """
        Subscribe to variable changes

        Args:
            var_name: Variable to watch
            callback: Function to call when variable changes

        Returns:
            Subscription object
        """
        if var_name not in self.subscriptions:
            self.subscriptions[var_name] = []

        subscription = Subscription(var_name=var_name, callback=callback)
        self.subscriptions[var_name].append(subscription)

        # Call immediately with current value
        try:
            current_value = self.runtime.state.get_var(var_name)
            callback(current_value)
        except:
            callback(None)

        return subscription

    def unsubscribe(self, subscription: Subscription) -> None:
        """Remove a subscription"""
        if subscription.var_name in self.subscriptions:
            subscription.active = False
            self.subscriptions[subscription.var_name].remove(subscription)

    def subscribe_all(self, callback: Callable) -> None:
        """Subscribe to all state changes"""
        self.global_listeners.append(callback)

    def notify(self, var_name: str, new_value: Any) -> None:
        """
        Notify subscribers of a variable change
        Called by runtime when state changes
        """
        # Notify specific subscribers
        if var_name in self.subscriptions:
            for sub in self.subscriptions[var_name]:
                if sub.active:
                    try:
                        sub.callback(new_value)
                    except Exception as e:
                        print(f"⚠️  Subscription callback error: {e}")

        # Notify global listeners
        for listener in self.global_listeners:
            try:
                listener(var_name, new_value)
            except Exception as e:
                print(f"⚠️  Global listener error: {e}")

    def notify_all(self) -> None:
        """Notify all subscribers of current state"""
        all_vars = self.runtime.state.get_all_vars()
        for var_name, value in all_vars.items():
            self.notify(var_name, value)

    def get_value(self, var_name: str, default=None) -> Any:
        """Get current value of a variable"""
        try:
            return self.runtime.state.get_var(var_name)
        except:
            return default

    def set_value(self, var_name: str, value: Any) -> None:
        """Set variable value and notify subscribers"""
        self.runtime.state.set_var(var_name, value)
        self.notify(var_name, value)

    def get_subscription_count(self, var_name: Optional[str] = None) -> int:
        """Get number of active subscriptions"""
        if var_name:
            return len(self.subscriptions.get(var_name, []))
        return sum(len(subs) for subs in self.subscriptions.values())

    def clear_subscriptions(self) -> None:
        """Clear all subscriptions"""
        self.subscriptions.clear()
        self.global_listeners.clear()
