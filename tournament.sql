-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

CREATE TABLE players 
  ( 
     id   SERIAL PRIMARY KEY, 
     name TEXT 
  ); 

CREATE TABLE matches 
  ( 
     id     SERIAL PRIMARY KEY, 
     winner INTEGER REFERENCES players(id), 
     loser  INTEGER REFERENCES players(id) 
  ); 

CREATE VIEW count_players 
AS 
  SELECT Count(*) 
  FROM   players; 

CREATE VIEW player_wins 
AS 
  SELECT players.id, 
         players.name, 
         Count(matches.winner) AS wins 
  FROM   players 
         left join matches 
                ON players.id = matches.winner 
  GROUP  BY players.id; 

CREATE VIEW player_loses 
AS 
  SELECT players.id, 
         players.name, 
         Count(matches.loser) AS loses 
  FROM   players 
         left join matches 
                ON players.id = matches.loser 
  GROUP  BY players.id; 

CREATE VIEW player_matches 
AS 
  SELECT players.id, 
         players.name, 
         Count(matches) AS matches 
  FROM   players 
         left join matches 
                ON players.id = matches.loser 
                    OR players.id = matches.winner 
  GROUP  BY players.id; 

CREATE VIEW player_standings 
AS 
  SELECT players.id, 
         players.name, 
         player_wins.wins, 
         player_matches.matches 
  FROM   player_wins, 
         players, 
         player_matches 
  WHERE  player_wins.id = players.id 
         AND players.id = player_matches.id 
  ORDER  BY wins DESC; 