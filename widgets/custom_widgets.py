# widgets/custom_widgets.py

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import SlideTransition
from kivy.graphics import Color, Ellipse, Line, RoundedRectangle, Rectangle
from kivy.properties import ListProperty, StringProperty, BooleanProperty

from config.colors import MANGO, LEAF, MINT_LINE, FOREST, SLATE_TEXT, WHITE, LINE

class DotWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(size_hint=(None, None), size=(10, 10), **kwargs)
        self.bind(pos=self._update, size=self._update)

    def _update(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(*MANGO)
            Ellipse(pos=self.pos, size=self.size)

class RoundedBox(BoxLayout):
    bg_color = ListProperty([1, 1, 1, 1])
    border_color = ListProperty([0, 0, 0, 0])
    radius = ListProperty([14])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._update, size=self._update, bg_color=self._update, border_color=self._update)

    def _update(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            if self.border_color[3] > 0:
                Color(*self.border_color)
                RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)
                Color(*self.bg_color)
                RoundedRectangle(pos=(self.x + 1, self.y + 1), size=(max(0, self.width - 2), max(0, self.height - 2)), radius=self.radius)
            else:
                Color(*self.bg_color)
                RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)

class RoundedButton(ButtonBehavior, BoxLayout):
    bg_color = ListProperty([0.106, 0.263, 0.196, 1])
    radius = ListProperty([14])
    text = StringProperty("")
    font_size = StringProperty("14sp")
    bold = BooleanProperty(True)
    text_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.lbl = Label(text=self.text, font_size=self.font_size, bold=self.bold, color=self.text_color, halign='center', valign='middle')
        self.lbl.bind(size=self.lbl.setter('text_size'))
        self.add_widget(self.lbl)
        self.bind(pos=self._update, size=self._update, bg_color=self._update, text=self._update_text)

    def _update_text(self, instance, val):
        self.lbl.text = val

    def _update(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)

class PillBadge(BoxLayout):
    bg_color = ListProperty([0.906, 0.945, 0.910, 1])
    text_color = ListProperty([0.106, 0.263, 0.196, 1])
    text = StringProperty("")
    font_size = StringProperty("10sp")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.padding = [12, 4, 12, 4]
        self.lbl = Label(text=self.text, font_size=self.font_size, bold=True, color=self.text_color)
        self.lbl.bind(texture_size=self._update_size)
        self.add_widget(self.lbl)
        self.bind(pos=self._update, size=self._update, bg_color=self._update)

    def _update_size(self, instance, val):
        self.width = val[0] + 24
        self.height = val[1] + 10

    def _update(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[999])

class CustomCheckBox(ButtonBehavior, Widget):
    active = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (26, 26)
        self.bind(pos=self._update, size=self._update, active=self._update)

    def _update(self, *args):
        self.canvas.clear()
        with self.canvas:
            if self.active:
                Color(*LEAF)
                RoundedRectangle(pos=self.pos, size=self.size, radius=[7])
                Color(1, 1, 1, 1)
                cx, cy = self.x, self.y
                Line(points=[cx + 7, cy + 13, cx + 11, cy + 8, cx + 19, cy + 18], width=2.2)
            else:
                Color(*MINT_LINE)
                RoundedRectangle(pos=self.pos, size=self.size, radius=[7])
                Color(1, 1, 1, 1)
                RoundedRectangle(pos=(self.x + 2, self.y + 2), size=(self.width - 4, self.height - 4), radius=[6])

    def on_release(self):
        self.active = not self.active

