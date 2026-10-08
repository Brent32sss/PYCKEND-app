# screens/history_screen.py

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle
from data.sample_data import COMPLETED_ORDERS

from config.colors import FOREST_DARK, WHITE, SLATE_BG, CHARCOAL, SLATE_TEXT, LEAF, MINT, LINE
from widgets.custom_widgets import RoundedBox, PillBadge, BottomNavBar

class HistoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "historial"

    def on_pre_enter(self):
        self.clear_widgets()
        main_layout = BoxLayout(orientation='vertical', spacing=0)

        header = BoxLayout(orientation='vertical', size_hint_y=None, height=100, padding=[20, 15, 20, 15], spacing=6)
        with header.canvas.before:
            Color(*FOREST_DARK)
            self.header_bg = Rectangle(size=header.size, pos=header.pos)
        header.bind(pos=self._update_header_bg, size=self._update_header_bg)

        lbl_title = Label(text="Historial de recolección", font_size="18sp", bold=True, color=WHITE, halign='left', valign='middle')
        lbl_title.bind(size=lbl_title.setter('text_size'))
        header.add_widget(lbl_title)

        lbl_sub = Label(text="Pedidos completados hoy", font_size="11sp", color=(0.7, 0.8, 0.75, 1), halign='left', valign='middle')
        lbl_sub.bind(size=lbl_sub.setter('text_size'))
        header.add_widget(lbl_sub)

        main_layout.add_widget(header)

        scroll = ScrollView(size_hint_y=1)
        list_layout = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=16)
        list_layout.bind(minimum_height=list_layout.setter('height'))

        with list_layout.canvas.before:
            Color(*SLATE_BG)
            self.list_bg = Rectangle(size=list_layout.size, pos=list_layout.pos)
        list_layout.bind(pos=self._update_list_bg, size=self._update_list_bg)

        # Aquí cargamos los datos dinámicamente
        for item in COMPLETED_ORDERS:
            card = RoundedBox(bg_color=WHITE, border_color=LINE, radius=[14], size_hint_y=None, height=78, padding=[14, 12, 14, 12])
            left_info = BoxLayout(orientation='vertical', size_hint_x=0.65, spacing=3)

            lbl_id = Label(text=f"{item['id']} · {item['client']}", font_size="13sp", bold=True, color=CHARCOAL, halign='left', valign='middle')
            lbl_id.bind(size=lbl_id.setter('text_size'))

            lbl_sub_info = Label(text=f"{item['items']} · Tiempo: {item['duration']}", font_size="11sp", color=SLATE_TEXT, halign='left', valign='middle')
            lbl_sub_info.bind(size=lbl_sub_info.setter('text_size'))

            left_info.add_widget(lbl_id)
            left_info.add_widget(lbl_sub_info)
            card.add_widget(left_info)

            right_box = BoxLayout(orientation='vertical', size_hint_x=0.35, spacing=2)
            badge = PillBadge(text="Completado", bg_color=MINT, text_color=LEAF)
            lbl_time = Label(text=item['time'], font_size="10sp", color=SLATE_TEXT, halign='right', valign='middle')
            lbl_time.bind(size=lbl_time.setter('text_size'))

            right_box.add_widget(badge)
            right_box.add_widget(lbl_time)
            card.add_widget(right_box)

            list_layout.add_widget(card)

        scroll.add_widget(list_layout)
        main_layout.add_widget(scroll)

        main_layout.add_widget(BottomNavBar(active_item="historial"))
        self.add_widget(main_layout)

    def _update_header_bg(self, instance, value):
        self.header_bg.pos = instance.pos
        self.header_bg.size = instance.size

    def _update_list_bg(self, instance, value):
        self.list_bg.pos = instance.pos
        self.list_bg.size = instance.size