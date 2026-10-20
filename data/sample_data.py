# data/sample_data.py

from datetime import datetime

PICKER_DATA = {
    "name": "Jacob Torres",
    "photo": "🧭",
    "role": "Picker · Tienda San Isidro",
    "shift": "Turno tarde",
    "notifications": 2,
    "stats": {"asignados": 5, "urgentes": 2, "puntualidad": "92%"},
}

# Mapa base según tu JSON
STORE_MAP = {
    "ENT": {"name": "Entrada / Salida", "cat": "Acceso"},
    "CAJ": {"name": "Cajas", "cat": "Punto de venta"},
    "REF": {"name": "Refrigeradores", "cat": "Lácteos y bebidas frías"},
    "G1": {"name": "Góndola 1", "cat": "Abarrotes secos"},
    "G2": {"name": "Góndola 2", "cat": "Snacks y galletas"},
    "G3": {"name": "Góndola 3", "cat": "Limpieza y cuidado"},
    "PAN": {"name": "Panes y frutas", "cat": "Perecibles"},
    "BOD": {"name": "Bodega (almacén)", "cat": "Stock de reposición"},
    "REC": {"name": "Recepción", "cat": "Ingreso de mercadería"}
}

ORDERS = [
    {
        "id": "#PK-4821",
        "client": "Valeria R.",
        "priority": "Urgente",
        "items": 5,
        "time": "10:30 a.m.",
        "products": [
            {"name": "Leche 1L", "sku": "LAC-001", "location": "Refrigeradores · Estante 1", "qty": "2 u.", "done": False, "zone": "REF"},
            {"name": "Arroz 1kg", "sku": "ABA-001", "location": "Góndola 1 · Estante 1", "qty": "3 kg", "done": False, "zone": "G1"},
            {"name": "Galletas", "sku": "SNA-002", "location": "Góndola 2 · Estante 1", "qty": "4 paq.", "done": False, "zone": "G2"},
            {"name": "Papel higiénico", "sku": "LIM-004", "location": "Góndola 3 · Estante 1", "qty": "1 paq.", "done": False, "zone": "G3"},
            {"name": "Manzana", "sku": "PER-008", "location": "Panes y frutas · Estante 2", "qty": "2 kg", "done": False, "zone": "PAN"},
        ]
    },
    {
        "id": "#PK-4809",
        "client": "Marco L.",
        "priority": "Normal",
        "items": 3,
        "time": "11:15 a.m.",
        "products": [
            {"name": "Gaseosa 2L", "sku": "BEB-003", "location": "Refrigeradores · Estante 2", "qty": "2 u.", "done": False, "zone": "REF"},
            {"name": "Detergente", "sku": "LIM-001", "location": "Góndola 3 · Estante 1", "qty": "1 u.", "done": False, "zone": "G3"},
            {"name": "Bolsas", "sku": "BOL-001", "location": "Cajas · Estante 1", "qty": "1 u.", "done": False, "zone": "CAJ"},
        ]
    }
]

# Lista dinámica para pedidos completados en la sesión actual
COMPLETED_ORDERS = [
    {"id": "#PK-4780", "client": "Carlos M.", "items": "8 productos", "time": "09:45 a.m.", "duration": "12 min"},
    {"id": "#PK-4752", "client": "Elena P.", "items": "5 productos", "time": "09:10 a.m.", "duration": "8 min"},
    {"id": "#PK-4711", "client": "Roberto G.", "items": "14 productos", "time": "08:30 a.m.", "duration": "18 min"},
]

def complete_order(order_dict):
    """Mueve un pedido de ORDERS a COMPLETED_ORDERS y actualiza stats"""
    if order_dict in ORDERS:
        ORDERS.remove(order_dict)
        
        # Calcular un tiempo simulado de recolección (ej. 15 mins)
        now = datetime.now()
        current_time = now.strftime("%I:%M %p").lower().replace("am", "a.m.").replace("pm", "p.m.")
        
        completed_entry = {
            "id": order_dict["id"],
            "client": order_dict["client"],
            "items": f"{order_dict['items']} productos",
            "time": current_time,
            "duration": "15 min" # Para la demo lo dejamos fijo
        }
        
        # Lo insertamos al principio de la lista del historial
        COMPLETED_ORDERS.insert(0, completed_entry)
        
        # Actualizamos stats
        PICKER_DATA["stats"]["asignados"] = max(0, PICKER_DATA["stats"]["asignados"] - 1)
        if order_dict["priority"] == "Urgente":
            PICKER_DATA["stats"]["urgentes"] = max(0, PICKER_DATA["stats"]["urgentes"] - 1)
            
 # Catálogo e inventario general de la tienda
STORE_INVENTORY = [
    {
        "sku": "LAC-001",
        "name": "Leche 1L",
        "zone": "REF",
        "location": "REF · Estante 1, nivel A",
        "stock": 36,
    },
    {
        "sku": "ABA-001",
        "name": "Arroz 1kg",
        "zone": "G1",
        "location": "G1 · Estante 1, nivel B",
        "stock": 50,
    },
    {
        "sku": "SNA-002",
        "name": "Galletas",
        "zone": "G2",
        "location": "G2 · Estante 1, nivel A",
        "stock": 24,
    },
    {
        "sku": "LIM-004",
        "name": "Papel higiénico",
        "zone": "G3",
        "location": "G3 · Estante 1, nivel C",
        "stock": 18,
    },
    {
        "sku": "PER-008",
        "name": "Manzana",
        "zone": "PAN",
        "location": "PAN · Estante 2, nivel A",
        "stock": 42,
    },
    {
        "sku": "BEB-003",
        "name": "Gaseosa 2L",
        "zone": "REF",
        "location": "REF · Estante 2, nivel B",
        "stock": 20,
    },
    {
        "sku": "LIM-001",
        "name": "Detergente",
        "zone": "G3",
        "location": "G3 · Estante 1, nivel A",
        "stock": 12,
    },
    {
        "sku": "BOL-001",
        "name": "Bolsas",
        "zone": "CAJ",
        "location": "CAJ · Estante 1",
        "stock": 150,
    },
]            