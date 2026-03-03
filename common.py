from seleniumbase import Driver
import json
import time
import random
import os
from datetime import datetime, timezone
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
def retweet_to_community(driver, account):
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
            # Case 1: Button exists (closed state)
            if driver.is_element_present('[aria-label="Choose audience"]'):
                driver.click('[aria-label="Choose audience"]')
                human_sleep("short")

            # Case 2: Dropdown already open
            elif driver.is_element_present("//span[contains(text(),'My Communities')]"):
                print("Audience menu already open")

            else:
                raise Exception("Audience UI not found")

        except Exception:
            print("⚠️ Audience selector missing")
            driver.press_keys("body", "ESC")
            return False

        # select community
        community_name= CommunityRetweet(account)
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
            print("STEP 1: Waiting for textarea...")
            driver.wait_for_element_visible(
                '[data-testid^="tweetTextarea"]',
                timeout=10
            )
            print("✔ STEP 1 PASSED")

            print("STEP 2: Clicking textarea...")
            driver.click('[data-testid^="tweetTextarea"]')
            print("✔ STEP 2 PASSED")

            human_sleep("tiny")

            print("STEP 3: Typing text...")
            driver.type(
                 '[contenteditable="true"][role="textbox"]', TextRetweet()      
            )
            print("✔ STEP 3 PASSED")

            human_sleep("short")

            print("STEP 4: Checking typed value...")
            typed_text = driver.get_text('[data-testid^="tweetTextarea"]')
            print("TEXT FOUND:", repr(typed_text))

        except Exception as e:
            print("❌ ERROR OCCURRED:", e)

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
# def retweet_to_community(driver, account):
#     try:
#         # 1. Open retweet menu
#         if not driver.is_element_present('[data-testid="retweet"]'):
#             print("⚠️ No retweet button")
#             return False

#         human_sleep("tiny")
#         driver.click('[data-testid="retweet"]')
#         human_sleep("tiny")

#         # 2. Click Quote (with retry)
#         quote_selector = "//div[@role='menuitem']//span[text()='Quote'] | //a[@role='menuitem']//span[contains(text(),'Quote')] | [data-testid='quote']"
#         try:
#             driver.wait_for_element(quote_selector, timeout=8)
#             driver.click(quote_selector)
#             print("✔ Clicked Quote")
#         except Exception:
#             print("⚠️ Quote option missing")
#             driver.press_keys("body", "ESC")
#             return False

#         human_sleep("mid")

#         # 3. Wait for Modal & Audience Selector
#         try:
#             # Wait for ANY modal-like element to appear
#             modal_selectors = ['[data-testid="sheetDialog"]', '[role="dialog"]', '.DraftEditor-root']
#             modal_found = False
#             for m_sel in modal_selectors:
#                 if driver.is_element_present(m_sel):
#                     modal_found = True
#                     break
            
#             if not modal_found:
#                 print("⚠️ Modal not detected, attempting to proceed anyway...")

#             # Try to find the audience button with even more variations
#             audience_btn_selectors = [
#                 '[aria-label="Choose audience"]',
#                 "//div[@role='button'][.//span[text()='Everyone']]",
#                 "//div[@role='button'][.//span[contains(text(), 'Everyone')]]",
#                 "//div[@aria-haspopup='menu']",
#                 "[data-testid='composer-audience-button']"
#             ]
            
#             found_btn = False
#             # Try clicking the audience button up to 2 times
#             for _ in range(2):
#                 for selector in audience_btn_selectors:
#                     if driver.is_element_present(selector):
#                         try:
#                             driver.click(selector)
#                             found_btn = True
#                             print(f"✔ Audience menu opened via: {selector}")
#                             break
#                         except:
#                             continue
#                 if found_btn: break
#                 human_sleep("short")
            
#             if not found_btn:
#                 print("⚠️ Could not open audience menu. Checking if already open...")
#                 if not driver.is_element_present("//span[contains(text(),'My Communities')]"):
#                     raise Exception("Audience button not found or clickable")
                    
#             human_sleep("short")
#         except Exception as e:
#             print(f"❌ Audience Step Failed: {e}")
#             # If we can't change audience, we might be posting to 'Everyone' by mistake
#             # Better to ESC and fail than post to the wrong place
#             driver.press_keys("body", "ESC")
#             return False

#         # 4. Select community
#         community_name = CommunityRetweet(account)
#         try:
#             # Very broad search for the community name
#             comm_xpath = f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{community_name.lower()}')]"
            
#             driver.wait_for_element(comm_xpath, timeout=10)
#             # Use JS click as a fallback for hidden/scrolled elements
#             target_element = driver.find_element(comm_xpath)
#             driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_element)
#             human_sleep("tiny")
#             try:
#                 driver.click(comm_xpath)
#             except:
#                 driver.js_click(comm_xpath)
            
#             print(f"✔ Selected community: {community_name}")
#             human_sleep("short")
#         except Exception as e:
#             print(f"⚠️ Community '{community_name}' not found: {e}")
#             driver.press_keys("body", "ESC")
#             return False

#         # 5. Type Comment
#         try:
#             textarea_selector = '[data-testid^="tweetTextarea"]'
#             driver.wait_for_element_visible(textarea_selector, timeout=10)
#             driver.click(textarea_selector)
#             human_sleep("tiny")
            
#             comment_text = TextRetweet()
#             driver.type('[contenteditable="true"][role="textbox"]', comment_text)
#             human_sleep("short")
#         except Exception as e:
#             print("❌ Comment error:", e)

#         # 6. Post
#         try:
#             btn_selector = '[data-testid="tweetButton"]'
#             driver.wait_for_element(btn_selector, timeout=5)
#             human_sleep("tiny")
#             try:
#                 driver.click(btn_selector)
#             except:
#                 driver.js_click(btn_selector)

#             print(f"✅ Successfully shared to: {community_name}")
#             human_sleep("short")
#             return True
#         except Exception:
#             print("⚠️ Final post button failed")
#             driver.press_keys("body", "ESC")
#             return False

#     except Exception as e:
#         print("❌ Critical Error:", e)
#         driver.press_keys("body", "ESC")
#         return False
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
def TextRetweet():
    with open("TextRetweet.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    if not lines:
        return None
    return random.choice(lines)
def CommunityRetweet(account):
    try:
        with open("community_list.json", "r", encoding="utf-8") as f:
            data = json.load(f)   # load full JSON list
    except Exception as e:
        print("Error loading JSON:", e)
        return None

    # Find the matching account
    for item in data:
        if item.get("account") == account:
            communities = item.get("community", [])
            if communities:
                return random.choice(communities)
            return None
    return None
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


def should_run_today():
    now = datetime.now(timezone.utc)

    # Unique seed per workflow per day
    workflow_name = os.environ.get("GITHUB_WORKFLOW", "default")
    seed_value = now.strftime("%Y-%m-%d") + workflow_name

    random.seed(seed_value)

    # Random 3–5 runs per day
    runs_today = random.randint(3, 5)

    # All possible 30-min slots
    possible_slots = [
        (h, m)
        for h in range(0, 24)
        for m in [0, 30]
    ]

    random.shuffle(possible_slots)

    selected_slots = possible_slots[:runs_today]

    print(f"{workflow_name} slots:", selected_slots)

    return (now.hour, now.minute) in selected_slots