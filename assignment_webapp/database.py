#!/usr/bin/env python3
"""
MediaServer Database module.
Contains all interactions between the webapp and the queries to the database.
"""

import configparser
import json
import sys
from time import strptime

from modules import pg8000


################################################################################
#   Welcome to the database file, where all the query magic happens.
#   My biggest tip is look at the *week 8 lab*.
#   Important information:
#       - If you're getting issues and getting locked out of your database.
#           You may have reached the maximum number of connections.
#           Why? (You're not closing things!) Be careful!
#       - Check things *carefully*.
#       - There may be better ways to do things, this is just for example
#           purposes
#       - ORDERING MATTERS
#           - Unfortunately to make it easier for everyone, we have to ask that
#               your columns are in order. WATCH YOUR SELECTS!! :)
#   Good luck!
#       And remember to have some fun :D
################################################################################

#############################
#                           #
# Database Helper Functions #
#                           #
#############################


#####################################################
#   Database Connect
#   (No need to touch
#       (unless the exception is potatoing))
#####################################################

def database_connect():
    """
    Connects to the database using the connection string.
    If 'None' was returned it means there was an issue connecting to
    the database. It would be wise to handle this ;)
    """
    # Read the config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    if 'database' not in config['DATABASE']:
        config['DATABASE']['database'] = config['DATABASE']['user']

    # Create a connection to the database
    connection = None
    try:
        # Parses the config file and connects using the connect string
        connection = pg8000.connect(database=config['DATABASE']['database'],
                                    user=config['DATABASE']['user'],
                                    password=config['DATABASE']['password'],
                                    host=config['DATABASE']['host'])
    except pg8000.OperationalError as operation_error:
        print("""Error, you haven't updated your config.ini or you have a bad
        connection, please try again. (Update your files first, then check
        internet connection)
        """)
        print(operation_error)
        return None

    # return the connection to use
    return connection


##################################################
# Print a SQL string to see how it would insert  #
##################################################

def print_sql_string(inputstring, params=None):
    """
    Prints out a string as a SQL string parameterized assuming all strings
    """

    if params is not None:
        if params != []:
            inputstring = inputstring.replace("%s", "'%s'")

    print(inputstring % params)


#####################################################
#   SQL Dictionary Fetch
#   useful for pulling particular items as a dict
#   (No need to touch
#       (unless the exception is potatoing))
#   Expected return:
#       singlerow:  [{col1name:col1value,col2name:col2value, etc.}]
#       multiplerow: [{col1name:col1value,col2name:col2value, etc.},
#           {col1name:col1value,col2name:col2value, etc.},
#           etc.]
#####################################################

def dictfetchall(cursor, sqltext, params=None):
    """ Returns query results as list of dictionaries."""

    result = []
    if (params is None):
        print(sqltext)
    else:
        print("we HAVE PARAMS!")
        print_sql_string(sqltext, params)

    cursor.execute(sqltext, params)
    cols = [a[0].decode("utf-8") for a in cursor.description]
    print(cols)
    returnres = cursor.fetchall()
    for row in returnres:
        result.append({a: b for a, b in zip(cols, row)})
    # cursor.close()
    return result


def dictfetchone(cursor, sqltext, params=None):
    """ Returns query results as list of dictionaries."""
    # cursor = conn.cursor()
    result = []
    cursor.execute(sqltext, params)
    cols = [a[0].decode("utf-8") for a in cursor.description]
    returnres = cursor.fetchone()
    result.append({a: b for a, b in zip(cols, returnres)})
    return result


#####################################################
#   Query (1)
#   Login
#####################################################

