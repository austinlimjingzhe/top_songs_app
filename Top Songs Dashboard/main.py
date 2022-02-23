from flask import Flask, render_template, request
from datetime import datetime,timedelta
import pandas as pd

app=Flask(__name__)

'''
general comments on the project:
    1. This project may not be continued for the long term so the data collected may be small.
       If data is to be collected for the long term, 
       consider using a SQL database
    2. This project was conceived with only this function in mind.
       Hence, as only 2 html pages need to be written, 
       there was no need for using template inheritance.
       If more functions are to be added to the application, 
       consider using template inheritance to reduce the amount of html coding for each page.
'''

@app.route("/",methods=["GET","POST"])
def home():
    return render_template("homepage.html")

@app.route("/top_songs",methods=["GET","POST"])
def songlist():
    talents=[]
    holostars=["みやび","イヅル","アルランディス","律可",
              "アステル","天真","ロベル",
              "シエン","オウガ"]
    holojp=["そら","ロボ子","すいせい","みこ","AZKi",
              "メル","フブキ","はあと","まつり","アキ",
              "ミオ","ころね","おかゆ",
              "あくあ","ちょこ","シオン","スバル","あやめ",
              "ぺこら","ノエル","マリン","るしあ","フレア",
              "ルナ","ココ","かなた","トワ","わため",
              "アロエ","ラミイ","ねね","ぼたん","ポルカ",
              "ラプラス","ルイ","クロヱ","いろは","こより"]
    holoid=["Risu","Moona","Iofi","Ollie","Reine","Anya"]
    holoen=["Calliope","Kiara","Ina'nis","Gura","Amelia","IRyS","Kronii","Mumei","Sana","Baelz","Fauna"]

    if request.method == "POST":
        branch=request.form.getlist('Branch')
        songtype=request.form.getlist("Song Type")
        endweek=datetime.strptime(request.form["Weekof"],"%Y-%m-%d").strftime("%d/%m/%Y")
        weekof=datetime.strptime(request.form["Weekof"],"%Y-%m-%d")+timedelta(days=1)
        weekof=weekof.strftime("%d/%m/%Y")
        topn=int(request.form["topn"])        
        sortmethod=request.form["sortmethod"]
        if "HoloStars" in branch:
            talents+=holostars
        if "HololiveJP" in branch:
            talents+=holojp
        if "HololiveID" in branch:
            talents+=holoid
        if "HololiveEN" in branch:
            talents+=holoen
        if len(branch)==0:
            talents+=(holostars+holojp+holoid+holoen)
        songs=pd.read_csv("./static/data/all_songs.csv")
        weekly_difference=songs.groupby("Video ID")["View Count"].diff(1).rename("Weekly Difference").fillna(0).astype(int)
        updated_songs=pd.concat([songs,weekly_difference],axis=1)
        
        monthly_difference=songs.groupby("Video ID")["View Count"].diff(4).rename("Monthly Difference").fillna(0).astype(int)
        updated_songs=pd.concat([updated_songs,monthly_difference],axis=1)
        
        age=pd.to_datetime(updated_songs["Date"],infer_datetime_format=True)-pd.to_datetime(updated_songs["Published"],infer_datetime_format=True)
        age=age.rename("Age")
        updated_songs=pd.concat([updated_songs,age],axis=1)

        updated_songs["Weekly Difference"]=updated_songs.apply(lambda x: x["View Count"] if x["Age"]>=timedelta(days=7) and x["Age"]<timedelta(days=14) else x["Weekly Difference"], axis=1)
        updated_songs["Monthly Difference"]=updated_songs.apply(lambda x: x["View Count"] if x["Age"]>=timedelta(days=31) and x["Age"]<timedelta(days=38) else x["Monthly Difference"], axis=1)

        #filter out premature and auto-generated songs
        updated_songs=updated_songs[updated_songs["Channel"].str.contains("Topic")==False]
        updated_songs=updated_songs[pd.to_datetime(updated_songs["Date"],infer_datetime_format=True)-pd.to_datetime(updated_songs["Published"],infer_datetime_format=True)>timedelta(days=7)]

        songs_ofinterest=updated_songs[updated_songs["Is Cover"].isin(songtype)&(updated_songs["Talents"].str.contains("|".join(talents)))]
        ranks=songs_ofinterest.groupby("Date")[sortmethod].rank(method="first",ascending=False).rename("Rank")
        songs_ofinterest=pd.concat([songs_ofinterest,ranks],axis=1)

        prev_rank=songs_ofinterest.groupby("Video ID")["Rank"].shift(1).rename("Previous Rank").fillna(0)
        songs_ofinterest=pd.concat([songs_ofinterest,prev_rank],axis=1)
        
        topn_songs=songs_ofinterest[songs_ofinterest["Date"]==weekof].sort_values(by=[sortmethod], ascending=False, ignore_index=True).head(topn)
        topn_songs["Weekly Difference"]=topn_songs["Weekly Difference"].apply(lambda x: f'{x:,}')
        topn_songs["Monthly Difference"]=topn_songs["Monthly Difference"].apply(lambda x: f'{x:,}')
        topn_songs["View Count"]=topn_songs["View Count"].apply(lambda x: f'{x:,}')
        
    return render_template("songlists.html",content=topn_songs, topn=topn, endweek=endweek, sortmethod=sortmethod, entries=len(topn_songs))
    
if __name__=="__main__":
    app.run()
