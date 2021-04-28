#My DND group has trouble updating their FantasyGrounds clients
#Which leads to everyone waiting for everyone else to update
#And that can sometimes take forever
#Passive agressvely remind your friends with this bot! 

from bs4 import BeautifulSoup
import requests
import re
import time
import os
from datetime import date, datetime
from discord_webhook import DiscordWebhook, DiscordEmbed 

WEBHOOK_URL = os.environ["WEBHOOK_URL"]

req = requests.get("https://www.fantasygrounds.com/filelibrary/patchnotes_v4.html")
forum = requests.get("https://www.fantasygrounds.com/forums/forumdisplay.php?37-City-Hall")

soup = BeautifulSoup(req.text, 'html.parser')
forum_soup = BeautifulSoup(forum.text, 'html.parser').findAll('li', {"class" : "nonsticky"})

links = []

for each_dev in forum_soup:
    for each_link in each_dev.findChildren('a', {"class" : "title"}, href=True):
        if re.match(r".*., 20.*", str(each_link)) != None:
            links.append(each_link)


previous = re.findall(r"Version 4\..*", soup.prettify())[1]
links[0]['href']

root_link = "https://www.fantasygrounds.com/forums/"
page_link = root_link + links[0]['href']

posts = BeautifulSoup(requests.get(page_link).text, 'html.parser')
releases = posts.find_all('div', {"class" : "postbody"})

#print(releases[-1])

release_len = len(releases)

#print(release_len)

release_notes = releases[-1].find_all('li')
notes = ""

for note in release_notes:
    notes += note.contents[0] + '\n'

#major_release_webhook = DiscordWebhook(WEBHOOK_URL, content="New Fantasy Grounds Major Update!\nVersion {0} has been released!\nMake sure to update!\n".format(previous))
#minor_release_webhook = DiscordWebhook(WEBHOOK_URL, content="New Fantasy Grounds Minor Release for {0}! Make sure to update!\n{1}".format(date.today().strftime("%B %d, %Y") ,"```\n" + notes + "```"))

release_len = 0

while True:
    year, month, day, hour, min = map(int, time.strftime("%Y %m %d %H %M").split())
    if date.weekday(date.today()) == 5 and hour == 23:
        dnd_night_hook = DiscordWebhook(WEBHOOK_URL, content="@everyone\nIt's DND night my dudes! \nTaco says, 'Update Your Fantasy Grounds!'\n")
        dnd_night_hook.execute()

    req = requests.get("https://www.fantasygrounds.com/filelibrary/patchnotes_v4.html")
    forum = requests.get("https://www.fantasygrounds.com/forums/forumdisplay.php?37-City-Hall")

    forum_soup = BeautifulSoup(forum.text, 'html.parser').findAll('li', {"class" : "nonsticky"})

    links = []

    for each_dev in forum_soup:
        for each_link in each_dev.findChildren('a', {"class" : "title"}, href=True):
            if re.match(r".*., 20.*", str(each_link)) != None:
                links.append(each_link)


    page_link = root_link + links[0]['href']
    posts = BeautifulSoup(requests.get(page_link).text, 'html.parser')
    releases = posts.find_all('div', {"class" : "postbody"})

    if len(releases) != release_len:
        release_len = len(releases)
        release_notes = releases[-1].find_all('li')
        notes = ""
        for note in release_notes:
            notes += note.contents[0] + '\n'
        minor_release_webhook = DiscordWebhook(WEBHOOK_URL, content="New Fantasy Grounds Minor Release for {0}! Make sure to update!\n{1}".format(date.today().strftime("%B %d, %Y") ,"```\n" + notes + "```"))
        minor_release_webhook.execute()

    latest = re.findall(r"Version 4\..*", BeautifulSoup(req.text, 'html.parser').prettify())[0]

    if latest != previous:
        previous = latest
        webhook = DiscordWebhook(WEBHOOK_URL, content="New Fantasy Grounds Update!\nVersion {0} has been released!\nMake sure to update!\n".format(previous))
        webhook.execute()

    time.sleep(3600)
    
