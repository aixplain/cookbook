# 🃏 Blackjack Agent

This notebook demonstrates how to build a simple Blackjack game using the [Deck of Cards API](https://deckofcardsapi.com/) and Python. The game includes player and dealer interactions for:

- Starting a new game
- Hitting (drawing a card)
- Standing (revealing dealer's hand and determining the winner)


---

## 📂 Contents

- `new(game_id="")`: Start a new game (shuffle & deal)
- `hit(game_id)`: Draws a new card for the player
- `stand(game_id)`: Ends the player's turn, dealer draws, and game is resolved

---

## ⚙️ How It Works

The agent:

- Uses the Deck of Cards API to manage shuffling and drawing cards
- Calculates scores by handling face cards and aces intelligently
- Stores game state using a game-specific deck ID
- Prints game state after every action

---

## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install aixplain
```

### 2. Run the Notebook

Open the notebook and run each section in sequence:

1. Start a new game with `new()`
2. Call `hit(game_id)` to draw a new card
3. Use `stand(game_id)` to end the round and reveal the result

---

## 🎮 Example Usage

```python
output = new()  # Starts a new game
print(output)

# Hit
print(hit(game_id="xyz123"))

# Stand
print(stand(game_id="xyz123"))
```


