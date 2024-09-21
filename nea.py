# Importing all necessary libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from collections import Counter
from scipy.stats import linregress
from matplotlib.ticker import FuncFormatter
from os.path import abspath, dirname, exists, join
from os import chmod
from tqdm import tqdm
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import os
import platform
import re
import time
import json

# Boolean variables used for F string condition statements 
file_existing = False
test_var = False

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

    elif os_type == "Linux":
        # Linux: Use zenity to create a pop-up (requires zenity to be installed)
        zenity_exists = os.system('which zenity > /dev/null 2>&1') == 0
        if zenity_exists:
            os.system(f'zenity --info --text="{message}" --title="{title}"')
        else:
            print(f"Error: 'zenity' not found. Please install zenity or use another pop-up method.")
    else:
        print(f"Unsupported OS: {os_type}")

def entering_desired_hashtag():
    while True:
        try:
            options = int(input('1) Enter your hashtag\n2) Quit \nEnter here: '))
            if options == 1:
                desired_hashtag = input('Please enter the hashtag you wish to search (with the # symbol as well): ')
                if re.match(r'^#\s*$', desired_hashtag): # Regex to check if it's only '#' or '#' followed by whitespace
                    print('Invalid tag. Hashtag must not be just the symbol itself or followed by only whitespace.')
                elif not desired_hashtag.startswith('#'):  # Ensure the hashtag starts with '#'
                    print('Invalid tag. Hashtag must start with #.')
                else:
                    return desired_hashtag  # Return valid hashtag
            elif options == 2:
                quit() # Quits the program
            else:
                print('\nEnter a valid option.\n')
        except ValueError:
            print('\nEnter a number of an option.\n') # Ask user to enter a number if the input isn't an integer

tagname = entering_desired_hashtag()
tagname_dupe_test = tagname



# Generates the file path from the program itself to ensure no accidental file creations are placed elsewhere
script_dir = dirname(abspath(__file__)) 

# Construct the file paths
hashtag_filename_captions = f'{tagname}captions.json'
hashtag_filename_seenids = f'{tagname}seenids.json'
captions_file_path = join(script_dir, hashtag_filename_captions)
seenids_file_path = join(script_dir, hashtag_filename_seenids)

def captions_seenids(desired_hashtag):
    global file_existing
    print(f'Received hashtag: {desired_hashtag}')
    # Check if the file already exists
    if exists(captions_file_path):
        print(f'A file for the hashtag "{desired_hashtag}" already exists. So, existing captions and seen IDs may be skipped when scraping.')
        file_existing = True
    else:
        try:    
            with open(captions_file_path, 'w') as f:
                pass  # Create the file emptily 
        except Exception as e:
            print(f"An error occurred: {e}")
    
    # Check if the file already exists
    if exists(seenids_file_path):
        print(f'A file for the hashtag "{desired_hashtag}" already exists. So, existing captions and seen IDs may be skipped when scraping.')
        file_existing = True
    else:
        try:    
            with open(seenids_file_path, 'w') as f:
                pass  # Create the file emptily
        except Exception as e:
            print(f"An error occurred: {e}")

captions_seenids(tagname) 

def web_scrape():
    
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
    
    
    wait()
    
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
    
    if test_var == False:
        test_var = True

