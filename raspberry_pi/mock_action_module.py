from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/buzzer', methods=['POST'])
def control_buzzer():
    # Module 4.5 simulation [cite: 70]
    data = request.json
    action = data.get("action")

    if action == "on":
        print("\n[MOCK PI] >>> BZZZZZZZZ! (Buzzer is ON)")
        return jsonify({"status": "Buzzer Activated"}), 200
    elif action == "off":
        print("\n[MOCK PI] >>> ... (Buzzer is OFF)")
        return jsonify({"status": "Buzzer Deactivated"}), 200
    
    return jsonify({"error": "Invalid action"}), 400

if __name__ == '__main__':
    # Running on localhost (127.0.0.1) for testing
    print("Mock Pi Server starting on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000)