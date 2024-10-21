from flask import Flask,jsonify,request
import ipl

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Cricket API"

@app.route('/ipl/ParticipatingTeams')
def teams():
    teams = ipl.teamsAPI()
    return jsonify(teams)

@app.route('/ipl/teamvsteam')
def teamvsteam():
    team_1 = request.args.get('team1')
    team_2 =request.args.get('team2')
    response = ipl.teamVteamAPI(team_1,team_2)
    return jsonify(response)

@app.route('/ipl/batsmanprofile')
def batsmanprofile():
    batter =request.args.get('Batsman')
    response = ipl.batsman_profile(batter)
    return jsonify(response)

@app.route('/ipl/bowlerprofile')
def bowlerprofile():
    bowler = request.args.get('Bowler')
    response = ipl.bowler_profile(bowler)
    return jsonify(response)

@app.route('/ipl/battervteam')
def battervteam():
    batter = request.args.get('Batsman')
    team = request.args.get('Opponent Team')
    response = ipl.battervsteam(batter,team)
    return jsonify(response)

@app.route('/ipl/bowlervteam')
def bowlervteam():
    bowler =request.args.get('bowler')
    team = request.args.get('Opponent team')
    response = ipl.bowlervsteam(bowler,team)
    return jsonify(response)
# Venue
@app.route('/ipl/venuestat')
def venuestat():
    venue = request.args.get('venue')
    response = ipl.venuestats(venue)
    return jsonify(response)

@app.route('/ipl/BattervBatter')
def BattervsBatter():
    batter1 = request.args.get('Batter1')
    batter2 = request.args.get('Batter2')
    response = ipl.BattervBatter(batter1,batter2)
    return jsonify(response)

@app.route('/ipl/BowlervBowler')
def BowlervsBowler():
    bowler1 = request.args.get('bowler1')
    bowler2 = request.args.get('bowler2')
    response = ipl.BowlervBowler(bowler1,bowler2)
    return jsonify(response)
# Error
@app.route('/ipl/BattervBowler')
def BattervsBowler():
    batter =  request.args.get('batter')
    bowler =  request.args.get('bowler')
    response = ipl.BattervBowler(batter,bowler)
    return jsonify(response)

@app.route('/ipl/mostcatches')
def mostcatches():
    response = ipl.most_catches
    return jsonify(response)

@app.route('/ipl/mostrunouts')
def mostrunouts():
    response = ipl.most_runouts
    return jsonify(response)

@app.route('/ipl/stumpings')
def stumpings():
    response = ipl.Stumpings
    return jsonify(response)

@app.route('/ipl/Mostducks')
def mostducks():
    response = ipl.ducks
    return jsonify(response)

@app.route('/ipl/most90s')
def most90s():
    response = ipl.most_scored_dict
    return jsonify(response)

@app.route('/ipl/Mostbowled')
def Mostbowled():
    response = ipl.Most_bowled
    return jsonify(response)

app.run(debug=True)
