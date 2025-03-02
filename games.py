import pandas as pd

def main():
    # Load the dataset
    games_2022 = pd.read_csv("games_2022.csv")  # Update path if necessary

    # Determine winners based on correct score columns
    games_2022["win"] = games_2022["team_score"] > games_2022["opponent_team_score"]

    # Group by team and calculate statistics
    team_stats = games_2022.groupby("team").agg(
        games_played=("game_id", "count"),
        wins=("win", "sum"),
        total_points_scored=("team_score", "sum"),
        total_points_allowed=("opponent_team_score", "sum")
    ).reset_index()

    # Calculate win percentage and point differential
    team_stats["win_percentage"] = team_stats["wins"] / team_stats["games_played"]
    team_stats["point_differential"] = team_stats["total_points_scored"] - team_stats["total_points_allowed"]

    # Rank teams based on win percentage and point differential
    team_stats = team_stats.sort_values(by=["win_percentage", "point_differential"], ascending=[False, False])

    # Display the top-ranked teams
    # print(team_stats.head(10))
    print(team_stats)

def main2():
    # Load the dataset
    games_2022 = pd.read_csv("games_2022.csv")  # Update path if necessary

    # Calculate possessions
    games_2022["possessions"] = (
        games_2022["FGA_2"] + games_2022["FGA_3"] - games_2022["OREB"] 
        + games_2022["TOV"] + (0.44 * games_2022["FTA"])
    )

    # Calculate offensive and defensive efficiency
    games_2022["offensive_efficiency"] = games_2022["team_score"] / games_2022["possessions"]
    games_2022["defensive_efficiency"] = games_2022["opponent_team_score"] / games_2022["possessions"]
    games_2022["net_rating"] = games_2022["offensive_efficiency"] - games_2022["defensive_efficiency"]

    # Aggregate team statistics
    team_stats = games_2022.groupby("team").agg(
        games_played=("game_id", "count"),
        avg_off_eff=("offensive_efficiency", "mean"),
        avg_def_eff=("defensive_efficiency", "mean"),
        avg_net_rating=("net_rating", "mean")
    ).reset_index()

    # Rank teams by net rating
    team_stats = team_stats.sort_values(by="avg_net_rating", ascending=False)

    # Display the top-ranked teams
    print(team_stats.head(10))

main()