from seleniumbase import Driver
import json
import time
import random
import os

# ===== Settings =====
SCROLL_SPEED = 10   # pixels per step (lower = slower & smoother)
RUN_TIME = 100      # total scroll duration
LOOPS = 5   
Gif="gif"        # number of processing cycles per account

def human_sleep(mode="short"):
    ranges = {
        "tiny":  (0.15, 0.6),   # micro pause before/after click
        "short": (0.8,  2.5),   # normal browsing
        "mid":   (2.5,  6.5),   # reading a tweet
        "long":  (8.0,  20.0),  # “distraction” / thinking
    }
    a, b = ranges.get(mode, ranges["short"])
    time.sleep(random.uniform(a, b))

# ===== Setup Browser =====
def setup(cookie_name):
    """Create a browser and load cookies for the given account"""
    driver = Driver(uc=True)
    driver.get("https://www.x.com/login")
    human_sleep("short")
    cookies_file = os.path.join("private_data", f"{cookie_name}.json")
    # cookies_file = os.path.join(f"{cookie_name}.json")
    with open(cookies_file, "r") as f:
        cookies = json.load(f)

    for cookie in cookies:
        cookie.pop("sameSite", None)
        cookie.pop("expiry", None)
        driver.add_cookie(cookie)

    driver.get("https://www.x.com")
    human_sleep("mid")
    return driver


# ===== Smooth Scrolling =====
def smooth_scroll(driver, duration=RUN_TIME, step=SCROLL_SPEED):
    print("🌀 Scrolling...")

    # randomize total scroll duration per call
    duration = random.uniform(duration * 0.6, duration * 1.4)

    start = time.time()
    y = 0

    while time.time() - start < duration:

        # vary step (speed variation)
        current_step = step * random.uniform(0.7, 1.3)
        y += current_step

        driver.execute_script(f"window.scrollTo(0, {y});")

        # micro delay between scroll steps
        time.sleep(random.uniform(0.05, 0.12))

        # ⭐ reading pause (most important)
        if random.random() < 0.12:
            human_sleep("mid")

        # ⭐ occasional early stop (very human)
        if random.random() < 0.03:
            print("🛑 User stopped scrolling early")
            break

    print("🎯 Done scrolling.")


# ===== Like Post =====
def like(driver):
    try:
        like_buttons = driver.find_elements('[data-testid="like"]')
        if like_buttons:
            like_buttons[0].click()
            print("❤️ Liked")
        else:
            print("⚠️ No like buttons found")
    except Exception as e:
        print("❌ Like failed:", e)
def GotoProfile(driver):
    try:
        driver.get("https://x.com/Dirtymom32")
        print("✅ Navigated to profile")
        human_sleep("mid")
        smooth_scroll(driver, duration=30)
        human_sleep("tiny")
        driver.execute_script("window.scrollTo(0, 0);")
        human_sleep("short")
        return True
    except Exception as e:
        print("❌ Profile navigation failed:", e)
        return False
