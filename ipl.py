import numpy as np
import pandas as pd
# import json
# class NpEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, np.integer):
#             return int(obj)
#         if isinstance(obj, np.floating):
#             return float(obj)
#         if isinstance(obj, np.ndarray):
#             return obj.tolist()
#         return super(NpEncoder, self).default(obj)

# General Operations
balls = pd.read_csv("balls.csv")
matches = pd.read_csv("matches.csv")

# Merging
ipl = balls.merge(matches,left_on="match_id",right_on="id",how="inner")

# Correcting team names
ipl.replace({"Rising Pune Supergiant":"Rising Pune Supergiants","Delhi Daredevils":"Delhi Capitals","Kings XI Punjab":"Punjab Kings"},inplace=True)

# Converting to date object
ipl['date'] = pd.to_datetime(ipl['date'])

# Number of unique teams participated till yet. 
unique = pd.concat((ipl["team1"],ipl["team2"])).unique()

# Participating Teams 
def teamsAPI():
    teams = list(ipl["team1"].unique())
    teams_dict = {
        "Teams":teams
    }
    return teams_dict

# Teams vs Teams 
def teamVteamAPI(team1,team2):
    if team1 in unique and team2 in unique :
        data = ipl[((ipl["team1"]==team1)&(ipl["team2"]==team2))|((ipl["team2"]==team1)&(ipl["team1"]==team2))]

        # Number of times faced each other
        Matches_Played = data["id"].unique().shape[0]

        Team_1_Won = data[data["winner"]==team1]["id"].nunique()

        Team_2_Won = data[data["winner"]==team2]["id"].nunique()

        no_result = Matches_Played - (Team_1_Won+Team_2_Won)

        response = {"Matches Played":str(Matches_Played),
                team1: str(Team_1_Won),
                team2: str(Team_2_Won),
                "No Result": str(no_result)}
        return response
    else :
        return "Invalid Team Name" 
       
# Batsman Profile
def batsman_profile(batsman_name):
    try:
        if batsman_name not in ipl['batter'].unique():
               return f"Error: Batsman '{batsman_name}' not found in the dataset"

        # Number of Innings
        num_innings = ipl[ipl["batter"]==batsman_name]["id"].nunique()

        # Number of Runs
        batsman_runs = ipl[ipl["batter"]==batsman_name]['batsman_runs'].sum()

        # Balls_faced
        Balls_faced = ipl[ipl["batter"]==batsman_name].shape[0] - ipl[(ipl["batter"]==batsman_name)&(ipl["extras_type"]=='wides')].shape[0]
        # Strike Rate 
        strike_rate = ((batsman_runs/Balls_faced)*100).round(2)
        # Number of times got out 
        num_outs = ipl[ipl['player_dismissed']==batsman_name].shape[0]

        # Average
        Avg = round(batsman_runs/num_outs,2)

        # Temp Dataframe
        scores_df = ipl[ipl["batter"]==batsman_name].groupby(["id"]).agg({'batsman_runs':'sum'})

        # Highest_Score
        ipl[ipl["batter"]==batsman_name].groupby(["id"]).agg({'batsman_runs':'sum'}).sort_values(ascending=False,by='batsman_runs').iloc[0]["batsman_runs"]

        # Last 5 innings
        last_five = ','.join([str(i) for i in scores_df.tail(5).reset_index()["batsman_runs"].to_list()])

        # 50s
        fifties = scores_df[(scores_df["batsman_runs"]>50)&(scores_df["batsman_runs"]<100)].shape[0]

        # 100s
        centuries = scores_df[scores_df["batsman_runs"]>100].shape[0]
        Batsman_dict = {"Innings Played":str(num_innings),
                        "Runs": str(batsman_runs),
                        "Average":str(Avg),
                        "Strike Rate":str(strike_rate),
                        "50s":str(fifties),
                        "100s":str(centuries),
                        "Last 5 Innings":last_five}
        return Batsman_dict
    except Exception as e:
        return f"Some Error Occurred {e}" 

