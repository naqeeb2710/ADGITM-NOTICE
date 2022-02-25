import os
import discord
from bs4 import BeautifulSoup
import requests
from discord.ext import commands,tasks
from replit import db



running=1
bot = commands.Bot(command_prefix = "$")

sendMsg=0

def updateDB(lis):
  db["data"]=lis
def getDB():
  if "data" in db.keys():
    return(db["data"])
  else:
    db["data"]=[]
    return([])

async def mssg(msg):
  print("Here i am")
  channel = discord.utils.get(client.get_all_channels(), name='adgitm-notices')
  await channel.send(msg)



@tasks.loop(minutes=0.1,count=10)
async def startt():
  msgs=[]
  sendMsg=0
  if not running:
    return
  print("running...")
  url = "https://adgitmdelhi.ac.in/notice"
  headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.3'}

  resp = requests.get(url,headers=headers)
  soup = BeautifulSoup(resp.text,'html.parser')
  mydivs = soup.find_all("h3", {"class": "entry-title"})
  mydivs=mydivs[:10]
  nameLis=[]
  linkLis=[]
  for i in mydivs:
      lis=str(i).split('"')
      link=lis[3]
      name=lis[7]
      nameLis.append(name)
      linkLis.append(link)
      
  prevLis = getDB()
  updateDB(nameLis)
  for i in prevLis:
      if i in nameLis:
          linkLis.remove(linkLis[nameLis.index(i)])
          nameLis.remove(i)
          
  if nameLis!=[]:
      #notify
      for i in nameLis:
        toSend=""
        sendMsg=1
        toSend= "New Notice: '"+ i +":"+str(linkLis[nameLis.index(i)])+"\n"
        msgs.append(toSend)
  if sendMsg:
    for i in msgs:
      await mssg(i)
      msgs.remove(i)
        
client = discord.Client()        



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
  

@client.event
async def on_message(message):
    global sendMsg
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    if message.content.startswith('$setup'):
      try:
        channel = discord.utils.get(client.get_all_channels(), name='adgitm-notices')
        await channel.send("Already rolling...")
        if not startt.is_running():
          startt.start()
        running = 1
      except:
        await message.guild.create_text_channel('adgitm-notices')
        if not startt.is_running():
          startt.start()
      
    if message.content.startswith('$start'):
      try:
        channel = discord.utils.get(client.get_all_channels(), name='adgitm-notices')
        await channel.send("Starting...")
        if not startt.is_running():
          startt.start()
        running = 1
      except:
        await message.channel.send('Setup toh krle bro! (By sending $setup)')
    if message.content.startswith('$stop'):
      running=0
      
    
    
#change update_fetch.start() to:
client.run(os.getenv('TOKEN'))
bot.run(os.getenv('TOKEN'))