def network_creation():

    with open(captions_file_path) as f:
        captions = json.load(f) 
        
    # Create a NetworkX graph
    hashtag_graph = nx.Graph()
    
    wait()
    
    # Process captions to create the hashtag graph
    for caption in captions:
        # Gather each pair of hashtags in a caption
        for i in range(len(caption)):
            for j in range(i + 1, len(caption)):
                tag1, tag2 = caption[i], caption[j]

                # If a connection between 2 hashtags already exists, increment the edge weight
                if hashtag_graph.has_edge(tag1, tag2):
                    hashtag_graph[tag1][tag2]['weight'] += 1
                else:
                    hashtag_graph.add_edge(tag1, tag2, weight=1) # If a connection between 2 hashtags does not exist, set their edge weight to 1

    wait()


    main_node = f'{tagname}'[1:]
    hashtag_graph.remove_node(main_node) # Remove the hashtag that was searched from the graph (as it will be #1 anyway due to it being the hashtag every video will contain, so it will be pointless to mention)

    wait()

    # Extract the largest connected component
    hashtag_graph = hashtag_graph.subgraph(max(nx.connected_components(hashtag_graph), key=len))


    n = hashtag_graph.number_of_nodes()
    e = hashtag_graph.number_of_edges()

    # Map node labels to integer indices
    label_to_index = {label: idx for idx, label in enumerate(hashtag_graph.nodes())}
    index_to_label = {idx: label for label, idx in label_to_index.items()}

    # Create an adjacency matrix using integer indices
    n = len(label_to_index)
    adj_matrix = np.zeros((n, n))

    # Add progress bar for adjacency matrix creation
    for u, v in tqdm(hashtag_graph.edges(), desc="Creating Adjacency Matrix", unit="edge", total=e):
        i, j = label_to_index[u], label_to_index[v]
        adj_matrix[i, j] = adj_matrix[j, i] = 1  # Assuming undirected graph

    # Calculate centrality values
    def calculate_betweenness_centrality(adj_matrix):
        n = adj_matrix.shape[0]
        betweenness = {i: 0.0 for i in range(n)}

        # Progress bar for betweenness calculation
        for s in tqdm(range(n), desc="Calculating Betweenness Centrality", unit="node", total=n):
            stack = []
            predecessors = [[] for _ in range(n)]
            sigma = np.zeros(n)
            sigma[s] = 1
            dist = -np.ones(n)
            dist[s] = 0
            queue = [s]

            while queue:
                v = queue.pop(0)
                stack.append(v)
                for w in range(n):
                    if adj_matrix[v, w] > 0:
                        if dist[w] < 0:
                            queue.append(w)
                            dist[w] = dist[v] + 1
                        if dist[w] == dist[v] + 1:
                            sigma[w] += sigma[v]
                            predecessors[w].append(v)

            delta = np.zeros(n)
            while stack:
                w = stack.pop()
                for v in predecessors[w]:
                    delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
                if w != s:
                    betweenness[w] += delta[w]

        betweenness = {node: bc / 2 for node, bc in betweenness.items()}
        return betweenness

    def calculate_closeness_centrality(adj_matrix):
        n = adj_matrix.shape[0]
        closeness = {i: 0.0 for i in range(n)}

        # Progress bar for closeness calculation
        for i in tqdm(range(n), desc="Calculating Closeness Centrality", unit="node", total=n):
            shortest_paths = np.full(n, np.inf)
            shortest_paths[i] = 0
            visited = np.zeros(n, dtype=bool)
            queue = [i]

            while queue:
                v = queue.pop(0)
                visited[v] = True
                for w in range(n):
                    if adj_matrix[v, w] > 0 and not visited[w]:
                        new_dist = shortest_paths[v] + 1
                        if new_dist < shortest_paths[w]:
                            shortest_paths[w] = new_dist
                            queue.append(w)

            sum_distances = np.sum(shortest_paths[shortest_paths != np.inf])
            if sum_distances > 0:
                closeness[i] = (n - 1) / sum_distances

        return closeness

    # Calculate centrality measures with progress tracking in the functions
    betweenness_centrality = calculate_betweenness_centrality(adj_matrix)
    closeness_centrality = calculate_closeness_centrality(adj_matrix)
    eigenvector_centrality = nx.eigenvector_centrality(hashtag_graph)
    weighted_eigenvector = nx.eigenvector_centrality(hashtag_graph, weight='weight')

    # Map results back to original labels
    betweenness_centrality = {index_to_label[i]: bc for i, bc in betweenness_centrality.items()}
    closeness_centrality = {index_to_label[i]: cc for i, cc in closeness_centrality.items()}


    # Sort and get the top 20 highest betweenness centrality nodes
    top_20_betweenness = [node for node, _ in sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:20]]

    # Sort and get the top 20 highest closeness centrality nodes
    top_20_closeness = [node for node, _ in sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:20]]
    
    # Sort and get the top 20 highest eigenvector centrality nodes
    top_20_eigenvector = [node for node, _ in sorted(eigenvector_centrality.items(), key=lambda x: x[1], reverse=True)[:20]]
    
    # Sort and get the top 20 highest eigenvector centrality nodes (weighted)
    top_20_eigen_weighted = [node for node, _ in sorted(weighted_eigenvector.items(), key=lambda x: x[1], reverse=True)[:20]]

    # Get degree and weighted degree and sort to get the top 20 nodes for each
    node_degrees = hashtag_graph.degree()
    top_20_degrees = [node for node, _ in sorted(node_degrees, key=lambda x: x[1], reverse=True)[:20]]

    weighted_node_degrees = hashtag_graph.degree(weight='weight')
    top_20_weighted_degrees = [node for node, _ in sorted(weighted_node_degrees, key=lambda x: x[1], reverse=True)[:20]]

    # Combine all the top 20 lists of hashtags to get an average list based on number of occurences of a node appearing in the list
    all_nodes = top_20_betweenness + top_20_closeness + top_20_degrees + top_20_weighted_degrees + top_20_eigenvector + top_20_eigen_weighted

    # Count occurrences of each node across the combined list
    node_occurrences = {}
    for node in all_nodes:
        if node in node_occurrences:
            node_occurrences[node] += 1
        else:
            node_occurrences[node] = 1

    # Sort nodes by their frequency of occurrence and get the top 20 most frequent nodes
    top_20_nodes_overall = sorted(node_occurrences.keys(), key=lambda x: node_occurrences[x], reverse=True)[:20]

    while True:
        export_to_gephi = input('Would you like to export to Gephi?\nEnter Y/N: ').lower()
        if export_to_gephi == 'y':
            nx.write_gexf(hashtag_graph, f'{script_dir}/{tagname}graph.gexf')  # Creates a .gexf file to view in network graphing software
            print('Exported!')
            break
        elif export_to_gephi == 'n':
            break
        else:
            print('Enter Y/N please.')
    
    # Output the results
    print("\nTop 20 nodes overall (combined):")
    for node in top_20_nodes_overall:
        print(node)
    
    wait()

    try:
        if exists(f'{script_dir}/{tagname}_top_20_list.txt'):
            print('A top 20 list of hashtags to put in your caption already exists.')
        else:
            with open(f'{script_dir}/{tagname}_top_20_list.txt', 'w') as f:
                for node in top_20_nodes_overall:
                    f.write(f'#{node}\n')
            chmod(f'{script_dir}/{tagname}_top_20_list.txt', 0o444)
            print('A list of your hashtags has been made into a file.')
    except FileNotFoundError as e:
        print(f'An error occurred: {e}')


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

