"""
inventario.py - Módulo de datos y consultas del minimarket
"""

# Tuplas con los 100 productos:
# (ID, Producto, Categoría, Stock, Precio, Pasillo, Estante, Nivel)
_RAW_DATA = [
    ("P001", "Agua San Luis 625 ml", "Bebidas", 24, 2.0, "P01", "E01", 1),
    ("P002", "Agua San Luis 1.5 L", "Bebidas", 18, 3.5, "P01", "E01", 2),
    ("P003", "Agua Cielo 625 ml", "Bebidas", 20, 1.8, "P01", "E01", 3),
    ("P004", "Coca-Cola 500 ml", "Gaseosas", 22, 3.5, "P01", "E02", 1),
    ("P005", "Coca-Cola 1.5 L", "Gaseosas", 12, 6.5, "P01", "E02", 2),
    ("P006", "Inca Kola 500 ml", "Gaseosas", 21, 3.5, "P01", "E03", 1),
    ("P007", "Inca Kola 1.5 L", "Gaseosas", 14, 6.5, "P01", "E03", 2),
    ("P008", "Pepsi 500 ml", "Gaseosas", 15, 3.0, "P01", "E03", 3),
    ("P009", "Sprite 500 ml", "Gaseosas", 13, 3.5, "P01", "E04", 1),
    ("P010", "Fanta 500 ml", "Gaseosas", 11, 3.5, "P01", "E04", 2),
    ("P011", "Red Bull 250 ml", "Energizantes", 16, 8.5, "P02", "E01", 1),
    ("P012", "Monster Energy 473 ml", "Energizantes", 10, 9.5, "P02", "E01", 2),
    ("P013", "Gatorade 500 ml", "Deportivas", 14, 4.5, "P02", "E02", 1),
    ("P014", "Sporade 500 ml", "Deportivas", 18, 3.0, "P02", "E02", 2),
    ("P015", "Powerade 500 ml", "Deportivas", 12, 4.0, "P02", "E02", 3),
    ("P016", "Pilsen Callao 355 ml", "Bebidas", 30, 4.5, "P02", "E03", 1),
    ("P017", "Cusqueña Dorada 330 ml", "Bebidas", 20, 6.0, "P02", "E03", 2),
    ("P018", "Cerveza Corona 355 ml", "Bebidas", 15, 7.0, "P02", "E03", 3),
    ("P019", "Papas Lays Clásicas", "Snacks", 17, 5.5, "P03", "E01", 1),
    ("P020", "Papas Lays Onduladas", "Snacks", 13, 5.5, "P03", "E01", 2),
    ("P021", "Doritos Nacho", "Snacks", 15, 5.5, "P03", "E01", 3),
    ("P022", "Chizitos", "Snacks", 12, 3.5, "P03", "E02", 1),
    ("P023", "Cheese Tris", "Snacks", 14, 3.5, "P03", "E02", 2),
    ("P024", "Cheetos", "Snacks", 11, 4.0, "P03", "E02", 3),
    ("P025", "Inka Chips", "Snacks", 10, 5.0, "P03", "E03", 1),
    ("P026", "Pringles Original", "Snacks", 9, 10.5, "P03", "E03", 2),
    ("P027", "Maní Salado", "Snacks", 16, 3.5, "P03", "E03", 3),
    ("P028", "Chocolate Sublime", "Chocolates", 25, 2.5, "P04", "E01", 1),
    ("P029", "Chocolate Princesa", "Chocolates", 20, 2.5, "P04", "E01", 2),
    ("P030", "Chocolate Triángulo", "Chocolates", 18, 2.5, "P04", "E01", 3),
    ("P031", "Kit Kat 41.5 g", "Chocolates", 15, 4.5, "P04", "E02", 1),
    ("P032", "Snickers 50 g", "Chocolates", 14, 4.0, "P04", "E02", 2),
    ("P033", "M&M's Chocolate", "Golosinas", 13, 4.5, "P04", "E02", 3),
    ("P034", "Oreo Original", "Galletas", 18, 4.5, "P04", "E03", 1),
    ("P035", "Casino Chocolate", "Galletas", 20, 2.5, "P04", "E03", 2),
    ("P036", "Casino Fresa", "Galletas", 17, 2.5, "P04", "E03", 3),
    ("P037", "Morochas", "Galletas", 16, 2.5, "P04", "E04", 1),
    ("P038", "Ritz Original", "Galletas", 12, 4.5, "P04", "E04", 2),
    ("P039", "Soda Field", "Galletas", 15, 2.0, "P04", "E04", 3),
    ("P040", "Pan de molde blanco", "Panificados", 12, 7.5, "P05", "E01", 1),
    ("P041", "Pan integral", "Panificados", 10, 8.5, "P05", "E01", 2),
    ("P042", "Croissant mantequilla", "Panificados", 8, 4.5, "P05", "E02", 1),
    ("P043", "Muffin chocolate", "Panificados", 9, 5.0, "P05", "E02", 2),
    ("P044", "Donut azúcar", "Panificados", 11, 3.5, "P05", "E02", 3),
    ("P045", "Yogurt Gloria Fresa", "Lácteos", 14, 4.5, "P05", "E03", 1),
    ("P046", "Yogurt Gloria Vainilla", "Lácteos", 12, 4.5, "P05", "E03", 2),
    ("P047", "Leche Gloria 1 L", "Lácteos", 20, 4.5, "P05", "E04", 1),
    ("P048", "Leche Laive 1 L", "Lácteos", 16, 4.8, "P05", "E04", 2),
    ("P049", "Jamón de pavita", "Refrigerados", 8, 9.5, "P06", "E01", 1),
    ("P050", "Queso Edam", "Refrigerados", 7, 12.0, "P06", "E01", 2),
    ("P051", "Queso fresco", "Refrigerados", 8, 9.5, "P06", "E01", 3),
    ("P052", "Hot Dog San Fernando", "Refrigerados", 10, 8.5, "P06", "E02", 1),
    ("P053", "Nuggets de pollo", "Congelados", 9, 13.5, "P06", "E02", 2),
    ("P054", "Hamburguesa de pollo", "Congelados", 8, 12.5, "P06", "E02", 3),
    ("P055", "Atún Primor", "Conservas", 13, 6.5, "P07", "E01", 1),
    ("P056", "Atún Florida", "Conservas", 11, 7.0, "P07", "E01", 2),
    ("P057", "Sardinas en tomate", "Conservas", 8, 5.5, "P07", "E01", 3),
    ("P058", "Mayonesa Alacena", "Salsas", 10, 7.5, "P07", "E02", 1),
    ("P059", "Ketchup Alacena", "Salsas", 9, 6.5, "P07", "E02", 2),
    ("P060", "Mostaza Alacena", "Salsas", 8, 5.5, "P07", "E02", 3),
    ("P061", "Ají Tarí", "Salsas", 10, 5.0, "P07", "E03", 1),
    ("P062", "Salsa de tomate", "Salsas", 9, 5.5, "P07", "E03", 2),
    ("P063", "Café instantáneo 100 g", "Despensa", 12, 12.5, "P08", "E01", 1),
    ("P064", "Café Altomayo 100 g", "Despensa", 10, 10.5, "P08", "E01", 2),
    ("P065", "Azúcar rubia 1 kg", "Despensa", 10, 5.0, "P08", "E02", 1),
    ("P066", "Arroz Costeño 1 kg", "Despensa", 12, 5.5, "P08", "E02", 2),
    ("P067", "Fideos Don Vittorio", "Despensa", 11, 4.5, "P08", "E03", 1),
    ("P068", "Avena Quaker", "Despensa", 9, 7.5, "P08", "E03", 2),
    ("P069", "Atún con verduras", "Conservas", 7, 7.5, "P08", "E03", 3),
    ("P070", "Sopa instantánea Ajinomen", "Despensa", 15, 3.0, "P08", "E04", 1),
    ("P071", "Detergente Bolívar", "Limpieza", 8, 7.5, "P09", "E01", 1),
    ("P072", "Detergente Ariel pequeño", "Limpieza", 7, 8.5, "P09", "E01", 2),
    ("P073", "Lavavajilla Ayudín", "Limpieza", 10, 5.5, "P09", "E02", 1),
    ("P074", "Lejía Clorox 1 L", "Limpieza", 8, 5.0, "P09", "E02", 2),
    ("P075", "Limpiador Poett", "Limpieza", 9, 6.5, "P09", "E03", 1),
    ("P076", "Esponja Scotch-Brite", "Limpieza", 12, 4.0, "P09", "E03", 2),
    ("P077", "Papel higiénico Elite x4", "Higiene", 14, 9.5, "P09", "E04", 1),
    ("P078", "Papel toalla Elite", "Higiene", 10, 8.5, "P09", "E04", 2),
    ("P079", "Servilletas Elite", "Higiene", 15, 4.0, "P09", "E04", 3),
    ("P080", "Jabón Dove", "Higiene personal", 11, 5.5, "P10", "E01", 1),
    ("P081", "Shampoo Head & Shoulders", "Higiene personal", 8, 18.5, "P10", "E01", 2),
    ("P082", "Shampoo Pantene", "Higiene personal", 9, 16.5, "P10", "E02", 1),
    ("P083", "Pasta dental Colgate", "Higiene personal", 13, 7.5, "P10", "E02", 2),
    ("P084", "Cepillo dental Colgate", "Higiene personal", 12, 8.5, "P10", "E02", 3),
    ("P085", "Desodorante Rexona", "Higiene personal", 10, 11.5, "P10", "E03", 1),
    ("P086", "Desodorante Dove", "Higiene personal", 9, 12.5, "P10", "E03", 2),
    ("P087", "Pañuelos Elite", "Higiene", 15, 3.5, "P10", "E04", 1),
    ("P088", "Pilas Duracell AA x2", "Accesorios", 8, 12.0, "P10", "E04", 2),
    ("P089", "Encendedor", "Accesorios", 10, 3.5, "P10", "E04", 3),
    ("P090", "Chicle Trident menta", "Golosinas", 20, 2.5, "P11", "E01", 1),
    ("P091", "Chicle Trident fresa", "Golosinas", 18, 2.5, "P11", "E01", 2),
    ("P092", "Halls menta", "Golosinas", 17, 2.0, "P11", "E02", 1),
    ("P093", "Halls cereza", "Golosinas", 15, 2.0, "P11", "E02", 2),
    ("P094", "Caramelos Ambrosoli", "Golosinas", 16, 3.0, "P11", "E03", 1),
    ("P095", "Barra de cereal Ángel", "Snacks", 13, 3.5, "P11", "E03", 2),
    ("P096", "Granola Nature Valley", "Snacks", 10, 7.5, "P11", "E04", 1),
    ("P097", "Galleta integral", "Galletas", 12, 4.0, "P11", "E04", 2),
    ("P098", "Cereal Zucaritas personal", "Cereales", 9, 6.5, "P12", "E01", 1),
    ("P099", "Cereal Chocapic personal", "Cereales", 8, 6.5, "P12", "E01", 2),
    ("P100", "Chocolate Milky Way", "Chocolates", 14, 4.5, "P12", "E02", 1),
]

