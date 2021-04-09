import time
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options 

options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument("--start-maximized")

def download_search_page(query: str) -> []:
    url = f'https://www.youtube.com/results?search_query={query}'

    with webdriver.Chrome(chrome_options=options) as drive:
        resources = []
        link = url.format(query=query)
        drive.get(link)

        html = drive.find_element_by_tag_name('html')

        # while True:
        #     html.send_keys(Keys.END)
        #     time.sleep(2)
        #     message = drive.find_element_by_id('message')
        #     if message is not None and message.text == 'Sem mais resultados':
        #         break

        elements = drive.find_elements_by_id('video-title')

        for element in elements:
            if element.get_attribute('href') is None:
                continue

            title = element.get_attribute('title')
            href = element.get_attribute('href')

            resources.append(dict(title=title, link=href, query=link))
        
        return resources

def __convert_str_view(view: str)-> int:
        view = view.replace('.', '')
        view_regex = re.compile(r'([\d]+\s)+')
        match = view_regex.match(view)
        
        if match is None:
            return 0

        view = match.group(0)

        view = ''.join([s.strip() for s in view if s.strip() != ''])
        return int(view)

def __extract_page_to_dict(driver: webdriver.Chrome) -> dict:

    data = dict()
    
    try:
        title = driver.find_element_by_css_selector('h1.title.style-scope.ytd-video-primary-info-renderer')
        if title is not None:
            data['title'] = title.text
    except:
        pass

    try:
        canal = driver.find_element_by_css_selector('a.yt-simple-endpoint.style-scope.yt-formatted-string')
        if canal is not None:
            data['canal_nome'] = canal.text
            data['canal_link'] = canal.get_property('href')
    except:
        pass

    try:
        views = driver.find_element_by_css_selector('span.view-count')
        if views is not None:
            data['view_counts'] = __convert_str_view(views.text)
    except:
        pass

    try:
        date = driver.find_element_by_css_selector('div#date > yt-formatted-string.style-scope.ytd-video-primary-info-renderer')
        if date is not None:
            data['video_date'] = date.text
    except:
        pass

    try:
        coments = driver.find_elements_by_css_selector('h2#count > yt-formatted-string > span')
        if coments is not None and len(coments) > 0:
            data['coments'] = coments[0].text
    except:
        pass
        
    try:
        likes = driver.find_elements_by_css_selector('div#top-level-buttons > ytd-toggle-button-renderer > a > yt-formatted-string')
        if likes is not None and len(likes) == 2:
            data['like'] = likes[0].get_attribute('aria-label')
            data['dislike'] = likes[1].get_attribute('aria-label')
    except:
        pass

    return data

def download_video_page(link: str) -> dict: 
    
    with webdriver.Chrome(chrome_options=options) as driver:

        driver.get(link)
        time.sleep(1)

        data = __extract_page_to_dict(driver)
        data['link'] = link
        return data
