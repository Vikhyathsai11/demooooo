from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/login', methods=['POST'])
def login():
    # Get JSON data from the request
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')

    # Print the name and password to the terminal
    print(f"Name: {name}")
    print(f"Password: {password}")

    # Return a response
    if name and password:
        return jsonify({"message": "Data received successfully!"}), 200
    else:
        return jsonify({"message": "Name or password missing!"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)