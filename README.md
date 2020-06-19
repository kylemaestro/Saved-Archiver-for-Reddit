# Saved Archiver for Reddit
## Introduction
If you're like me, you're constantly clicking 'save' on Reddit to keep interesting content handy for later. Unfortunately, only a combined 1,000 posts *and* comments may be saved at one time. If you've reached this limit, any new content you save will overwrite the oldest item you saved, losing it forever. But fear not! With this script, you can archive all of your saved post urls and comments to a text file for safekeeping. Images hosted on most platforms, including i.redd.it and imgur links (even albums, up to 20 images long) will also be downloaded.

The script uses the Reddit API's OAuth2 to authenticate and get permission to access your saved content, meaning that you don't ever need to input your password. Simply login on your web browser to your Reddit account, run the script, and away you go!

## Known Issues
 * Some i.redd.it images will fail to download
 * Images can be overwritten if another image is encountered with the exact same post title

## How to Use
First, open up a web browser of your choice and navigate to reddit.com. Log in to your Reddit account as normal. Next, double-click "start.bat" to start the script. It will ask you to copy and paste a url into the same browser you're logged into Reddit on. Reddit will then ask you to give the script permission to access your saved content and username. *Any other information, including your password, submissions, comments, etc will not and cannot be accessed by the script in any way whatsoever*.

After you've granted the script the permissions it needs, a blank page showing your *refresh token* will be shown. This page can be safely closed, it is not needed to proceed. The archiver will automatically begin downloading your saved content, writing the post titles and urls as well as full comments to "/saved/saved.txt". Images will be downloaded to the "/saved/images/" folder. Imgur albums will be grouped in folders with the Reddit username of the submitter as the folder name.

For accounts with large amounts of saved content, the download process could take some time. When the script has completed, the console will print "All items saved". At this point, it is safe to close the console window as the download process is complete.

## Acknowledgements
This script utilizes [PRAW](https://praw.readthedocs.io/en/latest/) to access and make calls to the Reddit API using Python. Portions of code provided [here](https://praw.readthedocs.io/en/latest/tutorials/refresh_token.html#refresh-token) are used to authenticate via the Reddit OAuth2 API service. [Imgur Downloader](https://github.com/jtara1/imgur_downloader) was used to handle the downloading of Imgur links and albums.
