import pandas as pd
from time import sleep
import random

# Creating the overs
over = 0.0
overs = [0]
for i in range(1, 121):
    over += 0.1
    if i % 6 == 0:
        over = int(over) + 1
    overs.append(round(over, 1))


class IPL:
    runs, wickets, balls, on_striker_runs, off_striker_runs = 0, 0, 0, 0, 0
    wicket_chances = ["lbw", "catch", "bold", "run out"]
    conversion = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6}

    def __init__(self, batting_team, bowling_team, overs_to_be_played):
        self.batting_team = batting_team
        self.bowling_team = bowling_team
        self.overs_to_be_played = overs_to_be_played
        self.bat_team = player_data[player_data["Team"] == batting_team]
        self.bowl_team = player_data[player_data["Team"] == bowling_team]
        self.bowlers_names = self.bowl_team.loc[((self.bowl_team["Status"] == "Bowler") |
                                                 (self.bowl_team["Status"] == "All-rounder"))]["Player Name"].values

        #The first value is for runs, second value is for the wickets and the third value is for the overs
        self.bowlers = {key: [0, 0, 0] for key in self.bowlers_names}
        self.active_bowler = random.choice(list(self.bowlers.keys()))
        self.active_bowler_runs, self.active_bowler_wickets, self.active_bowler_overs = 0, 0, 0

        # So that bowlers do batting after batsmen and all-rounders
        self.batsmen = list(self.bat_team.loc[((self.bat_team["Status"] == "Batsman") |
                                               (self.bat_team["Status"] == "All-rounder"))][
                                "Player Name"].values)

        self.batsmen.extend(list(self.bat_team[self.bat_team["Status"] == "Bowler"]["Player Name"].values))

        # First is for runs and second is for balls faced
        self.batsmen = {name: [0, 0] for name in self.batsmen}

        print(f"{batting_team} is batting and {bowling_team} is bowling")
        self.batsmen_names = list(self.batsmen.keys())
        self.on_striker = self.batsmen_names[0]
        self.off_striker = self.batsmen_names[1]
        self.on_striker_balls = 0
        self.off_striker_balls = 0

        #To get the next batsmen from the list
        self.batting_index = 2

        sleep(1)
        self.display_score()
        while self.balls < overs_to_be_played * 6 and self.wickets < 10:
            ball = input("What happened in this ball?\n>>>")
            if ball in ["1", "2", "3", "4", "5", "6", "one", "two", "three", "four", "five", "six"]:
                try:
                    self.runs += int(ball)
                    self.on_striker_runs += int(ball)
                    self.active_bowler_runs += int(ball)
                    self.on_striker_balls += 1
                    if ball in ["1", "3"]:
                        self.exchange_strike()
                except ValueError:
                    self.runs += self.conversion[ball]
                    self.on_striker_runs += self.conversion[ball]
                    self.active_bowler_runs += self.conversion[ball]
                    self.on_striker_balls += 1
                    if ball in ["one", "three"]:
                        self.exchange_strike()

            elif ball in ["0", "zero", "dot ball", "dot"]:
                self.on_striker_balls += 1

            elif ball in self.wicket_chances:
                self.wickets += 1
                self.active_bowler_wickets += 1
                self.on_striker_balls += 1
                self.change_batsmen(self.on_striker)

            elif ball == "wide":
                self.runs += 1
                self.balls -= 1

            else:
                print("\nInvalid input!! Please try again!\n")
                continue

            self.balls += 1

            if self.balls % 6 == 0:
                self.exchange_strike()
                self.change_bowler(self.active_bowler)

            #So that it doesn't display the score at the end of the match
            if self.balls < overs_to_be_played * 6 and self.wickets < 10:
                self.display_score()

        else:
            self.end_game()

    def exchange_strike(self):
        self.on_striker, self.off_striker = self.off_striker, self.on_striker
        self.on_striker_runs, self.off_striker_runs = self.off_striker_runs, self.on_striker_runs
        self.on_striker_balls, self.off_striker_balls = self.off_striker_balls, self.on_striker_balls

    def change_batsmen(self, batsman_out):
        self.batsmen[batsman_out][0] += self.on_striker_runs
        self.batsmen[batsman_out][1] += self.on_striker_balls
        self.on_striker = self.batsmen_names[self.batting_index]
        self.batting_index += 1
        self.on_striker_runs, self.on_striker_balls = 0, 0

    def change_bowler(self, old_bowler):
        # The second condition checks whether the bowler has exceeded his 4 overs
        while self.active_bowler == old_bowler or self.bowlers[self.active_bowler][2] >= 4:
            self.active_bowler = random.choice(list(self.bowlers.keys()))
        self.bowlers[old_bowler][0] += self.active_bowler_runs
        self.bowlers[old_bowler][1] += self.active_bowler_wickets
        self.bowlers[old_bowler][2] += 1
        self.active_bowler_runs, self.active_bowler_wickets, self.active_bowler_overs = 0, 0, 0

    def display_score(self):
        print()
        print(str(self.runs) + "-" + str(self.wickets))
        print(overs[self.balls])
        print(f"{self.on_striker} = {self.on_striker_runs}({self.on_striker_balls})")
        print(f"{self.off_striker} = {self.off_striker_runs}({self.off_striker_balls})")
        print(f"Bowler: {self.active_bowler} = \t{self.active_bowler_runs} - {self.active_bowler_wickets}")
        print()

    def end_game(self):
        self.batsmen[self.on_striker][0] += self.on_striker_runs
        self.batsmen[self.on_striker][1] += self.on_striker_balls
        self.batsmen[self.off_striker][0] +=  self.off_striker_runs
        self.batsmen[self.off_striker][1] += self.off_striker_balls
        print(self.bowl_team)
        print()
        print(f"{self.bowling_team} need {self.runs + 1} runs in {self.balls} balls to win")
        print()
        print("Match Statistics:")
        print(f"Batsmen({self.batting_team}):")
        for batsman, scores in self.batsmen.items():
            #If the number of balls faced by the batsmen are zero, then score won't be printed
            if scores[1] != 0:
                print(f"{batsman} scored {scores[0]} runs in {scores[1]} balls")
        print()
        print(f"Bowlers({self.bowling_team}):")
        for bowler, stats in self.bowlers.items():
            if stats[2] != 0:
                print(f"{bowler} gave {stats[0]} runs taking {stats[1]} wicket(s) in {stats[2]} over(s)")


