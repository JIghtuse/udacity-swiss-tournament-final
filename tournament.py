#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import logging
import psycopg2


def connect(database_name="tournament"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        cursor = db.cursor()
        return db, cursor
    except:
        logging.critical("Cannot connect to database {}".format(database_name))


def deleteMatches():
    """Remove all the match records from the database."""
    connection, cursor = connect()

    cursor.execute("delete from matches;")

    connection.commit()
    connection.close()


def deletePlayers():
    """Remove all the player records from the database."""
    connection, cursor = connect()

    cursor.execute("delete from players;")

    connection.commit()
    connection.close()


def countPlayers():
    """Returns the number of players currently registered."""
    connection, cursor = connect()

    cursor.execute("select count(id) from players;")
    players_count = cursor.fetchone()

    connection.commit()
    connection.close()
    return players_count[0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    connection, cursor = connect()

    query = "insert into players (name) values (%s)"
    query_params = (name,)
    cursor.execute(query, query_params)

    connection.commit()
    connection.close()


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
    connection, cursor = connect()

    # Standings are represented by player_standings view, so just get it
    query = "select * from player_standings;"
    cursor.execute(query)
    standings = cursor.fetchall()

    connection.commit()
    connection.close()
    return standings


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    connection, cursor = connect()

    # Store match data
    query = "insert into matches (winner, loser) values (%s,%s)"
    query_params = (winner, loser)
    cursor.execute(query, query_params)

    connection.commit()
    connection.close()


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
    connection, cursor = connect()

    # Needed information is in player_standings view, just filter it
    query = "select id, name from player_standings;"
    cursor.execute(query)
    standings = cursor.fetchall()

    connection.commit()
    connection.close()

    # transforms
    # [(id1, name1), (id2, name2), ...]
    # into
    # [(id1, name1, id2, name2), ...]
    pairings = [a + b for a, b in zip(standings[::2], standings[1::2])]
    return pairings
