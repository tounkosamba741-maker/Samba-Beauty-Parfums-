
from flask import Flask, request, redirect, render_template_string
from urllib.parse import quote
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DB = "samba_beauty.db"

# NUMERO WHATSAPP PROFESSIONNEL
WHATSAPP = "22383899524"

# MOT DE PASSE ADMINISTRATEUR
ADMIN_PASSWORD = "Samba2026!"

# PRODUITS DE LA BOUTIQUE
produits = [
    {
        "nom": "Parfum Élégance",
        "prix": 15000,
        "description": "Parfum élégant et raffiné.",
        "image": "https://images.unsplash.com/photo-1541643600914-78b084683601?w=500"
    },
    {
        "nom": "Parfum Royal",
        "prix": 20000,
        "description": "Une fragrance luxueuse.",
        "image": "https://images.unsplash.com/photo-1594035910387-fea47794261f?w=500"
    },
    {
        "nom": "Parfum Femme",
        "prix": 12000,
        "description": "Une senteur douce et séduisante.",
        "image": "https://images.unsplash.com/photo-1592945403244-b3fbafd7f539?w=500"
    },
    {
        "nom": "Parfum Homme",
        "prix": 18000,
        "description": "Une fragrance intense.",
        "image": "https://images.unsplash.com/photo-1590736969955-71cc94901144?w=500"
    }
]

# BASE DE DONNEES
def initialiser():
    con = sqlite3.connect(DB)
    con.execute("""
        CREATE TABLE IF NOT EXISTS commandes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            telephone TEXT,
            produit TEXT,
            quantite INTEGER,
            adresse TEXT,
            message TEXT,
            date TEXT
        )
    """)
    con.commit()
    con.close()

initialiser()

# DESIGN DE L'APPLICATION
STYLE = """
<style>
* {box-sizing:border-box}
body {
    margin:0;
    background:#101010;
    color:white;
    font-family:Arial;
}
header {
    background:black;
    padding:25px 10px;
    text-align:center;
    border-bottom:2px solid gold;
}
.logo {
    color:gold;
    font-size:27px;
    font-weight:bold;
}
.hero {
    text-align:center;
    padding:45px 15px;
    background:linear-gradient(135deg,#171717,#493b16);
}
h1,h2,h3 {color:gold}
h2 {text-align:center;margin-top:35px}
.products {
    display:grid;
    grid-template-columns:repeat(2,1fr);
    gap:12px;
    padding:12px;
}
.product {
    background:#222;
    border:1px solid #a68b36;
    border-radius:12px;
    text-align:center;
    overflow:hidden;
    padding-bottom:15px;
}
.product img {
    width:100%;
    height:155px;
    object-fit:cover;
}
.price {
    color:gold;
    font-size:18px;
    font-weight:bold;
    margin:12px;
}
button,.btn {
    display:inline-block;
    background:gold;
    color:black;
    padding:12px 15px;
    border:none;
    border-radius:7px;
    text-decoration:none;
    font-weight:bold;
    margin:5px;
}
.contact {
    background:#222;
    padding:20px;
    margin:20px 12px;
    border-radius:12px;
    text-align:center;
}
form {padding:15px}
input,textarea {
    width:100%;
    padding:13px;
    margin:8px 0;
    border-radius:7px;
    border:1px solid gold;
    background:#292929;
    color:white;
    font-size:15px;
}
textarea {height:80px}
footer {
    background:black;
    color:gold;
    text-align:center;
    padding:20px;
    margin-top:30px;
}
table {width:100%;border-collapse:collapse}
td,th {padding:8px;border-bottom:1px solid gold}
@media(max-width:350px) {
    .products {grid-template-columns:1fr}
}
</style>
"""

# PAGE D'ACCUEIL
@app.route("/")
def accueil():

    html = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Samba Beauty Parfums</title>
    """ + STYLE + """
    </head>
    <body>

    <header>
    <div class="logo">✨ SAMBA BEAUTY ✨</div>
    <p>PARFUMS ET BEAUTÉ</p>
    </header>

    <section class="hero">
    <h1>Bienvenue chez Samba Beauty Parfums</h1>
    <p>Le luxe, la beauté et l'élégance à votre portée.</p>
    <a class="btn" href="#boutique">Découvrir nos produits</a>
    </section>

    <h2 id="boutique">🌹 NOS PRODUITS</h2>
    <div class="products">
    """

    for p in produits:
        html += f"""
        <div class="product">
        <img src="{p['image']}">
        <h3>{p['nom']}</h3>
        <p>{p['description']}</p>
        <div class="price">{p['prix']:,} FCFA</div>
        <a class="btn" href="/commander/{quote(p['nom'])}">
        Commander
        </a>
        </div>
        """

    html += """
    </div>

    <section class="contact">
    <h2>CONTACTEZ-NOUS</h2>
    <p>Nous sommes disponibles pour vous conseiller.</p>

    <a class="btn"
    href="https://wa.me/""" + WHATSAPP + """">
    💬 WhatsApp
    </a>

    <a class="btn" href="tel:+""" + WHATSAPP + """">
    📞 Appeler
    </a>
    </section>

    <footer>
    <h3>SAMBA BEAUTY PARFUMS</h3>
    <p>Merci pour votre confiance ❤️</p>
    © 2026
    </footer>

    </body>
    </html>
    """

    return html


