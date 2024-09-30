# Importing all necessary libraries
from webscraping import *
from hashtag_network import *



# Boolean variable used for F string condition statement
file_existing = False

while True:
    try:
        with open(captions_file_path) as f:
            file_existing = True
        with open(seenids_file_path) as f:
            file_existing = True
    except FileNotFoundError:
        file_existing = False
        
    script = f'''
Welcome! This program obtains the optimal hashtags to put in your TikTok caption for your videos based on the content that you make.

An internet connection is *REQUIRED* for Step 1.
{'\nDue to files for '+ tagname + ' already existing,' + ' if the files are empty then please run Step 1.' + '\nOtherwise, run Step 2 to calculate your list of hashtags if not done already.' + '\nThere is a list of hashtags in the same directory as the program, if both steps are done.'  if file_existing else ''} 
Enter your choice below:

1) Step 1: Gathering the data for {tagname}
2) Step 2: Calculating the list of hashtags from {tagname} to put in your caption 
3) Quit the program
4) Return to start menu

Enter here: '''
    # 'script' uses a conditional statement within the F string such that if files for the hashtag that was inputted already exists, then write out a message that states that you can just retrieve the list via the text file produced
    try:
        option = int(input(script))
        if option == 1:
            web_scrape(tagname, captions_file_path, seenids_file_path)
        elif option == 2:
            print('TEEEEEEEEEEST')
            try:
                print('ouehrghiuhebrgiubergiuber')
                network_creation(tagname, captions_file_path)
            except FileNotFoundError:
                print(f'Please run Step 1 first with {tagname} as there are no files for this hashtag.')
                wait()
        elif option == 3:
            quit()
        elif option == 4:
            tagname, captions_file_path, seenids_file_path = update_tagname()
        else:
            print('Enter a choice available.')
            continue
    except ValueError:
        print('Enter a number please.')
        continue
        

# enter code to force the user to do the reCAPTCHA test but then before and after the test, disable any possible human interaction with the webdriver tab
# break down tests even further such that the user will enter a hashtag but not search first, and calculate the hashtags etc first
# the updated tagname function does not work properly
# add defensive programming such that if the hashtag entered is nsfw by tiktoks standards, invalidate the use of the hashtag
