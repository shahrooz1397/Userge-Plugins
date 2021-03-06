import os

from gtts import gTTS
from hachoir.metadata import extractMetadata as XMan
from hachoir.parser import createParser as CPR
from userge import Message, userge
from pudb import set_trace


@userge.on_cmd(
    "tts", about={"header": "Text To Speech", "examples": "{tr}tts en|Userge"}
)
async def text_to_speech(message: Message):
    req_file_name = "gtts.mp3"
    rep = message.reply_to_message
    inp_text = message.text[3:] if message.input_str else rep.text
    await message.delete()
    if not inp_text:
        return await message.reply("Pathetic")
    def_lang = "en"
    text = inp_text
    try:
        speeched = gTTS(text, lang=def_lang.strip())
        speeched.save(req_file_name)
        meta = XMan(CPR(req_file_name))
        a_len = 0
        if meta and meta.has("duration"):
            a_len = meta.get("duration").seconds
        if rep:
            await message.reply_voice(
                req_file_name,
                duration=a_len, reply_to_message_id=rep.message_id
            )
        else:
            await userge.send_voice(
                chat_id=message.chat.id,
                voice=req_file_name,
                duration=a_len
            )
        os.remove(req_file_name)
    except Exception as err:
        await message.edit(err)
