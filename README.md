# poker-ratings
calculate a rating for poker players. calculate expected chances of a player winning in a given line up.

# calculate with trueskill 
using the N-player truskill model, calculate ratings from Hustler Casino Live. results can be found in the ratings/567.csv file, which represents ratings calculations after the first 567 episodes of HCL. 

# calculate with adjusted elo / simple elo model 
trueskill results in wild ratings shifts when poker has higher natural variance. one potential option is to adjust the elo rating formula. the simple elo adjustment for N players is as follows:
1. players are ranked by performance
2. each player having 2 matches -- a loss vs player above and a win ve player below
3. update each player accordingly using this formula: 

regular elo: 
expected_outcome_1 = 1 / (1 + 10**((rating2-rating1) / 400))
expected_outcome_2 = 1 / (1 + 10**((rating1-rating2) / 400))
new_rating1 = rating1 + K * (result - expected_outcome_1)
new_rating2 = rating2 + K * ((1 - result) - expected_outcome_2 )

4. we also introduce an adjusted elo formula to mitigate the chance-based nature of the game. 