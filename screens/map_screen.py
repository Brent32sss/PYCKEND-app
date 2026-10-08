# screens/map_screen.py

from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line, RoundedRectangle, Ellipse

# Importamos CoreLabel para poder dibujar texto vectorial en el Canvas
from kivy.core.text import Label as CoreLabel 

from config.colors import WHITE, LINE, CHARCOAL, SLATE_TEXT, FOREST, MANGO, LEAF, SLATE_BG
from widgets.custom_widgets import RoundedBox, RoundedButton

class MapScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "mapa"

    def on_pre_enter(self):
        self.clear_widgets()

        app = App.get_running_app()
        order = app.current_order if hasattr(app, 'current_order') and app.current_order else None

        main_layout = BoxLayout(orientation='vertical', spacing=0)

        # Header
        header = BoxLayout(orientation='vertical', size_hint_y=None, height=75, padding=[20, 14, 20, 10], spacing=4)
        with header.canvas.before:
            Color(*WHITE)
            Rectangle(size=header.size, pos=header.pos)
            Color(*LINE)
            Line(points=[0, 0, header.width, 0], width=1)

        title_row = BoxLayout(size_hint_y=None, height=24)
        btn_back = Button(text="<", font_size="22sp", bold=True, color=CHARCOAL, size_hint_x=None, width=24, background_color=(0,0,0,0), background_normal='')
        btn_back.bind(on_release=self.go_back)
        title_row.add_widget(btn_back)

        lbl_mtitle = Label(text="Mapa de tienda", font_size="15sp", bold=True, color=CHARCOAL, halign='left', valign='middle')
        lbl_mtitle.bind(size=lbl_mtitle.setter('text_size'))
        title_row.add_widget(lbl_mtitle)

        lbl_exp = Label(text="[ ]", font_size="14sp", bold=True, color=SLATE_TEXT, size_hint_x=None, width=20)
        title_row.add_widget(lbl_exp)
        header.add_widget(title_row)

        lbl_sub = Label(text="Ruta optimizada", font_size="11sp", color=SLATE_TEXT, size_hint_y=None, height=18, halign='left')
        lbl_sub.bind(size=lbl_sub.setter('text_size'))
        header.add_widget(lbl_sub)

        main_layout.add_widget(header)

        # Map Area
        map_view = MapCanvasView()
        main_layout.add_widget(map_view)

        # Determinar Siguiente Parada Dinámicamente
        next_prod = None
        stop_index = 0
        if order and 'products' in order:
            for i, p in enumerate(order['products']):
                if not p.get('done', False):
                    next_prod = p
                    stop_index = i + 1
                    break

        if next_prod:
            banner_container = BoxLayout(size_hint_y=None, height=95, padding=[16, 8, 16, 8])
            next_banner = RoundedBox(bg_color=FOREST, radius=[14], padding=[14, 12, 14, 12], spacing=12)

            stop_badge = RoundedBox(size_hint=(None, None), size=(38, 38), bg_color=MANGO, radius=[10])
            stop_badge.add_widget(Label(text=str(stop_index), font_size="16sp", bold=True, color=WHITE))
            next_banner.add_widget(stop_badge)

            b_info = BoxLayout(orientation='vertical', spacing=2)
            lbl_tag = Label(text="SIGUIENTE PARADA", font_size="9sp", color=(0.7, 0.8, 0.75, 1), halign='left', valign='middle')
            lbl_tag.bind(size=lbl_tag.setter('text_size'))
            
            lbl_loc = Label(text=next_prod['location'], font_size="13sp", bold=True, color=WHITE, halign='left', valign='middle')
            lbl_loc.bind(size=lbl_loc.setter('text_size'))

            lbl_dist = Label(text=f"Producto: {next_prod['name']} ({next_prod['qty']})", font_size="11sp", color=(0.7, 0.8, 0.75, 1), halign='left', valign='middle')
            lbl_dist.bind(size=lbl_dist.setter('text_size'))

            b_info.add_widget(lbl_tag)
            b_info.add_widget(lbl_loc)
            b_info.add_widget(lbl_dist)
            next_banner.add_widget(b_info)

            banner_container.add_widget(next_banner)
            main_layout.add_widget(banner_container)

            footer = BoxLayout(size_hint_y=None, height=72, padding=[20, 10, 20, 10])
            btn_collect = RoundedButton(text="Marcar como recolectado", size_hint_y=None, height=52, bg_color=MANGO, radius=[14])
            btn_collect.bind(on_release=lambda x: self.mark_collected(x, next_prod))
            footer.add_widget(btn_collect)
            main_layout.add_widget(footer)
        else:
            # Caso todo recolectado
            footer = BoxLayout(size_hint_y=None, height=90, padding=[20, 10, 20, 10])
            btn_finish = RoundedButton(text="¡Pedido Completado! Volver", size_hint_y=None, height=52, bg_color=LEAF, radius=[14])
            btn_finish.bind(on_release=self.go_back)
            footer.add_widget(btn_finish)
            main_layout.add_widget(footer)

        self.add_widget(main_layout)

    def go_back(self, instance):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = "checklist"

    def mark_collected(self, instance, product):
        product['done'] = True
        
        content = BoxLayout(orientation='vertical', padding=20, spacing=14)
        content.add_widget(Label(text="Parada completada", font_size="16sp", bold=True, color=LEAF))
        content.add_widget(Label(text=f"{product['name']} marcado como recolectado.", font_size="12sp", color=SLATE_TEXT))

        btn = RoundedButton(text="Continuar ruta", size_hint_y=None, height=44, bg_color=FOREST, radius=[12])
        content.add_widget(btn)

        popup = Popup(title="Confirmación", content=content, size_hint=(0.85, 0.35))
        
        def on_close(x):
            popup.dismiss()
            self.on_pre_enter() # Recarga el mapa para la siguiente parada
            
        btn.bind(on_release=on_close)
        popup.open()


