from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp, sp

from config.colors import (
    FOREST, FOREST_DARK, MANGO, SLATE_BG, MINT, CHARCOAL,
    SLATE_TEXT, CORAL, CORAL_BG, WHITE, LINE
)
from widgets.custom_widgets import RoundedBox, PillBadge, BottomNavBar, UserAvatarWidget
from data.sample_data import ORDERS, PICKER_DATA


class DashboardScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "dashboard"

    def on_pre_enter(self):
        self.clear_widgets()

        main_layout = BoxLayout(orientation='vertical', spacing=0)

        # Encabezado verde con padding superior para librar el notch (dp(40))
        header = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(235),
            padding=[dp(20), dp(40), dp(20), dp(12)],
            spacing=dp(10),
        )
        with header.canvas.before:
            Color(*FOREST_DARK)
            self.header_bg = Rectangle(size=header.size, pos=header.pos)
        header.bind(pos=self._update_header_bg, size=self._update_header_bg)

        # Fila superior: Turno y Avisos
        top_row = BoxLayout(size_hint_y=None, height=dp(22))
        lbl_shift = Label(
            text=PICKER_DATA.get("shift", "Turno tarde"),
            font_size="11sp",
            color=(0.7, 0.8, 0.75, 1),
            size_hint_x=0.7,
            halign='left',
            valign='middle',
        )
        lbl_shift.bind(size=lbl_shift.setter('text_size'))

        lbl_notif = Label(
            text=f"Avisos: {PICKER_DATA.get('notifications', 2)}",
            font_size="11sp",
            color=(0.7, 0.8, 0.75, 1),
            size_hint_x=0.3,
            halign='right',
            valign='middle',
        )
        lbl_notif.bind(size=lbl_notif.setter('text_size'))

        top_row.add_widget(lbl_shift)
        top_row.add_widget(lbl_notif)
        header.add_widget(top_row)

        # Fila del usuario
        user_row = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(12))
        orange_badge = RoundedBox(
            size_hint=(None, None),
            size=(dp(44), dp(44)),
            bg_color=MANGO,
            radius=[dp(12)],
        )

        avatar_box = BoxLayout(size_hint=(None, None), size=(dp(44), dp(44)))
        avatar_box.add_widget(Widget(size_hint_x=1))
        avatar_box.add_widget(UserAvatarWidget(color=WHITE))
        avatar_box.add_widget(Widget(size_hint_x=1))
        orange_badge.add_widget(avatar_box)
        user_row.add_widget(orange_badge)

        u_info = BoxLayout(orientation='vertical', spacing=dp(2))
        lbl_uname = Label(
            text=PICKER_DATA["name"],
            font_size="16sp",
            bold=True,
            color=WHITE,
            halign='left',
            valign='middle',
        )
        lbl_uname.bind(size=lbl_uname.setter('text_size'))

        lbl_urole = Label(
            text=PICKER_DATA["role"],
            font_size="11sp",
            color=(0.7, 0.8, 0.75, 1),
            halign='left',
            valign='middle',
        )
        lbl_urole.bind(size=lbl_urole.setter('text_size'))

        u_info.add_widget(lbl_uname)
        u_info.add_widget(lbl_urole)
        user_row.add_widget(u_info)
        header.add_widget(user_row)

        # KPIs dinámicos
        asignados_val = str(len(ORDERS))
        urgentes_val = str(sum(1 for o in ORDERS if o.get('priority') == "Urgente"))
        puntualidad_val = PICKER_DATA.get("stats", {}).get("puntualidad", "92%")

        kpi_grid = GridLayout(cols=3, size_hint_y=None, height=dp(56), spacing=dp(8))
        for val, lbl in [(asignados_val, "Asignados"), (urgentes_val, "Urgentes"), (puntualidad_val, "A tiempo")]:
            kbox = RoundedBox(
                orientation='vertical',
                bg_color=[0.12, 0.32, 0.24, 1],
                radius=[dp(12)],
                padding=[dp(6), dp(6), dp(6), dp(6)],
            )
            kbox.add_widget(Label(text=val, font_size="16sp", bold=True, color=WHITE))
            kbox.add_widget(Label(text=lbl, font_size="10sp", color=(0.7, 0.8, 0.75, 1)))
            kpi_grid.add_widget(kbox)
        header.add_widget(kpi_grid)

        # Título de sección
        sec_title = Label(
            text="Pedidos asignados",
            font_size="13sp",
            bold=True,
            color=WHITE,
            size_hint_y=None,
            height=dp(22),
            halign='left',
            valign='middle',
        )
        sec_title.bind(size=sec_title.setter('text_size'))
        header.add_widget(sec_title)

        main_layout.add_widget(header)

        # Lista deslizable de pedidos
        scroll = ScrollView(size_hint_y=1)
        orders_layout = GridLayout(
            cols=1,
            spacing=dp(10),
            size_hint_y=None,
            padding=dp(16),
        )
        orders_layout.bind(minimum_height=orders_layout.setter('height'))

        with orders_layout.canvas.before:
            Color(*SLATE_BG)
            self.list_bg = Rectangle(size=orders_layout.size, pos=orders_layout.pos)
        orders_layout.bind(pos=self._update_list_bg, size=self._update_list_bg)

        if ORDERS:
            for order in ORDERS:
                card = OrderCard(order, self)
                orders_layout.add_widget(card)
        else:
            orders_layout.add_widget(
                Label(
                    text="¡No hay pedidos pendientes!",
                    font_size="14sp",
                    color=SLATE_TEXT,
                    size_hint_y=None,
                    height=dp(100),
                )
            )

        scroll.add_widget(orders_layout)
        main_layout.add_widget(scroll)

        # Barra de navegación inferior
        main_layout.add_widget(BottomNavBar(active_item="pedidos"))
        self.add_widget(main_layout)

    def _update_header_bg(self, instance, value):
        self.header_bg.pos = instance.pos
        self.header_bg.size = instance.size

    def _update_list_bg(self, instance, value):
        self.list_bg.pos = instance.pos
        self.list_bg.size = instance.size


