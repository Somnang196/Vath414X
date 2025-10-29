from seleniumbase import Driver
import os
import json
driver=Driver(uc=True)
driver.get("https://www.x.com")
find=input("y/n:").strip().lower()
if find=="y":
    cookies=driver.get_cookies()
    if cookies:
        with open("cookies.json", 'w', encoding='utf-8') as f:
            json.dump(cookies, f, ensure_ascii=False, indent=2)
        print("cookie found")
print("Done")
