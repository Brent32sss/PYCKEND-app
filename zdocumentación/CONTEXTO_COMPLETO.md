# 📋 CONTEXTO COMPLETO — PROYECTO PICKLY

**Última actualización:** 28 de septiembre, 2026  
**Estado:** App funcional en Python/Kivy, lista para extender  
**Plataforma:** Móvil (iOS/Android via Kivy)

---

## 🎯 RESUMEN DEL PROYECTO

**Nombre:** PICKLY — App de Recolección para Picker  
**Objetivo:** Aplicación móvil para gestionar la recolección de productos en tienda  
**Rol:** Picker (recolector de pedidos)  
**Tecnología:** Python + Kivy (cross-platform)  
**Estado:** MVP funcional con 4 pantallas

**Cambio reciente:** Se eliminó la vista de Cliente. Ahora es SOLO Picker.

---

## 🏗️ ARQUITECTURA TÉCNICA

### Stack Actual
```
Frontend: Kivy (Python UI framework)
Backend: None (datos en memoria por ahora)
Base de datos: None (hardcoded sample data)
Compilación Android: Buildozer
```

### Patrón MVC
- **Model:** `PICKER_DATA`, `ORDERS` (listas/dicts en memoria)
- **View:** `Screen` classes (LoginScreen, DashboardScreen, etc.)
- **Controller:** `on_press`, `on_checkbox`, bindings de Kivy

---

## 🎨 TOKENS DE DISEÑO

### Paleta de Colores (RGB 0–1 + Alpha)

```python
# Paleta completa para copiar/pegar en código

FOREST = (0.106, 0.263, 0.196, 1)           # #1B4332 - Headers principales, botones Picker
FOREST_DARK = (0.059, 0.184, 0.133, 1)      # #0F2E22 - Header dashboard Picker
MANGO = (1, 0.541, 0.239, 1)                # #FF8A3D - CTAs (botones), ruta en mapa, badges urgentes
MANGO_DARK = (0.906, 0.439, 0.118, 1)       # #E86F1E - Variante hover (no usada aún)

CREAM = (0.984, 0.973, 0.949, 1)            # #FBF8F2 - Fondo Cliente (NO USADO AHORA)
MINT = (0.906, 0.945, 0.910, 1)             # #E7F1E8 - Badges normales, fondo de chips
MINT_LINE = (0.812, 0.890, 0.827, 1)        # #CFE3D3 - Bordes de fields/líneas
SLATE_BG = (0.925, 0.941, 0.933, 1)         # #ECF0EE - Fondo general Picker
CHARCOAL = (0.118, 0.157, 0.133, 1)         # #1E2822 - Texto principal (títulos, labels)
SLATE_TEXT = (0.357, 0.408, 0.384, 1)       # #5B6862 - Texto secundario (hints, subtítulos)

CORAL = (1, 0.353, 0.373, 1)                # #FF5A5F - Estado urgente, error
LEAF = (0.184, 0.655, 0.416, 1)             # #2FA86A - Completado, checkmarks, "a tiempo"
SUN = (1, 0.752, 0.282, 1)                  # #FFC048 - En progreso (no usado aún)
WHITE = (1, 1, 1, 1)                        # #FFFFFF - Fondos claros
LINE = (0.882, 0.906, 0.886, 1)             # #E1E7E3 - Bordes sutiles entre elementos

LIGHT_MUTED = (0.623, 0.706, 0.658, 1)      # #9FB4A8 - Texto en headers oscuros (notificaciones, etc.)
```

### Tipografía
```python
SORA = "Sora, sans-serif"                   # Títulos, números, botones (bold 600–800)
INTER = "Inter, sans-serif"                 # Cuerpo, labels, hints (400–600)
MONO = "'JetBrains Mono', monospace"        # IDs de pedido, ubicaciones (600–700)
```

### Radios (border-radius)
- Pantallas: 26px (marco del teléfono)
- Headers: 24px (esquinas suavizadas)
- Tarjetas: 14–16px
- Botones: 12–14px
- Campos: 12px
- Chips/badges: 999px (circular)
- Checkboxes: 6px

---

## 📱 ESTRUCTURA DE PANTALLAS

### 1. LOGIN (LoginScreen)
**Ruta en código:** Clase `LoginScreen` ~línea 100

