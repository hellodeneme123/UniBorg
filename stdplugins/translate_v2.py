import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
import emoji
from googletrans import Translator
from uniborg.util import admin_cmd
from mtranslate import translate
from langdetect import detect

@borg.on(admin_cmd(pattern="tr ?(.*)"))
async def trtxxx(message):
        """Translates desired text to whatever language.\n\n
        Example usage:\n.trt <lang> with a replied message"""
        target = (arg_split_with(message, " "))
        if not target:
            await message.edit("<i>Specify the target language.</i>")
            return
        if target and len(target) < 2 and not message.is_reply:
            await message.edit("<i>Specify the text to be translated.</i>")
            return
        reply = await message.get_reply_message()
        text = (
            target[1] if not message.is_reply else
            reply.text)
        target = target[0]
        if reply and not reply.text:
            await message.edit("<i>Babe..Are you okay? You can not translate files you know.</i>")
            return
        await message.edit("<i>Translating...</i>")
        result = translate(text, target, 'auto')
        await message.edit(
                           "<b>Text:</b> <i>{}</i>\n"
                           "<b>Detected Language:</b> <i>{}</i>\n\n"
                           "<b>Translated to:</b>\n<i>{}</i>"
                           .format(text, detect(text), result))



def arg_split_with(message, char):
    args = get_arg(message).split(char)
    for space in args:
        if space.strip() == "":
            args.remove(space)
    return args

def get_arg(message):
    msg = message.raw_text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])