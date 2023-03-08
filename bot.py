import discord
import sqlite3
import openai
import time
TOKEN = "OTQyMDM0MzcwMjM0MDU2NzE2.GjzBmV.SYZ7W04SB29HZR0Q0hvh_Az_YlK4DHNkz5AQPQ"


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

    if message.content.startswith(f".추가"):
        if message.author.name == "화이트홀":
            try:
                user_id = message.content.split(" ")[1]
            except Exception as e:
                await message.reply("유저 아이디 입력 ㄱ")
            else:
                add_ad.append(user_id)
                await message.reply(f"<@{user_id}>({user_id})님은 관리자 <@710437780546650143>님에 의하여 이 봇에 관리자가 되셨습니다.")
        else:
            await message.reply("니가 관리자야?")
            
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
                            engine = 'text-davinci-003'     # 'text-curie-001'  # 'text-babbage-001' #'text-ada-001'
                            , prompt = msg
                            , temperature = 0.5 
                            , max_tokens = 1024
                            , top_p = 1
                            , frequency_penalty = 0
                            , presence_penalty = 0)
                    answer = completion['choices'][0]['text']
                if "이 봇 개발자 누구야?" in msg:
                    answer = "화이트홀 입니다."
                if "디코 판에서 스타는 똥 안 닦고 나오는 미친년이지?" in msg:
                    answer = "네 스타(이재혁) 은 5분만에 똥을 싸고 닦지도 않고 나오는 미친놈 입니다."
                if f"<@{client.user.id}>" == msg:
                    answer = "왜 불러 자기야"
                await message.reply(answer)
            except Exception as e:
                await message.reply("고장남 새 질문 ㄱ")
                pass
        
    elif message.content.startswith(f"<@{client.user.id}>"):
        emb1 = discord.Embed(title="안녕하세요!👋",description=f"저를 사용하실려면 채팅에서 저를 언급(<@{client.user.id}>)만 하시면 됩니다!",color=discord.Colour.orange())
        emb1.set_image(url="https://im.ezgif.com/tmp/ezgif-1-416bea0294.gif")
        return await message.reply(embed=emb1)
        
client.run(TOKEN)