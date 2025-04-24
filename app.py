from flask import Flask, request, render_template, jsonify, send_from_directory
import os

app = Flask(__name__)

# Fonction de prédiction Dummy
# Ici, nous supposons que les trois inputs sont des nombres.
# Pour cet exemple, nous définissons une règle simple :
#   Si (credit_history + married) est égal à 2 (c'est-à-dire un historique de crédit positif et marié)
#   ET si le revenu du co-demandeur est supérieur à 2000, alors le crédit est accordé.
# Sinon, le crédit est refusé.
def predict_credit(credit_history, married, coapplicant_income):
    try:
        ch = float(credit_history)
        m  = float(married)
        ci = float(coapplicant_income)
    except ValueError:
        return "Erreur: Valeurs invalides."
    
    # Exemple de règle (vous pouvez adapter)
    if ch == 1 and m == 1 and ci > 2000:
        return "Crédit accordé"
    else:
        return "Crédit refusé"

# Route pour servir le favicon (optionnel)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Route d'accueil : Affiche le formulaire
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', prediction_text=None)

# Route de prédiction (POST) : Traite le formulaire
@app.route('/predict', methods=['POST'])
def predict():
    # Récupérer les données du formulaire
    credit_history = request.form.get("credit_history")
    married        = request.form.get("married")
    coapplicant_income = request.form.get("coapplicant_income")
    
    # Vérifier que tous les champs sont remplis
    if not credit_history or not married or not coapplicant_income:
        return render_template('index.html',
                               prediction_text="Erreur : Veuillez remplir tous les champs.",
                               title="Simulation de votre Crédit")
    
    # Appliquer la fonction de prédiction
    result = predict_credit(credit_history, married, coapplicant_income)
    
    # Renvoie le template avec le résultat
    return render_template('index.html',
                           prediction_text=result,
                           title="Simulation de votre Crédit")

# Route de test (optionnel)
@app.route('/test', methods=['GET'])
def test():
    return "bonjour"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