# FORMULAIRE DE COMMANDE
@app.route("/commander/<nom>")
def commander(nom):

    return """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    """ + STYLE + """
    </head>
    <body>
    <header><div class="logo">SAMBA BEAUTY PARFUMS</div></header>

    <div class="contact">
    <h2>PASSER UNE COMMANDE</h2>

    <form action="/envoyer" method="POST">

    <input name="nom" placeholder="Votre nom" required>

    <input name="telephone" placeholder="Votre téléphone" required>

    <input name="produit" value='""" + nom.replace("'", "") + """'
    placeholder="Produit" required>

    <input name="quantite" type="number" min="1"
    value="1" required>

    <textarea name="adresse"
    placeholder="Adresse de livraison" required></textarea>

    <textarea name="message"
    placeholder="Message supplémentaire"></textarea>

    <button type="submit">ENVOYER MA COMMANDE</button>

    </form>
    </div>
    </body>
    </html>
    """


# ENREGISTRER LA COMMANDE
@app.route("/envoyer", methods=["POST"])
def envoyer():

    nom = request.form.get("nom", "").strip()
    telephone = request.form.get("telephone", "").strip()
    produit = request.form.get("produit", "").strip()
    adresse = request.form.get("adresse", "").strip()
    message = request.form.get("message", "").strip()

    try:
        quantite = int(request.form.get("quantite", "1"))
    except ValueError:
        return "Quantité invalide", 400

    if not nom or not telephone or not adresse or quantite < 1:
        return "Informations invalides", 400

    if produit not in [p["nom"] for p in produits]:
        return "Produit inconnu", 400

    con = sqlite3.connect(DB)

    con.execute("""
    INSERT INTO commandes
    (nom,telephone,produit,quantite,adresse,message,date)
    VALUES(?,?,?,?,?,?,?)
    """, (
        nom,
        telephone,
        produit,
        quantite,
        adresse,
        message,
        datetime.now().strftime("%d/%m/%Y %H:%M")
    ))

    con.commit()
    con.close()

    texte = f"""
Bonjour Samba Beauty Parfums !

Nouvelle commande :

Nom : {nom}
Téléphone : {telephone}
Produit : {produit}
Quantité : {quantite}
Adresse : {adresse}
Message : {message}
"""

    lien = "https://wa.me/" + WHATSAPP + "?text=" + quote(texte)

    return """
    <html><head><meta name="viewport"
    content="width=device-width,initial-scale=1">
    """ + STYLE + """
    </head>
    <body>
    <div class="contact">
    <h2>COMMANDE ENREGISTRÉE !</h2>
    <p>Merci pour votre confiance.</p>
    <a class="btn" href='""" + lien + """'>
    ENVOYER SUR WHATSAPP
    </a>
    <br><br>
    <a href="/">Retour à la boutique</a>
    </div>
    </body></html>
    """


# CONNEXION ADMINISTRATEUR
@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        password = request.form.get("password")

        if password == ADMIN_PASSWORD:

            con = sqlite3.connect(DB)
            con.row_factory = sqlite3.Row

            commandes = con.execute(
                "SELECT * FROM commandes ORDER BY id DESC"
            ).fetchall()

            con.close()

            lignes = ""

            for c in commandes:
                lignes += f"""
                <tr>
                <td>{c['nom']}</td>
                <td>{c['telephone']}</td>
                <td>{c['produit']}</td>
                <td>{c['quantite']}</td>
                <td>{c['adresse']}</td>
                <td>{c['date']}</td>
                </tr>
                """

            return """
            <html><head><meta name="viewport"
            content="width=device-width,initial-scale=1">
            """ + STYLE + """
            </head><body>
            <h2>ESPACE ADMINISTRATEUR</h2>
            <div style="overflow-x:auto">
            <table>
            <tr>
            <th>Client</th><th>Téléphone</th>
            <th>Produit</th><th>Qté</th>
            <th>Adresse</th><th>Date</th>
            </tr>
            """ + lignes + """
            </table></div>
            </body></html>
            """

        return "Mot de passe incorrect"

    return """
    <html><head><meta name="viewport"
    content="width=device-width,initial-scale=1">
    """ + STYLE + """
    </head><body>
    <div class="contact">
    <h2>ADMINISTRATEUR</h2>
    <form method="POST">
    <input type="password" name="password"
    placeholder="Mot de passe" required>
    <button type="submit">CONNEXION</button>
    </form>
    </div></body></html>
    """


# LANCEMENT DE L'APPLICATION
if __name__ == "__main__":
    print("SAMBA BEAUTY PARFUMS")
    print("Application démarrée !")
    app.run(host="0.0.0.0", port=5000, debug=False)
