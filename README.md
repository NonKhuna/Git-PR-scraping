# Git-PR-scraping

Bot agent to scrape pull request information form target repository.

# Getting Started
Requires
* selenium
* pandas

# Install library
```shell 
$ pip3 install -r requirements.txt 
```

# Config
- `number_pages`: Amount of page
- `url_pr`: Pull request url of target repository ex. https://github.com/freeCodeCamp/freeCodeCamp/pulls

```python
if __name__ == "__main__" :
    objects = PRObject()
    
    # Parameters 
    number_of_pages = 2
    url_pr = 'https://github.com/freeCodeCamp/freeCodeCamp/pulls?page=1&q=is%3Apr+is%3Aclosed' # link to pull request page
    
    get_data(url_pr,  objects, number_of_pages)
    df = pd.DataFrame({'title': objects.titles, 'link': objects.links, 'isSuccess': objects.isSuccesses, 'descriptions': objects.descriptions, 'commits':objects.commits, 'link_issues': objects.link_issues})
    df.to_csv("result.csv")
  ```
  
  
# Contributing
Credit: [Mr.Sern](https://github.com/sseerrnn)
