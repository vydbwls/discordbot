import discord
from discord.ext import commands
import random
import asyncio
from dotenv import load_dotenv

load_dotenv("discord_Li_token.env")  # .env 파일 로드
TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # 환경 변수에서 토큰 가져오기

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

#상태 바꾸기
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("!명령어 || 작동"))

@bot.event
async def on_command_error(ctx, error):
    # 커맨드를 찾을 수 없는 경우에만 CommandNotFound 오류를 처리합니다.
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("어~... 잘 모르겠어요!")

#초이스 기능
@bot.command()
async def choice(ctx, *choices):
    if len(choices) < 2:  # 선택지가 2개 미만일 경우 에러 메시지 전송
        await ctx.send('선택지가 하나밖에 없는걸요?',reference=ctx.message)
        return

    selected_choice = random.choice(choices)  # 선택지 중 하나 랜덤 선택
    await ctx.send(f'{selected_choice}',reference=ctx.message)

#음성참가
@bot.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("음? 어디로 들어가야하나요?", reference=ctx.message)
        return

    channel = ctx.author.voice.channel
    await channel.connect()     
    await ctx.send("내보낼 땐 !leave", reference=ctx.message)
    voice_client = await channel.connect()

    def check_members(channel):
        members = len(channel.members)  # 음성 채널의 멤버 수 확인
        return members == 1  # 봇 자신만 음성 채널에 남아있을 때 True 반환

    while True:
        await asyncio.sleep(60)  # 60초마다 확인

        if check_members(channel):
            await voice_client.disconnect()
            break

@bot.command()
async def leave(ctx):
    voice_client = ctx.voice_client
    if voice_client is not None:
        await voice_client.disconnect()
        await ctx.send("다음에 봐요~", reference=ctx.message)

#1d100다이스
@bot.command()
async def d100(ctx, dice1: int):
    dice = random.randint(1, 100)
    if 1 <= dice <= dice1 / 5:
        embed = discord.Embed(title="다이스 결과", color=discord.Color.brand_green())
        embed.add_field(name="", value=f"기능치:``{dice1}``\r\n결과 값:``{dice}``", inline=False)
        embed.add_field(name="> 극단적 성공", value="", inline=False)
        await ctx.channel.send(embed=embed, reference=ctx.message)

    elif dice1 / 5 < dice <= dice1 / 2:
        embed = discord.Embed(title="다이스 결과", color=discord.Color.dark_green())
        embed.add_field(name="", value=f"기능치:``{dice1}``\r\n결과 값:``{dice}``", inline=False)
        embed.add_field(name="> 어려운 성공", value="", inline=False)
        await ctx.channel.send(embed=embed, reference=ctx.message)

    elif dice1 / 2 < dice <= dice1:
        embed = discord.Embed(title="다이스 결과", color=discord.Color.dark_green())
        embed.add_field(name="", value=f"기능치:``{dice1}``\r\n결과 값:``{dice}``", inline=False)
        embed.add_field(name="> 성공", value="", inline=False)
        await ctx.channel.send(embed=embed, reference=ctx.message)

    elif dice == 1:
        embed = discord.Embed(title="다이스 결과", color=discord.Color.green())
        embed.add_field(name="", value=f"기능치:``{dice1}``\r\n결과 값:``{dice}``", inline=False)
        embed.add_field(name="> 대성공", value="", inline=False)
        await ctx.channel.send(embed=embed, reference=ctx.message)

    elif dice == 100:
        embed = discord.Embed(title="다이스 결과", color=discord.Color.red())
        embed.add_field(name="", value=f"기능치:``{dice1}``\r\n결과 값:``{dice}``", inline=False)
        embed.add_field(name="> 대실패", value="", inline=False)
        await ctx.channel.send(embed=embed, reference=ctx.message)

    else:
        embed = discord.Embed(title="다이스 결과", color=discord.Color.dark_red())
        embed.add_field(name="", value=f"기능치:``{dice1}``\r\n결과 값:``{dice}``", inline=False)
        embed.add_field(name="> 실패", value="", inline=False)
        await ctx.channel.send(embed=embed, reference=ctx.message)
    

#1d20 다이스
@bot.command()
async def d20(ctx):
    dice = random.randint(1,20)
    await ctx.channel.send("{}".format(dice), reference=ctx.message)

