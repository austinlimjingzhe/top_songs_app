#import libraries
import googleapiclient.discovery
import pandas as pd
from datetime import date
from datetime import datetime
import os

def find_talents(description,title): 
    '''
    Parameters
    ----------
    description : string of a video's description
    title : string of a video's title

    Returns list of Hololive talents involved in the music video
    -------
    This function first looks at the title to extract the talent(s)' name(s). Only they are not present
    in the title, the function then looks through the description of the video to find names.
    
    Known issues:
        1. Many talents can be involved in roles other than vocals such as Ina'nis illustrating the cover of Umamusume's opening
        which may not be what we want in terms of filtering
        2. Names could be part of common words or phrases such as the shortened form of Ina'nis' name, Ina. For this reason,
        Kira (HoloStars Gen 1) has been left out of the list. As the author's level of understanding in Japanese language is limited,
        there may be more similar issues with other names. (Another name that is a known issue is Iroha as it may be a common japanese phrase as well)
        3. Units such as SubaChocoLuna may be in the title and hence return only 1 of the many singers as the other names are abbreviated.
    
    Any alternative algorithm suggestions are welcome.

    '''
    hololive=["Calliope","Kiara","Ina'nis","Gura","Amelia","IRyS","Kronii","Mumei","Sana","Baelz","Fauna",
              "Risu","Moona","Iofi","Ollie","Reine","Anya",
              "そら","ロボ子","すいせい","みこ","AZKi",
              "メル","フブキ","はあと","祭り","アキ",
              "ミオ","ころね","おかゆ",
              "あくあ","ちょこ","シオン","スバル","あやめ",
              "ぺこら","ノエル","マリン","るしあ","フレア",
              "ルーナ","ココ","かなた","トワ","わため",
              "アロエ","ラミイ","ねね","ぼたん","ポルカ",
              "ラプラス","ルイ","クロヱ","いろは","こより",
              "みやび","イヅル","アルランディス","律可","キラ",
              "アステル","天真","ロベル",
              "シエン","オウガ"]
    talents_intitle=[ele for ele in hololive if (ele in title)]
    talents_indesc=[ele for ele in hololive if (ele in description)]
    if len(talents_intitle)!=0:
        return talents_intitle
    return talents_indesc

#set initial variables
playlist_id="PLQmVFdwvZgfXlb2RDXWV1NaPXgYPu786G"
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = "YOUR OWN DEVELOPER KEY"
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey = DEVELOPER_KEY)

video_ids=[]
search_playlist = youtube.playlistItems().list(playlistId=playlist_id,part="contentDetails",maxResults=50).execute()

for song in search_playlist["items"]:
    video_ids.append(song["contentDetails"]["videoId"])

while "nextPageToken" in search_playlist:
    search_playlist = youtube.playlistItems().list(playlistId=playlist_id,part="contentDetails",maxResults=50,pageToken=search_playlist["nextPageToken"]).execute()
    for song in search_playlist["items"]:
        video_ids.append(song["contentDetails"]["videoId"])

os.chdir("YOUR OWN FILE PATHWAY")
os.getcwd()

'''
#for the initial run, remove the triple inverted commas to initialize an empty DataFrame with the following columns.

songs_data=pd.DataFrame(columns=["Date","Video ID","Title","Channel","Talents","Published","View Count","Is Cover","Thumbnail"])

#after the first scrape, you can comment out this portion again using the triple inverted commas.
'''

songs_data=pd.read_csv("all_songs.csv",encoding="UTF-8")
scrapped_date=date.today().strftime("%d/%m/%Y")
for song in video_ids:
    try:
        search_vid=youtube.videos().list(id=song,part="statistics,snippet").execute()
        vid_title=search_vid["items"][0]["snippet"]["title"]
        view_count=search_vid["items"][0]["statistics"]["viewCount"]
        published_date=search_vid["items"][0]["snippet"]["publishedAt"]
        channel=search_vid["items"][0]["snippet"]["channelTitle"]
        thumbnail=search_vid["items"][0]["snippet"]["thumbnails"]["default"]["url"]
        description=search_vid["items"][0]["snippet"]["description"]
        singers=find_talents(description,vid_title)
        singers=" ".join(singers)
        if "cover" in vid_title.lower() or "歌ってみた" in vid_title:
            is_cover="cover"
        else:
            is_cover="original"
        published_date=datetime.strptime(published_date,"%Y-%m-%dT%H:%M:%SZ").strftime("%d/%m/%Y")
        new_data=pd.DataFrame([[scrapped_date,song,vid_title,channel,singers,published_date,view_count,is_cover,thumbnail]],columns=["Date","Video ID","Title","Channel","Talents","Published","View Count","Is Cover","Thumbnail"])
        songs_data=pd.concat([songs_data,new_data],axis=0)
    except:
        print("Songs after this have been privated. There are {} of privated songs".format(len(video_ids)-video_ids.index(song)))
        break
    
songs_data.to_csv("all_songs.csv",index=False,encoding="UTF-8")
