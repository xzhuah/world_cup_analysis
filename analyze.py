import numpy as np
import pandas as pd

def load_data(file):

    data = pd.read_csv(file)
    teams = set(data["team1"]).union(set(data["team2"]))
    return data.T,teams

def normalize_ability(ablility_df,prefer_amean,prefer_astd,prefer_dmean,prefer_dstd):

    attack_mean = np.mean(ablility_df.T["attack"])
    attack_std = np.std(ablility_df.T["attack"])
    defend_mean = np.mean(ablility_df.T["defend"])
    defend_std = np.std(ablility_df.T["defend"])
    print(attack_mean,defend_mean)
    ablility_df.T["attack"] = ( ablility_df.T["attack"] - attack_mean ) / attack_std
    ablility_df.T["defend"] = (ablility_df.T["defend"] - defend_mean) / defend_std

    ablility_df.T["attack"] = prefer_amean + prefer_astd * ablility_df.T["attack"]
    ablility_df.T["defend"] = prefer_dmean + prefer_dstd * ablility_df.T["defend"]

def init_statistic(data):
    win = {}
    loss = {}
    count = {}
    total_ball = 0
    game_count = 0
    for i in data:
        game = data[i]
        if game["team1"] not in win:
            win[game["team1"]] =0
            loss[game["team1"]] = 0
            count[game["team1"]]=0
        if game["team2"] not in win:
            win[game["team2"]] =0
            loss[game["team2"]] = 0
            count[game["team2"]] = 0

        win[game["team1"]] += game["point1"]
        win[game["team2"]] += game["point2"]
        total_ball += game["point1"]
        total_ball += game["point2"]
        count[game["team1"]] += 1
        loss[game["team1"]] += game["point2"]
        loss[game["team2"]] += game["point1"]
        count[game["team2"]] += 1
        game_count+=1

    total_ball /= (game_count*2)

    for key in win:
        win[key]/=count[key]
        loss[key]/=count[key]

        win[key] /= total_ball
        loss[key] /= total_ball
    return win,loss

def predict_score(team1,team2):
    print(team1)
    print(team2)
    print(team1["attack"]*team2["defend"],team2["attack"]*team1["defend"])
    return team1["attack"]*team2["defend"],team2["attack"]*team1["defend"]

def train(data,alpha=0.5,training_time=50):
    # initilization
    #print(len(data.T))
    teams = set(data.T["team1"]).union(set(data.T["team2"]))
    team_ability = pd.DataFrame(np.ones([2, len(teams)]), index=["attack", "defend"], columns=sorted(list(teams)))
    win, loss = init_statistic(data)
    for key in win:
        team_ability[key]["attack"] = win[key]
    for key in loss:
        team_ability[key]["defend"] = loss[key]
    print(team_ability)

    pattack_mean = np.mean(team_ability.T["attack"])
    pattack_std = np.std(team_ability.T["attack"])
    pdefend_mean = np.mean(team_ability.T["defend"])
    pdefend_std = np.std(team_ability.T["defend"])


    # training
    for _ in range(training_time):
        new_team_ability = team_ability.copy()
        for game_index in data:
            game = data[game_index]
            team1 = game["team1"]
            team2 = game["team2"]
            new_team_ability[team1]["attack"] = alpha * team_ability[team1]["attack"] \
                                                + (1 - alpha) * (game["point1"] / team_ability[team2]["defend"])

            new_team_ability[team2]["attack"] = alpha * team_ability[team2]["attack"] \
                                                + (1 - alpha) * (game["point2"] / team_ability[team1]["defend"])

            new_team_ability[team1]["defend"] = alpha * team_ability[team1]["defend"] \
                                                + (1 - alpha) * (game["point2"] / team_ability[team2]["attack"])

            new_team_ability[team2]["defend"] = alpha * team_ability[team2]["defend"] \
                                                + (1 - alpha) * (game["point1"] / team_ability[team1]["attack"])

        normalize_ability(new_team_ability, pattack_mean, pattack_std, pdefend_mean, pdefend_std)  # noramlization

        team_ability = new_team_ability  # update
    return team_ability

def evaluation(match_number = 1 + 1 + 2 ):
    data_file = "world2018score.csv"
    data, teams = load_data(data_file)

    right = 0
    wrong = 0

    for predict_index in range(64 - match_number, 64):

        # predict_index = 63 # which game to predict >32 <64

        team_ability = train(data.loc[:, 0:predict_index - 1], alpha=0.5, training_time=50)
        a, b = predict_score(team_ability[data[predict_index]["team1"]], team_ability[data[predict_index]["team2"]])
        print(data[predict_index]["point1"], data[predict_index]["point2"])
        if (a > b) == (data[predict_index]["point1"] > data[predict_index]["point2"]):
            print("right")
            right += 1
        else:
            print("wrong")
            wrong += 1
            a = input("input something to continue")
    print(right, wrong)

def predict(predict_index=63):# which game to predict index>32 and index <64, 63 for the final match:
    data_file = "world2018score.csv"
    data, teams = load_data(data_file)



    team_ability = train(data.loc[:, 0:predict_index - 1], alpha=0.5, training_time=50)
    a, b = predict_score(team_ability[data[predict_index]["team1"]], team_ability[data[predict_index]["team2"]])

    print(data[predict_index]["point1"], data[predict_index]["point2"])
    if (a > b) == (data[predict_index]["point1"] > data[predict_index]["point2"]):
        print("right")
    else:
        print("wrong")


if __name__ == "__main__":
    #evaluation()
    predict(63)

