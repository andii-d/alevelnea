# Importing necessary libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import json
import networkx as nx
import json
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from scipy.stats import linregress
from matplotlib.ticker import FuncFormatter

# Subroutine for running the menu to decide which part of the program to run
def menu():
    while True:
        try:
            menuinput = int(input('It is recommended you read the help section before running this program.\nPlease enter one of the following:'
                                  '\n\n1) Web Scraping Process'
                                  '\n2) Returning the hashtags'
                                  '\n3) Help + F&Q\n'))
            if menuinput < 1 or menuinput > 3:
                raise ValueError
        except ValueError:
            print('\nPlease enter a number within the options given.\n')
            continue
        else:
            print('Success')


driver = webdriver.Chrome()
# We can change the browser to Chrome, Firefox, etc

time.sleep(10)

driver.get("https://www.tiktok.com")
# Load the TikTok page

time.sleep(10)

# Paste all the cookies inside the cookies array

# When pasting, change all the 'true' and 'false' values to 'True' and 'False'
# (this is because Python reads boolean values with capitalization)

# FOLLOW THESE STEPS CLEARLY:

# For the variable 'sameSite'
# If its value is 'undefined':
# Make sure to change its value to either 'None', 'Strict' or 'Lax' if it is neither one
# If it's already one of the three values above, skip to the next one

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

for cookie in cookies:
    driver.add_cookie(cookie)
    
driver.refresh()
# After having refreshed the page, your WebDriver instance should have logged into your account

time.sleep(10)

# To find the search button, we will use the find_element function to insert the target hashtag
search_bar = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[2]/div/form/input')
# Enter the desired hashtag through Webdriver
search_bar.send_keys('#gaming')
search_bar.send_keys(Keys.ENTER)

time.sleep(10)

# Filtering the feed to only show videos 
video_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[3]/div')
video_button.click()


# Loading the captions

with open('/Users/andy/Desktop/School/tiktokscrape/alevelnea/captions.json') as f:
    tags = list(json.load(f))
    print(len(tags))

# Print the number of however many tags exist in the captions.json file


# Loading the seen video IDs

with open('/Users/andy/Desktop/School/tiktokscrape/alevelnea/seen.json') as f:
    seen_ids = set(json.load(f))
    print(len(seen_ids))
    
# Print the number of however many seen video IDs exist in the seen.json file

videoTab = driver.find_element(By.ID, 'tabs-0-panel-search_video')

videoPosts = videoTab.find_elements(By.CLASS_NAME, 'e19c29qe10')
posts_size = len(videoPosts)

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)
    posts = videoTab.find_elements(By.CLASS_NAME, 'e19c29qe10')
    if len(videoPosts) == posts_size:
        break
    else:
        posts_size = len(videoPosts)
        
time.sleep(5)

# Iterate through each found post
for post in videoPosts:
    # Obtain the link of every post found 
    videopostClassName = post.find_element(By.CLASS_NAME, "e1cg0wnj1")
    videopostID = videopostClassName.find_element(By.TAG_NAME, "a")
    videopostID = videopostID.get_attribute("href")
    
    if videopostID in seen_ids:
        continue
    # Add the unseen ID to all seen IDs
    seen_ids.add(videopostID)
    
    # Create a list of hashtags per caption in video
    videoCaptions = []
    # Locate the caption via all anchor elements
    videocaptionClassName = post.find_element(By.CLASS_NAME, "ejg0rhn0")
    videocaption = videocaptionClassName.find_elements(By.TAG_NAME, "a")
    
    # Obtain each hashtag in each post's caption
    for tag in videocaption:
        hashtag = tag.get_attribute("href")
        # Eliminate any instances where the caption contains a link or an @ to someone's account
        if '@' in hashtag.replace('https://www.tiktok.com/tag/', ''):
            continue
        # Add only the word of the hashtag to videoCaptions
        videoCaptions.append(hashtag.replace('https://www.tiktok.com/tag/', ''))
    
    # Eliminate any single hashtag captions
    if len(videoCaptions)  <= 1:
        continue
    
    # Filter the captions to have no duplicates and be all lowercase
    videoCaptions = list(dict.fromkeys(videoCaptions))
    videoCaptions = [hashtag.lower() for hashtag in videoCaptions]
    
    # Append them to the total list of all captions
    tags.append(videoCaptions)
    
time.sleep(5)

with open('/Users/andy/Desktop/School/tiktokscrape/alevelnea/captions.json', 'a') as a:
    json.dump(tags, a)

with open('/Users/andy/Desktop/School/tiktokscrape/alevelnea/seen.json', 'a') as b:
    # Convert to list
    json.dump(list(seen_ids), b)
    
print('Web scraping algo finished)')