**Componentes:**
- Brand: "🧭 pickly"
- Heading: "Bienvenido, equipo"
- 2 campos de texto: email, contraseña
- Link "¿Olvidaste tu contraseña?"
- Botón "Iniciar sesión" (FOREST)
- Footer: "Acceso exclusivo..."

**Datos de entrada:**
```python
email = "jacob.picker@tienda.com"  # dummy
password = "••••••••••"             # dummy
```

**Acción al presionar botón:**
```python
self.manager.current = "dashboard"  # Navega a pantalla 2
```

**Notas:**
- No hay validación real (todo pasa)
- Para producción: conectar a backend

---

### 2. DASHBOARD (DashboardScreen)
**Ruta en código:** Clase `DashboardScreen` ~línea 185

**Componentes:**

#### Header (170 px alto, FOREST_DARK)
- Turno: "Turno tarde" + notificaciones "🔔 2"
- Avatar + Nombre: "Jacob Torres"
- Rol: "Picker · Tienda San Isidro"
- KPIs (3 columnas):
  - "5 Asignados"
  - "2 Urgentes"
  - "92% A tiempo"
- Título: "Pedidos asignados"

#### Lista de pedidos (ScrollView)
Grid de tarjetas (OrderCard):
```python
[
    {
        "id": "#PK-4821",
        "client": "Valeria R.",
        "priority": "Urgente",      # rojo/coral
        "items": 9,
        "time": "10:30 a.m.",
        "products": [...]           # para checklist después
    },
    # ... más 3 pedidos
]
```

**Cada tarjeta muestra:**
- ID + Cliente
- Badge (Urgente/Normal)
- Items count
- Hora programada

#### Bottom Navigation (64 px)
4 items: Pedidos ✓ | Mapa | Historial | Perfil  
(Solo Pedidos está activo, otros deshabilitados)

---

### 3. CHECKLIST (ChecklistScreen)
**Ruta en código:** Clase `ChecklistScreen` ~línea 280

**Componentes:**

#### Header (140 px, WHITE con borde)
- Back arrow + "#PK-4821 · Valeria R." (monospace)
- Heading: "Lista de recolección"
- Barra de progreso: 44% lleno (4/9 productos)
- Badge de prioridad: "⏱ 10:30 a.m."

#### Items List (ScrollView)
Grid de ProductItem:
```python
[
    {
        "name": "Palta hass",
        "location": "Pasillo A · Estante 3 · Nivel 2",
        "qty": "1 kg",
        "done": False/True          # cambia al hacer checkbox
    },
    # ... 9 productos
]
```

**Cada item:**
- Checkbox (MINT_LINE → LEAF cuando checked)
- Nombre del producto
- Ubicación (badge MINT, monospace pequeño)
- Cantidad/Unidad (derecha)
- Al marcar: opacidad baja (0.55)

#### Action Button
"Ver ruta en el mapa" → navega a pantalla 4

---

### 4. MAP (MapScreen)
**Ruta en código:** Clase `MapScreen` ~línea 360

**Componentes:**

#### Header (80 px, WHITE)
- Back arrow + "Mapa de tienda"
- Subtitle: "Ruta optimizada · 4 paradas"
- Expand icon: "⤢"

