#! python3
import urllib.request
import os
import os.path
import praw
import random
import socket
import sys
import colorama
import time
from praw.models import Submission
from praw.models import Comment
from imgurdownloader import ImgurDownloader
from colorama import init, Fore
from os import path

"""
The following 3 functions were provided by the PRAW docs, located here:
https://praw.readthedocs.io/en/latest/tutorials/refresh_token.html#refresh-token

They create refresh tokens that we can use to authenticate with code flow
"""

def receive_connection():
    """Wait for and then return a connected socket..

    Opens a TCP connection on port 8080, and waits for a single client.

    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("localhost", 8080))
    server.listen(1)
    client = server.accept()[0]
    server.close()
    return client

def send_message(client, message):
    """Send message to client and close the connection."""
    print(message)
    client.send("HTTP/1.1 200 OK\r\n\r\n{}".format(message).encode("utf-8"))
    client.close()

def obtain_token():
    state = str(random.randint(0, 65000)) # exists only to verify our request at the end
    url = reddit.auth.url(scopes, state, "permanent") # this could also be temporary
    print("\nHowdy! Copy and paste this url in your browser to give this application")
    print("permission to access your saved content on Reddit: \n")
    print(Fore.CYAN + url)
    print(Fore.RESET)
    print("Make sure you're already logged in on your browser to the Reddit")
    print("account whose content you'd like to save!")
    print("\nAfter accepting the permission request, the archiver will automatically")
    print("begin downloading your saved content to the /saved folder within this directory\n")
    sys.stdout.flush()

    client = receive_connection()
    data = client.recv(1024).decode("utf-8")
    param_tokens = data.split(" ", 2)[1].split("?", 1)[1].split("&")
    params = {
        key: value for (key, value) in [token.split("=") for token in param_tokens]
    }

    #print("[Debug] param_tokens: {}".format(param_tokens))

    if state != params["state"]:
        send_message(
            client,
            "State mismatch. Expected: {} Received: {}".format(state, params["state"]),
        )
        return 1
    elif "error" in params:
        send_message(client, params["error"])
        return 1

    refresh_token = reddit.auth.authorize(params["code"])
    send_message(client, "Refresh token: {}".format(refresh_token))

    # If this shows your logged in username, it worked!
    #print("[Debug] reddit.user.me(): {}".format(reddit.user.me()))
    print("\nBeginning download of saved content for /u/{}\n".format(reddit.user.me()))

    return 0

# Downloads image from Imgur using the ImgurDownloader library
def download_from_imgur(link, post):
    MAX_ALBUM_LEN = 20 # only download full albums if >20 total images
    try:
        downloader = ImgurDownloader(link)
        if(downloader.num_images() <= MAX_ALBUM_LEN):
            # Group images by redditor name
            album_name = post.author.name
            downloader.save_images("./saved/images/{}".format(album_name))
    except:
        print("Error saving Imgur image: {}".format(link))

# Downlaods image from URL using urllib
def download_from_url(link, post, ext):
    try:
        path = "./saved/images/{}.{}".format(post.title, ext)
        urllib.request.urlretrieve(link, path)
    except:
        print("Error saving Reddit image: {}".format(link))

# Saves post title, body, and url to text file and downloads image to /images
def save_post(post):
    title = str(post.title)
    link = str(post.url)

    if post.is_self == False:
        f.write("POST: {}".format(title))
        f.write("\nURL: {}".format(link))
        f.write('\n\n')
    elif post.is_self == True:
        f.write("POST: {}".format(title))
        f.write("\nBODY: {}".format(post.selftext))
        f.write("\nURL: {}".format(link))
        f.write('\n\n')

    if "imgur" in link:
        download_from_imgur(link, post)
    elif "png" in link:
        download_from_url(link, post, "png")
    elif "jpeg" or "jpg" in link:
        download_from_url(link, post, "jpeg")

# Saves a comment to text file
def save_comment(comment):
    str_comment = str(comment.body)
    f.write("COMMENT: {}".format(str_comment))
    f.write("\nURL: {}".format(comment.permalink))
    f.write('\n\n')

# Archive all present items in account's saved history
def archive_everything():
    saved_stuff = reddit.user.me().saved(limit=None)
    post_count = 0
    comment_count = 0
    last_saved = ""

    for item in saved_stuff:
        # post #
        if isinstance(item, Submission):
            try:
                save_post(item)
                last_saved = "post"
                post_count += 1
            except:
                print("[Error] Could not save submission {}".format(item.id))

        # comment #
        elif isinstance(item, Comment):
            try:
                save_comment(item)
                last_saved = "comment"
                comment_count += 1
            except:
                print("[Error] Could not save comment {}".format(item.id))

        # Print current progress
        if last_saved == "post":
            print("Saved post {}".format(post_count))
        elif last_saved == "comment":
            print("Saved comment {}".format(comment_count))

    print("\nAll items saved")
    time.sleep(3)
    input("Press Enter to exit...")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# For colorama color terminal text setup
init()

# Initialize our request with the script's client information (reddit.com/prefs/apps)
client_id = "tkaDNC6nObkmIQ"
client_secret = "-H5wEpGkEEIO9rgRAkb81p_Y_6Y"
scopes = ["history","identity"]

reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri="http://localhost:8080",
    user_agent="Saved Archiver for Reddit",
)

obtain_token()

if path.exists("./saved") == False:
    os.mkdir("./saved")

# Opens output file in write mode
f = open("./saved/saved.txt", "w", encoding="utf-8")

# Saves saved content
archive_everything()
