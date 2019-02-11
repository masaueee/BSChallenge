# coding: utf-8
import apiclient.discovery
import apiclient.errors
from googleapiclient.discovery import build
from oauth2client.tools import argparser
import re

class videos(object):
    def __init__(self,id,title,viewcount,second):
        self.id = id
        self.title = title
        self.viewcount = viewcount
        self.second = second
    def __repr__(self):
        return "<videos '%s', '%s', '%s', '%d' >" % (self.id, self.title, self.viewcount, self.second)

#playlistIdを引数に、num[個]の動画を取得
def get_videoslist(PlaylistId, Num):
    DEVELOPER_KEY = "AIzaSyBKNUzJpzRVDWcbViHu8DrGqG8eU6jY3qE"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"


    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

    nextPageToken = ""
    count = 0
    num = Num   #動画の取得数
    contents_list = []

    while count < num:
        search_response = youtube.playlistItems().list(
            playlistId=PlaylistId,
            part="id,snippet",
            pageToken = nextPageToken,
            maxResults=1
            ).execute()

        item = search_response.get("items", [])
        nextPageToken = search_response.get("nextPageToken")

        if item[0]["snippet"]["resourceId"]["kind"]=="youtube#video":
            contents_list.append(item[0]["snippet"]["resourceId"]["videoId"])

            count+=1
    videos_list = []

    for content in contents_list:
        get_flag = True
        search_response = youtube.videos().list(
            id=content,
            part="id,snippet,statistics,contentDetails",
        ).execute()

        #videosリストに格納する情報を取得
        item = search_response.get("items", [])
        id = item[0]["id"]
        title = item[0]["snippet"]["title"]
        viewcount = item[0]["statistics"]["viewCount"]

        #動画が取得できない場合はリストに含めない
        if ("regionRestriction" in item[0]["contentDetails"]):
            if ("allowed" in item[0]["contentDetails"]["regionRestriction"]):
                if (not ("JP" in item[0]["contentDetails"]["regionRestriction"]["allowed"])):
                    get_flag = False
            elif ("blocked" in item[0]["contentDetails"]["regionRestriction"]):
                if ("JP" in item[0]["contentDetails"]["regionRestriction"]["blocked"]):
                    get_flag = False

        #durationはPT#M#S形式 PT15M51S:15分51秒
        duration = item[0]["contentDetails"]["duration"]
        min_txt = re.search('PT[0-9]*M', duration)
        sec_txt = re.search('[0-9]*S', duration)
        #minuteとsecondに変換
        if min_txt is None:
            minute = 0
        else:
            minute = int(re.sub('[^0-9]*', '', min_txt.group()))
        if sec_txt is None:
            second = 0
        else:
            second = int(re.sub('[^0-9]*', '', sec_txt.group()))

        if(minute<1):
            get_flag = False

        #videoごとの情報をvideosクラスに格納
        if get_flag:
            videos_list.append(videos(id,title,viewcount,minute*60+second))

    return videos_list
