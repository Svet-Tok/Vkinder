from datetime import datetime

import vk_api

from vk_api.exceptions import ApiError

import config
from db_handler.user_handler import UserDb


def _bdate_toyear(bdate):
    user_year = bdate.split('.')[2]
    now = datetime.now().year
    return now - int(user_year)


class VkTools:
    def __init__(self, access_token):

        self.vkapi = vk_api.VkApi(token=access_token)

    def get_users(self, user_id):
        try:
            response, = self.vkapi.method('users.get',
                                          {'user_id': user_id,
                                           'fields': 'city,sex,relation,bdate'
                                           }
                                          )
        except ApiError:
            return 'Нет доступа'

        result = {'name': (response['first_name'] + ' ' + response['last_name']) if
        'first_name' in response and 'last_name' in response else None,
                  'sex': response.get('sex'),
                  'city': response.get('city')['title'] if response.get('city') is not None else None,
                  'year': _bdate_toyear(response.get('bdate'))
                  }
        return result

    def search_candidates(self, params, offset):
        try:
            users = self.vkapi.method('users.search',
                                      {'sort': 1,
                                       'offset': offset,
                                       'sex': 1 if params['sex'] == 2 else 2,
                                       'status': 1,
                                       'age_from': params['year'] - 3,
                                       'age_to': params['year'] + 3,
                                       'has_photo': True,
                                       'count': 50,
                                       'hometown': params['city'],
                                       }
                                      )
        except ApiError as e:
            users = []
            print(f'error = {e}')
        result = [{'name': item['first_name'] + item['last_name'],
                   'id': item['id']
                   } for item in users['items'] if item['is_closed'] is False
                  ]

        return result

    def get_photos(self, id):
        try:
            photos = self.vkapi.method('photos.get',
                                       {'owner_id': id,
                                        'album_id': 'profile',
                                        'extended': 1,

                                        }
                                       )
        except ApiError as e:
            photos = {}
            print(f'error = {e}')

        result = [{'owner_id': item['owner_id'],
                   'id': item['id'],
                   'likes': item['likes']['count'],
                   'comments': item['comments']['count']
                   } for item in photos['items']
                  ]
        return result[:3]

        top_photos = []

        for item in self.sorting_likes(photos):
            top_photos.append(item)
        return top_photos

    @staticmethod
    def sorting_likes(photos):
        top_photos = []
        for photo in photos:
            if photo != ['Нет фото'] and photos != 'Нет доступа':
                top_photos.append(photo)
        return sorted(top_photos, reverse=True)[:3]


if __name__ == '__main__':
    user_id = 888888
    tools = VkTools(config.access_token)
    params = tools.get_users(user_id)
    candidates = tools.search_candidates(params, 20)
    candidate = candidates.pop()
    photos = tools.get_photos(candidate['id'])
