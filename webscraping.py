# Importing all necessary libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from os.path import abspath, dirname, exists, join
from tqdm import tqdm
import os
import re
import time
import json

# Subroutine to wait before the next step loads, ensuring that each step of the program is run correctly
def ping_website(url):
    try:
        # Adjust parameter for Windows and other linux/unix based OSs
        param = "-n" if os.name == "nt" else "-c"
        
        # Executing the ping command
        cmd = f"ping {param} 1 {url}"
        response = os.system(cmd)
        
        if response == 0:
            return True
        else:
            return False
    except Exception as e:
        return False

def wait():
    # Placeholder function
        x = input('Press Enter')

# def show_popup(message, title="TikTok Reminder"):
#     os_type = platform.system()
# 
#     if os_type == "Windows":
#         # Windows: Use PowerShell to create a pop-up message box
#         os.system(f'powershell -command "Add-Type -AssemblyName Microsoft.VisualBasic; [Microsoft.VisualBasic.Interaction]::MsgBox(\'{message}\', 0, \'{title}\')"')
# 
#     elif os_type == "Darwin":
#         # macOS: Use AppleScript via osascript
#         os.system(f'osascript -e \'display alert "{title}" message "{message}"\'')

def entering_desired_hashtag():
    while True:
        try:
            options = int(input('1) Enter your hashtag\n2) Quit \nEnter here: '))
            if options == 1:
                desired_hashtag = input('Please enter the hashtag you wish to search (with the # symbol as well): ')
                # If the hashtag entered has any foreign characters to alphanumeric characters, invalidate the hashtag
                if not re.match(r'^#[A-Za-z0-9]+$', desired_hashtag):
                        print('Invalid tag. A valid hashtag must start with # and be followed only by letters or numbers.')
                else:
                    return desired_hashtag  # Return valid hashtag
            elif options == 2:
                quit() # Quits the program
            else:
                print('\nEnter a valid option.\n')
        except ValueError:
            print('\nEnter a number of an option.\n') # Ask user to enter a number if the input isn't an integer

def update_tagname():
    
    # Store the hashtag to be used and potentially modified if needed
    new_tagname = entering_desired_hashtag()
    
    # Generates the file path from the program itself to ensure no accidental file creations are placed elsewhere
    script_dir = dirname(abspath(__file__)) 
    
    # Construct the file paths
    hashtag_filename_captions = f'{new_tagname}captions.json'
    hashtag_filename_seenids = f'{new_tagname}seenids.json'
    captions_file_path = join(script_dir, hashtag_filename_captions)
    seenids_file_path = join(script_dir, hashtag_filename_seenids)
    
    return new_tagname, captions_file_path, seenids_file_path

# Store the hashtag to be used and potentially modified if needed
tagname = entering_desired_hashtag()
# Generates the file path from the program itself to ensure no accidental file creations are placed elsewhere
script_dir = dirname(abspath(__file__)) 
# Construct the file paths
hashtag_filename_captions = f'{tagname}captions.json'
hashtag_filename_seenids = f'{tagname}seenids.json'
captions_file_path = join(script_dir, hashtag_filename_captions)
seenids_file_path = join(script_dir, hashtag_filename_seenids)
print(captions_file_path)


