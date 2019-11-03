#! python3
import praw
from praw.models import Submission
from praw.models import Comment
from imgurdownloader import ImgurDownloader

# Creates praw instance of Reddit account
# Fill in these values with those obtained by
# setting up API script access in app preferences
reddit = praw.Reddit(client_id='<client_id>', \
                     client_secret='<client_secret>', \
                     user_agent='<script_name>', \
                     username='<username>', \
                     password='<password>')

def print_post(post):
    print(post.title)
    print(post.url)

def print_comment(comment):
    print(comment.body)

def archive_saved():
    # Iterates through saved items and records to file
    saved_stuff = reddit.user.me().saved(limit=None)
    post_count = 0
    comment_count = 0
    last_saved = ""
    try:
        for item in saved_stuff:
            # post #
            if isinstance(item, Submission):
                title = str(item.title)
                link = str(item.url)

                f.write("POST: {}".format(title))
                f.write("\nURL: {}".format(link))
                f.write('\n\n')

                post_count = post_count + 1
                last_saved = "post"

                # Downloads Imgur images to /images folder
                MAX_ALBUM_LEN = 20
                if "imgur" in link:
                    try:
                        downloader = ImgurDownloader(link)
                        if(downloader.num_images() <= MAX_ALBUM_LEN):
                            # Group images by redditor name
                            album_name = item.author.name
                            downloader.save_images("./images/{}".format(album_name))
                    except:
                        print("Error saving image: {}".format(link))
            # comment #
            else:
                comment = str(item.body)

                f.write("COMMENT: {}".format(comment))
                f.write('\n\n')

                comment_count = comment_count + 1
                last_saved = "comment"

            # Print current progress
            if last_saved == "post":
                print("Saved post {}".format(post_count))
            elif last_saved == "comment":
                print("Saved comment {}".format(comment_count))

        print("\nAll items saved")
    except:
        # Always ends in HTTP 500 when end of saved history is reached
        print("\nEnd of saved history reached, all items saved")


# Opens output file in write mode
f = open("./saved.txt", "w", encoding="utf-8")

# Saves saved content
archive_saved()
