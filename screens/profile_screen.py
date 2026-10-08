from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from widgets.custom_widgets import RoundedBox, RoundedButton, BottomNavBar, UserAvatarWidget

from config.colors import (
    FOREST_DARK, MANGO, WHITE, SLATE_BG, CHARCOAL, SLATE_TEXT, LINE, CORAL, CORAL_BG
)
from data.sample_data import PICKER_DATA

class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "perfil"

        main_layout = BoxLayout(orientation='vertical', spacing=0)

        header = BoxLayout(orientation='vertical', size_hint_y=None, height=130, padding=[20, 15, 20, 15], spacing=10)
        with header.canvas.before:
            Color(*FOREST_DARK)
            self.header_bg = Rectangle(size=header.size, pos=header.pos)
        header.bind(pos=self._update_header_bg, size=self._update_header_bg)

        lbl_title = Label(text="Perfil del Picker", font_size="18sp", bold=True, color=WHITE, halign='left', valign='middle')
        lbl_title.bind(size=lbl_title.setter('text_size'))
        header.add_widget(lbl_title)

        user_row = BoxLayout(size_hint_y=None, height=48, spacing=12)
        orange_badge = RoundedBox(size_hint=(None, None), size=(42, 42), bg_color=MANGO, radius=[12])
        
        # --- AQUÍ ESTÁ EL FIX DEL ÍCONO DE PERFIL VECTORIAL ---
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

        main_layout.add_widget(header)

        scroll = ScrollView(size_hint_y=1)
        content = GridLayout(cols=1, spacing=14, size_hint_y=None, padding=16)
        content.bind(minimum_height=content.setter('height'))

        with content.canvas.before:
            Color(*SLATE_BG)
            self.content_bg = Rectangle(size=content.size, pos=content.pos)
        content.bind(pos=self._update_content_bg, size=self._update_content_bg)

        stats_card = RoundedBox(orientation='vertical', bg_color=WHITE, border_color=LINE, radius=[14], padding=[16, 14, 16, 14], spacing=10, size_hint_y=None, height=120)
        lbl_mtitle = Label(text="Métricas de Hoy", font_size="13sp", bold=True, color=CHARCOAL, size_hint_y=None, height=20, halign='left')
        lbl_mtitle.bind(size=lbl_mtitle.setter('text_size'))
        stats_card.add_widget(lbl_mtitle)

        stats_grid = GridLayout(cols=3, spacing=8)
        for val, lbl in [("12", "Recolectados"), ("14 min", "Prom. pedido"), ("95%", "Eficiencia")]:
            sb = BoxLayout(orientation='vertical')
            sb.add_widget(Label(text=val, font_size="14sp", bold=True, color=CHARCOAL))
            sb.add_widget(Label(text=lbl, font_size="9sp", color=SLATE_TEXT))
            stats_grid.add_widget(sb)
        stats_card.add_widget(stats_grid)
        content.add_widget(stats_card)

        info_card = RoundedBox(orientation='vertical', bg_color=WHITE, border_color=LINE, radius=[14], padding=[16, 14, 16, 14], spacing=12, size_hint_y=None, height=140)
        details = [
            ("Turno actual", PICKER_DATA["shift"]),
            ("ID de empleado", "#EMP-9021"),
            ("Versión de la app", "v1.2.0 Demo"),
        ]
        for label, val in details:
            row = BoxLayout(size_hint_y=None, height=22)
            lbl_l = Label(text=label, font_size="11sp", color=SLATE_TEXT, halign='left', valign='middle')
            lbl_l.bind(size=lbl_l.setter('text_size'))
            lbl_v = Label(text=val, font_size="11sp", bold=True, color=CHARCOAL, halign='right', valign='middle')
            lbl_v.bind(size=lbl_v.setter('text_size'))
            row.add_widget(lbl_l)
            row.add_widget(lbl_v)
            info_card.add_widget(row)
        content.add_widget(info_card)

        btn_logout = RoundedButton(text="Cerrar sesión", size_hint_y=None, height=48, bg_color=CORAL_BG, text_color=CORAL, radius=[12])
        btn_logout.bind(on_release=self.do_logout)
        content.add_widget(btn_logout)

        scroll.add_widget(content)
        main_layout.add_widget(scroll)

        main_layout.add_widget(BottomNavBar(active_item="perfil"))
        self.add_widget(main_layout)

    def _update_header_bg(self, instance, value):
        self.header_bg.pos = instance.pos
        self.header_bg.size = instance.size

    def _update_content_bg(self, instance, value):
        self.content_bg.pos = instance.pos
        self.content_bg.size = instance.size

    def do_logout(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = "login"