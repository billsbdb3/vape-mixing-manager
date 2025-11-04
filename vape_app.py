#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify
import json
import os
from google import genai

app = Flask(__name__)
DATA_FILE = "vape_data.json"

# Configure Gemini
os.environ['GOOGLE_API_KEY'] = "AIzaSyBqurpTCR5Tj_X-QwXUAzy0zQP2hcB7Nc0"
client = genai.Client()

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"flavors": {}, "nicotine": {}, "pg": 0, "vg": 0, "recipes": {}}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/inventory', methods=['GET'])
def get_inventory():
    return jsonify(load_data())

@app.route('/api/flavor', methods=['POST'])
def add_flavor():
    data = load_data()
    name = request.json['name']
    base = request.json['base']
    amount = request.json.get('amount', 0)
    data['flavors'][name] = {"base": base, "amount": amount}
    save_data(data)
    return jsonify({"success": True})

@app.route('/api/flavors/batch', methods=['POST'])
def add_flavors_batch():
    data = load_data()
    flavors = request.json
    for name, info in flavors.items():
        if isinstance(info, str):
            data['flavors'][name] = {"base": info, "amount": 0}
        else:
            data['flavors'][name] = {"base": info.get('base', 'pg'), "amount": info.get('amount', 0)}
    save_data(data)
    return jsonify({"success": True, "count": len(flavors)})

@app.route('/api/flavor', methods=['DELETE'])
def delete_flavor():
    data = load_data()
    name = request.json['name']
    if name in data['flavors']:
        del data['flavors'][name]
        save_data(data)
    return jsonify({"success": True})

@app.route('/api/nicotine', methods=['POST'])
def add_nicotine():
    data = load_data()
    strength = request.json['strength']
    pg = float(request.json['pg'])
    vg = float(request.json['vg'])
    data['nicotine'][strength] = {"pg": pg, "vg": vg}
    save_data(data)
    return jsonify({"success": True})

@app.route('/api/nicotine', methods=['DELETE'])
def delete_nicotine():
    data = load_data()
    strength = request.json['strength']
    if strength in data['nicotine']:
        del data['nicotine'][strength]
        save_data(data)
    return jsonify({"success": True})

@app.route('/api/base', methods=['POST'])
def add_base():
    data = load_data()
    data['pg'] += float(request.json['pg'])
    data['vg'] += float(request.json['vg'])
    save_data(data)
    return jsonify({"success": True})

@app.route('/api/recipe', methods=['POST'])
def save_recipe():
    data = load_data()
    recipe = request.json
    data['recipes'][recipe['name']] = recipe
    save_data(data)
    return jsonify({"success": True})

@app.route('/api/recipe', methods=['DELETE'])
def delete_recipe():
    data = load_data()
    name = request.json['name']
    if name in data['recipes']:
        del data['recipes'][name]
        save_data(data)
    return jsonify({"success": True})

@app.route('/api/inventory/update', methods=['POST'])
def update_inventory():
    data = request.json
    save_data(data)
    return jsonify({"success": True})

@app.route('/api/ai/suggest', methods=['POST'])
def ai_suggest():
    try:
        data = request.json
        flavors = data.get('flavors', [])
        user_prompt = data.get('prompt', '')
        
        base_prompt = f"""You are an expert vape juice mixer. Based on these available flavors, suggest ONE complete recipe.

Available flavors: {', '.join(flavors)}"""

        if user_prompt:
            base_prompt += f"\n\nUser request: {user_prompt}"
        
        base_prompt += """

Create a recipe with:
- Recipe name
- Total ml: 60
- Target nicotine: 3
- PG/VG ratio: 30 (just the PG number)
- Steep time (or SnV if shake and vape)
- Flavor percentages (realistic, typically 1-15% per flavor, total under 20%)

Respond ONLY with valid JSON in this exact format:
{"name": "Recipe Name", "total_ml": 60, "target_nic": 3, "target_pg": 30, "steep_time": "2 weeks", "flavors": {"Flavor Name": 5.0}}

Only use flavors from the available list."""
        
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=base_prompt
        )
        
        text = response.text
        
        import re
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            recipe = json.loads(json_match.group())
            return jsonify({"success": True, "recipe": recipe})
        else:
            return jsonify({"success": False, "error": "Could not parse AI response", "raw": text})
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5001)
