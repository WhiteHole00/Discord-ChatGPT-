import discord
import sqlite3
import openai
import time
TOKEN = "디스코드 봇 토큰"


intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

add_ad = []

@client.event
async def on_ready():
    print(f'Client_ID : {client.user.id}\nInvite_Link : https://discord.com/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot')
    await client.change_presence(activity=discord.Streaming(name= f"<@멘션> <할말>", url="https://www.twitch.tv/whitehole"))

@client.event
async def on_message(message):

    if message.author.id == 710437780546650143 or message.author.id in add_ad:
        if message.content.startswith("!등록"):
            try:
                key = message.content.split(" ")[1]
            except Exception as e:
                return await message.channel.send(f"!등록 <키>")
            else:
                con = sqlite3.connect("db.db")
                cur = con.cursor()
                cur.execute(f"SELECT * FROM main WHERE id == ?;", (message.author.id,))
                key_ = cur.fetchone()
                con.close()
                if key_ == None:
                    con = sqlite3.connect("db.db")
                    cur = con.cursor()
                    cur.execute("INSERT INTO main VALUES(?, ?);", (message.author.id, key))
                    con.commit()
                    con.close()
                    await message.reply(f"키 등록 완료")
                else:
                    await message.reply(f"이미 있음")


        if message.content.startswith(".라센"):
            if message.author.id == 710437780546650143:
                try:
                    con = sqlite3.connect("db.db")
                    cur = con.cursor()
                    cur.execute(f"SELECT * FROM main WHERE id == ?;", (message.author.id,))
                    key_ = cur.fetchone()
                    con.close()
                    license_key_ = key_[1]
                    if key_ == None:
                        return await message.channel.send(f"<@710437780546650143>이 라센 키 등록 해야댐")
                    else:
                        await message.reply("디엠 확인점")
                        await message.author.send(f"라센키 : {license_key_}")
                except Exception as e:
                    await message.reply("디엠 열어")
                    return
            else:
                await message.reply("니가 봇 개발자야?")

            
    if message.content.startswith(f"<@{client.user.id}> "):
        try:
            msg = message.content[22:]
            await message.add_reaction("🖕")
        except Exception as e:
            print(e)
            pass
        con = sqlite3.connect("db.db")
        cur = con.cursor()
        cur.execute(f"SELECT * FROM main WHERE id == ?;", ("710437780546650143",))
        key_ = cur.fetchone()
        con.close()
        if key_ == None:
            return await message.channel.send(f"<@710437780546650143>이 라센 키 등록 해야댐")
        else:
            try:
                license_key = key_[1]
                openai.api_key = license_key
                async with message.channel.typing():
                    completion = openai.Completion.create(
                            engine = 'text-davinci-003'  
                            , prompt = msg
                            , temperature = 0.5 
                            , max_tokens = 1024
                            , top_p = 1
                            , frequency_penalty = 0
                            , presence_penalty = 0)
                    answer = completion['choices'][0]['text']
            except Exception as e:
                await message.reply("고장남 새 질문 ㄱ")
                pass
        
    elif message.content.startswith(f"<@{client.user.id}>"):
        emb1 = discord.Embed(title="안녕하세요!👋",description=f"저를 사용하실려면 채팅에서 저를 언급(<@{client.user.id}>)만 하시면 됩니다!",color=discord.Colour.orange())
        emb1.set_image(url="https://im.ezgif.com/tmp/ezgif-1-416bea0294.gif")
        return await message.reply(embed=emb1)
        
client.run(TOKEN)
