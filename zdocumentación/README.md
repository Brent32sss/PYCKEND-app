# 📱 PICKLY — App de Recolección para Picker

Aplicación móvil funcional para gestionar la recolección de productos en tienda. Construida con **Python + Kivy**, lista para correr en computadora o compilar a APK para Android.

---

## 📦 Archivos del Proyecto

### 1. **picker_app.py** ⭐
Código principal de la aplicación. Contiene:
- **LoginScreen** — Pantalla de autenticación
- **DashboardScreen** — Lista de pedidos asignados
- **ChecklistScreen** — Checklist interactivo de productos
- **MapScreen** — Mapa y ruta de la tienda
- **PickerApp** — Gestor de pantallas

**Para ejecutar:**
```bash
python picker_app.py
```

---

### 2. **SETUP_INSTRUCCIONES.md** 📖
Guía completa de instalación, configuración y uso:
- Cómo instalar dependencias
- Cómo correr la app en computadora
- Cómo compilar a APK (Android)
- Estructura del código
- Troubleshooting

---

### 3. **buildozer.spec** ⚙️
Archivo de configuración para compilar la app a APK:
- Nombre y versión de la app
- Permisos Android (GPS, cámara, internet)
- Configuración de NDK y API
- Para usarlo: `buildozer android debug`

---

### 4. **requirements.txt** 📋
Dependencias Python necesarias:
```
kivy==2.2.1
buildozer==1.5.0
cython==3.0.0
Pillow>=9.0.0
```
**Para instalar:**
```bash
pip install -r requirements.txt
```

---

### 5. **svg-picker/** 📐
Archivos SVG de las pantallas (anteriores):
- `01-login-picker.svg`
- `02-picker-dashboard.svg`
- `03-picker-checklist.svg`
- `04-picker-mapa.svg`

Útiles si quieres usar los diseños como referencia en Penpot o exportarlos a otros formatos.

---

### 6. **app-picking-delivery-prototipo.html** 🌐
Prototipo HTML interactivo del diseño (incluye Cliente + Picker). Puede usarse como referencia visual o para presentar el diseño en navegador.

---

## 🚀 Quick Start

### Opción 1: Ejecutar en Computadora
```bash
pip install kivy
python picker_app.py
```
Se abre una ventana simulando un móvil (375×812 px).

### Opción 2: Compilar a APK (Android)
```bash
pip install -r requirements.txt
buildozer android debug
```
Genera: `bin/pickly-0.1-debug.apk`

Instalar:
```bash
adb install bin/pickly-0.1-debug.apk
```

---

## 🎨 Paleta de Colores

| Nombre | Hex | Uso |
|--------|-----|-----|
| Forest | #1B4332 | Headers, botones principales |
| Mango | #FF8A3D | CTAs, ruta en mapa |
| Mint | #E7F1E8 | Fondo de campos, badges normales |
| Slate BG | #ECF0EE | Fondo general |
| Leaf | #2FA86A | Completado, checkmarks |
| Coral | #FF5A5F | Urgente, error |
| Charcoal | #1E2822 | Texto principal |

---

## 📱 Flujo de la App

```
1. LOGIN
   ↓
2. DASHBOARD (Pedidos asignados)
   ├─ Tap pedido
   ↓
3. CHECKLIST (Lista de productos)
   ├─ Checkbox interactivo
   ├─ Botón "Ver ruta"
   ↓
4. MAPA (Ruta y posición)
   └─ Botón "Marcar como recolectado"
```

---

## 🔧 Estructura Técnica

```
PickerApp (Kivy App)
├── ScreenManager (gestor de pantallas)
│   ├── LoginScreen
│   ├── DashboardScreen
│   │   └── OrderCard (componente)
│   │   └── NavItem (componente)
│   ├── ChecklistScreen
│   │   └── ProductItem (componente interactivo)
│   └── MapScreen
│       └── MapCanvas (canvas SVG-like)
└── Data Layer
    ├── PICKER_DATA (datos del usuario)
    └── ORDERS (lista de pedidos)
```

---

## 🎯 Funcionalidades Implementadas

✅ Login funcional  
✅ Dashboard con lista de pedidos  
✅ Checklist interactivo (checkboxes)  
✅ Filtro visual (ítems recolectados se opacifican)  
✅ Mapa simplificado de tienda (grid de pasillos A–H)  
✅ Ruta optimizada (línea punteada)  
✅ Posición actual (punto pulsante)  
✅ Navegación entre pantallas  
✅ Responsive (adaptable a cualquier tamaño)  

---

## 🚧 Funcionalidades Futuras (TODO)

- [ ] Autenticación real (backend login)
- [ ] Geolocalización en tiempo real (GPS)
- [ ] WebSocket para pedidos en vivo
- [ ] Persistencia local (SQLite)
- [ ] Notificaciones push
- [ ] Historial de recolecciones
- [ ] Perfil de usuario
- [ ] Sincronización offline
- [ ] Mapa interactivo (Google Maps / Leaflet)
- [ ] Foto de productos recolectados

---

## 📊 Datos de Ejemplo

### Picker
```python
{
    "name": "Jacob Torres",
    "role": "Picker · Tienda San Isidro",
    "shift": "Turno tarde",
    "stats": {
        "asignados": 5,
        "urgentes": 2,
        "puntualidad": "92%"
    }
}
```

### Orden
```python
{
    "id": "#PK-4821",
    "client": "Valeria R.",
    "priority": "Urgente",  # o "Normal"
    "items": 9,
    "time": "10:30 a.m.",
    "products": [
        {
            "name": "Palta hass",
            "location": "Pasillo A · Estante 3 · Nivel 2",
            "qty": "1 kg",
            "done": False
        },
        # ... más productos
    ]
}
```

---

## 🔐 Seguridad

- ⚠️ Las credenciales de login están hardcodeadas (solo demo)
- ⚠️ No hay encriptación de datos
- Para producción: integrar con servidor seguro + JWT/OAuth2

---

## 📞 Soporte

Cualquier pregunta sobre:
- Instalación → Ver `SETUP_INSTRUCCIONES.md`
- Compilación → Consultar Buildozer docs
- Personalización → Editar `picker_app.py` directo

---

## 📄 Licencia

Este proyecto es de demostración educativa. Libre para usar y modificar.

---

**¡Lista para usar! 🚀**

Para empezar: `python picker_app.py`
