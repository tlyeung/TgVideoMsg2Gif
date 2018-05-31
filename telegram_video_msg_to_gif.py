from telegram.ext import Updater, MessageHandler, Filters
from moviepy.editor import *
import logging
import datetime


def video_msg(bot, update):
    name = '{}_{}_{}'.format(
        update.message.from_user.first_name, update.message.from_user.last_name,
        datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    update.message.video_note.get_file().download("{}.mp4".format(name))
    logger.info("{} {} sent video".format(
        update.message.from_user.first_name, update.message.from_user.last_name))
    clip = VideoFileClip("{}.mp4".format(name)).crop(x1=35, x2=205, y1=35, y2=205)
    clip.write_gif("{}.gif".format(name))
    bot.send_document(chat_id=update.message.chat_id,
                      document=open("{}.gif".format(name), 'rb'),
                      timeout=180)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    updater = Updater('')
    updater.dispatcher.add_handler(MessageHandler(Filters.text, video_msg))
    updater.dispatcher.add_handler(MessageHandler(Filters.video_note, video_msg))
    updater.start_polling()
    updater.idle()
