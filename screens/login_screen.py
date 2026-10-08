from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle

from config.colors import SLATE_BG, FOREST, CHARCOAL, SLATE_TEXT, WHITE, LINE
from widgets.custom_widgets import DotWidget, RoundedBox, RoundedButton

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "login"

        layout = BoxLayout(orientation='vertical', padding=[24, 20, 24, 24], spacing=16)
        with layout.canvas.before:
            Color(*SLATE_BG)
            self.bg_rect = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(pos=self._update_bg, size=self._update_bg)

        brand = BoxLayout(size_hint_y=None, height=40, spacing=8)
        dot = DotWidget()
        brand.add_widget(dot)
        
        lbl_brand = Label(text="PYCKEND", font_size="20sp", bold=True, color=FOREST, halign='left', valign='middle')
        lbl_brand.bind(size=lbl_brand.setter('text_size'))
        brand.add_widget(lbl_brand)
        layout.add_widget(brand)

        layout.add_widget(Label(size_hint_y=0.08))

        lbl_title = Label(text="Bienvenido, equipo", font_size="24sp", bold=True, color=CHARCOAL, size_hint_y=None, height=36, halign='left')
        lbl_title.bind(size=lbl_title.setter('text_size'))
        layout.add_widget(lbl_title)

        lbl_sub = Label(text="Ingresa tus datos para ver tus pedidos asignados.", font_size="12sp", color=SLATE_TEXT, size_hint_y=None, height=30, halign='left')
        lbl_sub.bind(size=lbl_sub.setter('text_size'))
        layout.add_widget(lbl_sub)

        layout.add_widget(Label(size_hint_y=0.04))

        lbl_u = Label(text="CORREO O USUARIO", font_size="10sp", bold=True, color=SLATE_TEXT, size_hint_y=None, height=18, halign='left')
        lbl_u.bind(size=lbl_u.setter('text_size'))
        layout.add_widget(lbl_u)

        f_email = RoundedBox(size_hint_y=None, height=48, bg_color=WHITE, border_color=LINE, radius=[14], padding=[12, 0, 12, 0])
        self.email_input = TextInput(text="jacob.picker@tienda.com", multiline=False, background_color=(0,0,0,0), foreground_color=CHARCOAL, font_size="13sp", padding=[0, 14])
        f_email.add_widget(self.email_input)
        layout.add_widget(f_email)

        lbl_p = Label(text="CONTRASEÑA", font_size="10sp", bold=True, color=SLATE_TEXT, size_hint_y=None, height=18, halign='left')
        lbl_p.bind(size=lbl_p.setter('text_size'))
        layout.add_widget(lbl_p)

        f_pass = RoundedBox(size_hint_y=None, height=48, bg_color=WHITE, border_color=LINE, radius=[14], padding=[12, 0, 12, 0])
        self.pass_input = TextInput(text="••••••••••", multiline=False, password=True, background_color=(0,0,0,0), foreground_color=CHARCOAL, font_size="13sp", padding=[0, 14])
        f_pass.add_widget(self.pass_input)
        layout.add_widget(f_pass)

        layout.add_widget(Label(size_hint_y=1))

        btn_login = RoundedButton(text="Iniciar sesión", size_hint_y=None, height=52, bg_color=FOREST, radius=[14])
        btn_login.bind(on_release=self.do_login)
        layout.add_widget(btn_login)

        lbl_foot = Label(text="Acceso exclusivo para personal de recolección", font_size="10sp", color=SLATE_TEXT, size_hint_y=None, height=20, halign='center')
        layout.add_widget(lbl_foot)

        self.add_widget(layout)

    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def do_login(self, instance):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = "dashboard"