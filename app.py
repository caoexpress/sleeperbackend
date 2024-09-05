from flask import Flask, request, jsonify
import requests
import logging

app = Flask(__name__)

# Setup basic logging
logging.basicConfig(level=logging.INFO)

# Sleeper API Base URL
BASE_URL = "https://api.sleeper.app/v1"

# Function to make a request to Sleeper API with improved error handling
def make_sleeper_api_call(endpoint):
    url = f"{BASE_URL}{endpoint}"
    logging.info(f"Making request to {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for HTTP codes 4xx/5xx

        logging.info(f"Successfully fetched data from {url}")
        return response.json()

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
        return {"error": f"HTTP error: {response.status_code} {response.text}"}, response.status_code

    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error occurred: {req_err}")
        return {"error": f"Request error: {str(req_err)}"}, 500

# Endpoint to get general league info
@app.route('/league/<league_id>', methods=['GET'])
def get_league(league_id):
    endpoint = f"/league/{league_id}"
    data, status_code = make_sleeper_api_call(endpoint)
    return jsonify(data), status_code

# Endpoint to get rosters in a league
@app.route('/league/<league_id>/rosters', methods=['GET'])
def get_rosters(league_id):
    endpoint = f"/league/{league_id}/rosters"
    data, status_code = make_sleeper_api_call(endpoint)
    return jsonify(data), status_code

# Endpoint to get league matchups
@app.route('/league/<league_id>/matchups/<week>', methods=['GET'])
def get_matchups(league_id, week):
    endpoint = f"/league/{league_id}/matchups/{week}"
    data, status_code = make_sleeper_api_call(endpoint)
    return jsonify(data), status_code

# Endpoint to get players (list of NFL players)
@app.route('/players/nfl', methods=['GET'])
def get_players():
    endpoint = "/players/nfl"
    data, status_code = make_sleeper_api_call(endpoint)
    return jsonify(data), status_code

# Endpoint to get draft data
@app.route('/draft/<draft_id>', methods=['GET'])
def get_draft(draft_id):
    endpoint = f"/draft/{draft_id}"
    data, status_code = make_sleeper_api_call(endpoint)
    return jsonify(data), status_code

# Endpoint to get user information by user_id
@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    endpoint = f"/user/{user_id}"
    data, status_code = make_sleeper_api_call(endpoint)
    return jsonify(data), status_code

# Endpoint to get user leagues (for a specific sport and season)
@app.route('/user/<user_id>/leagues/<sport>/<season>', methods=['GET'])
def get_user_leagues(user_id, sport, season):
    endpoint = f"/user/{user_id}/leagues/{sport}/{season}"
    data, status_code = make_sleeper_api_call(endpoint)
    return jsonify(data), status_code

# Endpoint to get transactions (waivers, trades, etc.) for a league and a specific week
@app.route('/league/<league_id>/transactions/<week>', methods=['GET'])
def get_transactions(league_id, week):
    endpoint = f"/league/{league_id}/transactions/{week}"
    data, status_code = make_sleeper_api_call(endpoint)
    return jsonify(data), status_code

# Endpoint to get traded picks
@app.route('/league/<league_id>/traded_picks', methods=['GET'])
def get_traded_picks(league_id):
    endpoint = f"/league/{league_id}/traded_picks"
    data, status_code = make_sleeper_api_call(endpoint)
    return jsonify(data), status_code

# Error handling for unsupported routes
@app.errorhandler(404)
def not_found(e):
    logging.error(f"Invalid API route accessed: {request.path}")
    return jsonify({"error": "Invalid API route. Please check the endpoint."}), 404

# Error handler for internal server errors
@app.errorhandler(500)
def internal_server_error(e):
    logging.error(f"Internal server error: {str(e)}")
    return jsonify({"error": "Internal server error occurred. Please try again later."}), 500

if __name__ == '__main__':
    logging.info("Starting Flask app on port 5001")
    app.run(debug=True, port=5001)
