import vk_api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

import config
from db_handler.user_handler import UserDb
from models.users import *
from vk_bot import VkTools


class BotVk():
    def __init__(self, community_token, access_token, age=None, sex=None, city=None):

        self.user_id = None
        self.session = None
        self.vk = vk_api.VkApi(token=community_token)
        self.longpoll = VkLongPoll(self.vk)
        self.vk_tools = VkTools(access_token)
        self.params = {}
        self.candidates = []
        self.offset = 0

        

    def message_send(self, user_id, message, attachment=None):
        self.vk.method('messages.send',
                       {'user_id': user_id,
                        'message': message,
                        'attachment': attachment,

                        'random_id': get_random_id()}
                       )

    def event_handler(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text.lower() == 'привет':

                    self.params = self.vk_tools.get_users(event.user_id)
                    self.message_send(
                        event.user_id, f'Привет, {self.params["name"]}')
                elif event.text.lower() == 'поиск':

                    self.message_send(
                        event.user_id, 'Начинаем поиск')
                    if self.candidates:
                        candidate = self.candidates.pop()
                        photos = self.vk_tools.get_photos(candidate['id'])
                        photo_string = ''
                        for photo in photos:
                            photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'
                    else:
                        self.candidates = self.vk_tools.search_candidates(
                            self.params, self.offset)

                        candidate = self.candidates.pop()

                        photos = self.vk_tools.get_photos(candidate['id'])
                        photo_string = ''
                        for photo in photos:
                            photo_string += f'photo{photo["owner_id"]}_{photo["id"]},'
                        self.offset += 50

                    self.message_send(
                        event.user_id,
                        f'имя: {candidate["name"]} ссылка: vk.com/{candidate["id"]}',
                        attachment=photo_string
                    )
                elif event.text.lower() == 'пока':
                    self.message_send(
                        event.user_id, 'До свидание!')
                else:
                    self.message_send(
                        event.user_id, 'Неизвестная команда')


if __name__ == '__main__':
    bot_interface = BotVk(config.community_token, config.access_token)
    bot_interface.event_handler()
    engine = create_engine(
        f'postgresql+psycopg2://{config.USERNAME}:{config.PASSWORD}@localhost'
        f':{config.PORT}/{config.DATABASE}')

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()
