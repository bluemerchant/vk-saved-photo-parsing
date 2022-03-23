import requests
import json
import math
import os

# DO NOT SHARE YOUR TOKENS OR OTHER PRIVATE DATA WITH ANYONE!!!

# you need to create your own app at https://vk.com/apps?act=manage
# how to send request to vk server https://vk.com/dev/first_guide
# use the latest API version https://vk.com/dev/versions

# insert APP_ID into URL below, allow your own app to access your photos, save the ACCESS TOKEN from generated URL (will work only for 24h)
# https://oauth.vk.com/authorize?client_id=PUT_YOUR_APP_ID_HERE&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=photos&response_type=token&v=5.81

access_token = 'ACCESS TOKEN'
owner_id = 'APP ID'

# will write summary data for album with saved photos
def write_json(data):
    with open('photos.json', 'w') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

# get the largest possible size of photo
# return width for horizontal photos and height for vertical photos
def get_largest_size(size_dict):
    if size_dict['width'] >= size_dict['height']:
        return size_dict['width']
    else:
        return size_dict['height']

def download_photo(url):
    r = requests.get(url, stream=True)

    filename = url.split('uniq_tag=')[-1] + '.jpg'

    with open(filename, 'bw') as file:

       for chunk in r.iter_content(4096):
           file.write(chunk)


# see https://vk.com/dev/photos.get
# 'rev': 1 ==> get latest photos first
# 'offset' ==> from which photo (serial number) save will begin (minimum 0)
# 'count' ==> number of photos we want to save (maximum 1000 per request) => each 1000 photos = 1 iteration
# every iteration will be saved individually

def main():
    number_of_saved_photos = requests.get('https://api.vk.com/method/photos.get', params={'owner_id': owner_id, 'v': 5.81, 'access_token': access_token, 'album_id': 'saved'}).json()['response']['count']
    number_of_save_iterations = math.floor(number_of_saved_photos/1000)
    for i in range(number_of_save_iterations+1):
        r = requests.get('https://api.vk.com/method/photos.get', params={'owner_id': owner_id, 'v': 5.81,
                                                                     'access_token': access_token,
                                                                     'album_id': 'saved',
                                                                     'photo_sizes': 1, 'rev': 0,
                                                                     'offset': 1000*i, 'count': 1000})
        write_json(r.json())
        photos = json.load(open('photos.json'))['response']['items']
        os.mkdir(f'vk_saved_photos{i + 1}')
        os.chdir(f'vk_saved_photos{i + 1}')

        for photo in photos:
            sizes = photo["sizes"]

            max_size_url = max(sizes, key=get_largest_size)['url']
            download_photo(max_size_url)
        os.chdir('..')


if __name__ == '__main__':
    main()