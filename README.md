# world cup analysis

## This is a world cup match predicting model writen in Python

The idea is: abstracts every team into two value (attack, defend),  the higher the attack value is, the better it is in attacking. The lower the defend value, the better it is in defending. When two team matches (attack1,defend1) vs (attack2, defend2)

team1 is expected to get attack1 * defend2 points while team2 is expected to get attack2 * defend1 points. The points here is not the expectation goals but it somehow reflect that value. So when attack1 * defend2 > attack2 * defend1, team 1 is more likely to win.

For every match that already happened update the two teams' attack and defend value by 
![](https://i.imgur.com/defDOk5.png)

the value are then be normalized.

train this model until it converged and do the prediction.

The dataset for this task is very small but this model achieved a 56.25, 62.5% and 75% correctness for prediction of the last 16, 8 and 4 matches respectively. (The more historical data, the better prediction it does). Most of the predictions follows the human experience very well, for example, the only mistake it made in the last 4 matches is Croatia vs England. The model doesn't think Croatia can beat England which many people also shares the same opinion. The model here assume that each team has a fixed ability to attack and defend which is obviously not true. Their ability will be affected by many other factors which can't be derived in the match scores.


