from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
import json 
from io import BytesIO
import xlsxwriter
from django.http import HttpResponse

def get_token():
    url = 'https://accounts.spotify.com/api/token'
    headers = {"Content-Type": 'application/x-www-form-urlencoded'}
    payload = {
        "grant_type": "client_credentials",
        "client_id": "***",
        "client_secret": "***",
    }
    res = requests.post(url, data=payload, headers=headers)
    json_string = res.content.decode('utf-8')
    dictionary = json.loads(json_string)
    return dictionary['access_token']

def number_to_excel_column(n):
    result = ""
    while n > 0:
        n -= 1
        result = chr(n % 26 + 65) + result
        n //= 26
    return result

@api_view(['GET'])
def export_playlist(req):
    link = req.data.get('playlist_link')
    link = link.split('https://open.spotify.com/playlist/')
    if link[0] == '':
        p_id = link[1].split('?')[0]
    else:
        pass
    url = f'https://api.spotify.com/v1/playlists/{p_id}'
    headers = {'Authorization': f'Bearer {get_token()}'}
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

def import_playlist(req):
    pass