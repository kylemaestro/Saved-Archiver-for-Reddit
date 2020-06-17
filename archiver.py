#! python3
import urllib.request
import os
import praw
import random
from praw.models import Submission
from praw.models import Comment
from imgurdownloader import ImgurDownloader

# Creates praw instance of Reddit account
reddit = praw.Reddit(client_id='tkaDNC6nObkmIQ', \
                     client_secret='-H5wEpGkEEIO9rgRAkb81p_Y_6Y', \
                     user_agent='Saved Archiver for Reddit', \
                     username='squidwardtoblerone', \
                     password='squidwardtoblerone')

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
    str_comment = str(comment.body)
    f.write("COMMENT: {}".format(str_comment))
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

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Opens output file in write mode
f = open("./saved/saved.txt", "w", encoding="utf-8")

# Saves saved content
archive_everything()
