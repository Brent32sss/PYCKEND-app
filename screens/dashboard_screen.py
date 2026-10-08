from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

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

    # Se usa on_pre_enter en lugar de __init__ para que se recargue al volver de la Checklist
    def on_pre_enter(self):
        self.clear_widgets()

        main_layout = BoxLayout(orientation='vertical', spacing=0)

        header = BoxLayout(orientation='vertical', size_hint_y=None, height=215, padding=[20, 15, 20, 15], spacing=10)
        with header.canvas.before:
            Color(*FOREST_DARK)
            self.header_bg = Rectangle(size=header.size, pos=header.pos)
        header.bind(pos=self._update_header_bg, size=self._update_header_bg)

        top_row = BoxLayout(size_hint_y=None, height=24)
        lbl_shift = Label(text="Turno tarde", font_size="11sp", color=(0.7, 0.8, 0.75, 1), size_hint_x=0.7, halign='left')
        lbl_shift.bind(size=lbl_shift.setter('text_size'))
        lbl_notif = Label(text="Avisos: 2", font_size="11sp", color=(0.7, 0.8, 0.75, 1), size_hint_x=0.3, halign='right')
        lbl_notif.bind(size=lbl_notif.setter('text_size'))
        top_row.add_widget(lbl_shift)
        top_row.add_widget(lbl_notif)
        header.add_widget(top_row)

        user_row = BoxLayout(size_hint_y=None, height=48, spacing=12)
        orange_badge = RoundedBox(size_hint=(None, None), size=(42, 42), bg_color=MANGO, radius=[12])

        avatar_box = BoxLayout(size_hint=(None, None), size=(42, 42))
        avatar_box.add_widget(Widget(size_hint_x=1))
        avatar_box.add_widget(UserAvatarWidget(color=WHITE))
        avatar_box.add_widget(Widget(size_hint_x=1))
        orange_badge.add_widget(avatar_box)

        user_row.add_widget(orange_badge)

        u_info = BoxLayout(orientation='vertical')
        lbl_uname = Label(text=PICKER_DATA["name"], font_size="15sp", bold=True, color=WHITE, halign='left', valign='middle')
        lbl_uname.bind(size=lbl_uname.setter('text_size'))
        lbl_urole = Label(text=PICKER_DATA["role"], font_size="11sp", color=(0.7, 0.8, 0.75, 1), halign='left', valign='middle')
        lbl_urole.bind(size=lbl_urole.setter('text_size'))
        u_info.add_widget(lbl_uname)
        u_info.add_widget(lbl_urole)
        user_row.add_widget(u_info)
        header.add_widget(user_row)

        # Cálculo dinámico para que los números cambien si completas un pedido
        asignados_val = str(len(ORDERS))
        urgentes_val = str(sum(1 for o in ORDERS if o.get('priority') == "Urgente"))

        kpi_grid = GridLayout(cols=3, size_hint_y=None, height=54, spacing=8)
        for val, lbl in [(asignados_val, "Asignados"), (urgentes_val, "Urgentes"), ("92%", "A tiempo")]:
            kbox = RoundedBox(orientation='vertical', bg_color=[0.12, 0.32, 0.24, 1], radius=[12], padding=[6, 4, 6, 4])
            kbox.add_widget(Label(text=val, font_size="15sp", bold=True, color=WHITE))
            kbox.add_widget(Label(text=lbl, font_size="9sp", color=(0.7, 0.8, 0.75, 1)))
            kpi_grid.add_widget(kbox)
        header.add_widget(kpi_grid)

        sec_title = Label(text="Pedidos asignados", font_size="13sp", bold=True, color=WHITE, size_hint_y=None, height=22, halign='left')
        sec_title.bind(size=sec_title.setter('text_size'))
        header.add_widget(sec_title)

        main_layout.add_widget(header)

        scroll = ScrollView(size_hint_y=1)
        orders_layout = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=16)
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
            orders_layout.add_widget(Label(text="¡No hay pedidos pendientes!", font_size="14sp", color=SLATE_TEXT, size_hint_y=None, height=100))

        scroll.add_widget(orders_layout)
        main_layout.add_widget(scroll)

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
        super().__init__(bg_color=WHITE, border_color=LINE, radius=[16], size_hint_y=None, height=84, padding=[14, 12, 14, 12], **kwargs)
        self.order = order
        self.dashboard = dashboard

        left_info = BoxLayout(orientation='vertical', size_hint_x=0.65, spacing=4)
        lbl_id = Label(text=f"{order['id']} · {order['client']}", font_size="13sp", bold=True, color=CHARCOAL, halign='left', valign='middle')
        lbl_id.bind(size=lbl_id.setter('text_size'))

        lbl_sub = Label(text=f"{order['items']} productos · {order['time']}", font_size="11sp", color=SLATE_TEXT, halign='left', valign='middle')
        lbl_sub.bind(size=lbl_sub.setter('text_size'))

        left_info.add_widget(lbl_id)
        left_info.add_widget(lbl_sub)
        self.add_widget(left_info)

        right_box = BoxLayout(size_hint_x=0.35)
        if order['priority'] == "Urgente":
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