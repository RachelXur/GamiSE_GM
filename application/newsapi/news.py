import requests      
  
def NewsofCA(): 
      
    # BBC news api 
    main_url = " http://newsapi.org/v2/top-headlines?country=ca&q=covid-19&SortBy=publishedAt&apiKey=1564aed20da04500abfa72dad9b1354f "
  
    # fetching data in json format 
    ca_news_page = requests.get(main_url).json() 
  
    # getting all articles in a string article 
    article = ca_news_page["articles"] 
  
    # empty list which will  
    # contain all trending news 
    results = [] 
    lists = []
    urls = []
    date = []
    image = []
    name = []
  
    for ar in article: 
        results.append(ar["title"])
        lists.append(ar["description"])
        urls.append(ar["url"])
        date.append(ar["publishedAt"])
        image.append(ar["urlToImage"])
        name.append(ar["source"])

    title = results[0]
    description = lists[0]
    links = urls[0]
    date = date[0]
    image = image[0]
    name = name[0]["name"]
    return title, description, links, date, image, name


        