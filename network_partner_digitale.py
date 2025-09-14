import folium
from folium import IFrame
import base64
import os

# Cartella dove si trovano immagini e script
base_path = "C:/Users/fabri/Desktop/SPINN_OFF"

# Dati dei partner con percorso assoluto delle immagini
stakeholders = {
    "PLAS_TEAM": {"coords": [43.715, 10.401], "descr": "Researcher", "img": os.path.join(base_path, "plas_team.png")},
    "Consorzio Pecorino Toscano DOP": {"coords": [42.763, 11.113], "descr": "Consorzio di valorizzazione", "img": os.path.join(base_path, "pecorino.png")},
    "Caseificio Sociale di Manciano": {"coords": [42.534, 11.504], "descr": "Azienda", "img": os.path.join(base_path, "caseificio.png")}
}

# Crea mappa scura
m = folium.Map(location=[43.0, 11.0], zoom_start=6, tiles="CartoDB dark_matter")

# Marker pulsanti con popup (immagini in base64)
for name, info in stakeholders.items():
    # Converti immagine in base64
    with open(info['img'], "rb") as f:
        img_data = f.read()
    img_base64 = base64.b64encode(img_data).decode()

    html = f"""
    <div style="text-align:center;">
        <h4 style="color: cyan;">{name}</h4>
        <p style="color:white;">{info['descr']}</p>
        <img src="data:image/png;base64,{img_base64}" width="120">
    </div>
    """
    iframe = IFrame(html, width=160, height=200)
    popup = folium.Popup(iframe, max_width=200)

    icon_html = f"""
    <div class="pulsing-marker"></div>
    """
    icon = folium.DivIcon(html=icon_html)

    folium.Marker(
        location=info["coords"],
        popup=popup,
        icon=icon
    ).add_to(m)

# Connessioni tra partner
connections = [
    ("PLAS_TEAM", "Consorzio Pecorino Toscano DOP"),
    ("Consorzio Pecorino Toscano DOP", "Caseificio Sociale di Manciano"),
    ("PLAS_TEAM", "Caseificio Sociale di Manciano")
]

for a, b in connections:
    folium.PolyLine(
        locations=[stakeholders[a]["coords"], stakeholders[b]["coords"]],
        color="cyan",
        weight=2,
        opacity=0.6,
    ).add_to(m)

# CSS per marker luminosi/pulsanti
css = """
<style>
.pulsing-marker {
  width: 20px;
  height: 20px;
  background: cyan;
  border-radius: 50%;
  box-shadow: 0 0 10px cyan;
  animation: pulse 1.5s infinite;
}
@keyframes pulse {
  0% { transform: scale(0.8); opacity: 0.7; }
  50% { transform: scale(1.3); opacity: 1; }
  100% { transform: scale(0.8); opacity: 0.7; }
}
</style>
"""
m.get_root().header.add_child(folium.Element(css))

# Salva HTML finale
output_file = os.path.join(base_path, "mappa_interattiva_finale.html")
m.save(output_file)
print(f"HTML generato! Apri '{output_file}' nel browser")
