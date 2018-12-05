from telegram.ext import Updater, MessageHandler, Filters
from moviepy.editor import *
import logging
import datetime


def text_msg(bot, update):
    update.message.reply_text("Send me a video message and I will reply you a gif!")
    logger.info("{} {} sent text".format(
        update.message.from_user.first_name, update.message.from_user.last_name))


def video_msg(bot, update):
    update.message.reply_text("processing!")
    name = '{}_{}_{}'.format(
        update.message.from_user.first_name, update.message.from_user.last_name,
        datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    update.message.video_note.get_file().download("{}.mp4".format(name))
    logger.info("{} {} sent video".format(
        update.message.from_user.first_name, update.message.from_user.last_name))
    clip = VideoFileClip("{}.mp4".format(name)).crop(x1=35, x2=205, y1=35, y2=205)
    if clip.fps > 40:
        clip.reader.close()
        clip.audio.reader.close_proc()
        update.message.reply_text("This file has problem so cannot make gif!!!")
    else:
        clip.write_videofile("{}-cropped.mp4".format(name), audio=False)
        clip.reader.close()
        clip.audio.reader.close_proc()
        bot.send_animation(chat_id=update.message.chat_id,
                      animation=open("{}-cropped.mp4".format(name), 'rb'),
                      timeout=600)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    updater = Updater('')
    updater.dispatcher.add_handler(MessageHandler(Filters.text, text_msg))
    updater.dispatcher.add_handler(MessageHandler(Filters.video_note, video_msg))
    updater.start_polling(timeout=60)
    updater.idle()
