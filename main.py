from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from screens.login_screen import LoginScreen
from screens.dashboard_screen import DashboardScreen
from screens.checklist_screen import ChecklistScreen
from screens.map_screen import MapScreen
from screens.history_screen import HistoryScreen
from screens.profile_screen import ProfileScreen


class PickerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_order = None

    def build(self):
        # Configuración segura de la ventana al iniciar la app
        if Window:
            Window.size = (375, 812)
            Window.clearcolor = (1, 1, 1, 1)

        sm = ScreenManager()
        sm.add_widget(LoginScreen())
        sm.add_widget(DashboardScreen())
        sm.add_widget(ChecklistScreen())
        sm.add_widget(MapScreen())
        sm.add_widget(HistoryScreen())
        sm.add_widget(ProfileScreen())

        return sm


if __name__ == "__main__":
    PickerApp().run()