player_data = pd.read_csv("Player Data.csv")
team1 = None
team2 = None
while True:
    team1 = input("Please enter the 1st team name:").upper()
    team2 = input("Please enter the 2nd team name:").upper()
    if team1 in player_data["Team"].unique() or team2 in player_data["Team"].unique():
        break
    print("\nPlease enter a valid team name!\n")

toss_winner = None

while True:
    toss_winner = input("Who won the toss?(Enter the team name please)\n>>>").upper()
    if toss_winner in [team1, team2]:
        break
    print("\nPlease choose a team from the ones entered!\n")

while True:
    result = input("What did they choose? (Batting/Bowling)\n>>>").lower()
    if (result in ["batting", "bat"] and toss_winner == team1) or (result in ["bowling", "bowl"] and toss_winner == team2):
        bat_team = team1
        bowl_team = team2
    elif (result in ["bowl", "bowling"] and toss_winner == team1) or (result in ["batting", "bat"] and toss_winner == team2):
        bat_team = team2
        bowl_team = team1
    else:
        print("\nInvalid choice ! Please try again.....\n")
        continue
    break

while True:
    overs_to_play = int(input("Enter the number of overs to be played (1 - 20)\n>>>"))
    if 1 <= overs_to_play <= 20:
        break
    print("Please enter a valid number of overs!")

game = IPL(bat_team, bowl_team, overs_to_play)
