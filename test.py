import requests
from datetime import datetime
import os
from supabase import create_client, Client

AZURE_SQL_CONNECTIONSTRING='Driver={ODBC Driver 18 for SQL Server};Server=tcp:server-twitter.database.windows.net,1433;Database=twitter-account;Uid=cdespaux;Pwd=database1!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;Authentification = ActiveDirectoryPassword'


import os
import pyodbc, struct
from azure import identity

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

url: str = "https://vxjsjimucaapphmdnmsg.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ4anNqaW11Y2FhcHBobWRubXNnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDQ4OTc4MDgsImV4cCI6MjAyMDQ3MzgwOH0.jFkLMUdGReU-oKG32ukXXFQyfHxkWA-4Ae09Tvmz6qM"
supabase: Client = create_client(url, key)

class account(BaseModel):
    username: str
    predict: int
    call: int
    
connection_string = AZURE_SQL_CONNECTIONSTRING

app = FastAPI()

@app.get("/all")
def get_persons():
    return supabase.table('Accounts').select('*').execute()

@app.get("/account/{username}")
def get_person(username: str):
    return supabase.table('Accounts').select('*').eq('id', username).execute()
@app.post("/account/")
def create_person(account: account):
    data, count = supabase.table('Accounts').insert({ "id": account.username,"predict": 1, "call": 0, "last_predict": datetime.now().strftime("%Y-%m-%d")}).execute()


@app.patch("/accountCall/{username}")
async def update_person(username: str):
   callSb = supabase.table('Accounts').select('call').eq('id', username).execute().data[0]['call']
   print(callSb)
   return supabase.table('Accounts').update({"call": callSb +1}).eq('id', username).execute()

@app.patch("/accountDate/{username}")
def update_person(username: str):
    return supabase.table('Accounts').update({"last_predict": datetime.now().strftime("%Y-%m-%d")}).eq('id', username).execute()


def get_conn():
  return Client


