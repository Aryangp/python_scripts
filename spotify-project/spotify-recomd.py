import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, url_for,session,redirect 
import os 
from dotenv import load_dotenv
load_dotenv()
#gloabal variable 
client_id=os.getenv("CLIENT_ID")
client_secret=os.getenv("CLIENT_SECRET")
app = Flask(__name__)

app.config['SESSION_COOKIE_NAME']=os.getenv("COOKIE_SECRET")
app.secret_key=os.getenv("SECRET_KEY")
TOKEN_INFO="DSDSDAD"
@app.route("/")
@app.route("/redirect")
@app.route('/saveDiscoverWeekly')

def create_oauth():
    return SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_url= url_for('redirect'),_external=True,
        
    )
    