# Estructura principal accesible por clave
PRODUCTOS = [
    {
        "id": r[0],
        "nombre": r[1],
        "categoria": r[2],
        "stock": r[3],
        "precio": r[4],
        "pasillo": r[5],
        "estante": r[6],
        "nivel": r[7],
        "ubicacion": f"{r[5]}-{r[6]}-N{r[7]}"
    }
    for r in _RAW_DATA
]

# Zonas operativas del plano [nombre, x, ancho, color_hex]
ZONAS_OPERATIVAS = [
    {"nombre": "Entrada / Salida", "x": 20, "ancho": 140, "color": "#cfd8dc"},
    {"nombre": "Cajas", "x": 170, "ancho": 230, "color": "#ffe0b2"},
    {"nombre": "Zona de picking", "x": 410, "ancho": 280, "color": "#fff59d"},
    {"nombre": "Recepción", "x": 700, "ancho": 280, "color": "#b2dfdb"},
]

# Paleta de colores de los 12 pasillos
COLORES_PASILLOS = [
    "#c8e6c9", "#bbdefb", "#fff9c4", "#f8bbd0",
    "#e1bee7", "#b3e5fc", "#ffe0b2", "#d7ccc8",
    "#dcedc8", "#ffccbc", "#c5cae9", "#b2dfdb"
]

