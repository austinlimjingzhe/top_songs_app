# Top Songs Dashboard
A Python implementation of a YouTube views scraper + Flask application displaying the Top Songs of a Playlist by Weekly Views.

## Introduction
Since YouTube has effectively invalidated my previous project on a Dislikes Checker, I was trying to find another YouTube Data API project to work on in my spare time. 

This project was inspired by the work done by members of the Hololive community,<a href="https://www.youtube.com/channel/UC94Mhi_4KZNX7bzHaoBnRTw">ホロ歌は癒しの万能薬hololive songs</a> and <a href="https://www.youtube.com/channel/UCfjDIiKHIhKuBxxmJVnW3vg">柊すいかのホロ歌部</a>, who have spent much effort in compiling the most viewed songs released by the talents of Hololive. Currently being a manual process, this project sought to automate the scraping of view counts and generation of a top N list of songs.

The following video shows a demonstration of the application:
<video src="https://user-images.githubusercontent.com/88301287/153442202-3840a981-303d-4735-986d-ea191c431d21.mp4"></video>

## Background
Hololive is an entertainment company under Cover Corporation. Its talents include Vtubers who occassionally release fully produced music videos of song covers and original songs. Fans of the talents and members of Hololive community like the ones referenced in the introduction are interested in catalogueing the weekly statistics of the top viewed songs produced by Hololive talents.

In theory, with some modifications, this application can be applied to track the weekly statistics of any video or group of videos, not just Hololive talents. I hope that my work can serve as an example for anyone out there who is also just starting to learn html and flask, and can be generalised to other playlist contexts. 

## Tools

1. Flask
2. Youtube API

## Features

1. Customized List Settings: Users can choose to filter the list by branch, type of song, top n and frequency of views
2. Graphs of views over time: Users can view a plot of the view counts as a modal window.

## Automating the Scraping of Views
To automate the scraping, the Windows Task Scheduler is used to run the <code>scheduler.bat</code> program every week. This will in turn run the <code>scraper.py</code> file to scrape the YouTube Data and store it in CSV files.

## Note:
As the talent agency occassionally brings new talents in, the list of talent names must be updated when that happens.
