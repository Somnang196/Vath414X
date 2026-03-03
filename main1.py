from common import retweet_to_community, setup, smooth_scroll, should_run_today, GotoProfile,work
import random, time

if __name__ == "__main__":
    print("✅ Running session")
    driver = setup("cookie1")
    work(driver,"18_Movies0")
    
#https://x.com/18_Movies0