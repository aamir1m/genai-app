from flask import current_app as app, jsonify, request

@app.route('/api/hello', methods=['POST'])
def hello():
    data = request.json
    message = data.get('message', 'World') 
    return jsonify({"output": f"Hello, {message}!"})
