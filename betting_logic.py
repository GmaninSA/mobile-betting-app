import requests

def fetch_odds(api_key):
    url = f"https://api.the-odds-api.com/v4/sports/baseball_mlb/odds/?regions=us&markets=h2h&apiKey={api_key}"
    res = requests.get(url)
    return res.json() if res.status_code == 200 else []

def pick_best_bet(matches):
    best = None
    best_spread = 0
    for match in matches:
        try:
            teams = match['teams']
            outcomes = match['bookmakers'][0]['markets'][0]['outcomes']
            odds = {o['name']: o['price'] for o in outcomes}
            fav = min(odds, key=odds.get)
            spread = max(odds.values()) - min(odds.values())
            if odds[fav] >= 1.44 and spread > best_spread:
                best = (teams, fav, odds[fav], spread)
                best_spread = spread
        except:
            continue
    return best
