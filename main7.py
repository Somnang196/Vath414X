from common import retweet_url, setup,smooth_scroll,post
if __name__ == "__main__":
    driver=setup("cookie7")
    retweet_url(driver, "https://x.com/username/status/123456789")
    driver.save_screenshot("debug.png")
    driver.quit()
#swapmom