def normalizar_texto(texto: str) -> str:
    """Elimina acentos y pasa a minúsculas para comparaciones flexibles."""
    import unicodedata
    return "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    ).lower()

def buscar_productos(termino: str) -> list:
    """Busca productos por coincidencia en nombre, ID o categoría."""
    q = normalizar_texto(termino.strip())
    if not q:
        return []
    return [
        p for p in PRODUCTOS
        if q in normalizar_texto(f"{p['nombre']} {p['id']} {p['categoria']}")
    ]

def obtener_por_pasillo(pasillo: str, estante: str = None) -> list:
    """Retorna los productos filtrados por pasillo (ej. 'P01') y estante opcional."""
    return [
        p for p in PRODUCTOS
        if p["pasillo"] == pasillo and (estante is None or p["estante"] == estante)
    ]

def obtener_resumen_pasillos() -> list:
    """Retorna la lista de pasillos con sus categorías, cantidad y color para el menú."""
    pasillos = sorted(list({p["pasillo"] for p in PRODUCTOS}))
    resumen = []
    for i, p_code in enumerate(pasillos):
        prods = [p for p in PRODUCTOS if p["pasillo"] == p_code]
        cats = sorted(list({p["categoria"] for p in prods}))
        max_estante = max(int(p["estante"].replace("E", "")) for p in prods)
        resumen.append({
            "pasillo": p_code,
            "categorias": cats,
            "total_productos": len(prods),
            "max_estante": max_estante,
            "color": COLORES_PASILLOS[i % len(COLORES_PASILLOS)],
            "x": 20 + i * 80
        })
    return resumen