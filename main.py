import httpx
import uvicorn
from fastapi import FastAPI
import subprocess
import asyncio
from datetime import datetime
from telegram import Bot
from config import *

app = FastAPI()
bot = Bot(token=TOKEN)

#Send message to telegram if error
async def send_telegram_message_on_error(pool, status):
     message = f'Error: Pool {pool} status is {status}'
     await bot.sendMessage(chat_id=CHAT_ID, text=message)

#Check zfs status by own API
async def get_my_zfs_status(url):
    while True:
        await asyncio.sleep(5)
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            zfs_status = response.json()
            for pool, data in zfs_status.items():
                status = data["Health"]
                if status != "ONLINE":
                    await send_telegram_message_on_error(pool, status)

#Background sheduler
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(get_my_zfs_status(URL))


#Main APP route
@app.get("/zfs_status")
async def root() -> dict:
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = {}
    check_command = ["zpool", "list", "-o", "name,size,cap,free,health"]
    zfs_pools = subprocess.check_output(check_command).decode().strip().split('\n')[1:]
    for pool in zfs_pools:
        name, size, capacity,free, health = pool.split()
        status[name] = {'Health': health,
                        'Capacity': capacity,
                        'Free': free,
                        "Timestamp": current_time}
    print(status)
    return status

if __name__ == '__main__':
    uvicorn.run(app, host=HOST, port=PORT)
