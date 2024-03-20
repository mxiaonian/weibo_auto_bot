
from DrissionPage import WebPage, ChromiumOptions

co = ChromiumOptions(read_file=False).set_paths(local_port='9222',
                                                browser_path=r'.\Chrome\App\chrome.exe',
                                                user_data_path=r'.\Chrome\userData')
page = WebPage(chromium_options=co, session_or_options=False)
# ע�⣺session_or_options=False

page.get('https://www.baidu.com')