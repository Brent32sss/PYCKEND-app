import os
import sys
from kivy.app import App
from kivy.core.text import Label as CoreLabel
from kivy.graphics import Color, Ellipse, Line, Rectangle, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex

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

# Importación robusta del nuevo módulo de inventario
try:
    import inventario
except ImportError:
    try:
        from data import inventario
    except ImportError:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
        import inventario


class MapCanvasView(Widget):
    """
    Lienzo interactivo que dibuja el plano técnico del minimarket (12 pasillos,
    4 zonas operativas) adaptado del SVG (1000x620) y traza rutas de picking.
    """

    def __init__(self, on_shelf_select=None, on_zone_select=None, **kwargs):
        super().__init__(**kwargs)
        self.on_shelf_select = on_shelf_select
        self.on_zone_select = on_zone_select

        self.target_pasillo = None
        self.target_estante = None
        self.target_zone = None

        self.shelf_rects = {}  # (pasillo, estante) -> (x, y, w, h)
        self.zone_rects = {}   # zone_name -> (x, y, w, h)

        self.bind(pos=self.draw_map, size=self.draw_map)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # 1. Verificar toque en estantes
            for (p_code, e_code), (rx, ry, rw, rh) in self.shelf_rects.items():
                if rx <= touch.x <= rx + rw and ry <= touch.y <= ry + rh:
                    if self.on_shelf_select:
                        self.on_shelf_select(p_code, e_code)
                    return True

            # 2. Verificar toque en zonas operativas inferiores
            for z_name, (rx, ry, rw, rh) in self.zone_rects.items():
                if rx <= touch.x <= rx + rw and ry <= touch.y <= ry + rh:
                    if self.on_zone_select:
                        self.on_zone_select(z_name)
                    return True

        return super().on_touch_down(touch)

    def draw_map(self, *args):
        self.canvas.clear()
        self.shelf_rects.clear()
        self.zone_rects.clear()

        if self.width < dp(50) or self.height < dp(50):
            return

        # Dimensiones del plano original SVG
        vw = 1000.0
        vh = 620.0

        margin = dp(6)
        avail_w = max(10, self.width - margin * 2)
        avail_h = max(10, self.height - margin * 2)

        # Escala proporcional manteniendo aspecto (letterbox)
        scale = min(avail_w / vw, avail_h / vh)
        off_x = self.x + (self.width - vw * scale) / 2.0
        off_y = self.y + (self.height - vh * scale) / 2.0

        def to_kivy_pos(sx, sy, sw, sh):
            rx = off_x + sx * scale
            ry = off_y + (vh - (sy + sh)) * scale
            rw = sw * scale
            rh = sh * scale
            return rx, ry, rw, rh

        def draw_label(text, cx, cy, font_size_px, color_rgba=(0.12, 0.12, 0.12, 1), bold=True):
            lbl = CoreLabel(
                text=text,
                font_size=max(7, font_size_px),
                color=color_rgba,
                bold=bold,
                halign="center",
                valign="middle",
            )
            lbl.refresh()
            tex = lbl.texture
            if tex:
                Color(1, 1, 1, 1)
                Rectangle(
                    pos=(cx - tex.size[0] / 2.0, cy - tex.size[1] / 2.0),
                    size=tex.size,
                    texture=tex,
                )

        with self.canvas:
            # Fondo del plano (Dark Mode como en el prototipo web)
            Color(0.11, 0.11, 0.10, 1)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])

            Color(0.24, 0.24, 0.24, 1)
            Line(rounded_rectangle=[self.x, self.y, self.width, self.height, dp(8)], width=1)

            # Perímetro exterior del minimarket
            bx, by, bw, bh = to_kivy_pos(5, 5, 990, 610)
            Color(0.35, 0.35, 0.35, 0.6)
            Line(rounded_rectangle=[bx, by, bw, bh, max(2, 6 * scale)], width=max(1, 2 * scale))

            # Dibujar los 12 Pasillos y sus Estantes
            pasillos_info = inventario.obtener_resumen_pasillos()

            for p_data in pasillos_info:
                p_code = p_data["pasillo"]
                a_x = p_data["x"]
                max_est = p_data["max_estante"]
                col_rgba = get_color_from_hex(p_data["color"])

                # Encabezado del pasillo (ej. P01)
                is_aisle_target = (self.target_pasillo == p_code)
                hx = off_x + (a_x + 30) * scale
                hy = off_y + (vh - 38) * scale
                header_color = (1, 0.85, 0.3, 1) if is_aisle_target else (0.9, 0.9, 0.9, 1)
                draw_label(p_code, hx, hy, int(13 * scale), color_rgba=header_color, bold=True)

                # Módulos verticales (E01 a E04)
                for e in range(1, 5):
                    e_code = f"E0{e}"
                    sy = 60 + (e - 1) * 90
                    rx, ry, rw, rh = to_kivy_pos(a_x, sy, 60, 90)

                    self.shelf_rects[(p_code, e_code)] = (rx, ry, rw, rh)

                    is_shelf_target = (
                        self.target_pasillo == p_code
                        and (self.target_estante == e_code or self.target_estante is None)
                    )

                    if e <= max_est:
                        # Estante activo con mercadería
                        Color(*col_rgba)
                        RoundedRectangle(pos=(rx, ry), size=(rw, rh), radius=[max(1, 4 * scale)])

                        if is_shelf_target:
                            Color(0.83, 0.18, 0.18, 1)  # Borde rojo destacado
                            Line(
                                rounded_rectangle=[rx - 1, ry - 1, rw + 2, rh + 2, max(2, 4 * scale)],
                                width=max(2.0, 3.5 * scale),
                            )
                        else:
                            Color(0.15, 0.15, 0.15, 0.7)
                            Line(rounded_rectangle=[rx, ry, rw, rh, max(1, 4 * scale)], width=1)

                        draw_label(e_code, rx + rw / 2.0, ry + rh / 2.0, int(11 * scale), color_rgba=(0.12, 0.12, 0.12, 1), bold=True)
                    else:
                        # Espacio libre / inactivo
                        Color(0.4, 0.4, 0.4, 0.25)
                        Line(rounded_rectangle=[rx, ry, rw, rh, max(1, 4 * scale)], width=1)

            # Dibujar las 4 Áreas Operativas Inferiores
            for z in inventario.ZONAS_OPERATIVAS:
                z_name = z["nombre"]
                zx, zy, zw, zh = to_kivy_pos(z["x"], 450, z["ancho"], 150)
                self.zone_rects[z_name] = (zx, zy, zw, zh)

                is_z_target = (self.target_zone == z_name)
                z_rgba = get_color_from_hex(z["color"])

                Color(*z_rgba)
                RoundedRectangle(pos=(zx, zy), size=(zw, zh), radius=[max(2, 5 * scale)])

                if is_z_target:
                    Color(0.83, 0.18, 0.18, 1)
                    Line(
                        rounded_rectangle=[zx - 1, zy - 1, zw + 2, zh + 2, max(2, 5 * scale)],
                        width=max(2.0, 3.5 * scale),
                    )
                else:
                    Color(0.15, 0.15, 0.15, 0.7)
                    Line(rounded_rectangle=[zx, zy, zw, zh, max(1, 4 * scale)], width=1)

                draw_label(z_name, zx + zw / 2.0, zy + zh / 2.0, int(12 * scale), color_rgba=(0.12, 0.12, 0.12, 1), bold=True)

            # Trazar Ruta de Picking (Polilínea ortogonal roja)
            if self.target_pasillo:
                try:
                    i = int(self.target_pasillo.replace("P", "")) - 1
                    target_ax = 20 + i * 80
                    shelf_num = int(self.target_estante.replace("E", "")) if self.target_estante else 1
                    cy = 60 + (shelf_num - 1) * 90 + 45
                    gx = target_ax + 70

                    # Puntos de la trayectoria en espacio SVG
                    svg_pts = [
                        (90, 450),       # Salida de Entrada/Salida
                        (90, 435),       # Pasillo central horizontal
                        (gx, 435),       # Giro hacia el pasillo objetivo
                        (gx, cy),        # Avance vertical
                        (target_ax + 60, cy),  # Llegada al estante
                    ]

                    kivy_pts = []
                    for sx, sy in svg_pts:
                        kx = off_x + sx * scale
                        ky = off_y + (vh - sy) * scale
                        kivy_pts.extend([kx, ky])

                    Color(0.83, 0.18, 0.18, 1)
                    Line(
                        points=kivy_pts,
                        width=max(2.0, 3.0 * scale),
                        dash_length=max(4, 7 * scale),
                        dash_offset=max(2, 4 * scale),
                    )

                    # Marcador de inicio (Entrada)
                    Color(0.83, 0.18, 0.18, 1)
                    Ellipse(pos=(kivy_pts[0] - dp(4), kivy_pts[1] - dp(4)), size=(dp(8), dp(8)))

                    # Marcador de llegada (Estante objetivo)
                    Color(0.95, 0.25, 0.25, 1)
                    Ellipse(pos=(kivy_pts[-2] - dp(5), kivy_pts[-1] - dp(5)), size=(dp(10), dp(10)))
                except (ValueError, IndexError):
                    pass


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
        header = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(68),
            padding=[dp(16), dp(10), dp(16), dp(8)],
            spacing=dp(2),
        )
        with header.canvas.before:
            Color(*WHITE)
            Rectangle(size=header.size, pos=header.pos)
            Color(*LINE)
            Line(points=[0, 0, header.width, 0], width=1)

        title_row = BoxLayout(size_hint_y=None, height=dp(26), spacing=dp(6))
        btn_back = Button(
            text="<",
            font_size="22sp",
            bold=True,
            color=CHARCOAL,
            size_hint_x=None,
            width=dp(28),
            background_color=(0, 0, 0, 0),
            background_normal="",
        )
        btn_back.bind(on_release=self.go_back)
        title_row.add_widget(btn_back)

        lbl_mtitle = Label(
            text="Plano del Minimarket (12 Pasillos)",
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
            text="Toca un estante o busca por producto / categoría.",
            font_size="11sp",
            color=SLATE_TEXT,
            size_hint_y=None,
            height=dp(16),
            halign="left",
            valign="middle",
        )
        lbl_sub.bind(size=lbl_sub.setter("text_size"))
        header.add_widget(lbl_sub)
        main_layout.add_widget(header)

        # 2. Barra de Búsqueda
        search_wrap = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            padding=[dp(16), dp(6), dp(16), dp(4)],
            spacing=dp(6),
        )
        with search_wrap.canvas.before:
            Color(*SLATE_BG)
            Rectangle(size=search_wrap.size, pos=search_wrap.pos)

        self.search_input = TextInput(
            hint_text="Buscar (ej. coca, P045, galletas, P04)...",
            multiline=False,
            background_color=WHITE,
            foreground_color=CHARCOAL,
            cursor_color=CHARCOAL,
            padding=[dp(10), dp(8), dp(10), dp(8)],
        )
        self.search_input.bind(text=self.on_search_change)
        search_wrap.add_widget(self.search_input)

        btn_clear = Button(
            text="✕",
            size_hint=(None, 1),
            width=dp(38),
            background_color=(0.85, 0.88, 0.90, 1),
            color=CHARCOAL,
            bold=True,
        )
        btn_clear.bind(on_release=self.clear_search)
        search_wrap.add_widget(btn_clear)
        main_layout.add_widget(search_wrap)

        # 3. Vista del Mapa Interactivo (Toma todo el espacio restante)
        map_container = BoxLayout(padding=[dp(12), dp(4), dp(12), dp(4)], size_hint_y=1)
        with map_container.canvas.before:
            Color(*SLATE_BG)
            Rectangle(size=map_container.size, pos=map_container.pos)

        self.map_view = MapCanvasView(
            on_shelf_select=self.on_shelf_selected,
            on_zone_select=self.on_zone_selected,
        )
        map_container.add_widget(self.map_view)
        main_layout.add_widget(map_container)

        # 4. Panel Inferior (Tarjeta de Detalles + Botón de Acción)
        self.bottom_panel = BoxLayout(
            orientation="vertical",
            padding=[dp(16), dp(6), dp(16), dp(14)],
            spacing=dp(8),
            size_hint_y=None,
            height=dp(185),
        )
        with self.bottom_panel.canvas.before:
            Color(*SLATE_BG)
            Rectangle(size=self.bottom_panel.size, pos=self.bottom_panel.pos)

        self.result_card = RoundedBox(
            orientation="vertical",
            bg_color=(0.14, 0.15, 0.17, 1),
            radius=[10],
            padding=[dp(12), dp(10), dp(12), dp(10)],
            spacing=dp(6),
            size_hint_y=None,
            height=dp(110),
        )

        self.lbl_result_count = Label(
            text="1 resultado(s)",
            font_size="13sp",
            bold=True,
            color=WHITE,
            size_hint_y=None,
            height=dp(18),
            halign="left",
        )
        self.lbl_result_count.bind(size=self.lbl_result_count.setter("text_size"))
        self.result_card.add_widget(self.lbl_result_count)

        grid_details = GridLayout(cols=3, size_hint_y=1, spacing=dp(6))

        # Columna: Producto
        col_p = BoxLayout(orientation="vertical", spacing=dp(2))
        col_p.add_widget(Label(text="Producto", font_size="10sp", bold=True, color=(0.65, 0.68, 0.72, 1), size_hint_y=None, height=dp(14)))
        self.lbl_p_name = Label(text="-", font_size="12sp", bold=True, color=WHITE, size_hint_y=None, height=dp(18))
        self.lbl_p_sku = Label(text="-", font_size="10sp", color=(0.7, 0.75, 0.8, 1), size_hint_y=None, height=dp(14))
        col_p.add_widget(self.lbl_p_name)
        col_p.add_widget(self.lbl_p_sku)
        grid_details.add_widget(col_p)

        # Columna: Pasillo / Ubicación
        col_z = BoxLayout(orientation="vertical", spacing=dp(2))
        col_z.add_widget(Label(text="Ubicación", font_size="10sp", bold=True, color=(0.65, 0.68, 0.72, 1), size_hint_y=None, height=dp(14)))
        self.lbl_z_name = Label(text="-", font_size="12sp", bold=True, color=WHITE, size_hint_y=None, height=dp(18))
        self.lbl_z_sub = Label(text="-", font_size="10sp", color=(0.7, 0.75, 0.8, 1), size_hint_y=None, height=dp(14))
        col_z.add_widget(self.lbl_z_name)
        col_z.add_widget(self.lbl_z_sub)
        grid_details.add_widget(col_z)

        # Columna: Stock
        col_s = BoxLayout(orientation="vertical", spacing=dp(2))
        col_s.add_widget(Label(text="Stock", font_size="10sp", bold=True, color=(0.65, 0.68, 0.72, 1), size_hint_y=None, height=dp(14)))
        self.lbl_s_qty = Label(text="-", font_size="15sp", bold=True, color=WHITE, size_hint_y=None, height=dp(22))
        col_s.add_widget(self.lbl_s_qty)
        grid_details.add_widget(col_s)

        self.result_card.add_widget(grid_details)
        self.bottom_panel.add_widget(self.result_card)

        # Botón de Recolección / Finalización
        self.action_box = BoxLayout(size_hint_y=None, height=dp(48))
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

        # Selección inicial
        if self.next_prod:
            self.show_product(self.next_prod)
            prod_name = self.next_prod.get("nombre") or self.next_prod.get("name", "")
            self.search_input.text = prod_name
        else:
            self.show_home()

    def show_home(self):
        """Muestra el estado general del minimarket sin selección puntual."""
        self.map_view.target_pasillo = None
        self.map_view.target_estante = None
        self.map_view.target_zone = None
        self.map_view.draw_map()

        self.lbl_result_count.text = "12 pasillos · 100 productos"
        self.lbl_p_name.text = "Toca un estante"
        self.lbl_p_sku.text = "o busca arriba"
        self.lbl_z_name.text = "General"
        self.lbl_z_sub.text = "12 pasillos activos"
        self.lbl_s_qty.text = "100 u."

    def show_product(self, prod, total_results=1):
        """Ubica un producto en el mapa y despliega sus metadatos."""
        pasillo = prod.get("pasillo")
        estante = prod.get("estante")
        nivel = prod.get("nivel", 1)

        # Si faltan campos de ubicación, buscamos en el catálogo de inventario
        if not pasillo or not estante:
            sku = prod.get("id") or prod.get("sku")
            name = prod.get("nombre") or prod.get("name")
            inv_match = next(
                (p for p in inventario.PRODUCTOS if p["id"] == sku or p["nombre"].lower() == str(name).lower()),
                None,
            )
            if inv_match:
                prod = inv_match
                pasillo = inv_match["pasillo"]
                estante = inv_match["estante"]
                nivel = inv_match["nivel"]
            else:
                pasillo = "P01"
                estante = "E01"

        self.map_view.target_pasillo = pasillo
        self.map_view.target_estante = estante
        self.map_view.target_zone = None
        self.map_view.draw_map()

        nombre = prod.get("nombre") or prod.get("name", "Producto")
        sku = prod.get("id") or prod.get("sku", "-")
        cat = prod.get("categoria", "")
        stock = prod.get("stock", 0)
        precio = prod.get("precio", 0.0)

        self.lbl_result_count.text = f"{total_results} resultado(s) · {pasillo}-{estante}-N{nivel}"
        self.lbl_p_name.text = nombre[:20] + ("..." if len(nombre) > 20 else "")
        self.lbl_p_sku.text = f"{sku} · {cat}" if cat else sku
        self.lbl_z_name.text = f"Pasillo {pasillo}"
        self.lbl_z_sub.text = f"{estante} · Nivel {nivel}"
        self.lbl_s_qty.text = f"{stock} u."

    def on_search_change(self, instance, value):
        query = value.strip()
        if not query:
            if self.next_prod:
                self.show_product(self.next_prod)
            else:
                self.show_home()
            return

        results = inventario.buscar_productos(query)

        # Búsqueda complementaria por código de pasillo (ej. 'p04')
        if not results:
            q_norm = inventario.normalizar_texto(query)
            results = [
                p for p in inventario.PRODUCTOS
                if q_norm == inventario.normalizar_texto(p["pasillo"])
                or q_norm == inventario.normalizar_texto(p["ubicacion"])
            ]

        if results:
            self.show_product(results[0], total_results=len(results))
        else:
            self.map_view.target_pasillo = None
            self.map_view.target_estante = None
            self.map_view.target_zone = None
            self.map_view.draw_map()

            self.lbl_result_count.text = "0 resultado(s)"
            self.lbl_p_name.text = "No encontrado"
            self.lbl_p_sku.text = "-"
            self.lbl_z_name.text = "-"
            self.lbl_z_sub.text = "Sin ubicación"
            self.lbl_s_qty.text = "0 u."

    def on_shelf_selected(self, pasillo, estante):
        """Evento al hacer tap sobre un estante del mapa."""
        prods = inventario.obtener_por_pasillo(pasillo, estante)
        if prods:
            first = prods[0]
            self.show_product(first, total_results=len(prods))
            self.search_input.text = first["nombre"]
        else:
            self.map_view.target_pasillo = pasillo
            self.map_view.target_estante = estante
            self.map_view.target_zone = None
            self.map_view.draw_map()

            self.lbl_result_count.text = f"{pasillo} · {estante}"
            self.lbl_p_name.text = f"Estante {estante}"
            self.lbl_p_sku.text = f"Pasillo {pasillo}"
            self.lbl_z_name.text = f"Pasillo {pasillo}"
            self.lbl_z_sub.text = f"{pasillo}-{estante}"
            self.lbl_s_qty.text = "0 u."

    def on_zone_selected(self, zone_name):
        """Evento al hacer tap sobre una de las 4 zonas operativas."""
        self.map_view.target_pasillo = None
        self.map_view.target_estante = None
        self.map_view.target_zone = zone_name
        self.map_view.draw_map()

        self.lbl_result_count.text = "Zona Operativa"
        self.lbl_p_name.text = zone_name
        self.lbl_p_sku.text = "Área de almacén"
        self.lbl_z_name.text = zone_name
        self.lbl_z_sub.text = "Acceso operativo"
        self.lbl_s_qty.text = "-"

    def clear_search(self, instance):
        self.search_input.text = ""

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "checklist"

    def mark_collected(self, instance, product):
        product["done"] = True

        p_name = product.get("nombre") or product.get("name", "Producto")
        content = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(14))
        content.add_widget(Label(text="Parada completada", font_size="16sp", bold=True, color=LEAF))
        content.add_widget(Label(text=f"{p_name} marcado como recolectado.", font_size="12sp", color=SLATE_TEXT))

        btn = RoundedButton(text="Continuar ruta", size_hint_y=None, height=dp(44), bg_color=FOREST, radius=[12])
        content.add_widget(btn)

        popup = Popup(title="Confirmación", content=content, size_hint=(0.85, 0.35))

        def on_close(x):
            popup.dismiss()
            self.on_pre_enter()

        btn.bind(on_release=on_close)
        popup.open()