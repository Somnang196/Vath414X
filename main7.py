from common import retweet_to_community, setup,smooth_scroll,post,GotoProfile
if __name__ == "__main__":
    driver=setup("cookie7")
    smooth_scroll(driver)
    GotoProfile(driver)
    retweet_to_community(driver, "Bokep Indo Viral")
    driver.save_screenshot("debug.png")
    driver.quit()
#swapmom