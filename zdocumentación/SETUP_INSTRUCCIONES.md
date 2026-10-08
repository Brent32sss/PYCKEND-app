# PICKLY — Picker Mobile App
## Setup e Instrucciones de Uso

---

## 1. REQUISITOS PREVIOS

### Windows / macOS / Linux
- **Python 3.8+** instalado
- **Kivy** framework
- Terminal/CMD

---

## 2. INSTALACIÓN RÁPIDA

### Paso 1: Instalar Kivy
```bash
pip install kivy
```

### Paso 2: Ejecutar la app en computadora
```bash
python picker_app.py
```

La app se abrirá en una ventana de 375×812 px (tamaño de móvil).

---

## 3. COMPILAR A APK (Android)

Para convertir la app a un archivo `.apk` instalable en teléfono Android, necesitas **Buildozer**.

### Instalación de Buildozer
```bash
pip install buildozer cython
```

### En Linux (Debian/Ubuntu), también instala:
```bash
sudo apt-get install build-essential libssl-dev libjpeg-dev zlib1g-dev \
    libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev \
    libharfbuzz0b libharfbuzz-dev libwebp6 libtiff5
```

### Crear configuración de Buildozer
En la carpeta del proyecto, ejecuta:
```bash
buildozer android debug
```

Esto genera un archivo `buildozer.spec`. **Abre el archivo y ajusta:**

```ini
[app]
title = Pickly
package.name = pickly
package.domain = com.pickly

[buildozer]
android.api = 31
android.minapi = 21
android.ndk = 25b
```

### Compilar APK
```bash
buildozer android debug
```

El archivo `.apk` estará en:
```
bin/pickly-0.1-debug.apk
```

---

## 4. INSTALAR EN ANDROID

### Método 1: USB (Recomendado)
1. Conecta tu teléfono Android por USB
2. Activa "Depuración USB" en Ajustes > Opciones de desarrollador
3. En la terminal:
   ```bash
   adb install bin/pickly-0.1-debug.apk
   ```

### Método 2: Transferencia manual
1. Copia el `.apk` a tu teléfono (Bluetooth, Google Drive, etc.)
2. Abre el archivo desde el administrador de archivos
3. Toca "Instalar"

---

## 5. FLUJO DE LA APP

### 1. **Login** (pantalla 1)
- Credenciales: `jacob.picker@tienda.com` / cualquier contraseña
- Toca "Iniciar sesión" para entrar

### 2. **Dashboard** (pantalla 2)
- Lista de 4 pedidos asignados
- Toca un pedido para ver detalles
- Barra de navegación inferior (solo Pedidos activo por ahora)

### 3. **Checklist** (pantalla 3)
- Lista de 9 productos del pedido
- Toca el checkbox para marcar como recolectado
- El producto se opaca al ser recolectado
- Botón "Ver ruta en el mapa" al final

### 4. **Mapa** (pantalla 4)
- Plano simplificado de la tienda (grid de pasillos A–H)
- Línea naranja punteada = ruta óptima
- Punto naranja = tu posición actual
- Número 3 = próxima parada
- Botón "Marcar como recolectado" al final

---

## 6. ESTRUCTURA DE CÓDIGO

```
picker_app.py
├── Color Tokens (FOREST, MANGO, LEAF, etc.)
├── Sample Data (PICKER_DATA, ORDERS)
├── LoginScreen — formulario auth
├── DashboardScreen — lista de pedidos
├── OrderCard — tarjeta individual de pedido
├── NavItem — ícono de navegación
├── ChecklistScreen — lista de productos
├── ProductItem — checkbox interactivo
├── MapScreen — canvas con mapa
├── MapCanvas — SVG-like drawing (líneas, círculos)
└── PickerApp — app principal (Kivy)
```

---

## 7. PERSONALIZACIÓN

### Cambiar colores
En la sección "COLOR TOKENS" al inicio:
```python
FOREST = (0.106, 0.263, 0.196, 1)  # RGB 0–1 + Alpha
MANGO = (1, 0.541, 0.239, 1)
```

### Agregar más pedidos
Edita la lista `ORDERS` con objetos:
```python
{
    "id": "#PK-XXXX",
    "client": "Nombre Cliente",
    "priority": "Urgente",  # o "Normal"
    "items": 9,
    "time": "HH:MM a.m.",
    "products": [...]
}
```

### Agregar más pantallas
1. Crea una clase heredando de `Screen`
2. Agrégala a `ScreenManager` en `PickerApp.build()`
3. Usa `self.manager.current = "nombre_pantalla"` para navegar

---

## 8. NOTAS DE DESARROLLO

- **Responsive:** La app usa `size_hint` de Kivy para adaptarse a distintos tamaños
- **Datos en memoria:** Los datos de pedidos están hardcodeados. Para un backend real, usa API REST (requests + json)
- **Sin persistencia:** Los cambios se pierden al cerrar. Agrega SQLite para persistencia
- **Mapas reales:** Para integrar Google Maps, usa `MapView` de `kivy-garden`

---

## 9. TROUBLESHOOTING

### "ModuleNotFoundError: No module named 'kivy'"
```bash
pip install kivy --upgrade
```

### La app se ve mal en móvil
- Ajusta `Window.size` en la línea inicial
- Usa `size_hint_y/x` en lugar de `height/width` fijos

### El APK no se instala
- Verifica que el teléfono es Android 6+
- Desactiva "Verificar apps desconocidas" si la instalación falla

### Buildozer tarda mucho
- Primera compilación es lenta (~10–20 min)
- Las siguientes son más rápidas

---

## 10. PRÓXIMOS PASOS

1. **Backend:** Conectar a un servidor (Flask, Django, FastAPI)
2. **Autenticación real:** Login con credenciales contra base de datos
3. **Geolocalización:** GPS en tiempo real en el mapa
4. **WebSocket:** Sincronización en vivo de pedidos
5. **Notificaciones:** Push para nuevos pedidos urgentes
6. **Almacenamiento local:** SQLite para caché offline

---

¡La app está lista para probar! 🚀