# Widget de íconos vectoriales dinámicos para la barra inferior
class NavIconWidget(Widget):
    icon_type = StringProperty('pedidos')
    color = ListProperty([0, 0, 0, 1])

    def __init__(self, icon_type, color, **kwargs):
        super().__init__(size_hint=(None, None), size=(22, 22), **kwargs)
        self.icon_type = icon_type
        self.color = color
        self.bind(pos=self._draw, size=self._draw, color=self._draw)

    def _draw(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(*self.color)
            cx, cy = self.center_x, self.center_y

            if self.icon_type == 'pedidos':
                # Ícono de Lista / Portapapeles
                Line(rounded_rectangle=(cx - 8, cy - 10, 16, 18, 3), width=1.5)
                Line(points=[cx - 4, cy + 4, cx + 4, cy + 4], width=1.5)
                Line(points=[cx - 4, cy, cx + 4, cy], width=1.5)
                Line(points=[cx - 4, cy - 4, cx + 2, cy - 4], width=1.5)

            elif self.icon_type == 'mapa':
                # Ícono de Ubicación / Pin de Mapa
                Line(circle=(cx, cy + 2, 6), width=1.5)
                Line(points=[cx, cy - 4, cx, cy - 9], width=1.5)
                Ellipse(pos=(cx - 2, cy + 0), size=(4, 4))

            elif self.icon_type == 'historial':
                # Ícono de Reloj
                Line(circle=(cx, cy, 9), width=1.5)
                Line(points=[cx, cy, cx, cy + 5], width=1.5)
                Line(points=[cx, cy, cx + 4, cy], width=1.5)

            elif self.icon_type == 'perfil':
                # Ícono de Usuario
                Line(circle=(cx, cy + 4, 4.5), width=1.5)
                Line(ellipse=(cx - 8, cy - 10, 16, 10, 0, 180), width=1.5)

class BottomNavItem(ButtonBehavior, BoxLayout):
    def __init__(self, icon_type, text, target, active, **kwargs):
        super().__init__(orientation='vertical', padding=[0, 6, 0, 4], spacing=2, **kwargs)
        self.target = target
        clr = FOREST if active else SLATE_TEXT

        # Contenedor para centrar el ícono vectorial
        icon_box = BoxLayout(size_hint_y=0.6)
        icon_box.add_widget(Widget(size_hint_x=1))
        icon_box.add_widget(NavIconWidget(icon_type=icon_type, color=clr))
        icon_box.add_widget(Widget(size_hint_x=1))

        self.add_widget(icon_box)
        self.add_widget(Label(text=text, font_size="9sp", bold=active, color=clr, size_hint_y=0.4))

    def on_release(self):
        app = App.get_running_app()
        if app and app.root:
            if app.root.current != self.target:
                direction = 'right' if self.target == 'dashboard' else 'left'
                app.root.transition = SlideTransition(direction=direction)
                app.root.current = self.target

class BottomNavBar(BoxLayout):
    def __init__(self, active_item="pedidos", **kwargs):
        super().__init__(size_hint_y=None, height=60, spacing=0, **kwargs)
        self.bind(pos=self._update, size=self._update)

        items = [
            ("pedidos", "Pedidos", "dashboard"),
            ("mapa", "Mapa", "mapa"),
            ("historial", "Historial", "historial"),
            ("perfil", "Perfil", "perfil")
        ]

        for icon_type, txt, target in items:
            active = (active_item.lower() == target or active_item.lower() == txt.lower())
            n_item = BottomNavItem(icon_type, txt, target, active)
            self.add_widget(n_item)

    def _update(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*WHITE)
            Rectangle(size=self.size, pos=self.pos)
            Color(*LINE)
            Line(points=[self.x, self.y + self.height, self.x + self.width, self.y + self.height], width=1)


class UserAvatarWidget(Widget):
    color = ListProperty([1, 1, 1, 1])

    def __init__(self, color=[1, 1, 1, 1], **kwargs):
        super().__init__(size_hint=(None, None), size=(24, 24), **kwargs)
        self.color = color
        self.bind(pos=self._draw, size=self._draw, color=self._draw)

    def _draw(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(*self.color)
            cx, cy = self.center_x, self.center_y
            # Cabeza
            Line(circle=(cx, cy + 4, 5), width=1.8)
            # Torso / Hombros
            Line(ellipse=(cx - 9, cy - 9, 18, 10, 0, 180), width=1.8)