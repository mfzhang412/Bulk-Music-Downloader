from pytube import YouTube
from bs4 import BeautifulSoup
import tkinter
from tkinter import filedialog
import requests


def choose():
    """Asks user if they want to download a YouTube video's audio file or an entire YouTube playlist's audio files.
    :return: the user's choice (1 for playlist, 2 for individual, -1 for an invalid option).
    """
    msg = """
    Which would you like to do (enter 1 or 2):
    (1) Playlist: download all the audio files from a YouTube playlist
    (2) Individual: download the audio file from a single YouTube video
    """
    print(msg)
    choice = int(input("").replace('\n','').replace('\t',''))
    if ((choice != 1) and (choice != 2)): return -1    #return -1 if invalid option
    return choice


def askSaveLocation():
    """Brings up dialogue to select folder for saving files.
    :return: the directory path for the save location.
    """
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()     #hide root window
    print("Please select a save location.")
    path = filedialog.askdirectory(parent=root, title='Please select a save location')
    root.destroy()      #destroy root window
    return path


def getPlaylistURLs(playlist_url):  #courtesy of https://gist.github.com/fffaraz/f3dcf48ae93b6c04adb9d74b1de711e5
    """Returns all the video urls and video names in the YouTube playlist.
    :param playlist_url: the YouTube playlist url.
    :return: a list of the video names and video urls from the playlist.
    """
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


def downloadVideoAudio(youtube_url, save_location):
    """Download the highest quality audio stream from the youtube video.
    :param youtube_url: the YouTube URL.
    :param save_location: the directory path for the save location.
    :return: true if song successfully downloaded, false otherwise.
    """
    yt = YouTube(youtube_url)
    try:
        yt.streams.filter(only_audio=True).first().download(save_location)   #downloads the highest quality audio stream and saves to designated folder
        print("Download complete.")
        return True
    except:
        print("---ERROR---" + video_names[i] + "\t\t" + video_urls[i])
        return False


def downloadPlaylistAudio(playlist_url, save_location):    #courtesy of https://github.com/nficano/pytube
    """Download the audio files of all the videos in a playlist.
    :param playlist_url: the YouTube playlist URL.
    :param save_location: the directory path for the save location.
    :return: true if playlist successfully downloaded, false otherwise.
    """
    l = getPlaylistURLs(playlist_url)
    video_names = l[0]
    video_urls = l[1]
    if (len(video_urls) == 0):
        print("Error: possibly invalid URL or playlist is not made public")
        return False
    for i in range(len(video_urls)):
        print("Downloading: " + video_names[i])
        success = downloadVideoAudio(video_urls[i],save_location)
    print("\n\nPlaylist finished downloading!")
    return True


def main():
    """Entry point for program.
    :return: None; breaks out of method if error arises.
    """
    #playlist_url = input("Enter YouTube playlist url: ")
    choice = choose()
    if choice == 1:
        url = input("Enter Youtube playlist url:\n")
    elif choice == 2:
        url = input("Enter YouTube video url:\n")
    else:   #check to see if choice is valid
        print("That is not a valid choice.")
        return
    save_location = askSaveLocation()
    if len(save_location) <= 0:     #check to see if a file path was chosen
        print("Did not choose a save location. Download cancelled. No actions made.")
        return
    try:
        print("Downloading... (this may take awhile)")
        if choice == 1:
            r = downloadPlaylistAudio(url,save_location)
        if choice == 2:
            r = downloadVideoAudio(url,save_location)
            print("\n\nSong finished downloading!")
    except:
        print("Error: possibly invalid URL")


if __name__ == "__main__":
    main()
