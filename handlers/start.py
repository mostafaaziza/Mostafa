from time import time
from datetime import datetime
from config import BOT_USERNAME, BOT_NAME, ASSISTANT_NAME, OWNER_NAME, UPDATES_CHANNEL, GROUP_SUPPORT
from helpers.filters import command
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from helpers.decorators import authorized_users_only


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)

async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


@Client.on_message(command("start") & filters.private & ~filters.edited)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>✨ **مرحبا {message.from_user.first_name}** \n
💭 **[{BOT_NAME}](https://t.me/{BOT_USERNAME}) هذا اسمي !**

⋆  **اختصاصي تشغيل الاغاني فلمحادثات الصوتيه**

⋆  **اضفني الان الي مجموعتك لكي تبدا الحفله**

⋆  **اضغط علي هذا الامر /help لعرض الاوامر**
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
                    InlineKeyboardButton(
                        "اضف البوت لمجموعتك", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")
                ],[
                    InlineKeyboardButton(
                        "جروب الدعم", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "قناه السورس", url=f"https://t.me/{UPDATES_CHANNEL}")               
                 ],[
                    InlineKeyboardButton(
                        "00:00", url="https://t.me/BANDA1M"
                    )
                ]
            ]
        ),
     disable_web_page_preview=True
    )


@Client.on_message(command(["start", f"start@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def start(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        f"""✔ **الروبوت قيد التشغيل**\n<b>💞 **ᴜᴘᴛɪᴍᴇ:**</b> `{uptime}`""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "جروب الدعم", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "قناه السورس", url=f"https://t.me/{UPDATES_CHANNEL}"
                    )
                ]
            ]
        )
    )

@Client.on_message(command(["help", f"help@{BOT_USERNAME}"]) & filters.group & ~filters.edited)
async def help(client: Client, message: Message):
    await message.reply_text(
        f"""<b>🤗 مرحبا {message.from_user.mention()}, يرجى النقر فوق الزر أدناه لرؤية رسالة المساعدة التي يمكنك قراءتها لاستخدام هذا الروبوت</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="✔ كيف تستعملني", url=f"https://t.me/{BOT_USERNAME}?start=help"
                    )
                ]
            ]
        )
    )

@Client.on_message(command("help") & filters.private & ~filters.edited)
async def help_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>• الاوامر 🛠 

- /play <اسم الأغنية> 
ـ تشغيل الأغنية التي طلبتها. 

- /playlist 
ـ عرض قائمة التشغيل الآن. 

- /song <اسم الاغنيه>
ـ تنزيل الأغاني التي تريدها بسرعة. 

- /search <اسم الاغنيه> 
ـ البحث في اليوتيوب مع التفاصيل. 

- /vsong <اسم الاغنيه>
ـ تنزيل مقاطع الفيديو التي تريدها بسرعة

- /lyric <اسم الاغنيه>
ـ إحضار كلمات الاغنيه. 

• الاوامر الخاصه بِ المشرفين فقط 👷‍♂️ . 
 
- /player  
ـ فتح لوحة إعدادات مشغل الموسيقى

- /pause 
ـ وقف تشغيل الاغنيه الحاليه. 

- /resume
ـ استئناف تشغيل الأغنية. 

- /skip 
ـ التقدم للأغنية التالية

- /end 
ـ إيقاف تشغيل الموسيقى. 

- /musicplayer on 
ـ لتعطيل مشغل الموسيقى في مجموعتك. 

- /musicplayer off 
- لتمكين مشغل الموسيقى في مجموعتك. 

- /userbotjoin 
- دعوة المساعد إلى الدردشه الحاليه 

- /userbotleave 
- إزالة المساعد من الدردشة الحالية. 

- /reload 
- تحديث قائمة الإدارة. 

- /uptime 
- التحقق من وقت تشغيل البوت

- /ping 
- تحقق من حالة البوت 

• الاوامر الخاصه بالمطورين🧙‍♂️

- /pmpermit on | off  
ـ قفل/فتح الدردشه ف الخاص. 

- /userbotleaveall 
- اطلب من المساعد مغادرة جميع المجموعات

- /gcast 
- عمل إذاعه

• الشات الخاص بالبوت المساعد 💬

- .yes 
- الموافقة على إرسال رسالة إلى المساعد في الخاص. 

- .no 
- رفض إرسال رسالة إلى المساعد في الخاص.
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "جروب الدعم", url=f"https://t.me/{GROUP_SUPPORT}"
                    ),
                    InlineKeyboardButton(
                        "قناة السورس", url=f"https://t.me/{UPDATES_CHANNEL}"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "00:00", url=f"https://t.me/BANDA1M/6"
                    )
                ]
            ]
        )
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("ᴘɪɴɢɪɴɢ...")
    delta_ping = time() - start
    await m_reply.edit_text(
        "🎶 `ᴘᴏɴɢ!!`\n"
        f"💞 `{delta_ping * 1000:.3f} ᴍs`"
    )


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}"]) & ~filters.edited)
@authorized_users_only
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🤖 ʙᴏᴛ sᴛᴀᴛᴜs:\n"
        f"➤ **ᴜᴘᴛɪᴍᴇ:** `{uptime}`\n"
        f"➤ **sᴛᴀʀᴛ ᴛɪᴍᴇ:** `{START_TIME_ISO}`"
    )
