import streamlit as st
from betting_logic import fetch_odds, pick_best_bet
import json

st.set_page_config(page_title="📱 Best Bet Today", layout="centered")
st.title("🎯 Best Bet of the Day")

api_key = st.secrets["ODDS_API_KEY"]
matches = fetch_odds(api_key)
bet = pick_best_bet(matches)

if bet:
    teams, favorite, odds, spread = bet
    st.subheader(f"{teams[0]} vs {teams[1]}")
    st.markdown(f"**Favorite:** {favorite} at **{odds}** odds")
    st.markdown(f"**True Spread:** {spread:.2f}")
else:
    st.warning("No suitable bets found today.")

try:
    with open("bankroll.json", "r") as f:
        bankroll = json.load(f)
except:
    bankroll = {"amount": 1000}

st.metric("💰 Bankroll", f"${bankroll['amount']:.2f}")

if st.button("Simulate Bet"):
    won = odds < 2
    payout = 50 * (odds - 1) if won else -50
    bankroll['amount'] += payout
    with open("bankroll.json", "w") as f:
        json.dump(bankroll, f)
    st.success(f"{'Won' if won else 'Lost'} ${abs(payout):.2f}")
