from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

def limpa(txt):
    return txt.strip().replace(" ", "").replace("-", "")

def luhn_ok(n):
    s, d = 0, False
    for dig in reversed(n):
        x = int(dig)
        if d:
            x *= 2
            if x > 9: x -= 9
        s += x
        d = not d
    return s % 10 == 0

def bandeira(n):
    if n[:2] in ("34", "37") and len(n) == 15: return "Amex"
    if n[:4] == "6011" or n[:2] in ("65", "64") and 16 <= len(n) <= 19: return "Discover"
    if 51 <= int(n[:2]) <= 55 and len(n) == 16: return "Mastercard"
    if n[0] == "4" and (len(n) == 13 or 16 <= len(n) <= 19): return "Visa"
    return "Desconhecida"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/validar", methods=["POST"])
def validar():
    data = request.get_json(force=True)
    num = limpa(data["numero"])
    ok = num.isdigit() and 13 <= len(num) <= 19 and luhn_ok(num)
    return jsonify(
        numero=num,
        bandeira=bandeira(num),
        valido=ok
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
