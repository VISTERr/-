import discord
from discord.ext import commands, tasks

# 봇 토큰과 특정 채널 ID 설정
TOKEN = 'MTI4OTUyMDgyMTU1MDg0NjA0Mw.GlPZ68.-lUNQqJWPNzwZ5JL67rdsv6F_o4IeZYwBe-Zp4'
TARGET_CHANNEL_ID = 1289520626901717070  # 이미지가 올라갈 채널 ID

# 유저별 등록 횟수를 저장할 딕셔너리
user_submission_count = {}

# 봇 프리픽스와 인텐트 설정
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents)

# 봇이 준비되었을 때 실행되는 이벤트
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    update_status.start()  # 상태 업데이트 태스크 시작

# 서버 수에 맞춰 상태 메시지 업데이트
@tasks.loop(minutes=10)  # 10분마다 상태 업데이트 (주기를 원하는 대로 조정 가능)
async def update_status():
    server_count = len(bot.guilds)  # 봇이 속해 있는 서버 수
    await bot.change_presence(activity=discord.Game(f"서버 {server_count}개에서 활동 중"))

# 작품 등록 명령어: 유저가 이미지를 첨부하면 특정 채널에 임베드로 전송
@bot.command(name='작품등록')
async def register_artwork(ctx):
    # 첨부 파일 확인
    if len(ctx.message.attachments) == 0:
        await ctx.send("> 이미지가 첨부되지 않았습니다. 작품 이미지를 첨부해주세요.")
        return

    # 첫 번째 첨부 파일 가져오기 (여러 개 있을 경우 첫 번째만 사용)
    attachment = ctx.message.attachments[0]

    # 유저 ID를 사용해 등록 횟수 업데이트
    user_id = ctx.author.id
    if user_id in user_submission_count:
        user_submission_count[user_id] += 1
    else:
        user_submission_count[user_id] = 1

    # 등록 횟수 가져오기
    submission_count = user_submission_count[user_id]

    # 특정 채널로 임베드 전송
    target_channel = bot.get_channel(TARGET_CHANNEL_ID)
    if target_channel:
        embed = discord.Embed(
            title="새로운 작품이 등록되었습니다!",
            description=f"등록자: {ctx.author.mention} \n등록 횟수: {submission_count}회"
        )
        embed.set_image(url=attachment.url)
        await target_channel.send(embed=embed)
        await ctx.send(f"> 작품이 성공적으로 등록되었습니다! 현재까지 {submission_count}번 작품을 등록하셨습니다.")
    else:
        await ctx.send("> 오류가 발생했습니다. 관리자가 채널 설정을 확인해주세요.")

# 봇 실행
bot.run(TOKEN)
