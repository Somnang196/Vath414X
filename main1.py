from seleniumbase import Driver
import json
import time
import random
import os
SCROLL_SPEED = 10       # pixels per step (lower = slower & smoother)
RUN_TIME = 100         # seconds total scroll time
PROCESS=0
# Start SeleniumBase with undetected Chrome
driver = Driver(uc=True)

# Open login page first
driver.get("https://www.x.com/login")
time.sleep(2)  # wait for page to load
cookies_file = os.path.join("private_data", "cookie1.json")
# Load cookies from JSON
with open(cookies_file, "r") as f:
    cookies = json.load(f)

for cookie in cookies:
    # Remove keys that may cause errors
    cookie.pop("sameSite", None)
    cookie.pop("expiry", None)
    driver.add_cookie(cookie)

# Reload the page to apply cookies
driver.get("https://www.x.com")
time.sleep(20)
def smooth_scroll(duration=RUN_TIME, step=SCROLL_SPEED):
    print("Scrolling")
    start = time.time()
    y = 0
    while time.time() - start < duration:
        y += step
        driver.execute_script(f"window.scrollTo(0, {y});")
        time.sleep(random.uniform(0.05, 0.1))  # smaller = faster, larger = slower
    print("🎯 Done scrolling.")
def retweet():
    retweet_buttons = driver.find_elements('[data-testid="retweet"]')
    if retweet_buttons:
        retweet_buttons[0].click()
        time.sleep(2)
    driver.click_if_visible('//*[text()="Repost"]')
    print("retweeted")
def like():
    like_buttons = driver.find_elements('[data-testid="like"]')
    if like_buttons:
        try:
            like_buttons[0].click()
            print("Liked")
        except Exception as e:
            print("❌ Could not click like:", e)
    else:
        print("⚠️ No like buttons found")
while PROCESS<5:
    time.sleep(10)
    driver.execute_script(f"window.scrollBy(0, 270);")
    like()
    time.sleep(1)
    retweet()
    time.sleep(2)
    smooth_scroll()
    time.sleep(4)
    driver.refresh()
    PROCESS += 1
print("Done")
time.sleep(5)
driver.quit()