# ===== Retweet Post =====
def retweet_to_community(driver, community_name):
    try:
        # open retweet menu
        if not driver.is_element_present('[data-testid="retweet"]'):
            print("⚠️ No retweet button")
            return False

        human_sleep("tiny")
        driver.click('[data-testid="retweet"]')
        human_sleep("tiny")

        # click Quote (fixed selector)
        try:
            driver.wait_for_element("//a[@role='menuitem']//span[contains(text(),'Quote')]", timeout=5)
            driver.click("//a[@role='menuitem']//span[contains(text(),'Quote')]")
        except Exception:
            print("⚠️ Quote option missing")
            driver.press_keys("body", "ESC")
            return False

        human_sleep("mid")

        # audience selector
        try:
            driver.wait_for_element('[aria-label="Choose audience"]', timeout=5)
            driver.click('[aria-label="Choose audience"]')
            human_sleep("short")
        except Exception:
            print("⚠️ Audience selector missing")
            driver.press_keys("body", "ESC")
            return False

        # select community
        try:
            driver.wait_for_element(f"//span[contains(text(),'{community_name}')]", timeout=6)
            driver.click(f"//span[contains(text(),'{community_name}')]")
            human_sleep("short")
        except Exception:
            print("⚠️ Community not found")
            driver.press_keys("body", "ESC")
            return False

        # optional comment (random)
        try:
            if random.random() < 0.5:
                driver.wait_for_element('[data-testid="tweetTextarea_0"]', timeout=5)
                human_sleep("tiny")
                driver.type('[data-testid="tweetTextarea_0"]', "Nice 🔥")
                human_sleep("short")
        except:
            pass

        # post
        try:
            driver.wait_for_element('[data-testid="tweetButton"]', timeout=5)
            human_sleep("tiny")

            try:
                driver.click('[data-testid="tweetButton"]')
            except:
                driver.js_click('[data-testid="tweetButton"]')

            print("✅ Shared to community")
            human_sleep("short")
            return True

        except Exception:
            print("⚠️ Post failed")
            driver.press_keys("body", "ESC")
            return False

    except Exception as e:
        print("❌ Community retweet error:", e)
        driver.press_keys("body", "ESC")
        return False
def Getstart(driver):
    with open("start.txt","r") as f:
        url=f.readlines()
    for i in url:
        smooth_scroll(driver)
        driver.get(i.strip())
        time.sleep(5)
        try:
            follow_button = driver.find_element('[data-testid$="-follow"]')
            follow_button.click()
            print("✅ Follow button clicked!")
        except Exception as e:
            print("❌ Could not click Follow:", e)
        driver.go_back()
        time.sleep(3)
    print("✅ Done following")
def check():
    videos = sorted(os.listdir(Gif))
    videos = [v for v in videos if v.endswith(".mp4")]
    video=random.choice(videos)
    return video
def post(driver):
    video=check()
    if video is None:
        driver.quit()
        return
    file_path = os.path.abspath(os.path.join(Gif, video))
    time.sleep(3)
    try:
            # 1️⃣ Open compose window
        driver.get("https://x.com/compose/tweet")
        time.sleep(5)
        # try:
        #     driver.click("//button[@aria-label='Choose audience']")
        #     driver.click("(//div[@role='menu']//span)[1]")
        #     time.sleep(1)
        #     # Wait for dropdown options to appea
        # except Exception as e: 
        #     print(e)
            # 2️⃣ Type caption
        driver.type('[aria-label="Post text"]', "Chudai..\n #nsfw #sex #porn #naked #nudes #hentai #squirt #pussy #goon")
        time.sleep(1)
        print("tittle completed")
            # 2️⃣ Type caption
            # 3️⃣ Upload video
        driver.send_keys('input[type="file"]', file_path)
        print("Uploading video...")
        time.sleep(100)  # wait for upload to finish

            # Click Post button
        try:
    # Try normal click first
            driver.click("//span[text()='Post' or text()='Tweet']")
        except Exception:
    # Fallback: use JS click if overlay still intercepts it
            driver.js_click("//span[text()='Post' or text()='Tweet']")
        print("✅ Posted successfully!")
        time.sleep(10)
    except Exception as e:
        print("❌ Error while posting:", e)
    driver.quit()
# ===== Full Process =====
def process(driver, loops=LOOPS):
    """Performs like, retweet, scroll, and refresh repeatedly"""
    for i in range(loops):
        print(f"\n--- Cycle {i + 1}/{loops} ---")
        time.sleep(10)
        driver.execute_script("window.scrollBy(0, 270);")
        time.sleep(2)
        like(driver)
        time.sleep(1)
        retweet(driver)
        time.sleep(2)
        smooth_scroll(driver)
        time.sleep(4)
        driver.refresh()
    print("✅ Done processing")
    time.sleep(5)
    driver.quit()
