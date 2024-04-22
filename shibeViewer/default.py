import xbmc
import xbmcgui
import xbmcplugin
import json
import urllib2
import sys
import urlparse

HANDLE = int(sys.argv[1])

def get_images(animal_type):
    url = "http://shibe.online/api/{animal_type}?count=100&urls=true&httpsUrls=true".format(animal_type=animal_type)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0'
    }
    request = urllib2.Request(url, headers=headers)
    try:
        response = urllib2.urlopen(request)
        image_urls = json.load(response)
        return image_urls
    except urllib2.URLError as e:
        xbmc.log('Error fetching images: {0}'.format(str(e)), xbmc.LOGERROR)
        return []

def add_directory_item(url, title, is_folder=False, thumbnail=''):
    li = xbmcgui.ListItem(title, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
    xbmcplugin.addDirectoryItem(handle=HANDLE, url=url, listitem=li, isFolder=is_folder)

def main():
    xbmcplugin.setContent(HANDLE, 'images')
    args = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)
    animal_type = args.get('animal_type')

    if animal_type:
        animal_type = animal_type[0]  # Extract the animal type from the list
        images = get_images(animal_type)
        # Format title to include animal type and index
        for idx, img_url in enumerate(images, start=1):
            title = '{0} - #{1}'.format(animal_type.capitalize(), idx)
            add_directory_item(img_url, title=title, is_folder=False, thumbnail=img_url)
        xbmcplugin.endOfDirectory(HANDLE)
    else:
        animal_types = {'Shibes': 'shibes', 'Cats': 'cats', 'Birds': 'birds'}
        for title, animal_type in animal_types.items():
            folder_url = '{0}?animal_type={1}'.format(sys.argv[0], animal_type)
            add_directory_item(folder_url, title, is_folder=True)
        xbmcplugin.endOfDirectory(HANDLE)

if __name__ == '__main__':
    main()
