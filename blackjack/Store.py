import json

def save_game_progress(player_name, player_score, player_cards, game_progress):
    data = {
        "player_name": player_name,
        "player_score": player_score,
        "player_cards": player_cards,
        "game_progress": game_progress
    }

    with open('game_progress.json', 'w') as file:
        json.dump(data, file)