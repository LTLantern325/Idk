"""
Python conversion of Supercell.Laser.Logic.Home.HomeMode.cs
Home mode class for managing home game mode
"""

from typing import Dict, List, Optional, Any
from .client_home import ClientHome

class HomeModeState:
    """Home mode states"""
    INACTIVE = 0
    LOADING = 1
    ACTIVE = 2
    MAINTENANCE = 3

class HomeMode:
    """Home mode class for managing home game mode"""

    def __init__(self):
        """Initialize home mode"""
        self.mode_id = 1  # Home mode ID
        self.state = HomeModeState.INACTIVE
        self.client_home: Optional[ClientHome] = None

        # Mode settings
        self.auto_save_enabled = True
        self.auto_save_interval = 60000  # 60 seconds in milliseconds
        self.last_auto_save = 0

        # Session data
        self.session_id = 0
        self.session_start_time = 0
        self.is_active = False

        # Tutorial/onboarding
        self.tutorial_step = 0
        self.tutorial_completed = False
        self.onboarding_flags = []

        # UI state
        self.current_screen = "home"
        self.screen_history = []
        self.popup_queue = []

        # Event tracking
        self.events_enabled = True
        self.event_listeners = {}

        # Background tasks
        self.background_tasks = []
        self.task_scheduler_active = False

        # Notifications
        self.notification_queue = []
        self.notification_settings = {
            'push_enabled': True,
            'sound_enabled': True,
            'vibration_enabled': True
        }

    def get_mode_id(self) -> int:
        """Get mode ID"""
        return self.mode_id

    def get_state(self) -> int:
        """Get current state"""
        return self.state

    def set_state(self, state: int) -> None:
        """Set current state"""
        old_state = self.state
        self.state = state
        self._on_state_changed(old_state, state)

    def get_client_home(self) -> Optional[ClientHome]:
        """Get client home"""
        return self.client_home

    def set_client_home(self, client_home: ClientHome) -> None:
        """Set client home"""
        self.client_home = client_home

    def initialize(self) -> bool:
        """Initialize home mode"""
        try:
            self.set_state(HomeModeState.LOADING)

            # Initialize client home if not set
            if not self.client_home:
                self.client_home = ClientHome()

            # Initialize tutorial
            if not self.tutorial_completed:
                self._initialize_tutorial()

            # Start background tasks
            self._start_background_tasks()

            # Set as active
            self.set_state(HomeModeState.ACTIVE)
            self.is_active = True

            return True

        except Exception as e:
            print(f"Failed to initialize HomeMode: {e}")
            self.set_state(HomeModeState.INACTIVE)
            return False

    def shutdown(self) -> None:
        """Shutdown home mode"""
        self.is_active = False
        self.set_state(HomeModeState.INACTIVE)

        # Stop background tasks
        self._stop_background_tasks()

        # Save data
        if self.client_home and self.auto_save_enabled:
            self._save_home_data()

    def update(self, delta_time: float) -> None:
        """Update home mode"""
        if not self.is_active or self.state != HomeModeState.ACTIVE:
            return

        current_time = int(delta_time * 1000)  # Convert to milliseconds

        # Update auto save
        if (self.auto_save_enabled and 
            current_time - self.last_auto_save >= self.auto_save_interval):
            self._save_home_data()
            self.last_auto_save = current_time

        # Update background tasks
        self._update_background_tasks(delta_time)

        # Process notification queue
        self._process_notifications()

        # Update client home
        if self.client_home:
            self.client_home.update_session_time(current_time)

    def navigate_to_screen(self, screen_name: str) -> bool:
        """Navigate to screen"""
        if screen_name == self.current_screen:
            return True

        # Add current screen to history
        if self.current_screen != "":
            self.screen_history.append(self.current_screen)

        # Limit history size
        if len(self.screen_history) > 10:
            self.screen_history.pop(0)

        old_screen = self.current_screen
        self.current_screen = screen_name

        self._on_screen_changed(old_screen, screen_name)
        return True

    def go_back(self) -> bool:
        """Go back to previous screen"""
        if not self.screen_history:
            return False

        previous_screen = self.screen_history.pop()
        old_screen = self.current_screen
        self.current_screen = previous_screen

        self._on_screen_changed(old_screen, previous_screen)
        return True

    def add_notification(self, notification_data: Dict[str, Any]) -> None:
        """Add notification to queue"""
        self.notification_queue.append(notification_data)

    def start_tutorial(self) -> None:
        """Start tutorial"""
        self.tutorial_step = 0
        self.tutorial_completed = False
        self._initialize_tutorial()

    def advance_tutorial(self) -> bool:
        """Advance tutorial to next step"""
        if self.tutorial_completed:
            return False

        self.tutorial_step += 1

        # Check if tutorial is complete
        max_tutorial_steps = 10  # Configurable
        if self.tutorial_step >= max_tutorial_steps:
            self.complete_tutorial()
            return False

        return True

    def complete_tutorial(self) -> None:
        """Complete tutorial"""
        self.tutorial_completed = True
        self.tutorial_step = 0

        # Grant tutorial rewards
        if self.client_home:
            self.client_home.add_resources(gold=1000, diamonds=50)

    def _initialize_tutorial(self) -> None:
        """Initialize tutorial system"""
        if not self.tutorial_completed:
            self.tutorial_step = 1

    def _on_state_changed(self, old_state: int, new_state: int) -> None:
        """Handle state change"""
        state_names = {
            HomeModeState.INACTIVE: "Inactive",
            HomeModeState.LOADING: "Loading",
            HomeModeState.ACTIVE: "Active",
            HomeModeState.MAINTENANCE: "Maintenance"
        }

        old_name = state_names.get(old_state, "Unknown")
        new_name = state_names.get(new_state, "Unknown")

        print(f"HomeMode state changed: {old_name} -> {new_name}")

    def _on_screen_changed(self, old_screen: str, new_screen: str) -> None:
        """Handle screen change"""
        print(f"Screen changed: {old_screen} -> {new_screen}")

    def _start_background_tasks(self) -> None:
        """Start background tasks"""
        self.task_scheduler_active = True

        # Add default background tasks
        self.background_tasks = [
            {'name': 'auto_save', 'interval': 60.0, 'last_run': 0.0},
            {'name': 'resource_generation', 'interval': 10.0, 'last_run': 0.0},
            {'name': 'quest_check', 'interval': 30.0, 'last_run': 0.0}
        ]

    def _stop_background_tasks(self) -> None:
        """Stop background tasks"""
        self.task_scheduler_active = False
        self.background_tasks.clear()

    def _update_background_tasks(self, delta_time: float) -> None:
        """Update background tasks"""
        if not self.task_scheduler_active:
            return

        for task in self.background_tasks:
            task['last_run'] += delta_time

            if task['last_run'] >= task['interval']:
                self._execute_background_task(task['name'])
                task['last_run'] = 0.0

    def _execute_background_task(self, task_name: str) -> None:
        """Execute background task"""
        if task_name == 'auto_save':
            self._save_home_data()
        elif task_name == 'resource_generation':
            self._generate_passive_resources()
        elif task_name == 'quest_check':
            self._check_quest_progress()

    def _save_home_data(self) -> bool:
        """Save home data"""
        if not self.client_home:
            return False

        try:
            # Save logic would go here
            print(f"Saved home data for player: {self.client_home.get_player_name()}")
            return True
        except Exception as e:
            print(f"Failed to save home data: {e}")
            return False

    def _generate_passive_resources(self) -> None:
        """Generate passive resources"""
        if self.client_home:
            # Small passive resource generation
            self.client_home.add_resources(gold=10)

    def _check_quest_progress(self) -> None:
        """Check quest progress"""
        # Quest checking logic would go here
        pass

    def _process_notifications(self) -> None:
        """Process notification queue"""
        if not self.notification_queue:
            return

        # Process one notification per update
        notification = self.notification_queue.pop(0)
        self._show_notification(notification)

    def _show_notification(self, notification: Dict[str, Any]) -> None:
        """Show notification"""
        print(f"Showing notification: {notification.get('message', 'No message')}")

    def get_state_name(self) -> str:
        """Get current state name"""
        state_names = {
            HomeModeState.INACTIVE: "Inactive",
            HomeModeState.LOADING: "Loading", 
            HomeModeState.ACTIVE: "Active",
            HomeModeState.MAINTENANCE: "Maintenance"
        }
        return state_names.get(self.state, "Unknown")

    def __str__(self) -> str:
        """String representation"""
        player_name = self.client_home.get_player_name() if self.client_home else "Unknown"
        return f"HomeMode({self.get_state_name()}, player='{player_name}', screen='{self.current_screen}')"
