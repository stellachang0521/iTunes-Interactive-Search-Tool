import requests
import json
import webbrowser



# classes

class Media:

    def __init__(self, title = 'No Title', author = 'No Author', release_year = 'No Release Year', url = 'No URL', json = None):
        if json == None:
            self.title = title
            self.author = author
            self.release_year = release_year
            self.url = url
        else:
            self.title = json['collectionName']
            self.author = json['artistName']
            self.release_year = json['releaseDate'][:4]
            self.url = json['collectionViewUrl']
        
    def info(self):
        return f"{self.title} by {self.author} ({self.release_year})"
        
    def length(self):
        return 0
        
        
class Song(Media):
        
    def __init__(self, title = 'No Title', author = 'No Author', release_year = 'No Release Year', url = 'No URL', album = 'No Album', genre = 'No Genre', track_length = 0, json = None):
        super().__init__(title = 'No Title', author = 'No Author', release_year = 'No Release Year', url = 'No URL', json = None)
        if json == None:
            self.title = title
            self.author = author
            self.release_year = release_year
            self.url = url
            self.album = album
            self.genre = genre
            self.track_length = track_length
        else:
            self.author = json['artistName']
            self.release_year = json['releaseDate'][:4]
            self.title = json['trackName']
            self.url = json['trackViewUrl']
            self.album = json['collectionName']
            self.genre = json['primaryGenreName']
            self.track_length = json['trackTimeMillis']
        
    def info(self):
        return f"{self.title} by {self.author} ({self.release_year}) [{self.genre}]"
        
    def length(self):
        return round(self.track_length * .001)
        
        
class Movie(Media):
    
    def __init__(self, title = 'No Title', author = 'No Author', release_year = 'No Release Year', url = 'No URL', rating = 'No Rating', movie_length = 0, json = None):
        super().__init__(title='No Title', author='No Author', release_year = 'No Release Year', url = 'No URL', json = None)
        if json == None:
            self.title = title
            self.author = author
            self.release_year = release_year
            self.url = url
            self.rating = rating
            self.movie_length = movie_length
        else:
            self.author = json['artistName']
            self.release_year = json['releaseDate'][:4]
            self.title = json['trackName']
            self.url = json['trackViewUrl']
            self.rating = json['contentAdvisoryRating']
            self.movie_length = json['trackTimeMillis']
    
    def info(self):
        return f"{self.title} by {self.author} ({self.release_year}) [{self.rating}]"
    
    def length(self):
        return round((self.movie_length * .001) / 60)
        


# json

def parsing(url):
    response = requests.get(url)
    #print(response.text)
    json_str = response.text
    json_dicts = json.loads(json_str)['results']
    #print(itunes_json)
    #type(itunes_json)

    # parsing through a json dictionary
    songs = []
    movies =[]
    others = []
    for entry in json_dicts:
        if entry['wrapperType'] == 'track':
            if entry['kind'] == 'song':
                songs.append(Song(json = entry))
            elif entry['kind'] == 'feature-movie':
                movies.append(Movie(json = entry))
        else:
            others.append(Media(json = entry))
            
    return songs, movies, others
        
        
def search_term():
    while True:
        parameter = input('\nEnter a search term, or type in "exit" to quit: ')
        if parameter == 'exit':
            return None
        else:
            return f'https://itunes.apple.com/search?term={parameter}'
    

#def input_term(parameter):
#    return f'https://itunes.apple.com/search?term={parameter}'


def create_dict(songs, movies, others):
    ### create dictionary
    media_dict = {}
    count = 0
    print('\nSONGS')
    if len(songs) == 0:
        print('There are no songs!')
    for s in songs:
        count += 1
        media_dict[count] = s
        print(str(count) + ' ' + s.info())
        
    print('\nMOVIES')
    if len(movies) == 0:
        print('There are no movies!')
    for m in movies:
        count += 1
        media_dict[count] = s
        print(str(count) + ' ' + m.info())
        
    print('\nOTHERS')
    if len(others) == 0:
        print('There are no other medias!')
    for o in others:
        count += 1
        media_dict[count] = s
        print(str(count) + ' ' + o.info())
        
    if len(songs)+len(movies)+len(others) == 0:
        print('\nThere are no medias at all!')
        
    return media_dict
    
    
def preview(media_dict):
    while True:
        parameter = input('\nEnter the number of results you hope to preview, or another search term, or exit: ')
        if parameter.isnumeric() and int(parameter) in media_dict.keys():
            parameter = int(parameter)
            return parameter
        elif parameter == 'exit':
            return None
        else:
            return f'https://itunes.apple.com/search?term={parameter}'
    

def print_preview(media_dict, num):
    print(f'\nLaunching\n{media_dict[num].url}\nin web browser......')
    webbrowser.open(media_dict[num].url)



# main code

if __name__ == "__main__":
    state = True
    search_url = search_term()

    if search_url != None:
        songs, movies, others = parsing(search_url)
        media_dict = create_dict(songs, movies, others)
    else:
        print('\nSearch closed.')
        state = False

    while state:
        p = preview(media_dict)
        if p != None:
            if type(p) == int:
                print_preview(media_dict, p)
            else:
                search_url = p

                if search_url != None:
                    songs, movies, others = parsing(search_url)
                    media_dict = create_dict(songs, movies, others)
                else:
                    print('\nSearch closed.')
                    state = False
                    
        else:
            print('\nSearch closed.')
            state = False
    
