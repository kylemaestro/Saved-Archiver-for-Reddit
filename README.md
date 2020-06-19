# Saved Archiver for Reddit
## Introduction
If you're like me, you're constantly clicking 'save' on Reddit to keep interesting content handy for later. Unfortunately, only a combined 1,000 posts *and* comments may be saved at one time. If you've reached this limit, any new content you save will overwrite the oldest item you saved, losing it forever. But fear not! With this script, you can archive all of your saved post urls and comments to a text file for safekeeping. Images hosted on most platforms, including i.redd.it and imgur links (even albums, up to 20 images long) will also be downloaded.

The script uses the Reddit API's OAuth2 to authenticate and get permission to access your saved content, meaning that you don't ever need to input your password. Simply login on your web browser to your Reddit account, run the script, and away you go!

## Known Issues
 * Some i.redd.it images will fail to download
 * Images can be overwritten if another image is encountered with the exact same post title

## Acknowledgements
This script utilizes [PRAW](https://praw.readthedocs.io/en/latest/) to access and make calls to the Reddit API using Python. Portions of code provided [here](https://praw.readthedocs.io/en/latest/tutorials/refresh_token.html#refresh-token) are used to authenticate via the Reddit OAuth2 API service. [Imgur Downloader](https://github.com/jtara1/imgur_downloader) was used to handle the downloading of Imgur links and albums. 
