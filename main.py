import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from oauth2client import client, tools
from oauth2client.file import Storage

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]


def main():
    CLIENT_SECRETS_FILE = "credentials/credentials.json"
    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"

    # Get credentials and create an API client
    credential_path = os.path.join('./', 'credentials/credential_sample.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRETS_FILE, SCOPES)
        credentials = tools.run_flow(flow, store)
    youtube = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

    # Fetch the user's playlists
    request = youtube.playlists().list(
        part="snippet, contentDetails",
        maxResults=25,
        mine=True
    )
    response = request.execute()

    # Print every playlists
    for index, playlist in enumerate(response["items"]):
        title = playlist["snippet"]["title"]
        count = playlist["contentDetails"]["itemCount"]
        print(
            f"{index + 1}. {title} ({count} videos)")

    # Ask which playlist to download
    index = int(
        input("\nWhich playlist would you like to download?\n"))
    playlist = response["items"][index - 1]

    # Ask whether or not it should download every video
    question = "Do you want to download every of them? (y/n)\n"
    dl_all = input(question)
    while dl_all != "y" and dl_all != "n":
        dl_all = input(question)

    # Fetch the playlist's videos
    req = youtube.playlistItems().list(
        part="snippet, contentDetails",
        playlistId=playlist['id'],
        maxResults=50
    )
    res = req.execute()

    folder = playlist["snippet"]["title"]
    if dl_all == "y":
        for video in res['items']:
            url = f"https://www.youtube.com/watch?v={video['contentDetails']['videoId']}"
            os.system(f"py dl.py {folder} {url}")

    else:
        for video in res['items']:
            question = f"{video['snippet']['title']} \nDownload? (y/n)"
            dl_vid = input(question)
            while dl_vid != "y" and dl_vid != "n":
                dl_vid = input(question)

            if dl_vid == "y":
                url = f"https://www.youtube.com/watch?v={video['contentDetails']['videoId']}"
                os.system(f"py dl.py {folder} {url}")


if __name__ == "__main__":
    main()
