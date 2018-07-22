from pytube import YouTube
from bs4 import BeautifulSoup
import requests

def getPlaylistURLs(playlist_url):  #courtesy of https://gist.github.com/fffaraz/f3dcf48ae93b6c04adb9d74b1de711e5
    video_names = []
    video_urls = []
    source = requests.get(playlist_url).text
    html = BeautifulSoup(source, 'html.parser')
    domain = 'https://www.youtube.com'
    for link in html.find_all('a',{'dir':'ltr'}):
        href = link.get('href')
        if (href.startswith('/watch?')):
            video_urls.append(domain+href)              #append url links
            video_names.append(link.string.strip())     #append video names
    return [video_names,video_urls]

def downloadAudio(youtube_url):
    """Download the highest quality audio stream from the youtube video"""
    yt = YouTube(youtube_url)
    try:
        yt.streams.filter(only_audio=True).first().download()   #downloads the highest quality audio stream
        return True
    except:
        return False

def downloadPlaylistAudio(playlist_url):    #courtesy of https://github.com/nficano/pytube
    """Download the audio files of all the videos in a playlist"""
    l = getPlaylistURLs(playlist_url)
    video_names = l[0]
    video_urls = l[1]
    for i in range(len(video_names)):
        print("Downloading: " + video_names[i])
        success = downloadAudio(video_urls[i])
        if success: print("Download complete!")
        else: print("---ERROR---" + video_names[i] + "\t\t" + video_urls[i])
    print("\n\nPlaylist finished downloading")
    return True


def main():
    """Main method"""
    playlist_url = 'https://www.youtube.com/playlist?list=PLLKYaQy8XYEz9FlbhzrAF4jvSMvvqab1p'
    r = downloadPlaylistAudio(playlist_url)


if __name__ == "__main__":
    main()
