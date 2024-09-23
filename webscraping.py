# Importing all necessary libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from os.path import abspath, dirname, exists, join
from os import chmod
import os
import platform
import re
import time
import json

# Generates the file path from the program itself to ensure no accidental file creations are placed elsewhere
script_dir = dirname(abspath(__file__)) 


'''
# Construct the file paths
hashtag_filename_captions = f'{tagname}captions.json'
hashtag_filename_seenids = f'{tagname}seenids.json'
captions_file_path = join(script_dir, hashtag_filename_captions)
seenids_file_path = join(script_dir, hashtag_filename_seenids)
'''

# Subroutine to wait before the next step loads, ensuring that each step of the program is run correctly
def wait():
        x = input('Press Enter')

def show_popup(message, title="TikTok Reminder"):
    os_type = platform.system()

    if os_type == "Windows":
        # Windows: Use PowerShell to create a pop-up message box
        os.system(f'powershell -command "Add-Type -AssemblyName Microsoft.VisualBasic; [Microsoft.VisualBasic.Interaction]::MsgBox(\'{message}\', 0, \'{title}\')"')

    elif os_type == "Darwin":
        # macOS: Use AppleScript via osascript
        os.system(f'osascript -e \'display alert "{title}" message "{message}"\'')

        
def entering_desired_hashtag():
    while True:
        try:
            options = int(input('1) Enter your hashtag\n2) Quit \nEnter here: '))
            if options == 1:
                desired_hashtag = input('Please enter the hashtag you wish to search (with the # symbol as well): ')
                if re.match(r'^#\s*$', desired_hashtag): # Regex to check if it's only '#' or '#' followed by whitespace
                    print('Invalid tag. Hashtag must not be just the symbol itself or followed by only whitespace.')
                    continue
                elif not desired_hashtag.startswith('#'):  # Ensure the hashtag starts with '#'
                    print('Invalid tag. Hashtag must start with #.')
                    continue
                else:
                    return desired_hashtag  # Return valid hashtag
            elif options == 2:
                quit() # Quits the program
            else:
                print('\nEnter a valid option.\n')
        except ValueError:
            print('\nEnter a number of an option.\n') # Ask user to enter a number if the input isn't an integer

