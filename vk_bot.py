from datetime import datetime

import vk_api

from vk_api.exceptions import ApiError

import config


def _bdate_toyear(bdate):
    user_year = bdate.split('.')[2]
    now = datetime.now().year
    return now - int(user_year)


class VkTools:
    def __init__(self, access_token):
        self.vkapi = vk_api.VkApi(token=access_token)

    def get_users(self, users_id):
        try:
            response, = self.vkapi.method('users.get',
                                          {'user_id': users_id,
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

    def get_photos(self, owner_id):
        try:
            photos = self.vkapi.method('photos.get',
                                       {'owner_id': owner_id,
                                        'album_id': 'profile',
                                        'extended': 1
                                        }
                                       )
        except ApiError as e:
            return 'Нет доступа'

        photos_candidate = []

        for i in range(10):
            try:
                photos_candidate.append(
                    [photos['items'][i]['likes']['count'],
                     'photo' + str(photos['items'][i]['owner_id']) + '_' + str(photos['items'][i]['id'])])
            except IndexError:
                photos_candidate.append(['Нет фото'])

        top_photos = []

        for item in self.sorting_likes(photos_candidate):
            top_photos.append(item)
        return top_photos

    @staticmethod
    def sorting_likes(photos_like):
        top_photos = []
        for photo in photos_like:
            if photo != ['Нет фото'] and photos_like != 'Нет доступа':
                top_photos.append(photo)
        return sorted(top_photos, reverse=True)[:3]


if __name__ == '__main__':
    user_id = 8888888
    tools = VkTools(config.access_token)
    params = tools.get_users(user_id)
    candidates = tools.search_candidates(params, 20)
    candidate = candidates.pop()
    photos = tools.get_photos(candidate['id'])
