"""
Route management.

This provides all of the websites routes and handles what happens each
time a browser hits each of the paths. This serves as the interaction
between the browser and the database while rendering the HTML templates
to be displayed.

You will have to make
"""

# Importing the required packages
import json

from modules import *
from flask import *
import database

user_details = {}  # User details kept for us
session = {}  # Session information (logged in state)
page = {}  # Determines the page information

# Initialise the application
app = Flask(__name__)
app.secret_key = """U29tZWJvZHkgb25jZSB0b2xkIG1lIFRoZSB3b3JsZCBpcyBnb25uYSBy
b2xsIG1lIEkgYWluJ3QgdGhlIHNoYXJwZXN0IHRvb2wgaW4gdGhlIHNoZWQgU2hlIHdhcyBsb29r
aW5nIGtpbmRhIGR1bWIgV2l0aCBoZXIgZmluZ2VyIGFuZCBoZXIgdGh1bWIK"""


#####################################################
#   INDEX
#####################################################

@app.route('/')
def index():
    """
    Provides the main home screen if logged in.
        - Shows user playlists
        - Shows user Podcast subscriptions
        - Shows superUser status
    """
    # Check if the user is logged in, if not: back to login.
    if ('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    page['title'] = 'User Management'

    # Get a list of user playlists
    user_playlists = None
    user_playlists = database.user_playlists(user_details['username'])
    # Get a list of subscribed podcasts
    user_subscribed_podcasts = None
    user_subscribed_podcasts = database.user_podcast_subscriptions(user_details['username'])
    # Get a list of in-progress items
    user_in_progress_items = None
    user_in_progress_items = database.user_in_progress_items(user_details['username'])
    # Data integrity checks
    if user_playlists == None:
        user_playlists = []

    if user_subscribed_podcasts == None:
        user_subscribed_podcasts = []

    if user_in_progress_items == None:
        user_in_progress_items = []

    return render_template('index.html',
                           session=session,
                           page=page,
                           user=user_details,
                           playlists=user_playlists,
                           subpodcasts=user_subscribed_podcasts,
                           usercurrent=user_in_progress_items)


#####################################################
#####################################################
####    User Management
#####################################################
#####################################################

#####################################################
#   LOGIN
#####################################################

@app.route('/login', methods=['POST', 'GET'])
def login():
    """
    Provides /login
        - [GET] If they are just viewing the page then render login page.
        - [POST] If submitting login details, check login.
    """
    # Check if they are submitting details, or they are just logging in
    if (request.method == 'POST'):
        # submitting details
        # The form gives back EmployeeID and Password
        login_return_data = database.check_login(
            request.form['username'],
            request.form['password']
        )

        # If it's null, saying they have incorrect details
        if login_return_data is None:
            page['bar'] = False
            flash("Incorrect username/password, please try again")
            return redirect(url_for('login'))

        # If there was no error, log them in
        page['bar'] = True
        flash('You have been logged in successfully')
        session['logged_in'] = True

        # Store the user details for us to use throughout
        global user_details
        user_details = login_return_data[0]

        return redirect(url_for('index'))

    elif (request.method == 'GET'):
        return (render_template('login.html', session=session, page=page))


#####################################################
#   LOGOUT
#####################################################

@app.route('/logout')
def logout():
    """
    Logs out of the current session
        - Removes any stored user data.
    """
    session['logged_in'] = False
    page['bar'] = True
    flash('You have been logged out')
    return redirect(url_for('index'))


#####################################################
#####################################################
####    List All items
#####################################################
#####################################################


#####################################################
#   List Artists
#####################################################
@app.route('/list/artists')
def list_artists():
    """
    Lists all the artists in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Artists'

    # Get a list of all artists from the database
    allartists = None
    allartists = database.get_allartists()

    # Data integrity checks
    if allartists == None:
        allartists = []

    return render_template('listitems/listartists.html',
                           session=session,
                           page=page,
                           user=user_details,
                           allartists=allartists)


#####################################################
#   List Songs
#####################################################
@app.route('/list/songs')
def list_songs():
    """
    Lists all the songs in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Songs'

    # Get a list of all songs from the database
    allsongs = None
    allsongs = database.get_allsongs()

    # Data integrity checks
    if allsongs == None:
        allsongs = []

    return render_template('listitems/listsongs.html',
                           session=session,
                           page=page,
                           user=user_details,
                           allsongs=allsongs)


#####################################################
#   List Podcasts
#####################################################
@app.route('/list/podcasts')
def list_podcasts():
    """
    Lists all the podcasts in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List podcasts'

    # Get a list of all podcasts from the database
    allpodcasts = None
    allpodcasts = database.get_allpodcasts()

    # Data integrity checks
    if allpodcasts == None:
        allpodcasts = []

    return render_template('listitems/listpodcasts.html',
                           session=session,
                           page=page,
                           user=user_details,
                           allpodcasts=allpodcasts)


#####################################################
#   List Movies
#####################################################
@app.route('/list/movies')
def list_movies():
    """
    Lists all the movies in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Movies'

    # Get a list of all movies from the database
    allmovies = None
    allmovies = database.get_allmovies()

    # Data integrity checks
    if allmovies == None:
        allmovies = []

    return render_template('listitems/listmovies.html',
                           session=session,
                           page=page,
                           user=user_details,
                           allmovies=allmovies)


#####################################################
#   List Albums
#####################################################
@app.route('/list/albums')
def list_albums():
    """
    Lists all the albums in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Albums'

    # Get a list of all Albums from the database
    allalbums = None
    allalbums = database.get_allalbums()

    # Data integrity checks
    if allalbums == None:
        allalbums = []

    return render_template('listitems/listalbums.html',
                           session=session,
                           page=page,
                           user=user_details,
                           allalbums=allalbums)


#####################################################
#   List TVShows
#####################################################
@app.route('/list/tvshows')
def list_tvshows():
    """
    Lists all the tvshows in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List TV Shows'

    # Get a list of all tvshows from the database
    alltvshows = None
    alltvshows = database.get_alltvshows()

    # Data integrity checks
    if alltvshows == None:
        alltvshows = []

    return render_template('listitems/listtvshows.html',
                           session=session,
                           page=page,
                           user=user_details,
                           alltvshows=alltvshows)


#####################################################
#####################################################
####    List Individual items
#####################################################
#####################################################

#####################################################
#   Individual Artist
#####################################################
@app.route('/artist/<artist_id>')
def single_artist(artist_id):
    """
    Show a single artist by artist_id in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'Artist ID: ' + artist_id

    # Get a list of all artist by artist_id from the database
    artist = None
    artist = database.get_artist(artist_id)

    # Data integrity checks
    if artist == None:
        artist = []

    return render_template('singleitems/artist.html',
                           session=session,
                           page=page,
                           user=user_details,
                           artist=artist)


#####################################################
#   Individual Song
#####################################################
@app.route('/song/<song_id>')
def single_song(song_id):
    """
    Show a single song by song_id in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'Song'

    # Get a list of all song by song_id from the database
    song = None
    song = database.get_song(song_id)

    songmetadata = None
    songmetadata = database.get_song_metadata(song_id)

    # Data integrity checks
    if song == None:
        song = []

    if songmetadata == None:
        songmetadata = []

    return render_template('singleitems/song.html',
                           session=session,
                           page=page,
                           user=user_details,
                           song=song,
                           songmetadata=songmetadata)


#####################################################
#   Query (6)
#   Individual Podcast
#####################################################
@app.route('/podcast/<podcast_id>')
def single_podcast(podcast_id):
    """
    Show a single podcast by podcast_id in your media server
    Can do this without a login
    """
    #########
    # TODO  #
    #########

    #############################################################################
    # Fill in the Function below with to do all data handling for a podcast     #
    #############################################################################

    podcast = database.get_podcast(podcast_id)
    page['title'] = ''  # Add the title
    all_podcastep = database.get_all_podcasteps_for_podcast(podcast_id)

    # Set up some variables to manage the returns from the database fucntions

    # Once retrieved, do some data integrity checks on the data

    # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES
    return render_template('singleitems/podcast.html',
                           session=session,
                           page=page,
                           user=user_details,
                           podcast=podcast,
                           podcastep=all_podcastep
                           )


#####################################################
#   Query (7)
#   Individual Podcast Episode
#####################################################
@app.route('/podcastep/<media_id>')
def single_podcastep(media_id):
    """
    Show a single podcast epsiode by media_id in your media server
    Can do this without a login
    """
    #########
    # TODO  #
    #########

    #############################################################################
    # Fill in the Function below with to do all data handling for a podcast ep  #
    #############################################################################
    podcastep = database.get_podcastep(media_id)

    page['title'] = ''  # Add the title

    # Set up some variables to manage the returns from the database fucntions

    # Once retrieved, do some data integrity checks on the data

    # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES
    return render_template('singleitems/podcastep.html',
                           session=session,
                           page=page,
                           user=user_details,
                           podcastep=podcastep)


#####################################################
#   Individual Movie
#####################################################
@app.route('/movie/<movie_id>')
def single_movie(movie_id):
    """
    Show a single movie by movie_id in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Movies'

    # Get a list of all movies by movie_id from the database
    movie = None
    movie = database.get_movie(movie_id)

    # Data integrity checks
    if movie == None:
        movie = []

    return render_template('singleitems/movie.html',
                           session=session,
                           page=page,
                           user=user_details,
                           movie=movie)


#####################################################
#   Individual Album
#####################################################
@app.route('/album/<album_id>')
def single_album(album_id):
    """
    Show a single album by album_id in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List Albums'

    # Get the album plus associated metadata from the database
    album = None
    album = database.get_album(album_id)

    album_songs = None
    album_songs = database.get_album_songs(album_id)

    album_genres = None
    album_genres = database.get_album_genres(album_id)

    # Data integrity checks
    if album_songs == None:
        album_songs = []

    if album == None:
        album = []

    if album_genres == None:
        album_genres = []

    return render_template('singleitems/album.html',
                           session=session,
                           page=page,
                           user=user_details,
                           album=album,
                           album_songs=album_songs,
                           album_genres=album_genres)


#####################################################
#   Individual TVShow
#####################################################
@app.route('/tvshow/<tvshow_id>')
def single_tvshow(tvshow_id):
    """
    Show a single tvshows and its eps in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'TV Show'

    # Get a list of all tvshows by tvshow_id from the database
    tvshow = None
    tvshow = database.get_tvshow(tvshow_id)

    tvshoweps = None
    tvshoweps = database.get_all_tvshoweps_for_tvshow(tvshow_id)

    # Data integrity checks
    if tvshow == None:
        tvshow = []

    if tvshoweps == None:
        tvshoweps = []

    return render_template('singleitems/tvshow.html',
                           session=session,
                           page=page,
                           user=user_details,
                           tvshow=tvshow,
                           tvshoweps=tvshoweps)


#####################################################
#   Individual TVShow Episode
#####################################################
@app.route('/tvshowep/<tvshowep_id>')
def single_tvshowep(tvshowep_id):
    """
    Show a single tvshow episode in your media server
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'List TV Shows'

    # Get a list of all tvshow eps by media_id from the database
    tvshowep = None
    tvshowep = database.get_tvshowep(tvshowep_id)

    # Data integrity checks
    if tvshowep == None:
        tvshowep = []

    return render_template('singleitems/tvshowep.html',
                           session=session,
                           page=page,
                           user=user_details,
                           tvshowep=tvshowep)


#####################################################
#   Query (10)
#   Individual Genre
#####################################################
@app.route('/genre/<genre_id>')
def single_genre(genre_id):
    """
    Show a single genre in your media server
    First, figure out what type of genre this is
    Then list all items that have that genre:
    1. Song Genre
        a. list all songs
    2. Film Genre
        a. list all tv shows and films
    3. Postcast Genre
        a. list all podcasts
    Can do this without a login
    """
    # # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    songs = database.get_genre_songs(genre_id)
    postcasts = database.get_genre_podcasts(genre_id)
    films = database.get_genre_movies_and_shows(genre_id)

    #########
    # TODO  #
    #########

    #############################################################################
    # Fill in the Function below with to do all data handling for a genre       #
    #############################################################################

    page['title'] = ''  # Add the title

    if len(songs) != 0:
        page['type'] = 'songs'
    elif len(postcasts) != 0:
        page['type'] = 'postcasts'
    elif len(films) != 0:
        page['type'] = 'films'
    else:
        page['type'] = 'invalid'

    # Identify the type of genre - you may need to add a new function to database.py to do this

    # Set up some variables to manage the returns from the database functions
    #   There are some function frameworks provided for you to do this.

    # Once retrieved, do some data integrity checks on the data

    # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES
    return render_template('singleitems/genre.html',
                           session=session,
                           page=page,
                           user=user_details,
                           songs=songs,
                           postcasts=postcasts,
                           films=films
                           )


#####################################################
#####################################################
####    Search Items
#####################################################
#####################################################

#####################################################
#   Search TVShow
#####################################################
@app.route('/search/tvshow', methods=['POST', 'GET'])
def search_tvshows():
    """
    Search all the tvshows in your media server
    """

    # Check if the user is logged in, if not: back to login.
    if ('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    page['title'] = 'TV Show Search'

    # Get a list of matching tv shows from the database
    tvshows = None
    if (request.method == 'POST'):
        tvshows = database.find_matchingtvshows(request.form['searchterm'])

    # Data integrity checks
    if tvshows == None or tvshows == []:
        tvshows = []
        page['bar'] = False
        flash("No matching tv shows found, please try again")
    else:
        page['bar'] = True
        flash('Found ' + str(len(tvshows)) + ' results!')
        session['logged_in'] = True

    return render_template('searchitems/search_tvshows.html',
                           session=session,
                           page=page,
                           user=user_details,
                           tvshows=tvshows)


#####################################################
#   Query (9)
#   Search Movie
#####################################################
@app.route('/search/movie', methods=['POST', 'GET'])
def search_movies():
    """
    Search all the movies in your media server
    """
    # Check if the user is logged in, if not: back to login.
    # if('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    #########
    # TODO  #
    #########

    #############################################################################
    # Fill in the Function below with to do all data handling for searching for #
    # a movie                                                                   #
    #############################################################################

    # database.find_matchingmovies
    page['title'] = ''  # Add the title

    if request.method == 'POST':
        # Set up some variables to manage the post returns

        movie = request.form['searchterm']
        movieInfo = database.find_matchingmovies(movie)
        # Once retrieved, do some data integrity checks on the data
        session['accessType'] = 'POST'
        # Once verified, send the appropriate data to

        # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES or Go elsewhere
        return render_template('searchitems/search_movies.html',
                               session=session,
                               page=page,
                               user=user_details,
                               movie=movieInfo
                               )
    else:
        session['accessType'] = 'GET'
        # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES
        return render_template('searchitems/search_movies.html',
                               session=session,
                               page=page,
                               user=user_details
                               )


#####################################################
#   Turn to adv search choice page
#####################################################
@app.route('/search/advance', methods=['POST', 'GET'])
def advance_search():
    """
        Advance Search
    """

    # Check if the user is logged in, if not: back to login.
    if ('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    page['title'] = 'Advance Search Choices'

    if request.method == 'GET':
        session['accessType'] = 'GET'
        # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES
        return render_template('searchitems/search_advance.html',
                               session=session,
                               page=page,
                               user=user_details)


#####################################################
#   Turn to adv search song page
#####################################################
@app.route('/search/adv/song', methods=['POST', 'GET'])
def advance_search_song():
    """
        Advance Search Song
    """

    # Check if the user is logged in, if not: back to login.
    if ('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    page['title'] = 'Advance Search Song'
    songs = None
    if request.method == 'GET':
        session['accessType'] = 'GET'
        # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES
        return render_template('searchitems/search_adv_song.html',
                               session=session,
                               page=page,
                               user=user_details)
    else:
        newdict = {}
        session['accessType'] = 'POST'

        #     tvshows = database.find_matchingtvshows(request.form['searchterm'])
        #
        # # Data integrity checks
        # if tvshows == None or tvshows == []:
        #     tvshows = []
        #     page['bar'] = False
        #     flash("No matching tv shows found, please try again")
        # else:
        #     page['bar'] = True
        #     flash('Found ' + str(len(tvshows)) + ' results!')
        #     session['logged_in'] = True

        songs = database.find_label_songs(request.form['song_title'],
                                          request.form['song_artistid'],
                                          request.form['song_genre'],
                                          request.form['song_length'])

        if songs == None or songs == []:
            songs = []
            page['bar'] = False
            flash("No matching songs found, please try again")
        else:
            page['bar'] = True
            flash('Found ' + str(len(songs)) + ' results!')
            session['logged_in'] = True

        return render_template('searchitems/search_adv_song.html',
                               session=session,
                               page=page,
                               user=user_details,
                               songs=songs)


#####################################################
#   Turn to adv search Tv Shows page
#####################################################
@app.route('/search/adv/tvshows', methods=['POST', 'GET'])
def advance_search_tvshows():
    """
        Advance Search Tv Shows
    """

    # Check if the user is logged in, if not: back to login.
    if ('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    page['title'] = 'Advance Search Tv Shows'

    if request.method == 'GET':
        session['accessType'] = 'GET'
        # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES
        return render_template('searchitems/search_adv_tvshows.html',
                               session=session,
                               page=page,
                               user=user_details)
    else:
        session['accessType'] = 'POST'

        tvshows = database.find_label_tvshows(request.form['tvshow_id'],
                                              request.form['tvshow_title'],
                                              request.form['tvshow_episode_count'],
                                              request.form['tvshow_genre'])
        if tvshows == None or tvshows == []:
            tvshows = []
            page['bar'] = False
            flash("No matching TV Show found, please try again")
        else:
            page['bar'] = True
            flash('Found ' + str(len(tvshows)) + ' results!')
            session['logged_in'] = True

        return render_template('searchitems/search_adv_tvshows.html',
                               session=session,
                               page=page,
                               user=user_details,
                               tvshows=tvshows)


#####################################################
#   Turn to adv search Podcast page
#####################################################
@app.route('/search/adv/podcast', methods=['POST', 'GET'])
def advance_search_podcast():
    """
        Advance Search Podcast
    """

    # Check if the user is logged in, if not: back to login.
    if ('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    page['title'] = 'Advance Search Podcast'

    if request.method == 'GET':
        session['accessType'] = 'GET'
        # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES
        return render_template('searchitems/search_adv_podcast.html',
                               session=session,
                               page=page,
                               user=user_details)
    else:
        session['accessType'] = 'POST'

        podcasts = database.find_label_podcasts(request.form['podcast_title'],
                                                request.form['podcast_genre'],
                                                request.form['last_update_time'],
                                                request.form['count'])

        if podcasts == None or podcasts == []:
            podcasts = []
            page['bar'] = False
            flash("No matching podcasts found, please try again")
        else:
            page['bar'] = True
            flash('Found ' + str(len(podcasts)) + ' results!')
            session['logged_in'] = True

        return render_template('searchitems/search_adv_podcast.html',
                               session=session,
                               page=page,
                               user=user_details,
                               podcasts=podcasts)


#####################################################
#   Turn to adv search Movie page
#####################################################
@app.route('/search/adv/movie', methods=['POST', 'GET'])
def advance_search_movie():
    """
        Advance Search Movie
    """

    # Check if the user is logged in, if not: back to login.
    # if ('logged_in' not in session or not session['logged_in']):
    #     return redirect(url_for('login'))

    page['title'] = 'Advance Search Movie'
    movies = None

    if request.method == 'GET':
        session['accessType'] = 'GET'
        # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES
        return render_template('searchitems/search_adv_movie.html',
                               session=session,
                               page=page,
                               user=user_details)
    else:
        session['accessType'] = 'POST'

        movies = database.find_label_movies(request.form['title'],
                                            request.form['release_yr'],
                                            request.form['genre'])

        if movies == None or movies == []:
            movies = []
            page['bar'] = False
            flash("No matching Movies found, please try again")
        else:
            page['bar'] = True
            flash('Found ' + str(len(movies)) + ' results!')
            session['logged_in'] = True

        return render_template('searchitems/search_adv_movie.html',
                               session=session,
                               page=page,
                               user=user_details,
                               movies=movies)


#####################################################
#   Add Movie
#####################################################
@app.route('/add/movie', methods=['POST', 'GET'])
def add_movie():
    """
    Add a new movie
    """
    # # Check if the user is logged in, if not: back to login.
    if ('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    page['title'] = 'Movie Creation'

    movies = None
    print("request form is:")
    newdict = {}
    print(request.form)

    # Check your incoming parameters
    if (request.method == 'POST'):

        # verify that the values are available:
        if ('movie_title' not in request.form):
            newdict['movie_title'] = 'Empty Film Value'
        else:
            newdict['movie_title'] = request.form['movie_title']
            print("We have a value: ", newdict['movie_title'])

        if ('release_year' not in request.form):
            newdict['release_year'] = '0'
        else:
            newdict['release_year'] = request.form['release_year']
            print("We have a value: ", newdict['release_year'])

        if ('description' not in request.form):
            newdict['description'] = 'Empty description field'
        else:
            newdict['description'] = request.form['description']
            print("We have a value: ", newdict['description'])

        if ('storage_location' not in request.form):
            newdict['storage_location'] = 'Empty storage location'
        else:
            newdict['storage_location'] = request.form['storage_location']
            print("We have a value: ", newdict['storage_location'])

        if ('film_genre' not in request.form):
            newdict['film_genre'] = 'drama'
        else:
            newdict['film_genre'] = request.form['film_genre']
            print("We have a value: ", newdict['film_genre'])

        if ('artwork' not in request.form):
            newdict[
                'artwork'] = 'https://user-images.githubusercontent.com/24848110/33519396-7e56363c-d79d-11e7-969b-09782f5ccbab.png'
        else:
            newdict['artwork'] = request.form['artwork']
            print("We have a value: ", newdict['artwork'])

        print('newdict is:')
        print(newdict)

        # forward to the database to manage insert
        movies = database.add_movie_to_db(newdict['movie_title'], newdict['release_year'], newdict['description'],
                                          newdict['storage_location'], newdict['film_genre'])

        max_movie_id = database.get_last_movie()[0]['movie_id']
        print(movies)
        if movies is not None:
            max_movie_id = movies[0]

        # ideally this would redirect to your newly added movie
        return single_movie(max_movie_id)
    else:
        return render_template('createitems/createmovie.html',
                               session=session,
                               page=page,
                               user=user_details)


#####################################################
#   Query (8)
#   Add song
#####################################################
@app.route('/add/song', methods=['POST', 'GET'])
def add_song():
    """
    Add a new Song
    """
    # # Check if the user is logged in, if not: back to login.
    if ('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    #########
    # TODO  #
    #########

    #############################################################################
    # Fill in the Function below with to do all data handling for adding a song #
    #############################################################################

    page['title'] = 'Song Creation'  # Add the title
    songs = None
    print("request form is:")
    newdict = {}
    print(request.form)

    if request.method == 'POST':
        # Set up some variables to manage the post returns
        if ('song_title' not in request.form):
            newdict['song_title'] = 'Empty Title'
        else:
            newdict['song_title'] = request.form['song_title']
            print("We have a value: ", newdict['song_title'])

        if ('song_length' not in request.form):
            newdict['song_length'] = '0'
        else:
            newdict['song_length'] = request.form['song_length']
            print("We have a value: ", newdict['song_length'])

        if ('description' not in request.form):
            newdict['description'] = 'Empty description field'
        else:
            newdict['description'] = request.form['description']
            print("We have a value: ", newdict['description'])

        if ('storage_location' not in request.form):
            newdict['storage_location'] = 'Empty storage location'
        else:
            newdict['storage_location'] = request.form['storage_location']
            print("We have a value: ", newdict['storage_location'])

        if ('song_genre' not in request.form):
            newdict['song_genre'] = 'pop'
        else:
            newdict['song_genre'] = request.form['song_genre']
            print("We have a value: ", newdict['song_genre'])

        if ('song_artistid' not in request.form):
            newdict['song_artistid'] = '33'
        else:
            newdict['song_artistid'] = request.form['song_artistid']
            print("We have a value: ", newdict['song_artistid'])

        if ('artwork' not in request.form):
            newdict[
                'artwork'] = 'https://user-images.githubusercontent.com/24848110/33519396-7e56363c-d79d-11e7-969b-09782f5ccbab.png'
        else:
            newdict['artwork'] = request.form['artwork']
            print("We have a value: ", newdict['artwork'])

        print('newdict is:')
        print(newdict)

        # forward to the database to manage insert
        songs = database.add_song_to_db(newdict['song_title'], newdict['song_length'], newdict['description'],
                                        newdict['storage_location'], newdict['song_genre'], newdict['song_artistid'])

        max_song_id = database.get_last_song()[0]['song_id']
        print(songs)
        if songs is not None:
            max_song_id = songs[0]
        # Set up some variables to manage the post returns

        # Once retrieved, do some data integrity checks on the data

        # Once verified, send the appropriate data to the database for insertion

        # NOTE :: YOU WILL NEED TO MODIFY THIS TO PASS THE APPROPRIATE VARIABLES
        return single_song(max_song_id)
        # return render_template('singleitems/song.html',
        #                       session=session,
        #                      page=page,
        #                      user=user_details)
    else:
        return render_template('createitems/createsong.html',
                               session=session,
                               page=page,
                               user=user_details)


@app.route('/getMovieName', methods=['GET', 'POST'])  # 路由
def getMovieName_advanced():
    sql = """
        select distinct m.movie_title from
        mediaserver.movie m left outer join
        mediaserver.mediaitemmetadata mimd on (m.movie_id = mimd.media_id)
        order by m.movie_title
    """
    test_result = database.get_result_simple(sql)
    arr = [str(each['movie_title']) for each in test_result]
    print(arr)
    testInfo = {'name': arr}
    print(test_result)
    """
    select distinct(md_value)
        from mediaserver.movie m left outer join 
            (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) mmd
        on (m.movie_id=mmd.media_id)
        where md_type_name = 'film genre'
    """

    return json.dumps(testInfo)


@app.route('/getMovieGenre', methods=['GET', 'POST'])  # 路由
def advanced_getMovieName():
    sql = """
        select distinct(md_value)
        from mediaserver.movie m left outer join 
            (mediaserver.mediaitemmetadata natural join mediaserver.metadata natural join mediaserver.MetaDataType) mmd
        on (m.movie_id=mmd.media_id)
        where md_type_name = 'film genre'
    """
    test_result = database.get_result_simple(sql)
    arr = [str(each['md_value']) for each in test_result]
    print(arr)
    testInfo = {'name': arr}
    print(test_result)

    return json.dumps(testInfo)


@app.route('/getTvShowName', methods=['GET', 'POST'])  # 路由
def getTVShowName_advanced():
    sql = """
        select distinct m.tvshow_title from
        mediaserver.tvshow m left outer join
        mediaserver.mediaitemmetadata mimd on (m.tvshow_id = mimd.media_id)
        order by m.tvshow_title
    """
    test_result = database.get_result_simple(sql)
    arr = [str(each['tvshow_title']) for each in test_result]
    print(arr)
    testInfo = {'name': arr}
    print(test_result)

    return json.dumps(testInfo)


@app.route('/getTvShowGenre', methods=['GET', 'POST'])  # 路由
def advanced_getTVShowGenre():
    sql = """
            select distinct(md_value)
            from mediaserver.tvshow t
            join mediaserver.tvshowmetadata t2 on t.tvshow_id = t2.tvshow_id
            join mediaserver.metadata m on t2.md_id = m.md_id
            join mediaserver.metadatatype m2 on m.md_type_id = m2.md_type_id
            where md_type_name = 'film genre';
    """
    test_result = database.get_result_simple(sql)
    arr = [str(each['md_value']) for each in test_result]
    print(arr)
    testInfo = {'name': arr}
    print(test_result)

    return json.dumps(testInfo)


@app.route('/getSongName', methods=['GET', 'POST'])  # 路由
def getSongName_advanced():
    sql = """
        select distinct m.song_title from
        mediaserver.song m left outer join
        mediaserver.mediaitemmetadata mimd on (m.song_id = mimd.media_id)
        order by m.song_title
    """
    test_result = database.get_result_simple(sql)
    arr = [str(each['song_title']) for each in test_result]
    print(arr)
    testInfo = {'name': arr}
    print(test_result)

    return json.dumps(testInfo)


@app.route('/getSongGenre', methods=['GET', 'POST'])  # 路由
def advanced_getSongGenre():
    sql = """
            SELECT Distinct(md_value)
            FROM mediaserver.Song JOIN mediaserver.Mediaitem ON (song_id = media_id)
            NATURAL JOIN mediaserver.MediaItemMetaData
            NATURAL JOIN mediaserver.Metadata
    """
    test_result = database.get_result_simple(sql)
    arr = [str(each['md_value']) for each in test_result]
    print(arr)
    testInfo = {'name': arr}
    print(test_result)

    """
                select distinct(artist_name)

            from mediaserver.song s
            join mediaserver.MediaItemMetaData a2 on s.song_id = a2.media_id
            join mediaserver.metadata m on a2.md_id = m.md_id
            join mediaserver.metadatatype m2 on m.md_type_id = m2.md_type_id
            join mediaserver.song_artists sa on s.song_id = sa.song_id
            join mediaserver.artist a on sa.performing_artist_id = a.artist_id
            order by artist_name
    """
    return json.dumps(testInfo)


@app.route('/getSongArtist', methods=['GET', 'POST'])  # 路由
def advanced_getSongArtist():
    sql = """
                select distinct(artist_name)

            from mediaserver.song s
            join mediaserver.MediaItemMetaData a2 on s.song_id = a2.media_id
            join mediaserver.metadata m on a2.md_id = m.md_id
            join mediaserver.metadatatype m2 on m.md_type_id = m2.md_type_id
            join mediaserver.song_artists sa on s.song_id = sa.song_id
            join mediaserver.artist a on sa.performing_artist_id = a.artist_id
            order by artist_name
    """
    test_result = database.get_result_simple(sql)
    arr = [str(each['artist_name']) for each in test_result]
    print(arr)
    testInfo = {'name': arr}
    print(test_result)

    return json.dumps(testInfo)




@app.route('/getPodcastName', methods=['GET', 'POST'])  # 路由
def getPodcastName_advanced():
    sql = """
            select distinct(podcast_title)
            from mediaserver.podcast
            natural join mediaserver.podcastmetadata
            natural join mediaserver.metadata
            natural join mediaserver.metadatatype
            order by podcast_title
    """
    test_result = database.get_result_simple(sql)
    arr = [str(each['podcast_title']) for each in test_result]
    print(arr)
    testInfo = {'name': arr}
    print(test_result)

    return json.dumps(testInfo)


@app.route('/getPodcastGenre', methods=['GET', 'POST'])  # 路由
def advanced_getPodcastGenre():
    sql = """
            select distinct md_value
            from mediaserver.podcast
            natural join mediaserver.podcastmetadata
            natural join mediaserver.metadata
            natural join mediaserver.metadatatype
            where md_type_name = 'podcast genre'
    """
    test_result = database.get_result_simple(sql)
    arr = [str(each['md_value']) for each in test_result]
    print(arr)
    testInfo = {'name': arr}
    print(test_result)

    return json.dumps(testInfo)