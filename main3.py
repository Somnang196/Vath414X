from common import setup,smooth_scroll
if __name__ == "__main__":
    driver=setup("cookie3")
    for i in range(3):
        smooth_scroll(driver)
    #New Brazzar