/*Create a table that adds the final outcome of the game to each event in game*/
CREATE OR REPLACE TABLE `baseball.archive_with_final_score` AS
with wins as (
SELECT  max(away_score) over(partition by game_date,home_team, away_team) max_away_score,
        max(home_score) over(partition by game_date,home_team, away_team) max_home_score,
        int64_field_0,
        game_date
FROM `assignment-1-391514.baseball.archive` 
)
SELECT b.* , 
        case 
        when max_away_score < max_home_score 
        then 1 else 0 
        end as home_team_win 
from `assignment-1-391514.baseball.archive` b
LEFT JOIN wins w 
ON b.game_date = w.game_date
AND b.int64_field_0 = w.int64_field_0
