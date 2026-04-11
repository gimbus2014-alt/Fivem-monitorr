from flask import Flask, render_template_string
import requests
import os

app = Flask(__name__)

SERVERS = {
    "Serwer 1 (jjj4kl)": "jjj4kl",
    "Serwer 2 (okz5dj)": "okz5dj"
}

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>FiveM Monitor</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="refresh" content="15">
    <style>
        body { font-family: Arial; padding: 15px; }
        input { width: 100%; padding: 10px; margin-bottom: 15px; font-size: 16px; }
        h3 { margin-top: 20px; }
        li { margin: 4px 0; }
    </style>
</head>
<body>

<h2>Gracze online</h2>

<input type="text" id="search" placeholder="Wpisz nick...">

<div id="servers">
{% for server, players in servers.items() %}
    <h3>{{server}}</h3>
    <ul>
    {% for player in players %}
        <li>{{player}}</li>
    {% endfor %}
    </ul>
{% endfor %}
</div>

<script>
const search = document.getElementById("search");

search.addEventListener("keyup", function() {
    const filter = search.value.toLowerCase();
    const items = document.querySelectorAll("li");

    items.forEach(item => {
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(filter) ? "" : "none";
    });
});
</script>

</body>
</html>
"""

def get_players(server_id):
    try:
        url = f"https://servers-frontend.fivem.net/api/servers/single/{server_id}"
        r = requests.get(url)
        data = r.json()
        players = data["Data"]["players"]
        return sorted([f"[ID:{p['id']}] {p['name']}" for p in players])
    except:
        return ["Błąd pobierania danych"]

@app.route("/")
def home():
    all_servers = {}

    for name, server_id in SERVERS.items():
        all_servers[name] = get_players(server_id)

    return render_template_string(HTML, servers=all_servers)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
