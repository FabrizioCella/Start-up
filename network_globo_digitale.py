import folium
from folium.plugins import AntPath

# --- BASE URL DELLE IMMAGINI SU GITHUB ---
base_url = "https://fabriziocella.github.io/Start-up/"

# Dati partner
stakeholders = [
    {
        "name": "PLAS_TEAM",
        "lat": 43.715, "lon": 10.401,
        "role": "Ricercatore",
        "descr": (
            "Si occupa di ricerca su sistemi zootecnici, agroforestazione, uso di sottoprodotti "
            "di origine agroindustriale, laboratorio associato per analisi dei foraggi, determinazione "
            "degli antiossidanti nelle carni e formaggi, e profilazione degli acidi grassi in prodotti di origine animale. "
            "Sviluppo di approcci partecipativi per la ricerca scientifica."
        ),
        "location": "Pisa, Università degli Studi di Pisa",
        "img": base_url + "plas_team.png"
    },
    {
        "name": "Caseificio Sociale di Manciano",
        "lat": 42.534, "lon": 11.504,
        "role": "Cooperativa",
        "descr": (
            "Rappresenta 200 aziende e lavora 10 milioni di litri di latte di pecora all'anno "
            "per la produzione di formaggi freschi e stagionati. Il prodotto di punta è il Pecorino del Cuore, "
            "risultato della ricerca in collaborazione con PLAS_TEAM."
        ),
        "location": "Manciano, Grosseto",
        "img": base_url + "caseificio.png"
    },
    {
        "name": "Consorzio Pecorino Toscano DOP",
        "lat": 42.763, "lon": 11.113,
        "role": "Consorzio di valorizzazione",
        "descr": (
            "Si occupa di controllare il rispetto del disciplinare di produzione, organizzare corsi di aggiornamento "
            "per gli allevatori del circuito e creare progetti di valorizzazione e marketing."
        ),
        "location": "Grosseto, Toscana",
        "img": base_url + "pecorino.png"
    },
    {
        "name": "Tenuta di Paganico",
        "lat": 42.833, "lon": 11.225,
        "role": "Azienda agricola",
        "descr": (
            "Produce carne bovina di razza Amaremmana allevata in sistema silvopastorale. Presenta anche un ristorante "
            "ed è attiva come azienda in diversi progetti di ricerca."
        ),
        "location": "Paganico, Grosseto",
        "img": base_url + "paganico.png"
    }
]

# Colori per ruolo/categoria
role_colors = {
    "Ricercatore": "cyan",
    "Cooperativa": "magenta",
    "Consorzio di valorizzazione": "orange",  # più visibile
    "Azienda agricola": "lime"
}

popup_text_color = "black"

# Crea mappa
m = folium.Map(location=[43.0, 11.0], zoom_start=7, tiles='CartoDB dark_matter')

# CSS globale per marker pulsanti
css = """
<style>
.glow-marker {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  animation: pulse 1.5s infinite;
}
@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.5); }
  100% { transform: scale(1); }
}
</style>
"""
m.get_root().html.add_child(folium.Element(css))

# Aggiungi marker con popup
for s in stakeholders:
    color = role_colors.get(s["role"], "cyan")
    
    marker_html = f"""
    <div class="glow-marker" style="
        background:{color};
        box-shadow: 0 0 10px {color}, 0 0 20px {color};
    "></div>
    """
    
    html_popup = f"""
    <div style="text-align:left; color:{popup_text_color}; width:250px;">
        <h4 style="color:{color};">{s['name']}</h4>
        <b>Ruolo:</b> {s['role']}<br>
        <b>Luogo:</b> {s['location']}<br>
        <b>Breve descrizione:</b> {s['descr']}<br>
        <img src="{s['img']}" width="150px" style="margin-top:5px;">
    </div>
    """
    
    popup = folium.Popup(html_popup, max_width=300)
    folium.Marker(
        location=[s["lat"], s["lon"]],
        icon=folium.DivIcon(html=marker_html),
        popup=popup
    ).add_to(m)

# Connessioni animate tra partner
connections = [
    ("PLAS_TEAM", "Consorzio Pecorino Toscano DOP"),
    ("PLAS_TEAM", "Caseificio Sociale di Manciano"),
    ("Caseificio Sociale di Manciano", "Consorzio Pecorino Toscano DOP"),
    ("PLAS_TEAM", "Tenuta di Paganico")
]

for c in connections:
    start = next(s for s in stakeholders if s["name"] == c[0])
    end = next(s for s in stakeholders if s["name"] == c[1])
    
    AntPath(
        locations=[[start["lat"], start["lon"]], [end["lat"], end["lon"]]],
        color='cyan',
        weight=3,
        opacity=0.8,
        delay=1000
    ).add_to(m)

# Salva la mappa HTML
save_path = r"C:\Users\fabri\Desktop\SPINN_OFF\network_2d_partner_interactive.html"
m.save(save_path)

print(f"✅ Mappa salvata: {save_path}")