def bowler_profile(bowler):
    try:
        # Number of Innings
        num_innigs = ipl[ipl["bowler"]==bowler]["id"].nunique()

        # Wickets
        wickets = ipl[(ipl["bowler"]==bowler)&(~ipl["dismissal_kind"].isin(['run out','retired hurt','obstructing the field','retired out']))]["is_wicket"].sum()

        # Strike Rate 
        balls_bowled = ipl[(ipl["bowler"]==bowler)&(~ipl["extras_type"].isin(["wides","noballs"]))].shape[0]
        bowling_strike_rate = (balls_bowled/wickets).round(2)

        # Economy
        runs_conceeded = ipl[ipl["bowler"]==bowler]['total_runs'].sum()
        Bowling_Economy = ((runs_conceeded/balls_bowled)*6).round(2)

        # Best Fig.
        fig_df = ipl[ipl["bowler"]==bowler].groupby(["id"]).agg({'total_runs':'sum','is_wicket':'sum'}).sort_values(by=['is_wicket','total_runs'],ascending=[False,True])
        best_bowling = f"{fig_df["is_wicket"].iloc[0]}/{fig_df["total_runs"].iloc[0]}"

        # Recent Performance
        recent_df = ipl[ipl["bowler"]==bowler].groupby(["id"]).agg({'total_runs':'sum','is_wicket':'sum'}).tail(5).reset_index()
        fig_string = ""
        for i in range(recent_df.shape[0]):
            fig_string = fig_string+str(recent_df.iloc[i]["is_wicket"])+'/'+str(recent_df.iloc[i]["total_runs"])+","
        

        bowler_dict = {"Innings" : str(num_innigs),
                    "Wickets" : str(wickets),
                    "Strike Rate" : str(bowling_strike_rate),
                    "Economy" : str(Bowling_Economy),
                    "Best Bowling Figure": best_bowling,
                    "Recent Performance" : fig_string}
        return bowler_dict
    except Exception as e:
        return f"Some Error Occurred {e}"
    
def battervsteam(batsman,team):
    try:    
        # Grouping and Merging to calculate runs, Balls Faced and Highest Scores
        playervsteam = ipl[ipl["batter"]==batsman].groupby('bowling_team').agg({'batsman_runs':'sum','batter':'count'}).merge(ipl[ipl["batter"]==batsman].groupby(['bowling_team','id']).agg({'batsman_runs':'sum'}).reset_index().sort_values(by='batsman_runs',ascending=False).drop_duplicates(subset="bowling_team",keep="first").rename(columns={'batsman_runs':'Highest Score'}),on='bowling_team').drop("id",axis=1).merge(ipl[(ipl["batter"]==batsman)&(ipl['player_dismissed']!=batsman)].drop_duplicates(subset = "id",keep="first")["bowling_team"].value_counts(),on="bowling_team").rename(columns={"count":"innings_not_outs"})

        #  Creating Strike rate and Average Columns
        playervsteam["Strike Rate"] = ((playervsteam["batsman_runs"]/playervsteam["batter"])*100).round(2)

        playervsteam["Average"] = (playervsteam["batsman_runs"]/playervsteam["innings_not_outs"]).round(2)

        # Renaming and dropping columns
        playervsteam = playervsteam.rename(columns={"bowling_team":"Opponent Team","batsman_runs":"Runs"}).drop(["batter","innings_not_outs"],axis=1).sort_values("Runs",ascending=False).set_index("Opponent Team")

        return playervsteam.loc[team].transpose().to_dict()
    except Exception as e:
        return f"Error Occurred {e}"

def bowlervsteam(bowler,team):
    try:
        # Matches Played
        matches = ipl[(ipl["bowler"] == bowler)&(ipl['batting_team']==team)]["id"].unique().shape[0]

        # Wickets Taken
        wickets = ipl[(ipl["bowler"]==bowler)&(~ipl["dismissal_kind"].isin(['run out','retired hurt','obstructing the field','retired out']))&(ipl['batting_team']==team)]["is_wicket"].sum()

        # Runs Given
        runs_conceeded = ipl[(ipl["bowler"] == bowler)&(ipl['batting_team']==team)]["total_runs"].sum()

        # Balls Bowled 
        balls_bowled = ipl[(ipl["bowler"] == bowler)&(ipl['batting_team']==team)].shape[0]

        # Strike Rate 
        if wickets ==0 :
            strike_rate = 'NA'
        else:
            strike_rate = (balls_bowled/wickets).round(2)
            
        # Economy
        Bowling_Economy = ((runs_conceeded/balls_bowled)*6).round(2)
        
        # Best Bowling 
        best_bowling = str(ipl[(ipl["bowler"] == bowler)&(ipl['batting_team']==team)].groupby("id").agg({'is_wicket':"sum","total_runs":"sum"}).reset_index().drop(columns="id").sort_values(by=["is_wicket","total_runs"],ascending=[False,True]).iloc[0].to_dict().get('is_wicket')
        )+'/'+str(ipl[(ipl["bowler"] == bowler)&(ipl['batting_team']==team)].groupby("id").agg({'is_wicket':"sum","total_runs":"sum"}).reset_index().drop(columns="id").sort_values(by=["is_wicket","total_runs"],ascending=[False,True]).iloc[0].to_dict().get('total_runs')
        )

        bowlervteam_dict ={
            "Innings":str(matches),
            "Wickets":str(wickets),
            "Strike Rate":str(strike_rate),
            "Economy":str(Bowling_Economy),
            "Best Fig":str(best_bowling)
        }
        return bowlervteam_dict
    except Exception as e:
        return f"Error Occurred {e}"

