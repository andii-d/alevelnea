# Importing all necessary libraries
from selenium.common.exceptions import NoSuchWindowException, WebDriverException
from webscraping import *
from hashtag_network import *

# Boolean variable used for F string condition statement
file_existing = False

while True:
    try:
        with open(captions_file_path) as f:
            file_existing = True if (f.readline().strip()) else False
        with open(seenids_file_path) as f:
            file_existing = True if (f.readline().strip()) else False
    except FileNotFoundError or json.JSONDecodeError:
        file_existing = False

    script = f'''
Welcome! This program obtains the optimal hashtags to put in your TikTok caption for your videos based on the content that you make.

An internet connection is *REQUIRED* for Step 1. {'Run this step first please, as ' + tagname + ' it is the first time it has been entered.' if not file_existing else ''}
{(
    'Due to files for ' + tagname + ' already existing,'
    + ' if the files are empty then please run Step 1.' 
    + '\nOtherwise, run Step 2 to calculate your list of hashtags if not done already.'
    + '\nThere is a saved list of hashtags in the same directory as the program, if both steps are done.'
    ) if file_existing else ''}
Enter your choice below:

1) Step 1: Gathering the data for {tagname}
2) Step 2: Calculating the list of hashtags from {tagname} to put in your caption
3) Quit the program
4) Return to start menu
{'5) View the graph of ' + tagname if exists((f'{script_dir}/{tagname}_graph.pdf')) else ''}
Enter here: '''

# 'script' uses conditional statements through the use of f strings to detect existing files 
    try:
        option = int(input(script))
        if option == 1:
            # If there is no ping repsponse from pinging TikTok, invalidate the option being entered
            if not ping_website('www.tiktok.com'):
                print('You must have an internet connection to proceed.')
                wait()
                continue
            else:
                print('Connected to the internet.')
                # If the ping response is valid, run the web scraping function
                try:
                    web_scrape(tagname, captions_file_path, seenids_file_path)
                except (NoSuchWindowException, WebDriverException):
                    print('The WebDriver tab has closed unexpectedly. Please re-run step 1.')
                    wait()
                    continue
        elif option == 2:
            try:
                network_creation(tagname, captions_file_path)
            except FileNotFoundError:
                # If the hashtag entered has no files, then invalidate the option being entered
                print(f'Please run Step 1 first with {tagname} as there are no files/data for this hashtag.')
                wait()
        elif option == 3:
            # Quits the program
            quit()
        elif option == 4:
            # Updates the hashtag entered and its respective file paths for captions and seen IDs
            tagname, captions_file_path, seenids_file_path = update_tagname()
        elif option == 5 and exists((f'{script_dir}/{tagname}_graph.pdf')):
            # Plot the graph for the user to view
            view_graph(tagname, graph=None, top_nodes=None)
        else:
            # If options 1-4 are not entered, remind the user to enter an option within the range
            print('Enter a choice available.')
            continue
    except ValueError:
        # If the option entered is not a number, remind the user to enter a number
        print('Enter a number please.')
        continue