#2d6 다이스
@bot.command()
async def d6_2(ctx, dice: int):
    dice1 = random.randint(1,6)
    dice2 = random.randint(1,6)
    if dice1 == 1 and dice2 == 1:
        embed = discord.Embed(title="다이스 결과", color=discord.Color.red())
        embed.add_field(name="", value=f"기능치:``{dice}``\r\n결과 값:``{dice1}`` , ``{dice2}`` > ``{dice1+dice2}``", inline=False)
        embed.add_field(name="> 펌블", value="", inline=False)
        await ctx.channel.send(embed=embed, reference=ctx.message)
    
    elif dice1 == 6 and dice2 == 6:
        embed = discord.Embed(title="다이스 결과", color=discord.Color.brand_green())
        embed.add_field(name="", value=f"기능치:``{dice}``\r\n결과 값:``{dice1}`` , ``{dice2}`` > ``{dice1+dice2}``", inline=False)
        embed.add_field(name="> 스페셜", value="", inline=False)
        await ctx.channel.send(embed=embed, reference=ctx.message)
    
    elif dice1 + dice2 >= dice:
        embed = discord.Embed(title="다이스 결과", color=discord.Color.dark_green())
        embed.add_field(name="", value=f"기능치:``{dice}``\r\n결과 값:``{dice1}`` , ``{dice2}`` > ``{dice1+dice2}``", inline=False)
        embed.add_field(name="> 성공", value="", inline=False)
        await ctx.channel.send(embed=embed, reference=ctx.message)

    elif dice1 + dice2 < dice:
        embed = discord.Embed(title="다이스 결과", color=discord.Color.dark_red())
        embed.add_field(name="", value=f"기능치:``{dice}``\r\n결과 값:``{dice1}`` , ``{dice2}`` > ``{dice1+dice2}``", inline=False)
        embed.add_field(name="> 실패", value="", inline=False)
        await ctx.channel.send(embed=embed, reference=ctx.message)

#랜덤 주사위
@bot.command()
async def d(ctx, dice: int):
    dice1 = random.randint(1, dice)
    await ctx.channel.send("{}".format(dice1), reference=ctx.message)

#간단한 대화 상호작용
@bot.command()
async def 안녕(ctx):
    await ctx.channel.send("반가워요~", reference=ctx.message)

#임베드 자기소개
@bot.command()
async def 명령어(ctx):
    embed = discord.Embed(title='제가 누구냐면-', 
                          description='아래를 참고해주세요~',color=discord.Color.blue())
    embed.add_field(name='> !안녕', value='간단한 인사~')
    embed.add_field(name='> !명령어', value='이 카드를 보는\r\n기능이에요.')
    embed.add_field(name='> !choice 선택1 선택2...', value='제가 한 번\r\n선택해볼게요!')
    embed.add_field(name='> !홀짝', value='간단한\r\n홀짝 게임!')
    embed.add_field(name='> !d100 특성치', value='누군가의~\r\n부름이 들려요~')
    embed.add_field(name='> !d20', value='드래곤과 모험\r\n좋아하세요?')
    embed.add_field(name='> !d6_2 기능치', value='그렇다면\r\n마법은요?')
    embed.add_field(name='> !join', value='다들 무슨\r\n얘기하세요~?')
    embed.add_field(name='> !d 숫자', value='랜덤 주사위~')
    await ctx.channel.send(embed=embed, reference=ctx.message)

#임베드 홀짝
@bot.command()
async def 홀짝(ctx):
    dice = random.randint(1,6)
    embed = discord.Embed(title= '게임 좋아하세요~?', description='선택한 뒤에 어떤 수가 나오는지 알려줄게요-',color=discord.Color.blue())
    embed.add_field(name='> 주사위의 눈', value='???')
    embed.add_field(name='> 홀수', value='🔴')
    embed.add_field(name='> 짝수', value='🔵')

    await ctx.message.delete()

    msg = await ctx.channel.send(embed=embed)
    await msg.add_reaction('🔴')
    await msg.add_reaction('🔵')

    try:
        def check(reaction, user):
            return str(reaction) in ['🔴', '🔵'] and user == ctx.author and reaction.message.id == msg.id
        reaction, user = await bot.wait_for('reaction_add',check=check)
        if(str(reaction) == '🔴' and dice % 2 == 1) or (str(reaction) == '🔵' and dice % 2 == 0):
            embed = discord.Embed(title='게임 좋아하세요~?', description='정답! 잘하시는데요?',color=discord.Color.blue())
        else:
            embed = discord.Embed(title='게임 좋아하세요~?', description='땡! 아쉽게 틀렸네요-',color=discord.Color.blue())
        embed.add_field(name='> 주사위의 눈', value = str(dice))
        embed.add_field(name='> 홀수', value='🔴')
        embed.add_field(name='> 짝수', value='🔵')
        await msg.clear_reactions()
        await msg.edit(embed=embed)
    except: pass



bot.run(TOKEN)
