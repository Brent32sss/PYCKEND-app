import json
from kivy.app import App
from kivy.core.text import Label as CoreLabel
from kivy.graphics import Color, Line, Rectangle, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from config.colors import (
    CHARCOAL,
    FOREST,
    LEAF,
    LINE,
    MANGO,
    SLATE_BG,
    SLATE_TEXT,
    WHITE,
)
from widgets.custom_widgets import RoundedBox, RoundedButton

try:
    from data.sample_data import STORE_INVENTORY, STORE_MAP
except ImportError:
    STORE_MAP = {
        "ENT": {"name": "Entrada / Salida", "cat": "Acceso"},
        "CAJ": {"name": "Cajas", "cat": "Punto de venta"},
        "REF": {"name": "Refrigeradores", "cat": "Lácteos y bebidas frías"},
        "G1": {"name": "Góndola 1", "cat": "Abarrotes secos"},
        "G2": {"name": "Góndola 2", "cat": "Snacks y galletas"},
        "G3": {"name": "Góndola 3", "cat": "Limpieza y cuidado"},
        "PAN": {"name": "Panes y frutas", "cat": "Perecibles"},
        "BOD": {"name": "Bodega (almacén)", "cat": "Stock de reposición"},
        "REC": {"name": "Recepción", "cat": "Ingreso de mercadería"},
    }
    STORE_INVENTORY = [
        {"name": "Leche 1L", "sku": "LAC-001", "location": "REF · Estante 1, nivel A", "zone": "REF", "stock": 36}
    ]


class MapCanvasView(Widget):
    """Lienzo que dibuja el plano del minimarket, resalta zonas y traza rutas."""

    def __init__(self, on_zone_select=None, **kwargs):
        super().__init__(**kwargs)
        self.on_zone_select = on_zone_select
        self.target_zone = None
        self.zone_rects = {}
        self.bind(pos=self.draw_map, size=self.draw_map)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            for z_key, (zx, zy, zw, zh) in self.zone_rects.items():
                if zx <= touch.x <= zx + zw and zy <= touch.y <= zy + zh:
                    if self.on_zone_select:
                        self.on_zone_select(z_key)
                    return True
        return super().on_touch_down(touch)

    def get_route_points(self, target_zone, base_x, base_y, w_total, h_total):
        def px(p):
            return base_x + (p / 100.0) * w_total

        def py(p):
            return base_y + (p / 100.0) * h_total

        start_x = px(14)
        start_y = py(23)

        if target_zone == "REF":
            return [start_x, start_y, start_x, py(84), px(53), py(84), px(53), py(88)]
        elif target_zone == "G1":
            return [start_x, start_y, start_x, py(75), px(28), py(75)]
        elif target_zone == "G2":
            return [start_x, start_y, start_x, py(59), px(28), py(59)]
        elif target_zone == "G3":
            return [start_x, start_y, start_x, py(43), px(28), py(43)]
        elif target_zone == "PAN":
            return [start_x, start_y, start_x, py(26), px(28), py(26)]
        elif target_zone in ["BOD", "REC"]:
            dest_y = 35 if target_zone == "BOD" else 21
            return [start_x, start_y, start_x, py(12), px(82), py(12), px(82), py(dest_y)]
        elif target_zone == "CAJ":
            return [start_x, start_y, px(12), py(23)]
        elif target_zone == "ENT":
            return [start_x, start_y, px(12), py(5)]
        return []

    def draw_map(self, *args):
        self.canvas.clear()
        self.zone_rects.clear()

        with self.canvas:
            Color(0.14, 0.15, 0.17, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[8])

            Color(0.24, 0.26, 0.28, 1)
            Line(rounded_rectangle=[self.x, self.y, self.width, self.height, 8], width=1)

            base_x = self.x + 12
            base_y = self.y + 12
            w_total = self.width - 24
            h_total = self.height - 24

            col_acc = (0.75, 0.88, 0.85, 1)
            col_caja = (0.98, 0.84, 0.72, 1)
            col_frio = (0.69, 0.82, 0.94, 1)
            col_g1 = (0.75, 0.88, 0.75, 1)
            col_g2 = (0.98, 0.94, 0.67, 1)
            col_g3 = (0.94, 0.74, 0.80, 1)
            col_pan = (0.83, 0.78, 0.75, 1)
            col_bod = (0.85, 0.74, 0.88, 1)

            def draw_zone(px_rel, py_rel, pw_rel, ph_rel, color, text_label="", zone_key=None):
                zx = base_x + (px_rel / 100.0) * w_total
                zy = base_y + (py_rel / 100.0) * h_total
                zw = (pw_rel / 100.0) * w_total
                zh = (ph_rel / 100.0) * h_total

                if zone_key:
                    self.zone_rects[zone_key] = (zx, zy, zw, zh)

                Color(*color)
                RoundedRectangle(pos=(zx, zy), size=(zw, zh), radius=[5])

                if zone_key and self.target_zone == zone_key:
                    Color(0.95, 0.25, 0.25, 1)
                    Line(rounded_rectangle=[zx - 2, zy - 2, zw + 4, zh + 4, 6], width=2.4)

                if text_label:
                    lbl = CoreLabel(text=text_label, font_size=10, color=(0.15, 0.18, 0.16, 1), bold=True, halign="center")
                    if "\n" in text_label:
                        lbl.text_size = (zw, None)
                    lbl.refresh()
                    tex = lbl.texture
                    Color(1, 1, 1, 1)
                    Rectangle(pos=(zx + (zw - tex.size[0]) / 2, zy + (zh - tex.size[1]) / 2), size=tex.size, texture=tex)

            draw_zone(0, 0, 25, 10, col_acc, "Entrada /\nSalida", "ENT")
            draw_zone(0, 13, 25, 20, col_caja, "Cajas", "CAJ")
            draw_zone(28, 88, 50, 12, col_frio, "Refrigeradores", "REF")
            draw_zone(28, 70, 50, 10, col_g1, "Góndola 1", "G1")
            draw_zone(28, 54, 50, 10, col_g2, "Góndola 2", "G2")
            draw_zone(28, 38, 50, 10, col_g3, "Góndola 3", "G3")
            draw_zone(28, 20, 50, 12, col_pan, "Panes y frutas", "PAN")
            draw_zone(82, 30, 18, 70, col_bod, "Bodega\n(almacén)", "BOD")
            draw_zone(82, 15, 18, 12, col_acc, "Recepción", "REC")

            if self.target_zone:
                pts = self.get_route_points(self.target_zone, base_x, base_y, w_total, h_total)
                if pts:
                    Color(0.95, 0.25, 0.25, 1)
                    Line(points=pts, width=2.4, dash_length=8, dash_offset=4)


class MapScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "mapa"
        self.next_prod = None
        self.stop_index = 0

    def on_pre_enter(self):
        self.clear_widgets()

        app = App.get_running_app()
        order = app.current_order if hasattr(app, "current_order") and app.current_order else None

        self.next_prod = None
        self.stop_index = 0
        if order and "products" in order:
            for i, p in enumerate(order["products"]):
                if not p.get("done", False):
                    self.next_prod = p
                    self.stop_index = i + 1
                    break

        main_layout = BoxLayout(orientation="vertical", spacing=0)

        # 1. Header con botón volver (<)
        header = BoxLayout(orientation="vertical", size_hint_y=None, height=68, padding=[16, 10, 16, 8], spacing=2)
        with header.canvas.before:
            Color(*WHITE)
            Rectangle(size=header.size, pos=header.pos)
            Color(*LINE)
            Line(points=[0, 0, header.width, 0], width=1)

        title_row = BoxLayout(size_hint_y=None, height=26, spacing=6)
        btn_back = Button(
            text="<",
            font_size="22sp",
            bold=True,
            color=CHARCOAL,
            size_hint_x=None,
            width=28,
            background_color=(0, 0, 0, 0),
            background_normal="",
        )
        btn_back.bind(on_release=self.go_back)
        title_row.add_widget(btn_back)

        lbl_mtitle = Label(
            text="Minimarket pequeño",
            font_size="15sp",
            bold=True,
            color=CHARCOAL,
            halign="left",
            valign="middle",
        )
        lbl_mtitle.bind(size=lbl_mtitle.setter("text_size"))
        title_row.add_widget(lbl_mtitle)
        header.add_widget(title_row)

        lbl_sub = Label(
            text="Toca una zona o busca un producto para ver la ruta señalizada.",
            font_size="11sp",
            color=SLATE_TEXT,
            size_hint_y=None,
            height=16,
            halign="left",
            valign="middle",
        )
        lbl_sub.bind(size=lbl_sub.setter("text_size"))
        header.add_widget(lbl_sub)
        main_layout.add_widget(header)

        # 2. Barra de Búsqueda
        search_wrap = BoxLayout(size_hint_y=None, height=50, padding=[16, 6, 16, 4], spacing=6)
        with search_wrap.canvas.before:
            Color(*SLATE_BG)
            Rectangle(size=search_wrap.size, pos=search_wrap.pos)

        self.search_input = TextInput(
            hint_text="Buscar producto (ej. Leche)...",
            multiline=False,
            background_color=WHITE,
            foreground_color=CHARCOAL,
            cursor_color=CHARCOAL,
            padding=[10, 8, 10, 8],
        )
        self.search_input.bind(text=self.on_search_change)
        search_wrap.add_widget(self.search_input)

        btn_clear = Button(
            text="✕",
            size_hint=(None, 1),
            width=38,
            background_color=(0.85, 0.88, 0.90, 1),
            color=CHARCOAL,
            bold=True,
        )
        btn_clear.bind(on_release=self.clear_search)
        search_wrap.add_widget(btn_clear)
        main_layout.add_widget(search_wrap)

        # 3. Vista del Mapa Interactivo
        map_container = BoxLayout(padding=[16, 4, 16, 4], size_hint_y=0.55)
        with map_container.canvas.before:
            Color(*SLATE_BG)
            Rectangle(size=map_container.size, pos=map_container.pos)

        self.map_view = MapCanvasView(on_zone_select=self.on_zone_selected)
        map_container.add_widget(self.map_view)
        main_layout.add_widget(map_container)

        # 4. Panel Inferior Limpio (Tarjeta + Botón)
        self.bottom_panel = BoxLayout(
            orientation="vertical",
            padding=[16, 8, 16, 16],
            spacing=8,
            size_hint_y=0.45,
        )
        with self.bottom_panel.canvas.before:
            Color(*SLATE_BG)
            Rectangle(size=self.bottom_panel.size, pos=self.bottom_panel.pos)

        self.result_card = RoundedBox(
            orientation="vertical",
            bg_color=(0.14, 0.15, 0.17, 1),
            radius=[10],
            padding=[12, 10, 12, 10],
            spacing=6,
            size_hint_y=None,
            height=110,
        )

        self.lbl_result_count = Label(
            text="1 resultado(s)",
            font_size="13sp",
            bold=True,
            color=WHITE,
            size_hint_y=None,
            height=18,
            halign="left",
        )
        self.lbl_result_count.bind(size=self.lbl_result_count.setter("text_size"))
        self.result_card.add_widget(self.lbl_result_count)

        grid_details = GridLayout(cols=3, size_hint_y=1, spacing=6)

        # Producto
        col_p = BoxLayout(orientation="vertical", spacing=2)
        col_p.add_widget(Label(text="Producto", font_size="10sp", bold=True, color=(0.65, 0.68, 0.72, 1), size_hint_y=None, height=14))
        self.lbl_p_name = Label(text="Leche 1L", font_size="13sp", bold=True, color=WHITE, size_hint_y=None, height=18)
        self.lbl_p_sku = Label(text="LAC-001", font_size="10sp", color=(0.7, 0.75, 0.8, 1), size_hint_y=None, height=14)
        col_p.add_widget(self.lbl_p_name)
        col_p.add_widget(self.lbl_p_sku)
        grid_details.add_widget(col_p)

        # Zona
        col_z = BoxLayout(orientation="vertical", spacing=2)
        col_z.add_widget(Label(text="Zona", font_size="10sp", bold=True, color=(0.65, 0.68, 0.72, 1), size_hint_y=None, height=14))
        self.lbl_z_name = Label(text="Refrigeradores", font_size="13sp", bold=True, color=WHITE, size_hint_y=None, height=18)
        self.lbl_z_sub = Label(text="REF · Estante 1, nivel A", font_size="10sp", color=(0.7, 0.75, 0.8, 1), size_hint_y=None, height=14)
        col_z.add_widget(self.lbl_z_name)
        col_z.add_widget(self.lbl_z_sub)
        grid_details.add_widget(col_z)

        # Stock
        col_s = BoxLayout(orientation="vertical", spacing=2)
        col_s.add_widget(Label(text="Stock", font_size="10sp", bold=True, color=(0.65, 0.68, 0.72, 1), size_hint_y=None, height=14))
        self.lbl_s_qty = Label(text="36", font_size="17sp", bold=True, color=WHITE, size_hint_y=None, height=22)
        col_s.add_widget(self.lbl_s_qty)
        grid_details.add_widget(col_s)

        self.result_card.add_widget(grid_details)
        self.bottom_panel.add_widget(self.result_card)

        # Botón de Acción de Picking
        self.action_box = BoxLayout(size_hint_y=None, height=50)
        if self.next_prod:
            self.btn_collect = RoundedButton(
                text=f"Marcar como recolectado (Parada {self.stop_index})",
                size_hint_y=1,
                bg_color=MANGO,
                radius=[12],
            )
            self.btn_collect.bind(on_release=lambda x: self.mark_collected(x, self.next_prod))
            self.action_box.add_widget(self.btn_collect)
        else:
            self.btn_finish = RoundedButton(
                text="¡Pedido Completado! Volver",
                size_hint_y=1,
                bg_color=LEAF,
                radius=[12],
            )
            self.btn_finish.bind(on_release=self.go_back)
            self.action_box.add_widget(self.btn_finish)

        self.bottom_panel.add_widget(self.action_box)
        main_layout.add_widget(self.bottom_panel)

        self.add_widget(main_layout)

        initial_name = self.next_prod["name"] if self.next_prod else "Leche 1L"
        self.search_input.text = initial_name

    def on_search_change(self, instance, value):
        query = value.strip().lower()
        if not query:
            if self.next_prod:
                self.show_product(self.next_prod)
            else:
                self.map_view.target_zone = None
                self.map_view.draw_map()
                self.lbl_result_count.text = "0 resultado(s)"
            return

        match = next(
            (p for p in STORE_INVENTORY if query in p["name"].lower() or query in p["sku"].lower()),
            None,
        )

        if match:
            self.show_product(match)
        else:
            self.map_view.target_zone = None
            self.map_view.draw_map()
            self.lbl_result_count.text = "0 resultado(s)"
            self.lbl_p_name.text = "No encontrado"
            self.lbl_p_sku.text = "-"
            self.lbl_z_name.text = "-"
            self.lbl_z_sub.text = "Sin ubicación"
            self.lbl_s_qty.text = "0"

    def show_product(self, prod):
        zone_code = prod.get("zone", "REF")
        zone_info = STORE_MAP.get(zone_code, {"name": zone_code, "cat": ""})

        self.map_view.target_zone = zone_code
        self.map_view.draw_map()

        self.lbl_result_count.text = "1 resultado(s)"
        self.lbl_p_name.text = prod.get("name", "")
        self.lbl_p_sku.text = prod.get("sku", "")
        self.lbl_z_name.text = zone_info.get("name", zone_code)
        self.lbl_z_sub.text = prod.get("location", f"{zone_code} · {zone_info.get('cat', '')}")
        self.lbl_s_qty.text = str(prod.get("stock", 0))

    def on_zone_selected(self, zone_code):
        prod = next((p for p in STORE_INVENTORY if p.get("zone") == zone_code), None)
        if prod:
            self.search_input.text = prod["name"]
        else:
            zone_info = STORE_MAP.get(zone_code, {"name": zone_code, "cat": ""})
            self.map_view.target_zone = zone_code
            self.map_view.draw_map()
            self.lbl_result_count.text = f"Zona: {zone_code}"
            self.lbl_p_name.text = zone_info.get("name", zone_code)
            self.lbl_p_sku.text = zone_info.get("cat", "")
            self.lbl_z_name.text = zone_info.get("name", zone_code)
            self.lbl_z_sub.text = zone_code
            self.lbl_s_qty.text = "-"

    def clear_search(self, instance):
        self.search_input.text = ""

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "checklist"

    def mark_collected(self, instance, product):
        product["done"] = True

        content = BoxLayout(orientation="vertical", padding=20, spacing=14)
        content.add_widget(Label(text="Parada completada", font_size="16sp", bold=True, color=LEAF))
        content.add_widget(Label(text=f"{product['name']} marcado como recolectado.", font_size="12sp", color=SLATE_TEXT))

        btn = RoundedButton(text="Continuar ruta", size_hint_y=None, height=44, bg_color=FOREST, radius=[12])
        content.add_widget(btn)

        popup = Popup(title="Confirmación", content=content, size_hint=(0.85, 0.35))

        def on_close(x):
            popup.dismiss()
            self.on_pre_enter()

        btn.bind(on_release=on_close)
        popup.open()