# Cricket Stats API

This is a Python-based Cricket Stats API built using Flask and Pandas. The API provides comprehensive cricket statistics covering various aspects of player, team, and venue performances.

## Features

The API offers endpoints to retrieve a wide range of cricket statistics, including:

Player Profiles:
  - Batsman Profile: Innings, Runs, Strike Rate, Highest Score, 100s, 50s, Average, Last 5 Innings.
  - Bowler Profile: Innings, Wickets, Strike Rate, Best Figures, Economy, Last 5 Innings.

Batsman vs Team: Runs, Strike Rate, Highest Score, Average.

Bowler vs Team: Runs Given, Wickets, Strike Rate, Best Figures, Economy.

Venue Stats:
  - Batting First Innings, Bowling First Innings, Highest Scores (Batsman, Bowler, Team), Lowest Team Score, Average First and Second Innings Score, Best Bowling Figures.

Seasonal Stats:
  - Points Table Season Wise.

Player vs Player:
  - Batsman vs Batsman (Profile Comparison), Bowler vs Bowler (Profile Comparison), Batsman vs Bowler (No. of times out, strike rate, runs, sixes, fours).

Miscellaneous Stats:
  - Most Catches, Most Runouts, Most Ducks, Most times on 90+, Highest Team Scores (Overall and Season Wise), Lowest Team Scores (Overall and Season Wise), Most Stumpings, Most times Bowled, Most Umpires, Most Matches Played.

## Technologies Used

Python: Backend logic and data processing.  
Flask: Framework to create RESTful API endpoints.  
Pandas: For handling and processing cricket data efficiently.


```bash
pip install flask pandas
```
