try:
    import argparse
    import json,time,os
    import selenium
    import requests,http,socket
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from fake_headers import Headers
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.firefox import GeckoDriverManager
except ModuleNotFoundError:
    print("Please download dependencies from requirement.txt")
except Exception as ex:
    print(ex)

class Tiktok:
    @staticmethod
    def init_driver(browser_name:str):
        def set_properties(browser_option):
            ua = Headers().generate()      #fake user agent
            browser_option.add_argument('--headless')
            browser_option.add_argument('--disable-extensions')
            browser_option.add_argument('--incognito')
            browser_option.add_argument('--disable-gpu')
            browser_option.add_argument('--log-level=3')
            browser_option.add_argument(f'user-agent={ua}')
            browser_option.add_argument('--disable-notifications')
            browser_option.add_argument('--disable-popup-blocking')

            return browser_option
        try:
            browser_name = browser_name.strip().title()

            ua = Headers().generate()      #fake user agent

            if browser_name.lower() == "chrome":
                browser_option = ChromeOptions()
                browser_option = set_properties(browser_option)
                driver = webdriver.Chrome(ChromeDriverManager().install(),options=browser_option) #chromedriver's path in first argument
            elif browser_name.lower() == "firefox":
                browser_option = FirefoxOptions()
                browser_option = set_properties(browser_option)
                driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),options=browser_option)
            else:
                driver = "Browser Not Supported!"
            return driver
        except Exception as ex:
            print(ex)

    @staticmethod
    def scrap(username,browser_name):
        try:
            URL = 'https://tiktok.com/@{}'.format(username)

            try:
                driver = Tiktok.init_driver(browser_name)
                driver.get(URL)
            except AttributeError:
                print("Driver is not set")
                exit()


            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.title_contains("@{}".format(username)))

            state_data = driver.execute_script("return window['SIGI_STATE']")
            loadList = state_data['ItemList']['user-post']['browserList']
            print(loadList)
            arr_test = [loadList[0]]
            data = {'name':username,'ids':arr_test}
            # json_data = json.dumps(data)
            response = requests.post(url='https://server-crawl.vercel.app/get-video', json=data)
            if response.status_code == 200:
                print("sucessfully fetched the data")
                print(response.json())
            else:
                print(f"Hello person, there's a {response.status_code} error with your request")
            # current_path =  os.path.dirname(os.path.abspath(__file__))
            # jsonString = json.dumps(loadList)
            # jsonFile = open(os.path.join(current_path,'data-crawl/{}.json'.format(username)), "w+")
            # jsonFile.write(jsonString)
            # jsonFile.close()
            driver.close()
            driver.quit()
        except Exception as ex:
            driver.close()
            driver.quit()
            print(ex)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("username",help="username to search")
    parser.add_argument("--browser",help="What browser your PC have?")

    args = parser.parse_args()
    browser_name = args.browser if args.browser is not None else "chrome"
    Tiktok.scrap(args.username,browser_name)



   #last updated - 18th March, 2022