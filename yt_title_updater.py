import os
import google_auth_oauthlib.flow  #pip install google-auth-oauthlib
import googleapiclient.discovery  #pip install google-api-python-client
import googleapiclient.errors
from time import sleep

#initialize permissions
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"  #update the json from google oauth. https://developers.google.com/youtube/v3/quickstart/python follow this!

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(api_service_name,
                                              api_version,
                                              credentials=credentials)

    while (True):
        request = youtube.videos().list(
            part="snippet,statistics",
            id="DA7Dtu7eO3E"  #change the video id from the yt URL.
        )
        response = request.execute()

        data = response['items'][0]
        video_snippet = data['snippet']

        org_title = video_snippet['title']

        views = data['statistics']['viewCount']
        likes = data['statistics']['likeCount']
        dislikes = data['statistics']['dislikeCount']

        title = "This video has {} views ,{} likes and {} dislikes.".format(
            views, likes, dislikes)

        if (org_title != title):
            video_snippet['title'] = title

            request = youtube.videos().update(part="snippet",
                                              body={
                                                  "id": "DA7Dtu7eO3E",
                                                  "snippet": video_snippet
                                              })
            response = request.execute()

            print("updated!")

        sleep(30)  #updates every 30 seconds


if __name__ == "__main__":
    main()

