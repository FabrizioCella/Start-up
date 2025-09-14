from pyvis.network import Network

# Creiamo la rete digitale
net = Network(height="750px", width="100%", bgcolor="#111111", font_color="white")

# Lista degli stakeholder con immagini e città
stakeholders = [
    {"nome": "Plast-Team", "tipo": "Partner", "citta": "Pisa", "immagine": "C:/Users/fabri/Desktop/immagini/plast_team.jpg"},
    {"nome": "Consorzio Pecorino Toscano DOP", "tipo": "Partner", "citta": "Grosseto", "immagine": "C:/Users/fabri/Desktop/immagini/pecorino_toscano.jpg"},
    {"nome": "Caseificio Sociale di Manciano", "tipo": "Partner", "citta": "Manciano", "immagine": "C:/Users/fabri/Desktop/immagini/caseificio_manciano.jpg"}
]

# Aggiungiamo i nodi con immagini
for s in stakeholders:
    net.add_node(
        s["nome"],
        label=s["nome"],
        title=f"{s['tipo']} - {s['citta']}",
        shape="image",
        image=s["immagine"],
        size=40
    )

# Connessioni tra stakeholder
edges = [
    ("Plast-Team", "Consorzio Pecorino Toscano DOP"),
    ("Consorzio Pecorino Toscano DOP", "Caseificio Sociale di Manciano"),
    ("Plast-Team", "Caseificio Sociale di Manciano")
]
for e in edges:
    net.add_edge(e[0], e[1])

# Salviamo l'HTML
net.show("network_partner.html")