class MapCanvasView(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.draw_map, size=self.draw_map)

    def draw_map(self, *args):
        self.canvas.clear()
        with self.canvas:
            # Fondo
            Color(*SLATE_BG)
            Rectangle(pos=self.pos, size=self.size)

            # --- DIBUJO DEL MINIMARKET ---
            base_x = self.x + 15
            base_y = self.y + 20
            w_total = self.width - 30
            h_total = self.height - 40

            # Colores por zona
            col_acc = (0.75, 0.88, 0.85, 1) # Entrada/Recepcion
            col_caja = (0.95, 0.85, 0.7, 1) # Cajas
            col_frio = (0.7, 0.85, 0.95, 1) # Refri
            col_g1 = (0.75, 0.88, 0.75, 1)  # G1
            col_g2 = (0.95, 0.95, 0.75, 1)  # G2
            col_g3 = (0.9, 0.75, 0.8, 1)    # G3
            col_pan = (0.85, 0.8, 0.78, 1)  # Panes
            col_bod = (0.85, 0.75, 0.88, 1) # Bodega

            def draw_zone(px, py, pw, ph, color, text_label=""):
                zx = base_x + (px / 100.0) * w_total
                zy = base_y + (py / 100.0) * h_total
                zw = (pw / 100.0) * w_total
                zh = (ph / 100.0) * h_total

                # Dibujar el rectángulo
                Color(*color)
                RoundedRectangle(pos=(zx, zy), size=(zw, zh), radius=[6])
                
                # Dibujar el texto si existe
                if text_label:
                    # Crear una etiqueta con CoreLabel
                    lbl = CoreLabel(text=text_label, font_size=11, color=(0.15, 0.2, 0.15, 1), halign='center')
                    
                    # Forzar el límite de ancho para textos con salto de línea (\n)
                    if "\n" in text_label:
                        lbl.text_size = (zw, None)
                    
                    lbl.refresh()
                    tex = lbl.texture
                    
                    # Restablecer el color a blanco antes de pegar la textura, sino se tiñe del color del rectángulo
                    Color(1, 1, 1, 1)
                    Rectangle(pos=(zx + (zw - tex.size[0]) / 2, zy + (zh - tex.size[1]) / 2), size=tex.size, texture=tex)

                return (zx + zw/2, zy + zh/2) # Retorna las coordenadas del centro

            # 1. Entrada (Abajo Izquierda)
            draw_zone(0, 0, 25, 10, col_acc, "Entrada /\nSalida")
            
            # 2. Cajas (Sobre la entrada)
            draw_zone(0, 13, 25, 20, col_caja, "Cajas")
            
            # 3. Refrigeradores (Arriba centro)
            c_ref = draw_zone(28, 88, 50, 12, col_frio, "Refrigeradores")
            
            # 4. Góndolas (Centro)
            c_g1 = draw_zone(28, 70, 50, 10, col_g1, "Góndola 1")
            c_g2 = draw_zone(28, 54, 50, 10, col_g2, "Góndola 2")
            c_g3 = draw_zone(28, 38, 50, 10, col_g3, "Góndola 3")
            c_pan = draw_zone(28, 20, 50, 12, col_pan, "Panes y frutas")

            # 5. Bodega (Derecha)
            draw_zone(82, 30, 18, 70, col_bod, "Bodega\n(almacén)")

            # 6. Recepción (Abajo Derecha)
            draw_zone(82, 15, 18, 12, col_acc, "Recepción")

            # --- RUTA SIMULADA ---
            Color(*MANGO)
            Line(points=[
                c_pan[0], c_pan[1],
                c_g3[0], c_g3[1],
                c_g2[0], c_g2[1],
                c_g1[0], c_g1[1],
                c_ref[0], c_ref[1]
            ], width=2, dash_length=8, dash_offset=4)

            # Paradas ya completadas o pendientes (puntos verdes)
            Color(*LEAF)
            Ellipse(pos=(c_pan[0]-6, c_pan[1]-6), size=(12, 12))
            Color(*FOREST)
            Ellipse(pos=(c_g3[0]-6, c_g3[1]-6), size=(12, 12))
            Color(*FOREST)
            Ellipse(pos=(c_g2[0]-6, c_g2[1]-6), size=(12, 12))
            
            # Siguiente Parada Animada (Destacada en Naranja)
            Color(*MANGO)
            Ellipse(pos=(c_g1[0]-10, c_g1[1]-10), size=(20, 20))
            Color(*WHITE)
            Ellipse(pos=(c_g1[0]-5, c_g1[1]-5), size=(10, 10))
            Color(*MANGO)
            Ellipse(pos=(c_g1[0]-3, c_g1[1]-3), size=(6, 6))