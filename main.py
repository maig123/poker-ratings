from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import bs4 as bs
import trueskill as ts
import csv
from copy import deepcopy

class Player():
    #rating_history = []

    def __init__(self, name, mu = 25, sigma = 8.333):
        self.current_rating = ts.Rating(float(mu), float(sigma))
        self.name = str(name).strip()
        self.rating_history = []
        self.rating_history.append([float(mu), float(sigma)])
    
    def update_rating(self, a):
        #self.rating = ts.Rating(float(mu), float(sigma))
        #new_list = [str(deepcopy(rating.mu)), str(deepcopy(self.rating.sigma))]
        #check if rating is the same 
        print()
        if self.current_rating.mu == float(a[0]):
            print("no change")
        else: 
            self.current_rating = ts.Rating(float(a[0]), float(a[1]))
            new_list = [float(a[0]), float(a[1])]
            #print("current" , self.rating_history)
            #print("adding::::" ,new_list)
            
            self.rating_history.append(new_list)

    #writes player info to datasource 
    def save_player(self):
        print(self.name)
        print(self.rating)
        print(self.rating_history)

    def load_player(self, file): 
        print("loading player")
                




def savedata(filename, thingtowrite): 
    print("########IMMMM SAVING DATA#########")
    f = open(filename, 'w+')
    
    
    f.write(thingtowrite)
    f.close() 

def extract_results(soup):
    table = soup.find('table', { 'class': 'mat-table cdk-table mat-elevation-z8 m-b-75'})
    rows = table.findAll('tr')
    name = ""
    winnings = ""
    players = list()
    for row in rows:
        cells = row.findChildren('td')
        inc = 0
        for cell in cells:
            if inc == 1: 
                name = cell.string
            if inc == 2: 
                winnings = cell.string
            inc += 1
        if name != "":
            players.append(name)
        print(name.strip(),winnings)
        
    return players 
        

def create_episode_string(episodenumber):
    #first 10 are 01-09,
    #therest are %20
    #%2001 = 01
    #%2010 = 10
    root = "https://www.trackingpoker.com/live/Episode%20"
    string = ""
    
    if episodenumber < 10: 
        string = root + "0" + str(episodenumber)
    else:
        string = root+str(episodenumber)
    return string



def processfile(file, current_stats_dict):
    soup = bs.BeautifulSoup(open(file), "html.parser")
    players = extract_results(soup)
    results = list()
    for person in players:
        print(person) 
        if not person in current_stats_dict: 
            results.append(Player(person))
        else: 
            results.append(Player(person, current_stats_dict[person][0], current_stats_dict[person][1]))
    ratinglist = []
    for result in results: 
        ratinglist.append([result.current_rating])
    testresult = ts.rate(ratinglist)

    #player_dict = {}

    for x in range(len(players)):
        results[x].current_rating = testresult[x]
        
        print(results[x].name + "," + str(results[x].current_rating[0].mu) + "," + str(results[x].current_rating[0].sigma))
        current_stats_dict[results[x].name] = [str(results[x].current_rating[0].mu), str(results[x].current_rating[0].sigma)]
    
    return current_stats_dict


#field_names = []
def savedata(outfile, player_dict):
    with open(outfile, 'w+') as f: 
        csvwriter = csv.writer(f, delimiter=",")

        for k,v in player_dict.items():
            csvwriter.writerow([k, v[0], v[1]])




getdata = False
if getdata:
    driver = webdriver.Chrome()

    start = 395
    finish = 397

    for x in range(start, finish):
        driver.get(create_episode_string(x))
        soup = bs.BeautifulSoup(driver.page_source, 'html.parser')
        savefile="site-data/" + str(x)+".html"
        savedata(savefile, soup.prettify())
        extract_results(soup)

    driver.close()

loaddata = False
if loaddata:
    loaded_data = {}
    results = processfile("site-data/1.html", loaded_data)
    excludelist = [395, 396, 551]
    for x in range(1,568): 
        if not x in excludelist:
            file = "site-data/" + str(x) + ".html"
            results = processfile(file, results)
            outfile = str(x)+".csv"
            savedata(outfile, results)

 


buildcharts = True
excludelist = [395, 396, 551]
results_sofar = {}
if buildcharts: 
    #loop through *.csv 
    for x in range(1, 567):
        if not x in excludelist:
            loadfile = "ratings/" +str(x) + ".csv"

            with open(loadfile,'r') as f:
                csvreader = csv.reader(f)
                for row in csvreader:
                    if not row[0] in results_sofar:
                        results_sofar[row[0]] = Player(name = row[0], mu = row[1], sigma = row[2])
                    else:
                        temp = [float(row[1]), float(row[2])]
                        results_sofar[row[0]].update_rating(temp)

