from flask import Flask, render_template_string
import requests
import os

app = Flask(__name__)

SERVER_ID = "okz5dj"
API_URL = f"https://servers-frontend.fivem.net/api/servers/single/{SERVER_ID}"

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>FiveM Monitor</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial; padding: 15px; }
        input { width: 100%; padding: 10px; margin-bottom: 10px; font-size: 16px; }
        li { margin: 5px 0; }
    </style>
</head>
<body>

<h2>Gracze online</h2>

<input type="text" id="search" placeholder="Wpisz nick...">

<ul id="playerList">
{% for player in players %}
    <li>{{player}}</li>
{% endfor %}
</ul>

<script>
const search = document.getElementById("search");
const items = document.querySelectorAll("#playerList li");

search.addEventListener("keyup", function() {
    const filter = search.value.toLowerCase();
    items.forEach(item => {
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(filter) ? "" : "none";
    });
});
</script>

</body>
</html>
"""

def get_players():
    try:
        r = requests.get(API_URL)
        data = r.json()
        players = data["Data"]["players"]
        return sorted([f"[ID:{p['id']}] {p['name']}" for p in players])
    except:
        return ["Błąd pobierania danych"]

@app.route("/")
def home():
    players = get_players()
    return render_template_string(HTML, players=players)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