def venuestats(venue):
    try:
        # Creating a Subset 
        subset_venue_data = ipl[ipl["venue"] == venue].groupby(["match_id",'inning']).agg({'total_runs':'sum','is_wicket':'sum'}).reset_index().set_index("match_id")

        # Excluding Super Overs 
        subset_venue_data = subset_venue_data[subset_venue_data['inning'].isin([1,2])]

        # First Inning Score 
        Average_First_inning_score = str(subset_venue_data[subset_venue_data['inning']==1][["total_runs","is_wicket"]].mean().round(0).astype(int).to_dict().get('total_runs'))+'/'+str(subset_venue_data[subset_venue_data['inning']==1][["total_runs","is_wicket"]].mean().round(0).astype(int).to_dict().get('is_wicket'))

        # Second Inning score 
        Average_second_inning_score = str(subset_venue_data[subset_venue_data['inning']==2][["total_runs","is_wicket"]].mean().round(0).astype(int).to_dict().get('total_runs'))+'/'+str(subset_venue_data[subset_venue_data['inning']==2][["total_runs","is_wicket"]].mean().round(0).astype(int).to_dict().get('is_wicket'))

        # Highest Score by Batsman
        Highest_Batsman_Score = ipl[ipl["venue"] == venue].groupby(["match_id",'batter']).agg({"batsman_runs":"sum"}).sort_values("batsman_runs",ascending=False).reset_index().drop(columns='match_id').iloc[0].to_dict()

        # Max Wickets by a Bowler
        Max_Wickets = ipl[(ipl["venue"]==venue)&(ipl['dismissal_kind'].isin(['caught', 'bowled','lbw','stumped', 'caught and bowled']))&(ipl['is_wicket']==1)].groupby("bowler").agg({"is_wicket":"sum"}).sort_values(by="is_wicket",ascending=False).reset_index().rename(columns={"is_wicket":"Wickets"}).iloc[0].to_dict()

        # Best Bowling Figure
        bowling_fig_df = ipl[(ipl["venue"]==venue)&(~ipl["dismissal_kind"].isin(['run out','retired hurt','obstructing the field','retired out']))].groupby(["match_id","bowler"]).agg({'is_wicket':"sum","total_runs":"sum"}).reset_index().sort_values(by=["is_wicket","total_runs"],ascending=[False,True]).drop(columns="match_id").rename(columns={"bowler":"Bowler","is_wicket":"Wickets","total_runs":"Runs Conceeded"})

        bowling_fig_df["Bowling Fig"] = bowling_fig_df["Wickets"].astype(str)+'/'+bowling_fig_df["Runs Conceeded"].astype(str)
        bowling_fig_df.drop(columns=["Wickets","Runs Conceeded"],inplace=True)
        bowling_fig_df.iloc[0].to_dict()

        # Best Team Score
        highest_score_team = ipl[ipl["venue"]==venue].groupby(["id","inning","batting_team"]).agg({"total_runs":"sum",'is_wicket':"sum"}).reset_index().sort_values(by=["total_runs","is_wicket"],ascending=[False,True]).drop(columns=["id","inning"])
        highest_score_team["Score"]=highest_score_team["total_runs"].astype(str)+"/"+highest_score_team["is_wicket"].astype(str)
        highest_score_team = highest_score_team.drop(columns=["total_runs","is_wicket"]).iloc[0].to_dict()

        venue_dict = {"First Inning Average Score":str(Average_First_inning_score),
                    "Second Inning Average Score":str(Average_second_inning_score),
                    "Highest Individual Score":str(Highest_Batsman_Score),
                    "Most Wickets Taken":str(Max_Wickets),
                    "Best Bowling Figure":str(bowling_fig_df.iloc[0].to_dict()),
                    "Highest Team Score":str(highest_score_team)
                    }
        

        return venue_dict
    except Exception as e:
        return f"Some Error Occurred : {e}"

