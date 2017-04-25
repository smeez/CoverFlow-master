from random import shuffle
from ProbDist import PoiBin
import random
from operator import itemgetter


#how much weight each specific match has. 32 is used in chess
kFactor = 90

class Standings:
    def __init__(self, teams):
        self.teams = teams
    def sortStandings(self, conference):
        point_sorted = {}
        for elem in self.teams:
            if elem.conference == conference:
                point_sorted[elem] = 2*elem.win  + elem.otl
        return (sorted(point_sorted.items(), key=itemgetter(1), reverse =True))
    def pointsToMakePlayoffs(self, conference):
        point_sorted = self.sortStandings(conference)
        return point_sorted[0][0]

    def getIndexInStandings(self, team):
        count = 0
        for elem in self.sortStandings(team.conference):
            if(elem[0] == team.name):
                break;
            else:
                count= count+1
        return count
    def getScheduleProbability(self, team, schedule):
        list = []
        for elem in schedule:
            list.append(EloCalculator.winPercentageBetween(team, elem))
        return list
    def getPlayoffProbability(self, team):
        team_competing= self.pointsToMakePlayoffs(team.conference)

        neededpoints = (team_competing.win * 2 + team_competing.otl)
        currentpoints = 2*team.win + team.otl


        ppg_top = neededpoints/team_competing.gamesplayed
        points_end = neededpoints+ppg_top*(82-team_competing.gamesplayed)
        ppg_needed = (points_end - currentpoints)/(82-team.gamesplayed)

        schedule = team.schedule
        schedule_perc = self.getScheduleProbability(team, schedule)

        print(schedule_perc)
        func = PoiBin(schedule_perc)
        print(int(len(schedule_perc)*(ppg_needed/2)))
        print(func.pmf(int(len(schedule)*(ppg_needed/2))))

        print("need pts", ppg_needed)

class EloCalculator:
    def calculateElo(team1, team2, result):
        #if result = 0, Team1 wins
        #if result = 1, Team2 wins
        #if result = 2, Team1 overtime loss
        #if result = 3, Team2 overtime loss
        transformation1 = pow(10, team1.ELO/400)
        transformation2 = pow(10, team2.ELO/400)
        expectedscore = transformation1/(transformation1 + transformation2)
        if(result == 1):
            adjustment = 1
            team1.win += 1
            team1.gamesplayed += 1
            team2.gamesplayed += 1
            team2.loss += 1
            team1.ELO += kFactor * (adjustment - expectedscore)
            team2.ELO -= kFactor * (adjustment - expectedscore)
        elif(result == 0):
            adjustment = 0
            team1.loss += 1
            team1.gamesplayed += 1
            team2.gamesplayed += 1
            team2.win += 1
            team1.ELO -= kFactor * (adjustment - expectedscore)
            team2.ELO += kFactor * (adjustment - expectedscore)
        elif(result ==2):
            team1.otl += 1
            team1.gamesplayed += 1
            team2.gamesplayed += 1
            team2.win +=1
            team1.ELO -= kFactor * (1 - expectedscore)
            team2.ELO += kFactor * (1 - expectedscore)
        else:
            team2.otl += 1
            team1.gamesplayed += 1
            team2.gamesplayed += 1
            team1.win +=1
            team1.ELO += kFactor * (1 - expectedscore)
            team2.ELO -= kFactor * (1 - expectedscore)

    def winPercentageBetween(team1, team2):
        winpercentage = team1.ELO / (team1.ELO + team2.ELO)
        return winpercentage

class Team:
    def __init__(self, schedule, gamesplayed, name, division, conference, win, loss, otl, ELO):
        self.name = name
        self.divison = division
        self.conference = conference
        self.win = win
        self.gamesplayed = gamesplayed
        self.schedule = schedule
        self.loss = loss
        self.otl = otl
        self.ELO = ELO
    def printElo(self):
        print(self.name, " : ", self.win, " - ", self.loss, " - ", self.otl, "  =   ", self.ELO)

def playGame(team1, team2):
    result = random.randint(0,4)
    EloCalculator.calculateElo(team1, team2, result)
    team1.printElo()
    team2.printElo()

def main():
    team2 = Team([], 0,"Islanders", "Metro", "East", 0, 0, 0, 1000)
    team3 = Team([], 0,"Blackhawks", "Metro", "West", 0, 0, 0, 1000)
    team1 = Team([team2, team3, team3, team2, team3, team2], 0, "Stars", "Metro", "East", 0,0,0,1000)

    listprob = [.47, .50, .50]
    func  = PoiBin(listprob)
    print(func.pmf(2))
    gamelength = 10

    #Stars win, Isles lose
    playGame(team3, team1)
    for index in range(10):
        playGame(team1, team2)

    teams = {team1, team2, team3}
    standing = Standings(teams)
    sorted = standing.sortStandings("East")
    print(standing.pointsToMakePlayoffs("East").win)
    standing.getPlayoffProbability(team1)
    #for index in range(gamelength):
    #    print("GAME ", index)
    #    print("win %", teams[0].winPercentageBetween(teams[1]))
    #    playGame(teams[0], teams[1])
    #    shuffle(teams)
    #    print("--------------")




if __name__ == "__main__": main()