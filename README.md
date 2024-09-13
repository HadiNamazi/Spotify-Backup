# Spotify Playlist Backup API

This project is a Django REST API for exporting and importing Spotify playlists. The API provides two main endpoints to backup playlists into an Excel file and import them back.

## Features

- **Export Playlist**: Fetches a Spotify playlist and exports it to an Excel file.
- **Import Playlist**: Imports a playlist from an Excel file back to Spotify.

## Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/HadiNamazi/spotify-backup.git
    ```

2. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up your environment variables** for the Spotify API credentials:
    ```
    SPOTIFY_CLIENT_ID
    SPOTIFY_CLIENT_SECRET
    ```

4. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

## Endpoints

### 1. Export Playlist

- **URL**: `/export-playlist/`
- **Method**: `GET`
- **Description**: Export a Spotify playlist to an Excel file.
- **Parameters**:
    - `playlist_link` (string): Spotify playlist link.
- **Example Request**:
    ```bash
    GET /export-playlist/?playlist_link=https://open.spotify.com/playlist/xyz123
    ```

### 2. Import Playlist

- **URL**: `/import-playlist/`
- **Method**: `POST`
- **Description**: Import a playlist from an Excel file back into Spotify.
- **Body Parameters**:
    - `playlist_link` (string): The link to the Spotify playlist to import the data to.
    - `excel_address` (string): The file path of the exported Excel file.
- **Example Request**:
    ```bash
    POST /import-playlist/
    Content-Type: application/json
    {
      "playlist_link": "https://open.spotify.com/playlist/xyz123",
      "excel_address": "/path/to/exported_playlist.xlsx"
    }

    ```
