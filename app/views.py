from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
import json 
from io import BytesIO
import xlsxwriter
from django.http import HttpResponse
import pandas as pd
from django.shortcuts import redirect
from django.urls import reverse
import os
from dotenv import load_dotenv

# loading .env file
load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

@api_view(['GET'])
def export_playlist(req):
    # playlist id
    link = req.data.get('playlist_link')
    link = link.split('https://open.spotify.com/playlist/')
    if link[0] == '':
        p_id = link[1].split('?')[0]
    else:
        pass

    # access token
    url = 'https://accounts.spotify.com/api/token'
    headers = {"Content-Type": 'application/x-www-form-urlencoded'}
    payload = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    res = requests.post(url, data=payload, headers=headers)
    json_string = res.content.decode('utf-8')
    dictionary = json.loads(json_string)['access_token']

    url = f'https://api.spotify.com/v1/playlists/{p_id}'
    headers = {
        'Authorization': f'Bearer {dictionary}'
    }
    res = requests.get(url, headers=headers)
    response = json.loads(res.text)
    PLname = response['name']
    items = response['tracks']['items']
    
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    worksheet.write('A1', 'Song name')
    worksheet.write('B1', 'URI')

    for i, item in enumerate(items):
        track = item['track']
        name = track['name']
        uri = track['uri']
        worksheet.write(f'A{i+2}', name)
        worksheet.write(f'B{i+2}', uri)

    worksheet.autofit()
    workbook.close()
    excel_response = HttpResponse(content_type='application/vnd.ms-excel')
    excel_response['Content-Disposition'] = f"attachment;filename={PLname.replace(' ','')}Playlist.xlsx"
    excel_response.write(output.getvalue())
    return excel_response

@api_view(['POST'])
def import_playlist(req):
    # profile id
    try:
        link = req.data.get('profile_link')
        link = link.split('https://open.spotify.com/user/')
        if link[0] == '':
            profile_id = link[1].split('?')[0]
        else:
            raise Exception
    except:
        return Response('You should enter a valid profile_link.', status=400)

    # access token
    url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "authorization_code",
        "code": req.query_params.get('code'),
        "redirect_uri": "http://localhost:8000/import-playlist/",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(url, data=data)
    access_token = response.json().get("access_token")

    # creating the playlist
    url = f'https://api.spotify.com/v1/users/{profile_id}/playlists'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    data = {
        "name": "Imported PL",
        "description": "",
        "public": False,
    }
    res = requests.post(url, headers=headers, json=data)
    response = json.loads(res.text)

    try:
        pl_id = response['id']
    except:
        return Response(status=403)

    # reading the excel file
    try:
        excel_address = req.data.get('excel_address')
        songs = pd.read_excel(excel_address).to_numpy()
        song_uris = [item[1] for item in songs]
    except:
        return Response('You should enter a valid excel_address.', status=400)
    
    # adding songs to playlist
    url = f'https://api.spotify.com/v1/playlists/{pl_id}/tracks'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    data = {
        "uris": song_uris,
    }
    res = requests.post(url, headers=headers, json=data)
    response = json.loads(res.text)

    return Response(status=200)

@api_view(['GET'])
def authorization(req):
    import_pl_url = req.build_absolute_uri(reverse('import_playlist'))
    url = f'https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={import_pl_url}&scope=playlist-modify-private'
    return redirect(url)