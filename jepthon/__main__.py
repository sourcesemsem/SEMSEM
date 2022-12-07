import sys

from aiohttp import web

import jepthon
from jepthon import BOTLOG_CHATID, PM_LOGGER_GROUP_ID, tbot

from .Config import Config
from .core.logger import logging
from .core.server import web_server
from .core.session import jepiq
from .utils import (
    add_bot_to_logger_group,
    load_plugins,
    mybot,
    saves,
    setup_bot,
    startupmessage,
    verifyLoggerGroup,
)

LOGS = logging.getLogger("سورس ريك ثون")

cmdhr = Config.COMMAND_HAND_LER


async def jepthons(session=None, client=None, session_name="Main"):
    if session:
        LOGS.info(f"••• جار بدأ الجلسة [{session_name}] •••")
        try:
            await client.start()
            return 1
        except:
            LOGS.error(f"خطأ في الجلسة {session_name}!! تأكد وحاول مجددا !")
            return 0
    else:
        return 0


# تأكد من تنصيب بعض الاكواد
async def jepthonstart(total):
    await setup_bot()
    await mybot()
    await verifyLoggerGroup()
    await add_bot_to_logger_group(BOTLOG_CHATID)
    if PM_LOGGER_GROUP_ID != -100:
        await add_bot_to_logger_group(PM_LOGGER_GROUP_ID)
    await startupmessage()
    await saves()


async def start_jepthon():
    try:
        tbot_id = await tbot.get_me()
        Config.TG_BOT_USERNAME = f"@{tbot_id.username}"
       jepiq.tgbot = tbot
        LOGS.info("•••  جار بدا سورس  ريك ثون •••")
        CLIENTR = await jepthons(Config.STRING_SESSION, sbb_b, "STRING_SESSION")
        await tbot.start()
        total = CLIENTR
        await load_plugins("plugins")
        await load_plugins("assistant")
        LOGS.info(f"تم انتهاء عملية التنصيب بنجاح على سكالينجو")
        LOGS.info(
            f"لمعرفة اوامر السورس ارسل {cmdhr}الاوامر\
        \nمجموعة قناة السورس  https://t.me/rickthon_group"
        )
        LOGS.info(f"» عدد جلسات التنصيب الحالية = {str(total)} «")
        await jepthonstart(total)
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, Config.PORT).start()
    except Exception as e:
        LOGS.error(f"{str(e)}")
        sys.exit()

if Config.VCMODE:
        await install_externalrepo("https://github.com/rick1128/Rickvc", "jepvc", "jepthonvc")

   jepiq.disconnect()
else:
    try:
       jepiq.run_until_disconnected()
    except ConnectionError:
        pass