def BattervBatter(bat1,bat2):
    batsman1 = batsman_profile(bat1)
    batsman2 = batsman_profile(bat2)
    compare_dict = {bat1:batsman1,
                    bat2:batsman2}
    return compare_dict

def BowlervBowler(bowl1,bowl2):
    bowler1 = bowler_profile(bowl1)
    bowler2 = bowler_profile(bowl2)
    compare_dict = {bowl1:bowler1,
                    bowl2:bowler2}
    return compare_dict

def BattervBowler(bat,bowl):
    try:
        # Extracting only relevant columns
        ipl_df = ipl[['id','inning', 'over', 'ball','batter', 'bowler','batsman_runs','is_wicket','player_dismissed','dismissal_kind', 'fielder']]

        # Adding Six and Four Count
        ipl_df["Six"] = (ipl_df["batsman_runs"]==6).astype(int)

        ipl_df["Four"] = (ipl_df["batsman_runs"]==4).astype(int)

        # Grouping according to Batsman and Bowler 
        bowlervsbatter_df = ipl_df[(~ipl_df["dismissal_kind"].isin(['run out','retired hurt','obstructing the field','retired out']))].groupby(["batter","bowler"]).agg({"batsman_runs":"sum","batter":"count","is_wicket":"sum","Six":"sum","Four":"sum","id":"nunique"}).rename(columns={"batsman_runs":"Runs","batter":"Balls Faced","is_wicket":"Out","id":"Innings"}).reset_index()
        
        #  Strike Rate 
        bowlervsbatter_df["Strike Rate"] = ((bowlervsbatter_df["Runs"]/bowlervsbatter_df["Balls Faced"])*100).round(2)

        # Final Sorting
        output = bowlervsbatter_df[(bowlervsbatter_df["batter"]==bat)&(bowlervsbatter_df["bowler"]==bowl)].reset_index().drop(columns="index").transpose().to_dict().get(0)
            
        return output
    except Exception as e:
        return f"Error Ocurred {e}"

# Most Catches
most_catches = ipl[(ipl['is_wicket']==1)&(ipl['dismissal_kind']=="caught")]["fielder"].value_counts().reset_index().rename(columns={"fielder":"Player","count":"Catches"}).iloc[0].to_dict()

# Most Runouts
most_runouts = ipl[(ipl['is_wicket']==1)&(ipl['dismissal_kind']=='run out')]["fielder"].value_counts().reset_index().rename(columns={"fielder":"Player","count":"Run Outs"}).iloc[0].to_dict()

# Most Stumpings
Stumpings = ipl[(ipl['is_wicket']==1)&(ipl['dismissal_kind']=='stumped')]["fielder"].value_counts().reset_index().rename(columns={"fielder":"Player","count":"Stumpings"}).iloc[0].to_dict()

# Most Ducks
duck_df = ipl.groupby(["batter","id"]).agg({"batsman_runs":"sum"}).rename(columns = {"batsman_runs":"Runs"}).reset_index().drop(columns="id")
ducks = duck_df[duck_df["Runs"]==0].value_counts().reset_index().drop(columns="Runs").rename(columns={"batter":"Batsman","count":"Ducks"}).iloc[0].to_dict()

# Players Scored Most in  90s:
duck_df[(duck_df["Runs"]>=90)&(duck_df["Runs"]<100)].value_counts().reset_index().drop(columns="Runs").rename(columns={"batter":"Batsman","count":"Times"})[["Batsman","Times"]].head()

most_scored = duck_df[(duck_df["Runs"]>=90)&(duck_df["Runs"]<100)].value_counts().reset_index().drop(columns="Runs").rename(columns={"batter":"Batsman","count":"Times"})[["Batsman","Times"]].head()
most_scored_dict = {i:j for i,j in zip(most_scored["Batsman"],most_scored["Times"])}

#  Most Bowled
Most_bowled = ipl[(ipl["player_dismissed"]==ipl["batter"])&(ipl["dismissal_kind"]=="bowled")]["batter"].value_counts().reset_index().rename(columns={"batter":"Batsman","count":"Times"}).iloc[0].to_dict()
