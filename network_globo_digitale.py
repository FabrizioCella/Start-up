import folium
from folium.plugins import AntPath, Fullscreen
import os

# -------------------------
# Dati dei partner
# -------------------------
stakeholders = [
    {
        "name": "PLAS_TEAM",
        "lat": 43.715, "lon": 10.401,
        "role": "Ricercatore",
        "descr": "Si occupa di ricerca su sistemi zootecnici, agroforestazione,"
                 "uso di sottoprodotti di origine agroindustriale, laboratorio associato per analisi dei foraggi, "
                 "determinazione degli antiossidanti nelle carni e formaggi, e profilazione degli acidi grassi in prodotti di origine animale. "
                 "Sviluppo di approcci partecipativi per la ricerca scientifica",
        "location": "Pisa, Università degli Studi di Pisa",
        "img": "https://fabriziocella.github.io/Start-up/plas_team.png"
    },
    {
        "name": "Caseificio Sociale di Manciano",
        "lat": 42.534, "lon": 11.504,
        "role": "Cooperativa",
        "descr": "Rappresenta 200 aziende e lavora 10 milioni di litri di latte di pecora all'anno per la produzione di formaggi freschi e stagionati."
                 "Il prodotto di punta è il Pecorino del Cuore, risultato della ricerca in collaborazione con PLAS_TEAM",
        "location": "Manciano, Grosseto",
        "img": "https://fabriziocella.github.io/Start-up/caseificio.png"
    },
    {
        "name": "Consorzio Pecorino Toscano DOP",
        "lat": 42.763, "lon": 11.113,
        "role": "Consorzio di valorizzazione",
        "descr": "Si occupa di controllare il rispetto del disciplinare di produzione,"
                 "organizzare corsi di aggiornamento per gli allevatori del circuito e creare progetti di valorizzazione e marketing",
        "location": "Grosseto, Toscana",
        "img": "https://fabriziocella.github.io/Start-up/pecorino.png"
    },
    {
        "name": "Tenuta di Paganico",
        "lat": 42.833, "lon": 11.225,
        "role": "Azienda agricola",
        "descr": "Produce carne bovina di razza Maremmana allevata in sistema silvopastorale...",
        "location": "Paganico, Grosseto",
        "img": "https://fabriziocella.github.io/Start-up/paganico.png"
    },
    {
        "name": "Oikos - Innovation for sustainable rural development",
        "lat": 43.769, "lon": 11.255,  # Firenze
        "role": "Innovation Broker",
        "descr": "Supporta lo sviluppo rurale sostenibile attraverso ricerca, networking tra stakeholder e implementazione di soluzioni innovative.",
        "location": "Firenze, Toscana",
        "img": "https://fabriziocella.github.io/Start-up/oikos.jpg"
    }
]

# -------------------------
# Colori dei marker
# -------------------------
role_colors = {
    "Ricercatore": "cyan",
    "Cooperativa": "magenta",
    "Consorzio di valorizzazione": "orange",
    "Azienda agricola": "lime",
    "Innovation Broker": "red"  # colore rosso per Oikos
}

# -------------------------
# Crea la mappa
# -------------------------
m = folium.Map(location=[43.0, 11.0], zoom_start=7, tiles='CartoDB dark_matter')
Fullscreen(position='topright').add_to(m)

# -------------------------
# CSS per marker pulsanti
# -------------------------
css = """
<style>
.glow-marker {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  animation: pulse 1.5s infinite;
}
@keyframes pulse {
  0% { transform: scale(1); opacity: 0.7; }
  50% { transform: scale(1.5); opacity: 1; }
  100% { transform: scale(1); opacity: 0.7; }
}
</style>
"""
m.get_root().html.add_child(folium.Element(css))

# -------------------------
# Aggiungi marker con popup
# -------------------------
for s in stakeholders:
    color = role_colors.get(s["role"], "cyan")
    
    marker_html = f"""
    <div class="glow-marker" style="
        background:{color};
        box-shadow: 0 0 10px {color}, 0 0 20px {color};
    "></div>
    """
    
    html_popup = f"""
    <div style="text-align:left; background: rgba(255,255,255,0.9); 
                padding:10px; border-radius:8px; max-width:250px;">
        <h4 style="color:{color}; margin-bottom:5px;">{s['name']}</h4>
        <b>Ruolo:</b> {s['role']}<br>
        <b>Luogo:</b> {s['location']}<br>
        <b>Breve descrizione:</b> {s['descr']}<br>
        <img src="{s['img']}" style="width:100%; height:auto; margin-top:5px; border-radius:4px;">
    </div>
    """
    
    popup = folium.Popup(html_popup, max_width=300)
    
    folium.Marker(
        location=[s["lat"], s["lon"]],
        icon=folium.DivIcon(html=marker_html),
        popup=popup
    ).add_to(m)

# -------------------------
# Connessioni animate tra partner (stile digitale)
# -------------------------
connections = [
    ("PLAS_TEAM", "Consorzio Pecorino Toscano DOP"),
    ("PLAS_TEAM", "Caseificio Sociale di Manciano"),
    ("Caseificio Sociale di Manciano", "Consorzio Pecorino Toscano DOP"),
    ("PLAS_TEAM", "Tenuta di Paganico"),
    ("Oikos - Innovation for sustainable rural development", "PLAS_TEAM"),
    ("Oikos - Innovation for sustainable rural development", "Caseificio Sociale di Manciano"),
    ("Oikos - Innovation for sustainable rural development", "Consorzio Pecorino Toscano DOP"),
    ("Oikos - Innovation for sustainable rural development", "Tenuta di Paganico")
]

# Trasforma stakeholders in dizionario per lookup rapido
stake_dict = {s["name"]: s for s in stakeholders}

for start_name, end_name in connections:
    start = stake_dict.get(start_name)
    end = stake_dict.get(end_name)

    if not start or not end:
        continue

    AntPath(
        locations=[[start["lat"], start["lon"]], [end["lat"], end["lon"]]],
        color="cyan",          
        weight=4,              
        opacity=0.9,           
        dash_array=[10, 20],   
        delay=600              
    ).add_to(m)

# -------------------------
# Salva il file HTML
# -------------------------
save_path = r"C:\Users\fabri\Desktop\SPINN_OFF"
os.makedirs(save_path, exist_ok=True)
file_name = "network_2d_partner_interactive.html"
full_path = os.path.join(save_path, file_name)

m.save(full_path)
print(f"✅ Mappa salvata: {full_path}")
