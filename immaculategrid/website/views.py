from flask import Blueprint, render_template, request
from .models import franch_df, player_names, on_teams, get_player_id

views = Blueprint("views", __name__)

# Randomizes 6 franchises used for game
franch_sample = franch_df().sample(n = 6)

# Dataframe that contains player ids mapped to search options
player_df = player_names()

# Dictionary displaying the color of each grid's button based on correct or incorrect/unanswered
class_dict = {
        "btn default": [
            "form_one", "form_two", "form_three",
            "form_four", "form_five", "form_six",
            "form_seven", "form_eight", "form_nine"
        ]
    }
btn_class = {v:k for k, li in class_dict.items() for v in li}

guesses = [0,1,2,3,4,5,6,7,8,9]

player_options = list(player_df['search_option'])

@views.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == "POST":
        form_id = request.form.get('form_id')
        player = request.form.get('player')
        team_one = request.form.get('team_one')
        team_two = request.form.get('team_two')

        if player not in player_options:
            btn_class[form_id] = "btn default"
        else:
            if on_teams(team_one, team_two, get_player_id(player)):
                btn_class[form_id] = "btn correct"
                player_options.remove(player)
                guesses.pop()
            else:
                btn_class[form_id] = "btn default"
                guesses.pop()

    if len(guesses) == 1:
        for key in btn_class.keys():
            if btn_class[key] == "btn default":
                btn_class[key] = "btn gameover"
            else:
                pass

    return render_template(
        'base.html',
        franchises = franch_sample,
        sources = list(franch_sample['franch_src']),
        btn_class = btn_class,
        player_names = player_options,
        correct = list(btn_class.values()).count('btn correct'),
        guesses = guesses[-1]
    )