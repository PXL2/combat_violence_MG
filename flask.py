from flask import Flask, request, jsonify

app = Flask(__name__)

# função criada com base nas respostas
# em cada estrutura condicional, tem número de risco.
def classificar_risco(respostas):
    risco = 0
    if respostas.get("agressor_presente"): risco += 2
    if respostas.get("ha_armas"): risco += 5
    if respostas.get("tem_filhos"): risco += 2
    if respostas.get("historico_violencia"): risco += 3

    if risco >= 5:
        return "ALTO"
    elif risco >= 3:
        return "MÉDIO"
    else:
        return "BAIXO"

@app.route("/")
def home():
    return "API AtendeIA rodando"

@app.route("/atender", methods=["POST"])
def atender():
    dados = request.get_json()

    if not dados.get("segura"):
        return jsonify({
            "mensagem": "Emergência detectada! Acionando protocolo de urgência e direcionando equipe.",
            "alerta": True
        })

    risco = classificar_risco(dados)

    resposta = {
        "risco": risco,
        "mensagem": f"Atendimento registrado. Risco classificado como: {risco}.",
        "alerta": True if risco == "ALTO" else False
    }
    return jsonify(resposta)

if __name__ == "__main__":
    app.run(debug=True)
