from common import retweet_to_community, setup, smooth_scroll, should_run_today, GotoProfile
import random, time

if __name__ == "__main__":
    # Only setup driver if selected
    driver = setup("cookie7")

    # Random chance to do action inside session
    if random.random() < 0.6:
        print("active session")
        scroll_times = random.randint(2, 7)

        for _ in range(scroll_times):
            smooth_scroll(driver)
            time.sleep(random.uniform(1.2, 4.5))

        if random.random() < 0.5:
            GotoProfile(driver)
            time.sleep(random.uniform(2, 5))

        if random.random() < 0.8:
            retweet_to_community(driver,"SwapFamily5423")

        driver.save_screenshot("debug.png")

    else:
        # Passive session
        print("passive session")
        scroll_times = random.randint(5, 12)

        for _ in range(scroll_times):
            smooth_scroll(driver)
            time.sleep(random.uniform(1.5, 5))

    driver.quit()
#https://x.com/SwapFamily5423