#### Map Canvas (40% alto, MapCanvas widget)
**Dibuja con canvas de Kivy:**
- Fondo: gris claro (#F2F5F3)
- Grid: 8 pasillos (A–H, 4 cols × 2 rows)
- Ruta: línea MANGO punteada (1 8) que conecta:
  1. Pasillo A (LEAF - completado)
  2. Pasillo B (FOREST - próximo)
  3. Pasillo C (FOREST)
  4. Pasillo D (MANGO - posición actual, punto pulsante)
- Distancia: "62 m"

#### Next Stop Info (100 px, FOREST)
- Número: "3"
- Label: "SIGUIENTE PARADA"
- Ubicación: "Pasillo C · Estante 2 · Nivel 3"
- Distancia: "62 m"

#### Action Button
"Marcar como recolectado" → popup de confirmación

---

## 💾 ESTRUCTURA DE DATOS

### PICKER_DATA (global)
```python
PICKER_DATA = {
    "name": "Jacob Torres",
    "photo": "🧭",                  # emoji (no imagen real)
    "role": "Picker · Tienda San Isidro",
    "shift": "Turno tarde",
    "notifications": 2,
    "stats": {
        "asignados": 5,
        "urgentes": 2,
        "puntualidad": "92%"
    }
}
```

### ORDERS (lista de dicts)
```python
ORDERS = [
    {
        "id": "#PK-4821",
        "client": "Valeria R.",
        "priority": "Urgente",      # "Urgente" o "Normal"
        "items": 9,                 # cantidad total
        "time": "10:30 a.m.",
        "products": [
            {
                "name": "Palta hass",
                "location": "Pasillo A · Estante 3 · Nivel 2",
                "qty": "1 kg",
                "done": False       # cambia interactivamente
            },
            # ... 8 más
        ]
    },
    # ... 3 más
]
```

### Formato de ubicación
**SIEMPRE usar:** `Pasillo X · Estante Y · Nivel Z`
- X: A–H (columna de pasillo)
- Y: 1–4 (número de estante vertical)
- Z: 1–3 (nivel/altura dentro del estante)

---

## 🔄 FLUJO DE NAVEGACIÓN

```
LOGIN
  │ (Iniciar sesión)
  ↓
DASHBOARD
  │ (Tap pedido)
  ↓
CHECKLIST
  │ (Ver ruta en mapa)
  ↓
MAP
  │ (Volver/back)
  ↓
CHECKLIST
  │ (back)
  ↓
DASHBOARD
```

Todas usan `SlideTransition(direction='left')` para animación suave.

---

## 🔌 CÓMO EXTENDER LA APP

### Agregar más pantallas
1. Crea una clase nueva heredando de `Screen`:
   ```python
   class MiPantalla(Screen):
       def __init__(self, **kwargs):
           super().__init__(**kwargs)
           self.name = "mi_pantalla"
           # ... layout código
   ```

2. Agrégala a `ScreenManager` en `PickerApp.build()`:
   ```python
   sm.add_widget(MiPantalla())
   ```

3. Navega desde otra pantalla:
   ```python
   self.manager.current = "mi_pantalla"
   ```

### Conectar a backend
1. Importa `requests`:
   ```python
   import requests
   ```

2. Reemplaza ORDERS en `on_pre_enter`:
   ```python
   response = requests.get("https://tu-api.com/pedidos")
   ORDERS = response.json()
   ```

3. POST al marcar como recolectado:
   ```python
   requests.post("https://tu-api.com/pedidos/4821/complete")
   ```

### Agregar GPS/Geolocalización
```python
from kivy.garden.android.gps import LocationListener

class GPSListener(LocationListener):
    def on_location(self, **kwargs):
        lat, lon = kwargs['lat'], kwargs['lon']
        # Actualizar posición en mapa
```

### Persistencia local (SQLite)
```python
import sqlite3

db = sqlite3.connect('pickly.db')
cursor = db.cursor()

# Guardar estado de checkbox
cursor.execute('''
    UPDATE products SET done=? WHERE id=?
''', (True, product_id))
db.commit()
```

### Notificaciones Push
```python
from plyer import notification

notification.notify(
    title="Nuevo pedido",
    message="Orden urgente #PK-5000",
    timeout=5
)
```

---

## 📊 MODIFICACIONES RECIENTES

### ✅ Cambios ya hechos:
1. Eliminado selector de rol inicial
2. Eliminada toda la vista de Cliente (catálogo, carrito, seguimiento)
3. Login directo a pantalla de Picker
4. Barra de navegación inferior en dashboard
5. Datos de ejemplo con 9 productos en primer pedido
6. Badge de prioridad en checklist ("⏱ 10:30 a.m.")
7. Mapa simplificado con grid de pasillos A–H

### ❌ Qué NO está implementado aún:
- Backend/API real
- Autenticación real
- GPS/Geolocalización en vivo
- Persistencia en BD
- Notificaciones push
- Cámara para fotos de productos
- Historial de recolecciones
- Perfil de usuario (nav item pero sin pantalla)
- Mapa interactivo real (Google Maps)

---

## 🛠️ CÓMO CONTINUAR EL DESARROLLO

### Próximos pasos recomendados (prioridad)

**Corto plazo (1-2 semanas):**
1. Conectar a backend (API REST)
2. Autenticación real (login contra servidor)
3. Persistencia local (SQLite para caché)
4. Notifications/Toast al completar parada

**Mediano plazo (2-4 semanas):**
1. GPS en tiempo real
2. Historial de recolecciones
3. Mapa interactivo (kivy-garden MapView)
4. Fotos de productos (cámara)

**Largo plazo (1-2 meses):**
1. WebSocket para pedidos en vivo
2. Sincronización offline
3. Analytics/reportes
4. Multi-idioma (i18n)

---

## 📁 ARCHIVOS DEL PROYECTO

```
/outputs/
├── picker_app.py                    # App principal (ESTE ES EL ARCHIVO CLAVE)
├── buildozer.spec                   # Config para Android APK
├── requirements.txt                 # Dependencias Python
├── README.md                        # Resumen rápido
├── SETUP_INSTRUCCIONES.md          # Guía de instalación
├── CONTEXTO_COMPLETO.md            # ESTE ARCHIVO
├── app-picking-delivery-prototipo.html  # Prototipo HTML (referencia visual)
└── svg-picker/                     # SVGs de diseño (referencia Penpot)
    ├── 01-login-picker.svg
    ├── 02-picker-dashboard.svg
    ├── 03-picker-checklist.svg
    └── 04-picker-mapa.svg
```

---

## 🔍 PUNTOS CLAVE A RECORDAR

1. **Datos en memoria:** Todo se pierde al cerrar la app. Implementar BD para persistencia.

2. **Colores RGB 0–1:** Kivy usa normalizados (0–1) no hexadecimales. Conversión:
   ```python
   # De hex #FF8A3D a RGB 0–1:
   r = 0xFF / 255 = 1.0
   g = 0x8A / 255 ≈ 0.541
   b = 0x3D / 255 ≈ 0.239
   ```

3. **Responsive:** Usa `size_hint_x/y` en lugar de ancho/alto fijos.

4. **Transiciones:** `SlideTransition(direction='left')` para navegación.

5. **Canvas Kivy:** Para dibujar (mapa), usa `with self.canvas:` y luego `Color()`, `Rectangle()`, `Line()`, etc.

6. **Componentes:** Los custom widgets (OrderCard, ProductItem, MapCanvas) heredan de `BoxLayout` o `Widget`.

---

## 📖 REFERENCIAS EXTERNAS

- **Kivy Docs:** https://kivy.org/doc/stable/
- **Buildozer Guide:** https://buildozer.readthedocs.io/
- **Kivy Garden:** https://garden.kivy.org/ (plugins adicionales)
- **Python 3 Docs:** https://docs.python.org/3/

---

## 💡 TIPS DE DESARROLLO

### Debug rápido
Agrega prints en los métodos clave:
```python
def do_login(self, instance):
    print("DEBUG: Entrando a dashboard")
    self.manager.current = "dashboard"
```

### Probar sin Kivy
Si Kivy no se instala bien, puedes hacer un prototipo rápido con Flask + HTML/JS:
```python
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', orders=ORDERS)
```

### Cambios "en caliente"
Edita el código, presiona Ctrl+C en la terminal y vuelve a ejecutar `python picker_app.py`. No necesitas recompilar a APK para cada cambio.

---

## 🎓 PARA QUIEN CONTINÚE EL PROYECTO

Si otra persona va a continuar:

1. **Lee primero este archivo** de principio a fin
2. **Abre `picker_app.py`** y lee los comentarios (# ====, def nombres claros)
3. **Ejecuta la app** y prueba cada pantalla
4. **Modifica un color/texto** para entender cómo funciona
5. **Luego expande:** agregar pantallas, conectar API, etc.

---

## 📞 TROUBLESHOOTING RÁPIDO

| Problema | Solución |
|----------|----------|
| "No module kivy" | `pip install kivy --upgrade` |
| Pantalla en blanco | Espera 5s, redimensiona ventana |
| App se cierra | `python picker_app.py 2>&1` para ver errores |
| Colores raros | Verifica RGB 0–1, no hex |
| Texto no se ve | Revisa color vs fondo (contraste) |

---

**¡Proyecto listo para continuar!** 🚀

Cualquier pregunta: busca en este documento primero, luego revisa `picker_app.py` línea a línea. El código está bien comentado.
