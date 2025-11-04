# Vape Juice Recipe Manager

A web-based application for managing vape juice recipes, inventory, and mixing calculations with AI-powered recipe suggestions.

## Features

- 📦 **Inventory Management** - Track flavors, nicotine bases, and quantities
- 🧮 **Recipe Calculator** - Calculate precise measurements by weight (grams)
- 💾 **Recipe Storage** - Save and load your favorite recipes
- 🤖 **AI Suggestions** - Get recipe ideas from Gemini AI
- 📊 **Mix Tracking** - Track how many times you've made each recipe
- ⚠️ **Low Stock Alerts** - Visual warnings for flavors running low
- 🎯 **Flavor Shots** - Create bulk flavor concentrates
- 📥 **Import/Export** - JSON import for flavors and recipes

## Quick Start (Docker)

### Prerequisites
- Docker and Docker Compose installed
- Google Gemini API key (for AI features)

### Deployment

1. **Clone the repository:**
```bash
git clone https://github.com/billsbdb3/vape-mixing-manager.git
cd vape-mixing-manager
```

2. **Set up environment variables:**
```bash
cp .env.example .env
nano .env  # Add your Google API key
```

Or set directly in docker-compose.yml:
```yaml
environment:
  - GOOGLE_API_KEY=your-api-key-here
```

3. **Start the application:**
```bash
docker-compose up -d
```

4. **Access the app:**
Open your browser to `http://localhost:5001`

### Management Commands

**View logs:**
```bash
docker-compose logs -f
```

**Stop:**
```bash
docker-compose down
```

**Restart:**
```bash
docker-compose restart
```

**Update after changes:**
```bash
git pull
docker-compose down
docker-compose build
docker-compose up -d
```

## Local Development

1. **Install dependencies:**
```bash
pip3 install -r requirements.txt
```

2. **Run the app:**
```bash
python3 vape_app.py
```

3. **Access:** `http://localhost:5001`

## Usage

### Adding Inventory
1. Navigate to "Add to Inventory"
2. Add flavors with base type (PG/VG) and quantity in grams
3. Add nicotine bases with strength and PG/VG ratio

### Creating Recipes
1. Enter batch size, nicotine strength, and PG/VG ratio
2. Add flavors with percentages
3. Click "Calculate Recipe" to see measurements
4. Save the recipe for later use

### AI Recipe Suggestions
1. Enter a prompt (e.g., "berry flavor", "creamy dessert")
2. Click "🤖 AI Suggest Recipe"
3. Review and adjust the suggested recipe
4. Calculate and save

### Importing Data

**Flavors (JSON format):**
```json
{
  "Strawberry (TFA)": {"base": "pg", "amount": 30.5},
  "Vanilla (CAP)": {"base": "pg", "amount": 25.0}
}
```

**Recipes (JSON format):**
```json
{
  "total_ml": 60,
  "target_nic": 3,
  "target_pg": 30,
  "steep_time": "2 weeks",
  "nic_base": "100",
  "flavors": {
    "Strawberry (TFA)": 5,
    "Vanilla (CAP)": 3
  }
}
```

## Data Persistence

All data is stored in `vape_data.json` which is mounted as a Docker volume, ensuring your recipes and inventory persist across container restarts.

## Port Configuration

Default port is 5001. To change, edit `docker-compose.yml`:
```yaml
ports:
  - "8080:5001"  # Change 8080 to your desired port
```

## Tech Stack

- **Backend:** Python Flask
- **Frontend:** Vanilla JavaScript
- **AI:** Google Gemini API
- **Deployment:** Docker

## License

MIT
