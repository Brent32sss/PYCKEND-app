# widgets/custom_widgets.py

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import SlideTransition
from kivy.graphics import Color, Ellipse, Line, RoundedRectangle, Rectangle
from kivy.properties import ListProperty, StringProperty, BooleanProperty
from kivy.metrics import dp, sp

from config.colors import MANGO, LEAF, MINT_LINE, FOREST, SLATE_TEXT, WHITE, LINE


class DotWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(size_hint=(None, None), size=(dp(10), dp(10)), **kwargs)
        self.bind(pos=self._update, size=self._update)

    def _update(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(*MANGO)
            Ellipse(pos=self.pos, size=self.size)


class RoundedBox(BoxLayout):
    bg_color = ListProperty([1, 1, 1, 1])
    border_color = ListProperty([0, 0, 0, 0])
    radius = ListProperty([dp(14)])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._update, size=self._update, bg_color=self._update, border_color=self._update)

    def _update(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            if len(self.border_color) == 4 and self.border_color[3] > 0:
                Color(*self.border_color)
                RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)
                Color(*self.bg_color)
                RoundedRectangle(
                    pos=(self.x + dp(1), self.y + dp(1)),
                    size=(max(0, self.width - dp(2)), max(0, self.height - dp(2))),
                    radius=self.radius,
                )
            else:
                Color(*self.bg_color)
                RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)


class RoundedButton(ButtonBehavior, BoxLayout):
    bg_color = ListProperty([0.106, 0.263, 0.196, 1])
    radius = ListProperty([dp(14)])
    text = StringProperty("")
    font_size = StringProperty("14sp")
    bold = BooleanProperty(True)
    text_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.lbl = Label(
            text=self.text,
            font_size=self.font_size,
            bold=self.bold,
            color=self.text_color,
            halign='center',
            valign='middle',
        )
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
        self.padding = [dp(12), dp(4), dp(12), dp(4)]
        self.lbl = Label(text=self.text, font_size=self.font_size, bold=True, color=self.text_color)
        self.lbl.bind(texture_size=self._update_size)
        self.add_widget(self.lbl)
        self.bind(pos=self._update, size=self._update, bg_color=self._update)

    def _update_size(self, instance, val):
        self.width = val[0] + dp(24)
        self.height = val[1] + dp(10)

    def _update(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(999)])


class CustomCheckBox(ButtonBehavior, Widget):
    active = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(26), dp(26))
        self.bind(pos=self._update, size=self._update, active=self._update)

    def _update(self, *args):
        self.canvas.clear()
        with self.canvas:
            if self.active:
                Color(*LEAF)
                RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(7)])
                Color(1, 1, 1, 1)
                cx, cy = self.x, self.y
                Line(
                    points=[
                        cx + dp(7), cy + dp(13),
                        cx + dp(11), cy + dp(8),
                        cx + dp(19), cy + dp(18),
                    ],
                    width=dp(2.2),
                )
            else:
                Color(*MINT_LINE)
                RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(7)])
                Color(1, 1, 1, 1)
                RoundedRectangle(
                    pos=(self.x + dp(2), self.y + dp(2)),
                    size=(max(0, self.width - dp(4)), max(0, self.height - dp(4))),
                    radius=[dp(6)],
                )

    def on_release(self):
        self.active = not self.active


class NavIconWidget(Widget):
    icon_type = StringProperty('pedidos')
    color = ListProperty([0, 0, 0, 1])

    def __init__(self, icon_type, color, **kwargs):
        super().__init__(size_hint=(None, None), size=(dp(24), dp(24)), **kwargs)
        self.icon_type = icon_type
        self.color = color
        self.bind(pos=self._draw, size=self._draw, color=self._draw)

    def _draw(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(*self.color)
            cx, cy = self.center_x, self.center_y

            if self.icon_type == 'pedidos':
                Line(rounded_rectangle=(cx - dp(8), cy - dp(10), dp(16), dp(18), dp(3)), width=dp(1.5))
                Line(points=[cx - dp(4), cy + dp(4), cx + dp(4), cy + dp(4)], width=dp(1.5))
                Line(points=[cx - dp(4), cy, cx + dp(4), cy], width=dp(1.5))
                Line(points=[cx - dp(4), cy - dp(4), cx + dp(2), cy - dp(4)], width=dp(1.5))

            elif self.icon_type == 'mapa':
                Line(circle=(cx, cy + dp(2), dp(6)), width=dp(1.5))
                Line(points=[cx, cy - dp(4), cx, cy - dp(9)], width=dp(1.5))
                Ellipse(pos=(cx - dp(2), cy), size=(dp(4), dp(4)))

            elif self.icon_type == 'historial':
                Line(circle=(cx, cy, dp(9)), width=dp(1.5))
                Line(points=[cx, cy, cx, cy + dp(5)], width=dp(1.5))
                Line(points=[cx, cy, cx + dp(4), cy], width=dp(1.5))

            elif self.icon_type == 'perfil':
                Line(circle=(cx, cy + dp(4), dp(4.5)), width=dp(1.5))
                Line(ellipse=(cx - dp(8), cy - dp(10), dp(16), dp(10), 0, 180), width=dp(1.5))


class BottomNavItem(ButtonBehavior, BoxLayout):
    def __init__(self, icon_type, text, target, active, **kwargs):
        super().__init__(
            orientation='vertical',
            padding=[0, dp(6), 0, dp(4)],
            spacing=dp(2),
            **kwargs
        )
        self.target = target
        clr = FOREST if active else SLATE_TEXT

        icon_box = BoxLayout(size_hint_y=0.6)
        icon_box.add_widget(Widget(size_hint_x=1))
        icon_box.add_widget(NavIconWidget(icon_type=icon_type, color=clr))
        icon_box.add_widget(Widget(size_hint_x=1))

        self.add_widget(icon_box)
        self.add_widget(Label(text=text, font_size="10sp", bold=active, color=clr, size_hint_y=0.4))

    def on_release(self):
        app = App.get_running_app()
        if app and app.root:
            if app.root.current != self.target:
                direction = 'right' if self.target == 'dashboard' else 'left'
                app.root.transition = SlideTransition(direction=direction)
                app.root.current = self.target


class BottomNavBar(BoxLayout):
    def __init__(self, active_item="pedidos", **kwargs):
        super().__init__(size_hint_y=None, height=dp(62), spacing=0, **kwargs)
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
            Line(points=[self.x, self.y + self.height, self.x + self.width, self.y + self.height], width=dp(1))


class UserAvatarWidget(Widget):
    color = ListProperty([1, 1, 1, 1])

    def __init__(self, color=[1, 1, 1, 1], **kwargs):
        super().__init__(size_hint=(None, None), size=(dp(24), dp(24)), **kwargs)
        self.color = color
        self.bind(pos=self._draw, size=self._draw, color=self._draw)

    def _draw(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(*self.color)
            cx, cy = self.center_x, self.center_y
            Line(circle=(cx, cy + dp(4), dp(5)), width=dp(1.8))
            Line(ellipse=(cx - dp(9), cy - dp(9), dp(18), dp(10), 0, 180), width=dp(1.8))