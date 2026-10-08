from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle, Line, RoundedRectangle
from kivy.clock import Clock
from kivy.animation import Animation

from config.colors import (
    WHITE, LINE, CHARCOAL, SLATE_TEXT, LEAF, MINT, FOREST, SLATE_BG, MANGO
)
from widgets.custom_widgets import PillBadge, RoundedBox, CustomCheckBox, RoundedButton
from data.sample_data import ORDERS, complete_order

# === SIMULADOR DE CÁMARA (LÁSER) ===
class ScannerPopup(Popup):
    def __init__(self, product_name, on_success, **kwargs):
        super().__init__(**kwargs)
        self.title = f"Escaneando SKU: {product_name}..."
        self.title_color = WHITE
        self.title_size = "13sp"
        self.size_hint = (0.85, 0.4)
        self.auto_dismiss = False
        self.background_color = (0, 0, 0, 0.8)
        self.separator_color = MANGO
        self.on_success = on_success

        self.layout = FloatLayout()
        
        with self.layout.canvas.before:
            Color(0.15, 0.15, 0.15, 1)
            self.bg = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(pos=self._update_rect, size=self._update_rect)

        self.laser = Widget(size_hint=(0.9, None), height=2, pos_hint={'center_x': 0.5, 'y': 0.9})
        with self.laser.canvas:
            Color(1, 0.2, 0.2, 0.9)
            self.laser_rect = Rectangle(size=self.laser.size, pos=self.laser.pos)
        self.laser.bind(pos=self._update_laser, size=self._update_laser)
        
        self.layout.add_widget(self.laser)
        self.content = self.layout

    def _update_rect(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size

    def _update_laser(self, instance, value):
        self.laser_rect.pos = instance.pos
        self.laser_rect.size = instance.size

    def on_open(self):
        anim = Animation(pos_hint={'y': 0.1}, duration=0.6) + Animation(pos_hint={'y': 0.9}, duration=0.6)
        anim.repeat = True
        anim.start(self.laser)
        Clock.schedule_once(self.finish_scan, 1.5)

    def finish_scan(self, dt):
        Animation.cancel_all(self.laser)
        self.dismiss()
        if self.on_success:
            self.on_success()


# === PANTALLA CHECKLIST ===
class ChecklistScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "checklist"

    def on_pre_enter(self):
        self.clear_widgets()
        app = App.get_running_app()
        order = app.current_order if hasattr(app, 'current_order') and app.current_order else (ORDERS[0] if ORDERS else None)

        if not order:
            self.go_back(None)
            return

        main_layout = BoxLayout(orientation='vertical', spacing=0)

        header = BoxLayout(orientation='vertical', size_hint_y=None, height=135, padding=[20, 14, 20, 14], spacing=6)
        with header.canvas.before:
            Color(*WHITE)
            Rectangle(size=header.size, pos=header.pos)
            Color(*LINE)
            Line(points=[0, 0, header.width, 0], width=1)

        top_bar = BoxLayout(size_hint_y=None, height=24, spacing=8)
        btn_back = Button(text="<", font_size="22sp", bold=True, color=CHARCOAL, size_hint_x=None, width=24, background_color=(0,0,0,0), background_normal='')
        btn_back.bind(on_release=self.go_back)
        top_bar.add_widget(btn_back)

        lbl_oid = Label(text=f"{order['id']} · {order['client']}", font_size="11sp", color=SLATE_TEXT, halign='left', valign='middle')
        lbl_oid.bind(size=lbl_oid.setter('text_size'))
        top_bar.add_widget(lbl_oid)
        header.add_widget(top_bar)

        lbl_title = Label(text="Lista de recolección", font_size="16sp", bold=True, color=CHARCOAL, size_hint_y=None, height=24, halign='left')
        lbl_title.bind(size=lbl_title.setter('text_size'))
        header.add_widget(lbl_title)

        total_items = len(order['products']) if order['products'] else order['items']
        completed_items = sum(1 for p in order['products'] if p.get('done')) if order['products'] else 0
        ratio = (completed_items / total_items) if total_items > 0 else 0

        p_track = Widget(size_hint_y=None, height=6)
        def draw_track(*args):
            p_track.canvas.clear()
            with p_track.canvas:
                Color(*LINE)
                RoundedRectangle(pos=p_track.pos, size=p_track.size, radius=[3])
                Color(*LEAF)
                RoundedRectangle(pos=p_track.pos, size=(p_track.width * ratio, p_track.height), radius=[3])
        p_track.bind(pos=draw_track, size=draw_track)
        header.add_widget(p_track)

        badge_box = BoxLayout(size_hint_y=None, height=26)
        time_badge = PillBadge(text=f"Tiempo: {order['time']} · {completed_items}/{total_items} recolectados", bg_color=MINT, text_color=FOREST)
        badge_box.add_widget(time_badge)
        header.add_widget(badge_box)

        main_layout.add_widget(header)

        scroll = ScrollView(size_hint_y=1)
        items_layout = GridLayout(cols=1, spacing=8, size_hint_y=None, padding=16)
        items_layout.bind(minimum_height=items_layout.setter('height'))

        with items_layout.canvas.before:
            Color(*SLATE_BG)
            self.items_bg = Rectangle(size=items_layout.size, pos=items_layout.pos)
        items_layout.bind(pos=lambda inst, val: setattr(self.items_bg, 'pos', val), size=lambda inst, val: setattr(self.items_bg, 'size', val))

        for i, product in enumerate(order['products']):
            card = ProductCard(product, i, self)
            items_layout.add_widget(card)

        scroll.add_widget(items_layout)
        main_layout.add_widget(scroll)

        footer = BoxLayout(size_hint_y=None, height=76, padding=[20, 12, 20, 12])
        if completed_items == total_items and total_items > 0:
            btn_finish = RoundedButton(text="Finalizar Recolección", size_hint_y=None, height=52, bg_color=LEAF, radius=[14])
            btn_finish.bind(on_release=lambda x: self.complete_and_go_back(order))
            footer.add_widget(btn_finish)
        else:
            btn_map = RoundedButton(text="Ver ruta en el mapa", size_hint_y=None, height=52, bg_color=FOREST, radius=[14])
            btn_map.bind(on_release=self.go_to_map)
            footer.add_widget(btn_map)
            
        main_layout.add_widget(footer)
        self.add_widget(main_layout)

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = "dashboard"

    def go_to_map(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = "mapa"

    # ¡CORRECCIÓN AQUÍ! Ahora está correctamente dentro de ChecklistScreen
    def complete_and_go_back(self, order_dict):
        complete_order(order_dict)
        
        popup_content = BoxLayout(orientation='vertical', padding=20)
        popup_content.add_widget(Label(text="¡Excelente trabajo!", font_size="18sp", bold=True, color=LEAF))
        popup = Popup(title="Pedido Finalizado", content=popup_content, size_hint=(0.8, 0.3), auto_dismiss=True)
        popup.open()
        
        Clock.schedule_once(lambda dt: popup.dismiss(), 1.5)
        Clock.schedule_once(lambda dt: self.go_back(None), 1.6)


# === TARJETA DE PRODUCTO ===
class ProductCard(RoundedBox):
    def __init__(self, product, idx, checklist, **kwargs):
        super().__init__(bg_color=WHITE, border_color=LINE, radius=[14], size_hint_y=None, height=80, padding=[12, 10, 12, 10], spacing=10, **kwargs)
        self.product = product
        self.checklist = checklist

        self.chk = CustomCheckBox(active=product['done'])
        self.chk.bind(active=self.on_toggle)
        self.add_widget(self.chk)

        info_box = BoxLayout(orientation='vertical', size_hint_x=0.55, spacing=3)
        lbl_pname = Label(text=product['name'], font_size="13sp", bold=True, color=CHARCOAL, halign='left', valign='middle')
        lbl_pname.bind(size=lbl_pname.setter('text_size'))

        loc_badge = PillBadge(text=product['location'], bg_color=MINT, text_color=FOREST, font_size="9sp")
        info_box.add_widget(lbl_pname)
        info_box.add_widget(loc_badge)
        self.add_widget(info_box)

        action_box = BoxLayout(orientation='vertical', size_hint_x=0.35, spacing=4)
        lbl_qty = Label(text=product['qty'], font_size="12sp", bold=True, color=SLATE_TEXT, halign='right', valign='middle')
        lbl_qty.bind(size=lbl_qty.setter('text_size'))
        action_box.add_widget(lbl_qty)

        if not product['done']:
            btn_scan = RoundedButton(text="Escanear", font_size="10sp", bg_color=MANGO, radius=[8], size_hint_y=None, height=28)
            btn_scan.bind(on_release=self.open_scanner)
            action_box.add_widget(btn_scan)
        else:
            action_box.add_widget(Widget(size_hint_y=None, height=28))

        self.add_widget(action_box)

        if product['done']:
            self.opacity = 0.55

    def open_scanner(self, instance):
        popup = ScannerPopup(product_name=self.product['name'], on_success=self.mark_as_done)
        popup.open()

    def mark_as_done(self):
        self.chk.active = True 

    def on_toggle(self, instance, val):
        self.product['done'] = val
        self.opacity = 0.55 if val else 1.0
        self.checklist.on_pre_enter()