class OrderCard(ButtonBehavior, RoundedBox):
    def __init__(self, order, dashboard, **kwargs):
        super().__init__(
            bg_color=WHITE,
            border_color=LINE,
            radius=[dp(14)],
            size_hint_y=None,
            height=dp(76),
            padding=[dp(14), dp(10), dp(14), dp(10)],
            **kwargs
        )
        self.order = order
        self.dashboard = dashboard

        left_info = BoxLayout(orientation='vertical', size_hint_x=0.68, spacing=dp(3))
        lbl_id = Label(
            text=f"{order['id']} · {order['client']}",
            font_size="13sp",
            bold=True,
            color=CHARCOAL,
            halign='left',
            valign='middle',
        )
        lbl_id.bind(size=lbl_id.setter('text_size'))

        lbl_sub = Label(
            text=f"{order['items']} productos · {order['time']}",
            font_size="11sp",
            color=SLATE_TEXT,
            halign='left',
            valign='middle',
        )
        lbl_sub.bind(size=lbl_sub.setter('text_size'))

        left_info.add_widget(lbl_id)
        left_info.add_widget(lbl_sub)
        self.add_widget(left_info)

        right_box = BoxLayout(size_hint_x=0.32)
        if order.get('priority') == "Urgente":
            badge = PillBadge(text="Urgente", bg_color=CORAL_BG, text_color=CORAL)
        else:
            badge = PillBadge(text="Normal", bg_color=MINT, text_color=FOREST)
        right_box.add_widget(badge)
        self.add_widget(right_box)

    def on_release(self):
        self.dashboard.manager.transition = SlideTransition(direction='left')
        app = App.get_running_app()
        app.current_order = self.order
        self.dashboard.manager.current = "checklist"