while True:
    try:
        option = int(input(script))
        if option == 1:
            web_scrape()
        elif option == 2:
            network_creation()
        elif option == 3:
            quit()
        elif option == 4:
            tagname = entering_desired_hashtag()
            if tagname != tagname_dupe_test:
                print(tagname, tagname_dupe_test)
                file_existing = False
                captions_seenids(tagname)
        else:
            print('Enter a choice available.')
    except ValueError:
        print('Enter a number please.')
        

# enter code to force the user to do the reCAPTCHA test but then before and after the test, disable any possible human interaction with the webdriver tab
# break down tests even furthr such that the user will enter a hashtag but not search first, and calculate the hashtags etc first
# the updated tagname function does not work properly
# add defensive programming such that if the hashtag entered is nsfw by tiktoks standards, invalidate the use of the hashtag

'''
# Focus on reCAPTCHA element
captcha = driver.find_element(By.ID, 'recaptcha-anchor')  # or appropriate locator
driver.execute_script("arguments[0].scrollIntoView(true);", captcha)
captcha.click()  # Optionally start the process by clicking the CAPTCHA box

# Inject JS to disable user interaction for everything except reCAPTCHA
driver.execute_script("""
    document.body.style.pointerEvents = 'none';  // Disable all pointer events
    var captcha = document.querySelector('#recaptcha-anchor');
    captcha.style.pointerEvents = 'auto';  // Re-enable pointer events for reCAPTCHA
""")

# Open the CAPTCHA in a new tab
driver.execute_script("window.open('');")  # Open a new tab
driver.switch_to.window(driver.window_handles[-1])  # Switch to the new tab

# Load the CAPTCHA URL here (use the actual URL containing the CAPTCHA)
driver.get("URL_with_CAPTCHA")


import time
from selenium.webdriver.common.by import By

def wait_for_captcha():
    while True:
        try:
            # Assuming the CAPTCHA status changes (e.g., greying out after completion)
            if driver.find_element(By.CLASS_NAME, 'recaptcha-checkbox-checked'):
                print('CAPTCHA solved.')
                break
        except:
            pass
        time.sleep(1)  # Poll every second to check if CAPTCHA is done


driver.execute_script("""
    var overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.backgroundColor = 'rgba(0,0,0,0.5)';
    overlay.style.zIndex = '9999';
    overlay.style.display = 'flex';
    overlay.style.alignItems = 'center';
    overlay.style.justifyContent = 'center';
    overlay.innerHTML = '<h1 style="color: white;">Please complete the CAPTCHA</h1>';
    document.body.appendChild(overlay);
""")


from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Run headless browser initially
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

# Do web scraping...

# Detect CAPTCHA and switch to normal mode
chrome_options.headless = False
driver = webdriver.Chrome(options=chrome_options)


''' 
