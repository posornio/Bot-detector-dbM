import os
import requests
import json
from datetime import datetime
from pydantic import BaseModel

from supabase import create_client, Client

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)

url: str = "https://vxjsjimucaapphmdnmsg.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ4anNqaW11Y2FhcHBobWRubXNnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDQ4OTc4MDgsImV4cCI6MjAyMDQ3MzgwOH0.jFkLMUdGReU-oKG32ukXXFQyfHxkWA-4Ae09Tvmz6qM"
supabase: Client = create_client(url, key)

class account(BaseModel):
    username: str
    predict: int
    call: int
    
    
app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')



@app.route("/all", methods=['GET'])
def get_persons():
    persons = supabase.table('Accounts').select('*').execute().model_dump_json()
    persons_data = json.loads(persons).get('data')
    return persons_data
@app.route("/account/", methods=['GET'])
def get_person():
    username = request.args.get('username')
    user= supabase.table('Accounts').select('*').eq('id', username).execute().model_dump_json()
    username_data = json.loads(user).get('data')[0]
    return username_data

@app.route("/account/", methods=['POST'])
def create_person():
    account = request.get_json()
    print(account)
    data, count = supabase.table('Accounts').insert({ "id": account.get('username'),"predict": 1, "call": 0, "last_predict": datetime.now().strftime("%Y-%m-%d")}).execute()
    return 'ok'

@app.route("/accountCall/", methods=['PATCH'])
def update_call():
    username = request.args.get('username')
    callSb = supabase.table('Accounts').select('call').eq('id', username).execute().data[0]['call']
    print(callSb)
    supabase.table('Accounts').update({"call": callSb +1}).eq('id', username).execute()
    return 'ok'
@app.route("/accountDate/", methods=['PATCH'])
def update_person():
    username = request.args.get('username')
    supabase.table('Accounts').update({"last_predict": datetime.now().strftime("%Y-%m-%d")}).eq('id', username).execute()
    return 'ok'


if __name__ == '__main__':
   app.run()
