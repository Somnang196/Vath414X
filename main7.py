from common import retweet_url, setup,smooth_scroll,post,GotoProfile
if __name__ == "__main__":
    driver=setup("cookie7")
    smooth_scroll(driver)
    GotoProfile(driver)
    retweet_url(driver,"Bokep Indo Viral")
    driver.save_screenshot("debug.png")
    driver.quit()
#swapmom