def check_login(username, password):
    """
    Check that the users information exists in the database.
        - True => return the user data
        - False => return None
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below in a manner similar to Wk 08 Lab to log the user in #
        #############################################################################

        sql = """SELECT *
                 FROM mediaserver.useraccount
                 WHERE username=%s AND password=%s
                 """
        # username = "james.smith"
        # password = "2KK8oykkvp"
        # print(username)
        # print(password)

        r = dictfetchone(cur, sql, (username, password))
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except Exception as e:
        # If there were any errors, return a NULL row printing an error to the debug
        print("the exception is [{}]".format(e))
        print("Error Invalid Login")
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Is Superuser? -
#   is this required? we can get this from the login information
#####################################################

def is_superuser(username):
    """
    Check if the user is a superuser.
        - True => Get the departments as a list.
        - False => Return None
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """SELECT isSuper
                 FROM mediaserver.useraccount
                 WHERE username=%s AND isSuper"""
        print("username is: " + username)
        cur.execute(sql, (username))
        r = cur.fetchone()  # Fetch the first row
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (1 b)
#   Get user playlists
#####################################################
def user_playlists(username):
    """
    Check if user has any playlists
        - True -> Return all user playlists
        - False -> Return None
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        ###############################################################################
        # Fill in the SQL below and make sure you get all the playlists for this user #
        ###############################################################################
        sql = """
            select a.collection_id,collection_name,count(*) as count
            from mediaserver.mediacollection a
            join mediaserver.mediacollectioncontents m on a.collection_id = m.collection_id
            join mediaserver.mediaitem m2 on m.media_id = m2.media_id
            where username = %s
            group by a.collection_id, collection_name
            order by a.collection_id,a.collection_name,count
        """

        print("username is: " + username)
        r = dictfetchall(cur, sql, (username,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting User Playlists:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (1 a)
#   Get user podcasts
#####################################################
def user_podcast_subscriptions(username):
    """
    Get user podcast subscriptions.
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #################################################################################
        # Fill in the SQL below and get all the podcasts that the user is subscribed to #
        #################################################################################

        sql = """
            select * from mediaserver.subscribed_podcasts a
            inner join mediaserver.podcast b on a.podcast_id = b.podcast_id
            where username=%s
        """

        r = dictfetchall(cur, sql, (username,))
        print("return val is:")
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Podcast subs:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (1 c)
#   Get user in progress items
#####################################################
def user_in_progress_items(username):
    """
    Get user in progress items that aren't 100%
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        ###################################################################################
        # Fill in the SQL below with a way to find all the in progress items for the user #
        ###################################################################################

        sql = """
        select *,play_count as playcount from mediaserver.UserMediaConsumption
        join mediaserver.mediaitem m on m.media_id = usermediaconsumption.media_id
        where username=%s and progress != 100

        """

        r = dictfetchall(cur, sql, (username,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting User Consumption - Likely no values:", sys.exc_info()[0])
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Get all artists
#####################################################
def get_allartists():
    """
    Get all the artists in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select 
            a.artist_id, a.artist_name, count(amd.md_id) as count
        from 
            mediaserver.artist a left outer join mediaserver.artistmetadata amd on (a.artist_id=amd.artist_id)
        group by a.artist_id, a.artist_name
        order by a.artist_name;"""

        r = dictfetchall(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Artists:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Get all songs
#####################################################
def get_allsongs():
    """
    Get all the songs in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select 
            s.song_id, s.song_title, string_agg(saa.artist_name,',') as artists
        from 
            mediaserver.song s left outer join 
            (mediaserver.Song_Artists sa join mediaserver.Artist a on (sa.performing_artist_id=a.artist_id)
            ) as saa  on (s.song_id=saa.song_id)
        group by s.song_id, s.song_title
        order by s.song_id"""

        r = dictfetchall(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Songs:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Get all podcasts
#####################################################
def get_allpodcasts():
    """
    Get all the podcasts in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select 
                p.*, pnew.count as count  
            from 
                mediaserver.podcast p, 
                (select 
                    p1.podcast_id, count(*) as count 
                from 
                    mediaserver.podcast p1 left outer join mediaserver.podcastepisode pe1 on (p1.podcast_id=pe1.podcast_id) 
                    group by p1.podcast_id) pnew 
            where p.podcast_id = pnew.podcast_id;"""

        r = dictfetchall(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Podcasts:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Get all albums
#####################################################
def get_allalbums():
    """
    Get all the Albums in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select 
                a.album_id, a.album_title, anew.count as count, anew.artists
            from 
                mediaserver.album a, 
                (select 
                    a1.album_id, count(distinct as1.song_id) as count, array_to_string(array_agg(distinct ar1.artist_name),',') as artists
                from 
                    mediaserver.album a1 
			left outer join mediaserver.album_songs as1 on (a1.album_id=as1.album_id) 
			left outer join mediaserver.song s1 on (as1.song_id=s1.song_id)
			left outer join mediaserver.Song_Artists sa1 on (s1.song_id=sa1.song_id)
			left outer join mediaserver.artist ar1 on (sa1.performing_artist_id=ar1.artist_id)
                group by a1.album_id) anew 
            where a.album_id = anew.album_id;"""

        r = dictfetchall(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Albums:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (3 a,b c)
#   Get all tvshows
#####################################################
def get_alltvshows():
    """
    Get all the TV Shows in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all tv shows and episode counts #
        #############################################################################
        sql = """
                select t.tvshow_id, tvshow_title,count(*)
                from mediaserver.tvepisode
                join mediaserver.tvshow t on tvepisode.tvshow_id = t.tvshow_id
                group by t.tvshow_id, tvshow_title
                order by tvshow_id
                """

        r = dictfetchall(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Get all movies
#####################################################
def get_allmovies():
    """
    Get all the Movies in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select 
            m.movie_id, m.movie_title, m.release_year, count(mimd.md_id) as count
        from 
            mediaserver.movie m left outer join mediaserver.mediaitemmetadata mimd on (m.movie_id = mimd.media_id)
        group by m.movie_id, m.movie_title, m.release_year
        order by movie_id;"""

        r = dictfetchall(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Movies:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Get one artist
#####################################################
def get_artist(artist_id):
    """
    Get an artist by their ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select *
        from mediaserver.artist a left outer join 
            (mediaserver.artistmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) amd
        on (a.artist_id=amd.artist_id)
        where a.artist_id=%s"""

        r = dictfetchall(cur, sql, (artist_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Artist with ID: '" + artist_id + "'", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (2 a,b,c)
#   Get one song
#####################################################
def get_song(song_id):
    """
    Get a song by their ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about a song    #
        # and the artists that performed it                                         #
        #############################################################################
        sql = """
            select s.song_id,song_title,
                    length,
                   m2.md_type_name as md_type_name,
                   md_value as md_value,
                   aa.artist_name as artists

            from mediaserver.song s
            join (select s.song_id,string_agg(a.artist_name,',') as artist_name from mediaserver.song s
                    join mediaserver.song_artists sa on s.song_id = sa.song_id
                    join mediaserver.artist a on sa.performing_artist_id = a.artist_id
                    group by s.song_id
                 ) aa on s.song_id = aa.song_id
            left join mediaserver.MediaItemMetaData a2 on s.song_id = a2.media_id
            left join mediaserver.metadata m on a2.md_id = m.md_id
            left join mediaserver.metadatatype m2 on m.md_type_id = m2.md_type_id     
            where s.song_id = %s
        """
        print(type(song_id))

        print(sql)
        r = dictfetchall(cur, sql, (song_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Songs:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (2 d)
#   Get metadata for one song
#####################################################
def get_song_metadata(song_id):
    """
    Get the meta for a song by their ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all metadata about a song       #
        #############################################################################

        

        sql = """
           select song_title,
                    length,
                   m2.md_type_name as md_type_name,
                   md_value as md_value,
                   string_agg(distinct(artist_name), ',') as artists

            from mediaserver.song s
            join mediaserver.MediaItemMetaData a2 on s.song_id = a2.media_id
            join mediaserver.metadata m on a2.md_id = m.md_id
            join mediaserver.metadatatype m2 on m.md_type_id = m2.md_type_id
            join mediaserver.song_artists sa on s.song_id = sa.song_id
            join mediaserver.artist a on sa.performing_artist_id = a.artist_id
            where s.song_id = %s
            group by song_title,length, m2.md_type_name,md_value
        """
        r = dictfetchall(cur, sql, (song_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting song metadata for ID: " + song_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (6 a,b,c,d,e)
#   Get one podcast and return all metadata associated with it
#####################################################
def get_podcast(podcast_id):
    """
    Get a podcast by their ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about a podcast #
        # including all metadata associated with it                                 #
        #############################################################################
        sql = """
            select podcast_id, podcast_title as podcast_name, podcast_uri,podcast_last_updated, md_type_name, md_value
            from mediaserver.podcast
            natural join mediaserver.podcastmetadata
            natural join mediaserver.metadata
            natural join mediaserver.metadatatype
            where podcast_id = %s
        """

        r = dictfetchall(cur, sql, (podcast_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Podcast with ID: " + podcast_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (6 f)
#   Get all podcast eps for one podcast
#####################################################
def get_all_podcasteps_for_podcast(podcast_id):
    """
    Get all podcast eps for one podcast by their podcast ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # podcast episodes in a podcast                                             #
        #############################################################################

        sql = """
                SELECT podcastepisode.media_id AS Podcast_Episode_ID,
                podcast_episode_title AS Podcast_Episode_Title,
                podcast_episode_URI AS Podcast_Episode_URI,
                podcast_episode_published_date AS
                Podcast_Episode_Date_Published,
                podcast_episode_length AS Podcast_Episode_Length, md_value, md_type_name
                FROM mediaserver.PodcastEpisode NATURAL JOIN mediaserver.MediaItem NATURAL JOIN
                mediaserver.MediaItemmetadata NATURAL JOIN mediaserver.MetaData
                NATURAL JOIN mediaserver.MetaDataType
                WHERE podcast_id = %s order by podcast_episode_published_date desc
        """

        r = dictfetchall(cur, sql, (podcast_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Podcast Episodes for Podcast with ID: " + podcast_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (7 a,b,c,d,e,f)
#   Get one podcast ep and associated metadata
#####################################################
def get_podcastep(podcastep_id):
    """
    Get a podcast ep by their ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about a         #
        # podcast episodes and it's associated metadata                             #
        #############################################################################
        sql = """
            select media_id, podcast_episode_title,podcast_episode_uri, podcast_episode_published_date,podcast_episode_length,md_type_name, md_value
            from mediaserver.podcastepisode
            natural join mediaserver.mediaitemmetadata
            natural join mediaserver.metadata
            natural join mediaserver.metadatatype
            where media_id = %s
        """

        r = dictfetchall(cur, sql, (podcastep_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Podcast Episode with ID: " + podcastep_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (5 a,b)
#   Get one album
#####################################################
def get_album(album_id):
    """
    Get an album by their ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about an album  #
        # including all relevant metadata                                           #
        #############################################################################
        sql = """
            SELECT a1.album_title AS album_title, m2.md_type_name AS md_type_name
            ,m.md_value
            FROM mediaserver.album a1
            JOIN mediaserver.albummetadata a on a1.album_id = a.album_id
            JOIN mediaserver.metadata m on m.md_id = a.md_id
            JOIN mediaserver.metadatatype m2 on m2.md_type_id = m.md_type_id
            WHERE a1.album_id = %s;

        """

        r = dictfetchall(cur, sql, (album_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Albums with ID: " + album_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (5 d)
#   Get all songs for one album
#####################################################
def get_album_songs(album_id):
    """
    Get all songs for an album by the album ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # songs in an album, including their artists                                #
        #############################################################################
        sql = """
            SELECT s.song_id AS song_id, s.song_title AS song_title, array_to_string(array_agg(artist_name),',') AS artists
            FROM mediaserver.album a1
            JOIN mediaserver.album_songs as1 on a1.album_id = as1.album_id
            JOIN mediaserver.song s on as1.song_id = s.song_id
            JOIN mediaserver.song_artists sa on s.song_id = sa.song_id
            RIGHT JOIN mediaserver.artist a on a.artist_id = sa.performing_artist_id
            WHERE a1.album_id = %s
            GROUP BY s.song_id, s.song_title, as1.track_num
            ORDER BY as1.track_num;
        """

        r = dictfetchall(cur, sql, (album_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except Exception as e:
        # If there were any errors, return a NULL row printing an error to the debug
        print("the error msg [{}]".format(e))
        print("Unexpected error getting Albums songs with ID: " + album_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None

def get_result_simple(sql):
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    r = dictfetchall(cur, sql, ())
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return r


#####################################################
#   Query (5 c)
#   Get all genres for one album
#####################################################
def get_album_genres(album_id):
    """
    Get all genres for an album by the album ID in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # genres in an album (based on all the genres of the songs in that album)   #
        #############################################################################
        sql = """
            SELECT DISTINCT md_value
            FROM mediaserver.album a1
            JOIN mediaserver.album_songs "as" on a1.album_id = "as".album_id
            JOIN mediaserver.song s on s.song_id = "as".song_id
            JOIN mediaserver.audiomedia a on a.media_id = s.song_id
            JOIN mediaserver.mediaitem m on m.media_id = a.media_id
            JOIN mediaserver.mediaitemmetadata m2 on m.media_id = m2.media_id
            JOIN mediaserver.metadata m3 on m3.md_id = m2.md_id
            WHERE a1.album_id = %s;
        """

        r = dictfetchall(cur, sql, (album_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Albums genres with ID: " + album_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (10)
#   May require the addition of SQL to multiple
#   functions and the creation of a new function to
#   determine what type of genre is being provided
#   You may have to look at the hard coded values
#   in the sampledata to make your choices
#####################################################

#####################################################
#   Query (10)
#   Get all songs for one song_genre
#####################################################
def get_genre_songs(genre_id):
    """
    Get all songs for a particular song_genre ID in your media server
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # songs which belong to a particular genre_id                               #
        #############################################################################
        sql = """
            SELECT Distinct(song_id) AS Item_ID, song_title AS Item_name, 'Song' AS Item_type
            FROM mediaserver.Song JOIN mediaserver.Mediaitem ON (song_id = media_id)
            NATURAL JOIN mediaserver.MediaItemMetaData
            NATURAL JOIN mediaserver.Metadata
            WHERE md_value = %s
        """

        r = dictfetchall(cur, sql, (genre_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Songs with Genre ID: " + genre_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (10)
#   Get all podcasts for one podcast_genre
#####################################################
def get_genre_podcasts(genre_id):
    """
    Get all podcasts for a particular podcast_genre ID in your media server
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # podcasts which belong to a particular genre_id                            #
        #############################################################################
        sql = """
            SELECT DISTINCT(podcast_id) AS Item_ID, podcast_title AS Item_name, 'Podcast' AS Item_type
            FROM mediaserver.Podcast NATURAL JOIN mediaserver.podcastmetadata
            NATURAL JOIN mediaserver.Metadata
            WHERE md_value = %s
        """

        r = dictfetchall(cur, sql, (genre_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting Podcasts with Genre ID: " + genre_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (10)
#   Get all movies and tv shows for one film_genre
#####################################################
def get_genre_movies_and_shows(genre_id):
    """
    Get all movies and tv shows for a particular film_genre ID in your media server
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # movies and tv shows which belong to a particular genre_id                 #
        #############################################################################
        sql = """
            select t.tvshow_id as item_id,
                   tvshow_title as item_title,
                   'TVShow' as item_type

            from mediaserver.tvshow t
            join mediaserver.tvshowmetadata t2 on t.tvshow_id = t2.tvshow_id
            join mediaserver.metadata m on t2.md_id = m.md_id
            join mediaserver.metadatatype m2 on m.md_type_id = m2.md_type_id
            where md_value = %s
            union all
            select distinct(movie_id) as item_id, movie_title as item_title, 'Moive' as item_type
            from mediaserver.movie mo
            join mediaserver.mediaitem mi on mo.movie_id = mi.media_id
            join mediaserver.MediaItemMetaData mdimd on mo.movie_id = mdimd.media_id
            natural join mediaserver.MetaData
            where md_value = %s
        """

        r = dictfetchall(cur, sql, (genre_id, genre_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except Exception as e:
        # If there were any errors, return a NULL row printing an error to the debug
        print("the Error msg [{}]".format(e))
        print("Unexpected error getting Movies and tv shows with Genre ID: " + genre_id, sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (4 a,b)
#   Get one tvshow
#####################################################
def get_tvshow(tvshow_id):
    """
    Get one tvshow in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about a tv show #
        # including all relevant metadata       #
        #############################################################################
        sql = """
            select t.tvshow_id, tvshow_title,m.md_id, md_type_name, md_value
            from mediaserver.tvshow t
            join mediaserver.tvshowmetadata t2 on t.tvshow_id = t2.tvshow_id
            join mediaserver.metadata m on t2.md_id = m.md_id
            join mediaserver.metadatatype m2 on m.md_type_id = m2.md_type_id
            where t.tvshow_id = %s
        """

        r = dictfetchall(cur, sql, (tvshow_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except Exception as e:
        # If there were any errors, return a NULL row printing an error to the debug
        print("error is [{}]".format(e))
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (4 c)
#   Get all tv show episodes for one tv show
#####################################################
def get_all_tvshoweps_for_tvshow(tvshow_id):
    """
    Get all tvshow episodes for one tv show in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about all       #
        # tv episodes in a tv show                                                  #
        #############################################################################
        sql = """
            select distinct *
            from mediaserver.tvepisode
            join mediaserver.tvshow t on tvepisode.tvshow_id = t.tvshow_id
            where t.tvshow_id = %s
            order by media_id

        """

        r = dictfetchall(cur, sql, (tvshow_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Get one tvshow episode
#####################################################
def get_tvshowep(tvshowep_id):
    """
    Get one tvshow episode in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select * 
        from mediaserver.TVEpisode te left outer join 
            (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) temd
            on (te.media_id=temd.media_id)
        where te.media_id = %s"""

        r = dictfetchall(cur, sql, (tvshowep_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################

#   Get one movie
#####################################################
def get_movie(movie_id):
    """
    Get one movie in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """select *
        from mediaserver.movie m left outer join 
            (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) mmd
        on (m.movie_id=mmd.media_id)
        where m.movie_id=%s;"""

        r = dictfetchall(cur, sql, (movie_id,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All Movies:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Find all matching tvshows
#####################################################
def find_matchingtvshows(searchterm):
    """
    Get all the matching TV Shows in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
            select 
                t.*, tnew.count as count  
            from 
                mediaserver.tvshow t, 
                (select 
                    t1.tvshow_id, count(te1.media_id) as count 
                from 
                    mediaserver.tvshow t1 left outer join mediaserver.TVEpisode te1 on (t1.tvshow_id=te1.tvshow_id) 
                    group by t1.tvshow_id) tnew 
            where t.tvshow_id = tnew.tvshow_id and lower(tvshow_title) ~ lower(%s)
            order by t.tvshow_id;"""

        r = dictfetchall(cur, sql, (searchterm,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (9)
#   Find all matching Movies
#####################################################
def find_matchingmovies(searchterm):
    """
    Get all the matching Movies in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about movies    #
        # that match a given search term                                            #
        #############################################################################
        sql = """
            SELECT DISTINCT(movie_id), movie_title, release_year, count(md_value)
            FROM mediaserver.Movie JOIN mediaserver.MediaItem ON (movie_id = media_id)
            NATURAL JOIN mediaserver.mediaitemmetadata
            NATURAL JOIN mediaserver.metadata
            NATURAL JOIN mediaserver.metadatatype
            WHERE lower(movie_title) ~ lower(%s)
            group by movie_id, movie_title, release_year
        """

        r = dictfetchall(cur, sql, (searchterm,))
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error getting All TV Shows:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Add a new Movie
#####################################################
def add_movie_to_db(title, release_year, description, storage_location, genre):
    """
    Add a new Movie to your media server
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
        SELECT 
            mediaserver.addMovie(
                %s,%s,%s,%s,%s);
        """

        cur.execute(sql, (storage_location, description, title, release_year, genre))
        conn.commit()  # Commit the transaction
        r = cur.fetchone()
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error adding a movie:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query (8)
#   Add a new Song
#####################################################
def add_song_to_db(song_title, song_length, description, storage_location, song_genre, song_artistid):
    """
    Get all the matching Songs in your media server
    """
    #########
    # TODO  #
    #########
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
            SELECT 
                mediaserver.addSong(
                     %s,%s,%s,%s,%s,%s);
            """

        cur.execute(sql, (storage_location, description, song_title, song_length, song_genre, song_artistid))
        conn.commit()  # Commit the transaction
        r = cur.fetchone()
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error adding a song:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None

    #############################################################################
    # Fill in the Function  with a query and management for how to add a new    #
    # song to your media server. Make sure you manage all constraints           #
    #############################################################################


#####################################################
#   Get last Movie
#####################################################
def get_last_movie():
    """
    Get all the latest entered movie in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
        select max(movie_id) as movie_id from mediaserver.movie"""

        r = dictfetchone(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error adding a movie:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Get last Song
#####################################################
def get_last_song():
    """
    Get all the latest entered song in your media server
    """

    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        # Try executing the SQL and get from the database
        sql = """
        select max(song_id) as song_id from mediaserver.song"""

        r = dictfetchone(cur, sql)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error adding a song:", sys.exc_info()[0])
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#  FOR MARKING PURPOSES ONLY
#  DO NOT CHANGE

def to_json(fn_name, ret_val):
    """
    TO_JSON used for marking; Gives the function name and the
    return value in JSON.
    """
    return {'function': fn_name, 'res': json.dumps(ret_val)}


#####################################################
#   Query hard
#   Find all song which have the label
#####################################################
def find_label_songs(song_title, artist_name, genre, length):
    """
    Get all the matching songs in your media server
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about song      #
        # that match a given search term                                            #
        #############################################################################

        sql = None
        sql = """SELECT song_id, song_title,md.md_type_id,s.length, string_agg(distinct(artist_name), ',') as artist, string_agg(distinct(md_value), ',') as genre
                        FROM mediaserver.Song s JOIN mediaserver.Mediaitem mi ON (s.song_id = mi.media_id)
                        NATURAL JOIN mediaserver.song_artists sa
                        JOIN mediaserver.artist a on sa.performing_artist_id = a.artist_id
                        JOIN mediaserver.MediaItemMetaData mimd on s.song_id=mimd.media_id
                        JOIN mediaserver.Metadata md on mimd.md_id = md.md_id
                        JOIN mediaserver.Metadatatype mdt on mdt.md_type_id= md.md_type_id
                        where md.md_type_id = 1
                         """
        param = ()
        if song_title != "":
            condition_title = """ and LOWER(song_title) ~ LOWER(%s)"""
            sql = sql+condition_title
            param = param +(song_title,)

        if artist_name != "":
            condition_artist = """ and lower(artist_name) ~ lower(%s)"""
            sql = sql+condition_artist
            param = param + (artist_name,)

        if genre != "":
            condition_genre = """ and lower(md.md_value) ~ lower(%s)"""
            sql = sql+condition_genre
            param = param + (genre,)

        if length != "":
            try:
                if length[0:2] == ">=" or length[0:2] == "<=":
                    temp = int(length[2:])
                    if temp > 0:
                        if length[0:2] == ">=":
                            condition_length = """ and s.length >= cast(%s as integer)"""
                            length = length[2:]
                        elif length[0:2] == "<=":
                                condition_length = """ and s.length <= cast(%s as integer)"""
                                length = length[2:]
                        else:
                            cur.close()  # Close the cursor
                            conn.close()  # Close the connection to the db
                            return None
                        sql = sql + condition_length
                        param = param + (length,)
                    else:
                        cur.close()  # Close the cursor
                        conn.close()  # Close the connection to the db
                        return None

                elif length[0] == ">" or length[0] == "<" or length[0] == "=":
                    temp = int(length[1:])
                    if temp > 0:
                        if length[0] == ">":
                                condition_length = """ and s.length > cast(%s as integer)"""
                                length = length[1:]
                        elif length[0] == "<":
                            condition_length = """ and s.length < cast(%s as integer)"""
                            length = length[1:]
                        elif length[0] == "=":
                            condition_length = """ and s.length = cast(%s as integer)"""
                            length = length[1:]
                        else:
                            cur.close()  # Close the cursor
                            conn.close()  # Close the connection to the db
                            return None
                        sql = sql + condition_length
                        param = param + (length,)
                    else:
                        cur.close()  # Close the cursor
                        conn.close()  # Close the connection to the db
                        return None

                else:
                    cur.close()  # Close the cursor
                    conn.close()  # Close the connection to the db
                    return None

            except ValueError:
                cur.close()  # Close the cursor
                conn.close()  #
                return None

        sql = sql+""" group by song_id,song_title,md.md_type_id"""
        print(sql)
        r = dictfetchall(cur, sql,param)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("No eligible song")
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query hard
#   Find all movie which have the label
#####################################################
def find_label_movies(title, release_year, genre):
    """
    Get all the matching songs in your media server
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:

        sql = None
        sql = """
                SELECT movie_id, movie_title, release_year, count(mimd.md_id) as count, string_agg(distinct(md_value), ',') as genre
                FROM mediaserver.Movie JOIN mediaserver.MediaItem ON (movie_id = media_id)
                NATURAL JOIN mediaserver.mediaitemmetadata mimd
                NATURAL JOIN mediaserver.metadata md
                NATURAL JOIN mediaserver.metadatatype
                Where movie_id = media_id
                """

        param = ()
        if title != "":
            condition_title = """and LOWER(movie_title) ~ LOWER(%s)"""
            sql = sql+condition_title
            param = param +(title,)

        if release_year != "":
            try:
                if release_year[0:2] == ">=" or release_year[0:2] == "<=":
                    temp = int(release_year[2:])
                    if temp > 0:
                        if release_year[0:2] == ">=":
                            condition_year = """ and cast(release_year as integer) >= cast(%s as integer)"""
                            release_year = release_year[2:]
                        elif release_year[0:2] == "<=":
                            condition_year = """ and cast(release_year as integer) <= cast(%s as integer)"""
                            release_year = release_year[2:]
                        else:
                            cur.close()  # Close the cursor
                            conn.close()  # Close the connection to the db
                            return None
                        sql = sql + condition_year
                        param = param + (release_year,)
                    else:
                        cur.close()  # Close the cursor
                        conn.close()  # Close the connection to the db
                        return None

                elif release_year[0] == ">" or release_year[0] == "<" or release_year[0] == "=":
                    temp = int(release_year[1:])
                    if temp > 0:
                        if release_year[0] == ">":
                            condition_year = """ and cast(release_year as integer) > cast(%s as integer)"""
                            release_year = release_year[1:]
                        elif release_year[0] == "<":
                            condition_year = """ and cast(release_year as integer) < cast(%s as integer)"""
                            release_year = release_year[1:]
                        elif release_year[0] == "=":
                            condition_year = """ and cast(release_year as integer) = cast(%s as integer)"""
                            release_year = release_year[1:]
                        else:
                            cur.close()  # Close the cursor
                            conn.close()  # Close the connection to the db
                            return None
                        sql = sql + condition_year
                        param = param + (release_year,)
                    else:
                        cur.close()  # Close the cursor
                        conn.close()  # Close the connection to the db
                        return None
                else:
                    cur.close()  # Close the cursor
                    conn.close()  # Close the connection to the db
                    return None

            except ValueError:
                cur.close()  # Close the cursor
                conn.close()  # Close the connection to the db
                return None

        if genre != "":
            condition_genre = """and lower(md.md_value) ~ lower(%s)"""
            sql = sql+condition_genre
            param = param + (genre,)

        sql = sql+"""group by movie_id, movie_title, release_year"""
        r = dictfetchall(cur, sql,param)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("No eligible movie")
        raise

    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None


#####################################################
#   Query hard
#   Find all podcast which have the label
#####################################################
def find_label_podcasts(podcast_title, podcast_genre, last_update_time , count):
    """
    Get all the matching podcast in your media server
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about movies    #
        # that match a given search term                                            #
        #############################################################################

        sql = None
        sql = """select p.podcast_id as podcast_id, podcast_title , podcast_last_updated, string_agg(distinct(md_value), ',') as md_values, pnew.count as count
                from mediaserver.podcast p
                    natural join mediaserver.podcastmetadata
                    natural join mediaserver.metadata
                    natural join mediaserver.metadatatype
                    , (select p1.podcast_id, count(*) as count
                        from mediaserver.podcast p1
                        left outer join mediaserver.podcastepisode pe1 on (p1.podcast_id=pe1.podcast_id)
                        group by p1.podcast_id) pnew
                where p.podcast_id = pnew.podcast_id """

        param = ()
        if podcast_title != "":
            condition_title = """ and LOWER(podcast_title) ~ LOWER(%s)"""
            sql = sql+condition_title
            param = param +(podcast_title,)

        if podcast_genre != "":
            condition_genre = """ and lower(md_value) ~ lower(%s)"""
            sql = sql+condition_genre
            param = param + (podcast_genre,)


        if last_update_time != "":
            try:
                if last_update_time[0:2] == ">=" or last_update_time[0:2] == "<=":
                    temp = int(last_update_time[2:6])
                    if temp > 0:
                        if last_update_time[6:7] == "-":
                            temp_1 = int(last_update_time[7:9])
                            if 0 < temp_1 < 12:
                                if last_update_time[9:10] == "-":
                                    temp_2 = int(last_update_time[10:12])
                                    if 0 < temp_2 < 31:
                                        if last_update_time[0:2] == ">=":
                                            condition_last_update_time = """ and podcast_last_updated >= cast(%s as date) """
                                            last_update_time = last_update_time[2:]
                                        elif last_update_time[0:2] == "<=":
                                            condition_last_update_time = """ and podcast_last_updated <= cast(%s as date)"""
                                            last_update_time = last_update_time[2:]
                                        else:
                                            cur.close()  # Close the cursor
                                            conn.close()  # Close the connection to the db
                                            return None
                                        sql = sql + condition_last_update_time
                                        param = param + (last_update_time,)
                                    else:
                                        cur.close()  # Close the cursor
                                        conn.close()  # Close the connection to the db
                                        return None
                                else:
                                    cur.close()  # Close the cursor
                                    conn.close()  # Close the connection to the db
                                    return None
                            else:
                                cur.close()  # Close the cursor
                                conn.close()  # Close the connection to the db
                                return None
                        else:
                            cur.close()  # Close the cursor
                            conn.close()  # Close the connection to the db
                            return None
                    else:
                        cur.close()  # Close the cursor
                        conn.close()  # Close the connection to the db
                        return None

                elif last_update_time[0] == ">" or last_update_time[0] == "<" or last_update_time[0] == "=":
                    temp_3 = int(last_update_time[1:5])
                    if temp_3 > 0:
                        if last_update_time[5:6] == "-":
                            temp_1 = int(last_update_time[6:8])
                            if 0 < temp_1 < 12:
                                if last_update_time[8:9] == "-":
                                    temp_2 = int(last_update_time[9:11])
                                    if 0 < temp_2 < 31:
                                        if last_update_time[0] == ">":
                                            condition_last_update_time = """ and podcast_last_updated > cast(%s as date)"""
                                            last_update_time = last_update_time[1:]
                                        elif last_update_time[0] == "<":
                                            condition_last_update_time = """ and podcast_last_updatedt < cast(%s as date)"""
                                            last_update_time = last_update_time[1:]

                                        elif last_update_time[0] == "=":
                                            condition_last_update_time = """ and podcast_last_updated = cast(%s as date)"""
                                            last_update_time = last_update_time[1:]
                                        else:
                                            cur.close()  # Close the cursor
                                            conn.close()  # Close the connection to the db
                                            return None
                                        sql = sql + condition_last_update_time
                                        param = param + (last_update_time,)
                                    else:
                                        cur.close()  # Close the cursor
                                        conn.close()  # Close the connection to the db
                                        return None
                                else:
                                    cur.close()  # Close the cursor
                                    conn.close()  # Close the connection to the db
                                    return None
                            else:
                                cur.close()  # Close the cursor
                                conn.close()  # Close the connection to the db
                                return None
                        else:
                            cur.close()  # Close the cursor
                            conn.close()  # Close the connection to the db
                            return None
                    else:
                        cur.close()  # Close the cursor
                        conn.close()  # Close the connection to the db
                        return None

                else:
                    cur.close()  # Close the cursor
                    conn.close()  # Close the connection to the db
                    return None


            except ValueError:
                cur.close()  # Close the cursor
                conn.close()  #
                return None

        if count != "":
            try:
                if count[0:2] == ">=" or count[0:2] == "<=":
                    temp = int(count[2:])
                    if temp > 0:
                        if count[0:2] == ">=":
                            condition_count = """ and pnew.count >= cast(%s as integer)"""
                            count = count[2:]
                        elif count[0:2] == "<=":
                            condition_count = """ and pnew.count <= cast(%s as integer)"""
                            count = count[2:]
                        else:
                            cur.close()  # Close the cursor
                            conn.close()  # Close the connection to the db
                            return None
                        sql = sql + condition_count
                        param = param + (count,)
                    else:
                        cur.close()  # Close the cursor
                        conn.close()  # Close the connection to the db
                        return None

                elif count[0] == ">" or count[0] == "<" or count[0] == "=":
                    temp = int(count[1:])
                    if temp > 0:
                        if count[0] == ">":
                            condition_count = """ and pnew.count > cast(%s as integer)"""
                            count = count[1:]
                        elif count[0] == "<":
                            condition_count = """ and pnew.count < cast(%s as integer)"""
                            count = count[1:]

                        elif count[0] == "=":
                            condition_count = """ and pnew.count = cast(%s as integer)"""
                            count = count[1:]
                        else:
                            cur.close()  # Close the cursor
                            conn.close()  # Close the connection to the db
                            return None
                        sql = sql+condition_count
                        param = param + (count,)
                    else:
                        cur.close()  # Close the cursor
                        conn.close()  # Close the connection to the db
                        return None
                else:
                    cur.close()  # Close the cursor
                    conn.close()  # Close the connection to the db
                    return None

            except ValueError:
                cur.close()  # Close the cursor
                conn.close()  #
                return None

        sql = sql+""" group by p.podcast_id, podcast_title,podcast_last_updated,pnew.count"""
        print(sql)
        r = dictfetchall(cur, sql,param)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("No eligible song")
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None
#####################################################
#   Query hard
#   Find all tvshow which have the label
#####################################################
def find_label_tvshows(tvshow_id, tvshow_title, tvshow_episode_count, tvshow_genre):
    """
    Get all the matching songs in your media server
    """
    conn = database_connect()
    if (conn is None):
        return None
    cur = conn.cursor()
    try:
        #########
        # TODO  #
        #########

        #############################################################################
        # Fill in the SQL below with a query to get all information about tvshow    #
        # that match a given search term                                            #
        #############################################################################

        sql = None

        sql = """
                SELECT t.tvshow_id, tvshow.tvshow_title, tvs.count AS count, string_agg(distinct(md_value), ',') as md_values
                FROM mediaserver.tvepisode t
                NATURAL JOIN mediaserver.tvshow
                NATURAL JOIN mediaserver.tvshowmetadata
                NATURAL JOIN mediaserver.metadata
                natural join mediaserver.metadatatype,
                    (select s.tvshow_id, tvshow_title,count(*) as count
                    from mediaserver.tvepisode
                    join mediaserver.tvshow s on tvepisode.tvshow_id = s.tvshow_id
                    group by s.tvshow_id, tvshow_title
                    order by tvshow_id) tvs
                WHERE t.tvshow_id = tvs.tvshow_id """

        param = ()

        if tvshow_id != "":
            try:
                temp_tvshowid = int(tvshow_id)
                if temp_tvshowid > 0:
                    condition_id = """AND t.tvshow_id = %s"""
                    sql = sql + condition_id
                    param = param + (tvshow_id,)
                else:
                    cur.close()  # Close the cursor
                    conn.close()  #
                    return None
            except ValueError:
                cur.close()  # Close the cursor
                conn.close()  #
                return None

        if tvshow_title != "":
            condition_title = """and LOWER(tvshow.tvshow_title) ~ LOWER(%s)"""
            sql = sql + condition_title
            param = param + (tvshow_title,)

        if tvshow_episode_count != '':
            try:
                if tvshow_episode_count[0:2] == ">=" or tvshow_episode_count[0:2] == "<=":
                    temp = int(tvshow_episode_count[2:])
                    if temp > 0:
                        if tvshow_episode_count[0:2] == ">=":
                            condition_count = """ AND tvs.count >= %s"""
                            tvshow_episode_count = tvshow_episode_count[2:]
                        elif tvshow_episode_count[0:2] == "<=":
                            condition_count = """ AND tvs.count <= %s"""
                            tvshow_episode_count = tvshow_episode_count[2:]
                        else:
                            cur.close()  # Close the cursor
                            conn.close()  # Close the connection to the db
                            return None
                        sql = sql + condition_count
                        param = param + (tvshow_episode_count,)
                    else:
                        cur.close()  # Close the cursor
                        conn.close()  # Close the connection to the db
                        return None

                elif tvshow_episode_count[0] == ">" or tvshow_episode_count[0] == "<" or tvshow_episode_count[0] == "=":
                    temp = int(tvshow_episode_count[1:])
                    if temp > 0:
                        if tvshow_episode_count[0] == ">":
                            condition_count = """ AND tvs.count > %s"""
                            tvshow_episode_count = tvshow_episode_count[1:]
                        elif tvshow_episode_count[0] == "<":
                            condition_count = """ AND tvs.count < %s"""
                            tvshow_episode_count = tvshow_episode_count[1:]
                        elif tvshow_episode_count[0] == "=":
                            condition_count = """ AND tvs.count = %s"""
                            tvshow_episode_count = tvshow_episode_count[1:]
                        else:
                            cur.close()  # Close the cursor
                            conn.close()  # Close the connection to the db
                            return None
                        sql = sql + condition_count
                        param = param + (tvshow_episode_count,)
                    else:
                        cur.close()  # Close the cursor
                        conn.close()  # Close the connection to the db
                        return None

                else:
                    cur.close()  # Close the cursor
                    conn.close()  # Close the connection to the db
                    return None

            except ValueError:
                cur.close()  # Close the cursor
                conn.close()  #
                return None

        if tvshow_genre != "":
            condition_genre = """ and lower(md_value) ~ lower(%s)"""
            sql = sql+condition_genre
            param = param + (tvshow_genre,)

        sql = sql + """ group by t.tvshow_id, tvshow.tvshow_title,tvs.count"""
        print(sql)
        r = dictfetchall(cur, sql, param)
        print("return val is:")
        print(r)
        cur.close()  # Close the cursor
        conn.close()  # Close the connection to the db
        return r
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("No eligible TV Show")
        raise
    cur.close()  # Close the cursor
    conn.close()  # Close the connection to the db
    return None

