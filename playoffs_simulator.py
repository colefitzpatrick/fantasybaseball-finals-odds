import random
import operator

runs = 0
num_runs = 1000000    #set the number of runs for the simulation

#The 6 remaining matchups over the next 3 days
game1a = ["Fire", "Smog"]
game1b = ["Pilots", "Huskies"]
game2a = ["Fire", "Huskies"]
game2b = ["Pilots", "Smog"]
game3a = ["Smog", "Huskies"]
game3b = ["Pilots", "Fire"]

top3tiebreak = 0 
bottomthreetie = 0

playofftracker = []    #blank list where the playoff teams from each simulation will be added

#function that selects a winner given the game and updates the wins dictionary and the appropriate H2H matchup dictionary
def winner(game, matchup):
    game_winner = random.choice(game)
    wins[game_winner] = wins.get(game_winner, 0) + 1
    matchup[game_winner] = matchup.get(game_winner, 0) + 1
    
while runs < num_runs:
    #existing number of wins
    wins = {"Smog": 1, "Pilots": 5, "Fire": 3, "Huskies": 3}
    
    #existing H2H records
    smog_vs_pilots = {"Smog": 0, "Pilots": 2}
    smog_vs_huskies = {"Smog": 1, "Huskies": 1}
    smog_vs_fire = {"Smog": 0, "Fire": 2}   
    fire_vs_huskies = {"Fire": 1, "Huskies": 1}
    fire_vs_pilots = {"Fire": 0, "Pilots": 2}
    huskies_vs_pilots = {"Huskies": 1, "Pilots": 1}
    
    runs += 1
    playoffs = []
    
    #runs through the remaining games
    winner(game1a, smog_vs_fire)
    winner(game1b, huskies_vs_pilots)
    winner(game2a, fire_vs_huskies)
    winner(game2b, smog_vs_pilots)
    winner(game3a, smog_vs_huskies)
    winner(game3b, fire_vs_pilots)
    
    #orders the dictionary by value in descending order
    sorted_wins = dict(sorted(wins.items(), key=operator.itemgetter(1),reverse=True))      
    firstplace = tuple(sorted_wins.items())[0][0]    #gets the key of 1st place
    secondplace = tuple(sorted_wins.items())[1][0]    #gets the key of 2nd place
    thirdplace = tuple(sorted_wins.items())[2][0]    #gets the key of 3rd place
    fourthplace = tuple(sorted_wins.items())[3][0]    #gets the key of 4th place

    if sorted_wins[firstplace] > sorted_wins[thirdplace]:  #advances the first place team to playoffs if they have more wins than top 3
        playoffs.append(firstplace)
    elif sorted_wins[firstplace] == sorted_wins[thirdplace]:   #in the event there is a 3 way tie at the top, checks the Fire vs. Huskies tiebreaker
        if fire_vs_huskies["Fire"] == 1:
            playoffs.append("Pilots")
            #Fire eliminated by H2H top 3 tiebreak
        else:
            #INCONCLUSIVE - Top 2 determined by Fpts
            top3tiebreak += 1
    else:
        pass
    
    if sorted_wins[secondplace] > sorted_wins[thirdplace]:     #advances 2nd place to the playoffs in the simple cases that they have more wins than 3rd place
        playoffs.append(secondplace)
    #looks at the tiebreaker cases where 2nd and 3rd place are tied in wins, but have more wins than 4th place
    elif (sorted_wins[secondplace] == sorted_wins[thirdplace]) and (sorted_wins[thirdplace] > sorted_wins[fourthplace]):
        if (secondplace == "Smog" and thirdplace == "Fire") or (secondplace == "Fire" and thirdplace == "Smog"):
            tiebreak = max(smog_vs_fire.items(), key=operator.itemgetter(1))[0]
            playoffs.append(tiebreak)
        elif (secondplace == "Smog" and thirdplace == "Huskies") or (secondplace == "Huskies" and thirdplace == "Smog"):
            tiebreak = max(smog_vs_huskies.items(), key=operator.itemgetter(1))[0]
            playoffs.append(tiebreak)
        elif (secondplace == "Huskies" and thirdplace == "Fire") or (secondplace == "Fire" and thirdplace == "Huskies"):
            tiebreak = max(fire_vs_huskies.items(), key=operator.itemgetter(1))[0]
            playoffs.append(tiebreak)
        elif (secondplace == "Pilots" and thirdplace == "Fire") or (secondplace == "Fire" and thirdplace == "Pilots"):
            tiebreak = max(fire_vs_pilots.items(), key=operator.itemgetter(1))[0]
            playoffs.append(tiebreak)
        elif (secondplace == "Huskies" and thirdplace == "Pilots") or (secondplace == "Pilots" and thirdplace == "Huskies"):
            tiebreak = max(huskies_vs_pilots.items(), key=operator.itemgetter(1))[0]
            playoffs.append(tiebreak)
        else:
            pass
    elif sorted_wins[secondplace] == sorted_wins[fourthplace]:      #looks at the case where 2nd/3rd/4th place are all tied in wins
        if fire_vs_huskies["Huskies"] == 1:     #If Huskies lose the H2H tiebreaker with the Fire, then the Fire advance
            playoffs.append("Fire")
            #Fire advances in 3 way tiebreaker
        else:
            bottomthreetie += 1
            #INCONCLUSIVE - Bottom three tiebreaked by Fpts
            pass
    else:
        pass
    
    #adds to the playofftracker list if there was a conclusive result
    if len(playoffs) == 2:
        playofftracker.append(playoffs[0])
        playofftracker.append(playoffs[1])
    else:
        pass

smogplayoffs = round(playofftracker.count("Smog") / runs * 100, 2)
pilotplayoffs = round((playofftracker.count("Pilots") + bottomthreetie) / runs * 100, 2) #Pilots make the playoffs in the case of a bottomthreetie
fireplayoffs = round(playofftracker.count("Fire") / runs * 100, 2)
huskyplayoffs = round(playofftracker.count("Huskies") / runs * 100, 2)


#Reporting Section
print("Top 3 Fpts tiebreaker (NP, FW, HAL): " + str(round((top3tiebreak / runs * 100), 2)) + "%")
print("Bottom 3 Fpts tiebreaker (LA, HAL, FW): " + str(round((bottomthreetie / runs * 100), 2)) + "%")
print("Smog playoff chances: " + str(smogplayoffs) + "%")
print("Fire playoff chances: " + str(fireplayoffs) + "%")
print("Husky playoff chances: " + str(huskyplayoffs) + "%")
print("Pilots playoff chances: " + str(pilotplayoffs) + "%")
    
