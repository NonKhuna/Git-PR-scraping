from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


class PRObject() :
    def __init__(self) :
        self.titles = []
        self.links = []
        self.isSuccesses = []
        self.descriptions = []
        self.commits = []
        self.link_issues = []
    
    def add_item(self, title, link, isSuccess, description, commit, link_issue) :
        self.titles.add(title)
        self.links.add(link)
        self.isSuccesses.add(isSuccess)
        self.descriptions.add(description)
        self.commits.add(commit)
        self.link_issues.append(link_issue)
    
    def add_items(self, titles, links, isSuccesses, descriptions, commits, link_issues) :
        self.titles += titles
        self.links += links
        self.isSuccesses += isSuccesses
        self.descriptions += descriptions
        self.commits += commits
        self.link_issues += link_issues


def get_information_PR(driver, link) :
    """
        params: driver
                link: url of PR 
    """
    driver.get(link)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'comment-body.markdown-body.js-comment-body.soft-wrap.css-overflow-wrap-anywhere.user-select-contain.d-block')))
    title = driver.find_element(By.CLASS_NAME, 'js-issue-title.markdown-title').text
    description = driver.find_element(By.CLASS_NAME, 'comment-body.markdown-body.js-comment-body.soft-wrap.css-overflow-wrap-anywhere.user-select-contain.d-block').text
    
    link_issues = []
    try :
        issues = driver.find_elements(By.CLASS_NAME, "Truncate.truncate-with-responsive-width.my-1")
        for li in issues :
            li_a = li.find_element(By.TAG_NAME, 'a').text
            link_issues.append(li_a)
    except :
        pass
    
    
    link_commits = link+"/commits"
    driver.get(link_commits)
    commits = driver.find_elements(By.XPATH, '//a[@class="Link--primary text-bold js-navigation-open markdown-title"]')
    commits = [commit.text for commit in commits]
    
    return title, description, commits, link_issues

def get_Link_each_PR(driver, objects):
    titles = []
    links = []
    isSuccesses = []
    descriptions = []
    commits = []
    link_issues = []
    current_url =  driver.current_url
    
    div = driver.find_elements(By.CLASS_NAME, "flex-auto.min-width-0.p-2.pr-3.pr-md-2")
    for d in div:
        link = d.find_element(By.CLASS_NAME, "Link--primary.v-align-middle.no-underline.h4.js-navigation-open.markdown-title")
        link_href = link.get_attribute('href')
        links.append(link_href)
        tick = d.find_element(By.CLASS_NAME, "d-inline-block.mr-1").find_element(By.CLASS_NAME,"commit-build-statuses").find_element(By.TAG_NAME, "a").get_attribute('class')
        successText = tick[len("color-fg-"):len("color-fg-")+len("success")]
        func = lambda x: x == "success"
        isSuccesses.append(func(successText))

    # navigate to each page
    for link in links :
        information = get_information_PR(driver, link)
        titles.append(information[0])
        descriptions.append(information[1])
        commits.append(information[2])
        link_issues.append(information[3])
    # back to current page
    driver.get(current_url)
    
    objects.add_items(titles, links, isSuccesses, descriptions, commits, link_issues)


def get_data(start_url, objects, num_pages=10) :


    driver = webdriver.Chrome()
    driver.get(start_url)

    current_iter = 1
    while current_iter <= num_pages:
        try:
            get_Link_each_PR(driver, objects)
          
            current_iter += 1
            print(driver.find_element(By.XPATH, '//em[@class="current"]').text)
            driver.find_element(By.XPATH, '//a[@class="next_page"]').click()

            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, '//em[@class="current"]'),str(current_iter)))
        except:
            break


if __name__ == "__main__" :
    objects = PRObject()
    
    # Parameters 
    number_of_pages = 2
    url_pr = 'https://github.com/freeCodeCamp/freeCodeCamp/pulls?page=1&q=is%3Apr+is%3Aclosed' # link to pull request page
    
    get_data(url_pr,  objects, number_of_pages)
    df = pd.DataFrame({'title': objects.titles, 'link': objects.links, 'isSuccess': objects.isSuccesses, 'descriptions': objects.descriptions, 'commits':objects.commits, 'link_issues': objects.link_issues})
    df.to_csv("out2.csv")