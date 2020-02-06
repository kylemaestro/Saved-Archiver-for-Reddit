#! python3
import urllib.request
import os
import praw
import random
from praw.models import Submission
from praw.models import Comment
from imgurdownloader import ImgurDownloader

# Creates praw instance of Reddit account
reddit = praw.Reddit(client_id='your_id_here', \
                     client_secret='your_secret_here', \
                     user_agent='your_user_agent_here', \
                     username='your_reddit_username_here', \
                     password='your_password_here')

# Downloads image from Imgur using the ImgurDownloader library
def download_from_imgur(link, post):
    MAX_ALBUM_LEN = 20 # only download full albums if >20 total images
    try:
        downloader = ImgurDownloader(link)
        if(downloader.num_images() <= MAX_ALBUM_LEN):
            # Group images by redditor name
            album_name = post.author.name
            downloader.save_images("./images/{}".format(album_name))
    except:
        print("Error saving Imgur image: {}".format(link))

# Downlaods image from URL using urllib
def download_from_url(link, post, ext):
    # Random integer suffix prevents overwriting of multiple images from same author
    try:
        path = "./images/{}{}.{}".format(post.author.name, random.randint(0, 99999), ext)
        urllib.request.urlretrieve(link, path)
    except:
        print("Error saving Reddit image: {}".format(link))

# Saves post title and url to text file and downloads image to /images
def save_post(post):
    title = str(post.title)
    link = str(post.url)

    f.write("POST: {}".format(title))
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
    comment = str(item.body)
    f.write("COMMENT: {}".format(comment))
    f.write('\n\n')

# Archive all present items in account's saved history
def archive_everything():
    saved_stuff = reddit.user.me().saved(limit=None)
    post_count = 0
    comment_count = 0
    last_saved = ""
    try:
        for item in saved_stuff:
            # post #
            if isinstance(item, Submission):
                save_post(item)
                last_saved = "post"
                post_count += 1

            # comment #
            else:
                save_comment(item)
                last_saved = "comment"
                comment_count += 1

            # Print current progress
            if last_saved == "post":
                print("Saved post {}".format(post_count))
            elif last_saved == "comment":
                print("Saved comment {}".format(comment_count))

        print("\nAll items saved")
    except:
        # Always ends in HTTP 500 when end of saved history is reached
        print("\nEnd of saved history reached, all items saved")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Opens output file in write mode
f = open("./saved.txt", "w", encoding="utf-8")

# Saves saved content
archive_everything()