def web_scrape(tagname, captions_file_path, seenids_file_path):
#     def disable_all_input():
#         driver.execute_script("""
# document.addEventListener('mousedown', function(e) { e.stopPropagation(); e.preventDefault(); }, true);
# document.addEventListener('mouseup', function(e) { e.stopPropagation(); e.preventDefault(); }, true);
# document.addEventListener('click', function(e) { e.stopPropagation(); e.preventDefault(); }, true);
# document.addEventListener('dblclick', function(e) { e.stopPropagation(); e.preventDefault(); }, true);
# document.addEventListener('keydown', function(e) { e.stopPropagation(); e.preventDefault(); }, true);
# document.addEventListener('keyup', function(e) { e.stopPropagation(); e.preventDefault(); }, true);
# """)
#         print('Overlay Added')

    def accept_cookies():
        try:
            # Locate the entire banner for the cookie policy tab
            cookies_tab_full = driver.find_element(By.XPATH, "/html/body/tiktok-cookie-banner") 
            shadow_root = driver.execute_script('return arguments[0].shadowRoot', cookies_tab_full)
            # Access the shadow root DOM inside the banner
            element_inside_shadow = shadow_root.find_element(By.CLASS_NAME, 'button-wrapper')
            button_element = element_inside_shadow.find_element(By.CSS_SELECTOR, 'button')
            # Click the first button that appears in HTML (in order it is 'Decline all' then 'Accept all')
            button_element.click()
        except NoSuchElementException:
            pass
        
    def nsfw_hashtag(old_tagname):
        try:
            # Locate the link to the community guidelines page if an NSFW hashtag is entered (will come up with a prompt)
            nsfw_guidelines_element = driver.find_element(By.CSS_SELECTOR, "a[href='https://www.tiktok.com/community-guidelines?lang=en']") 
            if nsfw_guidelines_element:
                print(f'The hashtag {old_tagname} has no search results as it is deemed NSFW. Enter a new one.')
                wait()
                return True
        except NoSuchElementException:
            print('Not found')
            return False
            
    
    print('IMPORTANT: Every time a "Press Enter" prompt appears, please check to see if TikTok is making you perform a reCAPTCHA test.\nPlease do not touch the WebDriver tab at all unless the prompt is required to be completed, as this will break the program.')
    
    wait()  

    # Load the search engine browser
    driver = webdriver.Chrome()
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
    
    driver.refresh()
    # After having refreshed the page, your WebDriver instance should have logged into the account
    accept_cookies()
    wait()
    
    # To find the search button, we will use the find_element function to insert the target hashtag
    
    search_bar = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[2]/div/form/input')
    # Enter the desired hashtag
    search_bar.send_keys(tagname)
    search_bar.send_keys(Keys.ENTER)
    
    accept_cookies()
    wait()
    
    # Filtering the feed to only show videos 
    video_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div')
    video_button.click()

    wait()
    
    # Return True to return back to the main menu to change the hashtag
    nsfw = nsfw_hashtag(tagname)
    
    if nsfw:
        # Return True to the nea.py file to quit the web scraping process
        return True
    else:
        pass


    # Loading all the captions from the file
    try:
        with open(captions_file_path) as f:
            first_line = f.readline().strip()  # Read the first line and remove any leading/trailing whitespace
            if not first_line:
                print("The file is empty.")
                tags = list()  # Initialize as an empty list
            else:
                f.seek(0)  # Reset file pointer to the beginning
                try:
                    tags = list(json.load(f))  # Try to load the JSON content
                except json.JSONDecodeError:
                    print("Error: The file contains invalid JSON data.")
                    tags = list()  # Initialize as an empty list
    except FileNotFoundError:
        print(f"{captions_file_path} not found, creating a new file.")
        tags = list()  # Initialize as an empty list
        with open(captions_file_path, 'w') as f:
            pass  # Create an empty file if it doesn't exist

    # Loading the seen video IDs from the file
    try:
        with open(seenids_file_path) as f:
            first_line = f.readline().strip()  # Read the first line and remove any leading/trailing whitespace
            if not first_line:
                print("The file is empty.")
                seen_ids = set()  # Initialize as an empty set
            else:
                f.seek(0)  # Reset file pointer to the beginning
                try:
                    seen_ids = set(json.load(f))  # Try to load the JSON content
                except json.JSONDecodeError:
                    print("Error: The file contains invalid JSON data.")
                    seen_ids = set()  # Initialize as an empty set
    except FileNotFoundError:
        print(f"{seenids_file_path} not found, creating a new file.")
        seen_ids = set()  # Initialize as an empty set
        with open(seenids_file_path, 'w') as f:
            pass  # Create an empty file if it doesn't exist

    wait()
    
    # Locate the element of the video tab itself which contains the video element objects
    resultsTab = driver.find_element(By.CLASS_NAME, 'eegew6e2')
    resultsTab2 = resultsTab.find_element(By.CLASS_NAME, 'eegew6e0')

    # Gather all the videos by their individual elements
    postsTab = resultsTab2.find_elements(By.CLASS_NAME, 'e19c29qe19')

    while True:
        # Scrolls to the bottom of the page automatically
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5) # Every 5 seconds, gather all the video objects currently loaded
        postsTab = resultsTab.find_elements(By.CLASS_NAME, 'e19c29qe19')
        print(len(postsTab), 'postsTab')
        try:
            end_result = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div[2]')
            if end_result.text == 'No more results' or 'No more videos':
                break
            else:
                continue
        except NoSuchElementException:
            pass
        
        # if len(postsTab) == postsTabSize: # If the size of the current posts loaded is the same as the amount of all the posts together, break out the loop
        #     break
        # else:
        #     postsTabSize = len(postsTab) # Update the current amount of videos found under the hashtag
    
    wait()
    
    # Iterate through each post found with a loading bar
    for post in tqdm(postsTab, desc="Processing posts"):
        # Obtain the link of every post found 
        postsTabClassName = post.find_element(By.CLASS_NAME, 'e1cg0wnj1')
        postsTabID = postsTabClassName.find_element(By.TAG_NAME, "a")
        postsTabID = postsTabID.get_attribute("href")
    
        if postsTabID in seen_ids:
            continue
        
        # Add the unseen ID to all seen IDs
        seen_ids.add(postsTabID)
        
        # Create a list of hashtags per caption in video
        postCaptions = []
        
        # Locate the caption via all anchor elements within the caption
        caption_full = post.find_element(By.CLASS_NAME, 'etrd4pu0')
        postcaption = caption_full.find_element(By.CLASS_NAME, 'ejg0rhn1')
        postcaption = postcaption.find_elements(By.TAG_NAME, 'a')
    
        # Obtain each hashtag in each post's caption
        for tag in postcaption:
            hashtag = tag.get_attribute("href")
    
            # Eliminate any instances where the caption contains a link or an @ to someone's account
            if '@' in hashtag.replace('https://www.tiktok.com/tag/', ''):
                continue
            
            # Add only the word of the hashtag to videoCaptions
            postCaptions.append(hashtag.replace('https://www.tiktok.com/tag/', ''))
    
        # Eliminate any single hashtag captions
        if len(postCaptions) <= 1:
            continue
        
        # Filter the captions to have no duplicates and be all lowercase
        postCaptions = list(dict.fromkeys(postCaptions))
        postCaptions = [hashtag.lower() for hashtag in postCaptions]
    
        # Append them to the total list of all captions
        tags.append(postCaptions)
        
    wait()
    
    # Write the updated captions to the file
    with open(captions_file_path, 'w') as a:
        json.dump(tags, a)
    
    # Write the updated seen IDs to the file
    with open(seenids_file_path, 'w') as b:
        json.dump(list(seen_ids), b)