def web_scrape(tagname, captions_file_path, seenids_file_path):
    
    def nsfw_hashtag():
        try:
            nsfw_guidelines_element = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div[2]/div/p')
            nsfw_guidelines_text = nsfw_guidelines_element.text
            if 'Community Guidelines' in nsfw_guidelines_text:
                print(f"The hashtag {tagname} does not comply with TikTok's guidelines and cannot be searched up for data.\nPlease choose a different hashtag. ")
                wait()
                tagname = entering_desired_hashtag()
        
        except NoSuchElementException:
            pass
        
    def background_check_captcha_element():
        try:
            captcha_element = driver.find_element(By.XPATH, '/html/body/div[7]/div/div[1]/div[1]/a')
            show_popup('Please check the TikTok page to complete the CAPTCHA test, to continue your data gathering.', 'COMPLETE CAPTCHA IMAGE TEST ON TIKTOK')

        except NoSuchElementException:
            pass
    
    print('IMPORTANT: Every time a "Press Enter" prompt appears, please check to see if TikTok is making you perform a reCAPTCHA test.\nPlease do not touch the WebDriver tab at all unless the prompt is required to be completed, as this will break the program.')
    
    wait()  

    driver = webdriver.Chrome()
    # Load the search engine browser
    # We can change the search engine to Chrome, Firefox, etc

    driver.get("https://www.tiktok.com")
    # Load the TikTok page

    # The cookies of the placeholder TikTok account made for this program (strictly used only for the function of this program)
    
    # If pasting the cookies of a different TikTok account using web extensions into this variable, you must change the value of 'sameSite' to either 'Lax', 'Strict' or 'None's
    cookies = [
    {
        "domain": ".tiktok.com",
        "expirationDate": 1711410247.940897,
        "hostOnly": False,
        "httpOnly": True,
        "name": "ak_bmsc",
        "path": "/",
        "sameSite": "None",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "81A8FC08D156E0732154F1C1D154FC10~000000000000000000000000000000~YAAQP+44F0tUdHGOAQAADRySdxdIqCx8UKhb2bFg35hrw4hmaNYfp19zuo5qvbf08pHMkh9bErmmsF02wtaH4wGglhHoVJlkm6YG50pHGy2KGlAElp7VstGj/VBAFfRRqKxKg5b92DfEuhN4buFYbMUgEee+fR/O2UQHJLtAKx0fobiYe1L+20TH5bpMuO5FnIR7B3UrdDwTULj5XMz2qyo+zf/OEdviwNkO+mZ43obF0nU/iwB51gU2ITGZQx3AZWSzg9wugfml4VIuE2W7ZmBGbi+6UKOdCl/VWN7+4BLeDm0EVVtsAk3m7RiMO+7eg/TmzldbuXQN7T4FlNUlSsq6B7cSsUBGBHv0aklekdmioGF0io/uy5ZaefWmh6TnCzPwNP6jQp4=",
        "id": 1
    },
    {
        "domain": ".tiktok.com",
        "expirationDate": 1711410248.129629,
        "hostOnly": False,
        "httpOnly": False,
        "name": "bm_sv",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "EAB75E3B221521E62A4B4260353E3471~YAAQP+44F3xUdHGOAQAAbKmSdxcfBg+jNohqnVoi+FH4uxJoh2ehwZKv7zFAno4H6M+lwhFuo1gKfTxkobR1y7o0COlWhviUX68flo6dvvQrPlEda9wKDvrul5cPURKiUNtbjeZFpQsxpt+Ob3mb+pMRQcHzOoZS8HYqbr5fq+N6hJk/+pe5zhr01ywIGKDyYILV1Vc74JpF9MCuHd63Uy3Wfe6VhhbQ1Uf3E6leLnfP8o/CWiuxenaLHUGRI1E9~1",
        "id": 2
    },
    {
        "domain": ".tiktok.com",
        "expirationDate": 1716587082.188543,
        "hostOnly": False,
        "httpOnly": True,
        "name": "cmpl_token",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "AgQQAPOYF-RO0rWe7N_5Yd0Z_GBpPwLbP6MTYNCjjA",
        "id": 3
    },
    {
        "domain": ".tiktok.com",
        "expirationDate": 1745099053,
        "hostOnly": False,
        "httpOnly": False,
        "name": "cookie-consent",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "{%22ga%22:True%2C%22af%22:True%2C%22fbp%22:True%2C%22lip%22:True%2C%22bing%22:True%2C%22ttads%22:True%2C%22reddit%22:True%2C%22hubspot%22:True%2C%22version%22:%22v10%22}",
        "id": 4
    },
    {
        "domain": ".tiktok.com",
        "expirationDate": 1712267096.481687,
        "hostOnly": False,
        "httpOnly": False,
        "name": "msToken",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "8BTLLKkt73zlVJ3TdEWp_HCZUDos2_tIrrFvg7w7Fi0QdJkLD1V6p-pHBATJwTymi4jiGKBv9xG2FDn2hlRgbK07Os-n8c-6lsMlu2OMkvvQMM2wByxJ-sGv3MI-q0OGOfPctqnmI0OMa8qn",
        "id": 5
    },
    {
        "domain": ".tiktok.com",
        "expirationDate": 1716587082.188494,
        "hostOnly": False,
        "httpOnly": True,
        "name": "multi_sids",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "7322855710425023520%3Ac57015c75d069ba9e5ec4ee47864320c",
        "id": 6
    },
    {
        "domain": ".tiktok.com",
        "expirationDate": 1742939085.697279,
        "hostOnly": False,
        "httpOnly": True,
        "name": "odin_tt",
        "path": "/",
        "sameSite": "None",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "4033e10750123e5ce51b6061fd3d7f75c457c88952fad51995ff4c95c0525b072a0642b71f735b44e2894fedf983e6b35b132ff423136eceecf8790c3f98057132462ae88b68b64a1d4e847369106582",
        "id": 7
    },
    {
        "domain": ".tiktok.com",
        "expirationDate": 1716587049.96529,
        "hostOnly": False,
        "httpOnly": False,
        "name": "passport_csrf_token",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "bd63a896477aece35ce96db125676542",
        "id": 8
    },
    {
        "domain": ".tiktok.com",
        "expirationDate": 1716587049.965335,
        "hostOnly": False,
        "httpOnly": False,
        "name": "passport_csrf_token_default",
        "path": "/",
        "sameSite": "None",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "bd63a896477aece35ce96db125676542",
        "id": 9
    },
    {
        "domain": ".tiktok.com",
        "hostOnly": False,
        "httpOnly": False,
        "name": "s_v_web_id",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "session": True,
        "storeId": "0",
        "value": "verify_lu7h6vyr_V3sZnYa9_GGMo_4012_Awsq_h4F4IPvv2B7t",
        "id": 10
    },
    {
        "domain": ".tiktok.com",
        "expirationDate": 1726955082.188585,
        "hostOnly": False,
        "httpOnly": True,
        "name": "sessionid",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "c57015c75d069ba9e5ec4ee47864320c",
        "id": 11
    },
    {
        "domain": ".tiktok.com",
        "expirationDate": 1726955082.188592,
        "hostOnly": False,
        "httpOnly": True,
        "name": "sessionid_ss",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "c57015c75d069ba9e5ec4ee47864320c",
        "id": 12
    },
    {
        "domain": ".tiktok.com",
        "expirationDate": 1742507082.18856,
        "hostOnly": False,
        "httpOnly": True,
        "name": "sid_guard",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "c57015c75d069ba9e5ec4ee47864320c%7C1711403082%7C15552000%7CSat%2C+21-Sep-2024+21%3A44%3A42+GMT",
        "id": 13
    },
    {
        "domain": ".tiktok.com",
        "expirationDate": 1726955082.188579,
        "hostOnly": False,
        "httpOnly": True,
        "name": "sid_tt",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "c57015c75d069ba9e5ec4ee47864320c",
        "id": 14
    },
    {
        "domain": ".tiktok.com",
        "expirationDate": 1726955082.188598,
        "hostOnly": False,
        "httpOnly": True,
        "name": "sid_ucp_v1",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "1.0.0-KDZlMGNiYTNhMjZkOWY3NjgxZjRkMTVhNTJjZjAzYjAyY2ZkOWJmM2MKIAigiMyKh8-A0GUQyuCHsAYYswsgDDCmhYCtBjgEQOoHEAUaCHVzZWFzdDJhIiBjNTcwMTVjNzVkMDY5YmE5ZTVlYzRlZTQ3ODY0MzIwYw",
        "id": 15
    },
    {
        "domain": ".tiktok.com",
        "expirationDate": 1726955082.188605,
        "hostOnly": False,
        "httpOnly": True,
        "name": "ssid_ucp_v1",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "1.0.0-KDZlMGNiYTNhMjZkOWY3NjgxZjRkMTVhNTJjZjAzYjAyY2ZkOWJmM2MKIAigiMyKh8-A0GUQyuCHsAYYswsgDDCmhYCtBjgEQOoHEAUaCHVzZWFzdDJhIiBjNTcwMTVjNzVkMDY5YmE5ZTVlYzRlZTQ3ODY0MzIwYw",
        "id": 16
    },
    {
        "domain": ".tiktok.com",
        "expirationDate": 1726955082.890151,
        "hostOnly": False,
        "httpOnly": True,
        "name": "store-country-code",
        "path": "/",
        "sameSite": "None",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "gb",
        "id": 17
    },
    {
        "domain": ".tiktok.com",
        "expirationDate": 1726955082.89016,
        "hostOnly": False,
        "httpOnly": True,
        "name": "store-country-code-src",
        "path": "/",
        "sameSite": "None",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "uid",
        "id": 18
    },
    {
        "domain": ".tiktok.com",
        "expirationDate": 1726955082.890139,
        "hostOnly": False,
        "httpOnly": True,
        "name": "store-idc",
        "path": "/",
        "sameSite": "None",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "useast2a",
        "id": 19
    },
    {
        "domain": ".tiktok.com",
        "expirationDate": 1726955084.129576,
        "hostOnly": False,
        "httpOnly": True,
        "name": "tt_chain_token",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "jZFyHA9j9GTHzWHXcwqyJg==",
        "id": 20
    },
    {
        "domain": ".tiktok.com",
        "hostOnly": False,
        "httpOnly": True,
        "name": "tt_csrf_token",
        "path": "/",
        "sameSite": "Lax",
        "secure": True,
        "session": True,
        "storeId": "0",
        "value": "hYnXbFH5-qS57O30-cRLK1wX07MFEe6k6orQ",
        "id": 21
    },
    {
        "domain": ".tiktok.com",
        "expirationDate": 1726955082.890169,
        "hostOnly": False,
        "httpOnly": True,
        "name": "tt-target-idc",
        "path": "/",
        "sameSite": "None",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "useast2a",
        "id": 22
    },
    {
        "domain": ".tiktok.com",
        "expirationDate": 1742939082.556328,
        "hostOnly": False,
        "httpOnly": True,
        "name": "tt-target-idc-sign",
        "path": "/",
        "sameSite": "None",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "MwoQV_Ne4XD7qlL0w2jZpiq-7iI-ha16tLXS7gpK54x3Q5rNPJXlQCQm5TvsuLR_8zCwHpdqjDySLc_PeIkRGoiUYNwj3rQ9tLCJTQL4cbipKtg8JMCQmBDuFXnRMTfX1M1d25MoPGGArKwNE9uWVK3RPFcz7gSuwvSG__Wj3dcgpYqdH0m_30ZuYRSacMIgH4V4EXIol20J40JUdGgyGSh2icB72LZjNurp1ulL8ld9Hcl2JgpOgNKKDx2qYxF5L7QPE3EvtqlwX5HD-bQzfqcTpG56nN-mlM9x1XjNhX6n9nSLmSMTDdy6PUruyeVKf1IBbvA3fv1lVXDe_rjiMAoW05VvTqpzMulB50xWDYxwhQwiiioACcXZoFpOqugXLdXlE-Y-fvAvFSCd6QR1oipJe9fQ8TQ_7oxkGfpMG01F39BK7JOXdK_7E3g2UVixyo3eXoSjXtKHzGwwfXgcu8sFdqgml84kb-aKtWFK5i7D-2c38wMlt7F79qRe_2Se",
        "id": 23
    },
    {
        "domain": ".tiktok.com",
        "expirationDate": 1742939084.816002,
        "hostOnly": False,
        "httpOnly": True,
        "name": "ttwid",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "1%7CUNh-Srvn4rKSQZenI_1KlWxwCI_FZc7qsnRTL7mBRIU%7C1711403084%7C43f5422fceb0f3e15391ce4078fedaeea8ace64fb1678273dffb76addc52ce8b",
        "id": 24
    },
    {
        "domain": ".tiktok.com",
        "expirationDate": 1726955082.188567,
        "hostOnly": False,
        "httpOnly": True,
        "name": "uid_tt",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "7a92940912acb965113b3b8bb26593cf9b0adc6da951368e05bffac6ae7ede97",
        "id": 25
    },
    {
        "domain": ".tiktok.com",
        "expirationDate": 1726955082.188573,
        "hostOnly": False,
        "httpOnly": True,
        "name": "uid_tt_ss",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "7a92940912acb965113b3b8bb26593cf9b0adc6da951368e05bffac6ae7ede97",
        "id": 26
    },
    {
        "domain": ".www.tiktok.com",
        "hostOnly": False,
        "httpOnly": False,
        "name": "passport_fe_beating_status",
        "path": "/",
        "sameSite": "None",
        "secure": False,
        "session": True,
        "storeId": "0",
        "value": "True",
        "id": 27
    },
    {
        "domain": ".www.tiktok.com",
        "expirationDate": 1711835053,
        "hostOnly": False,
        "httpOnly": False,
        "name": "perf_feed_cache",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "{%22expireTimestamp%22:1711573200000%2C%22itemIds%22:[%227320940160982535456%22%2C%227330512782397345044%22%2C%227321343158913125665%22]}",
        "id": 28
    },
    {
        "domain": ".www.tiktok.com",
        "expirationDate": 1737323084,
        "hostOnly": False,
        "httpOnly": False,
        "name": "tiktok_webapp_theme",
        "path": "/",
        "sameSite": "None",
        "secure": True,
        "session": False,
        "storeId": "0",
        "value": "light",
        "id": 29
    },
    {
        "domain": "www.tiktok.com",
        "expirationDate": 1719179082,
        "hostOnly": True,
        "httpOnly": False,
        "name": "last_login_method",
        "path": "/",
        "sameSite": "None",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "handle",
        "id": 30
    },
    {
        "domain": "www.tiktok.com",
        "expirationDate": 1719179096,
        "hostOnly": True,
        "httpOnly": False,
        "name": "msToken",
        "path": "/",
        "sameSite": "None",
        "secure": False,
        "session": False,
        "storeId": "0",
        "value": "8BTLLKkt73zlVJ3TdEWp_HCZUDos2_tIrrFvg7w7Fi0QdJkLD1V6p-pHBATJwTymi4jiGKBv9xG2FDn2hlRgbK07Os-n8c-6lsMlu2OMkvvQMM2wByxJ-sGv3MI-q0OGOfPctqnmI0OMa8qn",
        "id": 31
    }
    ]
    
    # Load the account's cookies into the browser
    for cookie in cookies:
        driver.add_cookie(cookie)
    
    wait()
    
    driver.refresh()
    # After having refreshed the page, your WebDriver instance should have logged into the account
    background_check_captcha_element()
    wait()
    
    # To find the search button, we will use the find_element function to insert the target hashtag
    search_bar = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[2]/div/form/input')
    # Enter the desired hashtag
    search_bar.send_keys(tagname)
    search_bar.send_keys(Keys.ENTER)
    
    background_check_captcha_element()
    wait()
    
    # Filtering the feed to only show videos 
    video_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div')
    video_button.click()

    nsfw_hashtag()
    background_check_captcha_element()
    wait()

    # Loading all the captions from the file
    with open(captions_file_path) as f:
        first_line = f.readline().strip()  # Read the first line and remove any leading/trailing whitespace
        if not first_line:
            print("The file is empty.")
            tags = list()
        else:
            f.seek(0)  # Reset file pointer to the beginning
            tags = list(json.load(f))

    wait()

    # Loading the seen video IDs from the file
    with open(seenids_file_path) as f:
        first_line = f.readline().strip()  # Read the first line and remove any leading/trailing whitespace
        if not first_line:
            print("The file is empty.")
            seen_ids = set()
        else:
            f.seek(0)  # Reset file pointer to the beginning
            seen_ids = set(json.load(f))
        
    wait()
    
    # Locate the element of the video tab itself which contains the video element objects
    resultsTab = driver.find_element(By.ID, 'tabs-0-panel-search_video')

    background_check_captcha_element()
    wait()

    # Gather all the videos by their individual elements
    postsTab = resultsTab.find_elements(By.CLASS_NAME, 'e19c29qe10')
    postsTabSize = len(postsTab)
    
    background_check_captcha_element()
    wait()

    while True: 
        # Scrolls to the bottom of the page automatically
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5) # Every 5 seconds, gather all the video objects currently loaded
        postsTab = resultsTab.find_elements(By.CLASS_NAME, 'e19c29qe10')
        if len(postsTab) == postsTabSize: # If the size of the current posts loaded is the same as the amount of all the posts together, break out the loop
            break
        else:
            postsTabSize = len(postsTab) # Update the current amount of videos found under the hashtag
    
    wait()
    
    # '/html/body/div[7]/div/div[1]/div[1]/a' is the captcha name button
    # Iterate through each post found
    for post in postsTab:
        # Obtain the link of every post found 
        postsTabClassName = post.find_element(By.CLASS_NAME, "e1cg0wnj1")
        postsTabID = postsTabClassName.find_element(By.TAG_NAME, "a")
        postsTabID = postsTabID.get_attribute("href")

        if postsTabID in seen_ids:
            continue
        # Add the unseen ID to all seen IDs
        seen_ids.add(postsTabID)

        # Create a list of hashtags per caption in video
        postCaptions = []
        # Locate the caption via all anchor elements
        postcaptionClassName = post.find_element(By.CLASS_NAME, "ejg0rhn0")
        postcaption = postcaptionClassName.find_elements(By.TAG_NAME, "a")

        # Obtain each hashtag in each post's caption
        for tag in postcaption:
            hashtag = tag.get_attribute("href")
            # Eliminate any instances where the caption contains a link or an @ to someone's account
            if '@' in hashtag.replace('https://www.tiktok.com/tag/', ''):
                continue
            # Add only the word of the hashtag to videoCaptions
            postCaptions.append(hashtag.replace('https://www.tiktok.com/tag/', ''))

        # Eliminate any single hashtag captions
        if len(postCaptions)  <= 1:
            continue
        
        # Filter the captions to have no duplicates and be all lowercase
        postCaptions = list(dict.fromkeys(postCaptions))
        postCaptions = [hashtag.lower() for hashtag in postCaptions]

        # Append them to the total list of all captions
        tags.append(postCaptions)
        
    wait()
    
    with open(captions_file_path, 'a') as a:
        json.dump(tags, a)

    with open(seenids_file_path, 'a') as b:
        # Convert to list
        json.dump(list(seen_ids), b)