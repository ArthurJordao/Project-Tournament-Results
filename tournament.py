#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        print("<error message>")


def deleteMatches():
    """Remove all the match records from the database."""
    conn, c = connect()
    c.execute("TRUNCATE matches")
    conn.commit()
    conn.close


def deletePlayers():
    """Remove all the player records from the database."""
    conn, c = connect()
    c.execute("TRUNCATE players CASCADE")
    conn.commit()
    conn.close


def countPlayers():
    """Returns the number of players currently registered."""
    conn, c = connect()
    c.execute("SELECT * FROM count_players")
    rows = c.fetchone()
    number_of_players = int(rows[0])
    conn.close()
    return number_of_players


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    conn, c = connect()
    query = "INSERT INTO players (name) VALUES (%s)"
    params = (name,)
    c.execute(query, params)
    conn.commit()
    conn.close


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn, c = connect()
    c.execute("SELECT id, name, wins, matches FROM player_standings")
    rows = c.fetchall()
    player_stadings = [(row[0], row[1], row[2], row[3]) for row in rows]
    conn.close()
    return player_stadings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn, c = connect()
    query = "INSERT INTO matches (winner, loser) VALUES (%s, %s)"
    params = (winner, loser)
    c.execute(query, params)
    conn.commit()
    conn.close


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    number_of_players = countPlayers()
    rows = playerStandings()
    swiss_pairings = []
    x = 0
    while x < number_of_players:
        id_one = rows[x][0]
        name_one = rows[x][1]
        x = x + 1
        id_two = rows[x][0]
        name_two = rows[x][1]
        x = x + 1
        swiss_pairings.append((id_one, name_one, id_two, name_two))
    return swiss_pairings