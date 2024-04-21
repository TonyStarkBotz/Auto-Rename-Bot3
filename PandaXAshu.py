import asyncio
import requests
from datetime import datetime, timedelta
from pytz import timezone
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from config import Config
from aiohttp import web
from route import web_server

class Bot(Client):

    def __init__(self):
        super().__init__(
            name="renamer",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username  
        self.uptime = Config.BOT_UPTIME     
        
        if Config.WEBHOOK:
            app = web.AppRunner(await web_server())
            await app.setup()       
            await web.TCPSite(app, "0.0.0.0", 8080).start()     
        print(f"{me.first_name} Is Started.....✨️")
        for id in Config.ADMIN:
            try: 
                await self.send_message(Config.LOG_CHANNEL, f"**{me.first_name}  Is Started.....✨️**")                                
            except: 
                pass
        
        # Schedule the task to redeploy the app after 7 hours
        asyncio.create_task(self.redeploy_app())

        # Send initial restart message if logging channel is configured
        if Config.LOG_CHANNEL:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time = curr.strftime('%I:%M:%S %p')
                await self.send_message(Config.LOG_CHANNEL, f"**{me.mention} Is Restarted !!**\n\n📅 Date : `{date}`\n⏰ Time : `{time}`\n🌐 Timezone : `Asia/Kolkata`\n\n🉐 Version : `v{__version__} (Layer {layer})`</b>")                                
            except Exception as e:
                print("Please Make This Is Admin In Your Log Channel")
                print(f"Error sending initial restart message: {e}")

    async def redeploy_app(self):
        await asyncio.sleep(10)  # 7 hours in seconds
        try:
            response = requests.post('https://api.render.com/v1/owner/srv-coillftjm4es739qjnk0/services/srv-coillftjm4es739qjnk0/deploy', headers={'Authorization': 'Bearer hC6xRth8Rag'})
            if response.status_code == 200:
                print("Render app redeployed successfully.")
            else:
                print(f"Failed to redeploy Render app. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error redeploying Render app: {e}")

Bot().run()
