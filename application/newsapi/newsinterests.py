import requests

def NewsofInterest(): 
      
    # BBC news api 
    inmain_url = " http://newsapi.org/v2/everything?language=en&q=business&SortBy=publishedAt&apiKey=1564aed20da04500abfa72dad9b1354f "
  
    # fetching data in json format 
    interests_news_page = requests.get(inmain_url).json() 
  
    # getting all articles in a string article 
    inarticle = interests_news_page["articles"] 
  
    # empty list which will  
    # contain all trending news 
    inresults = [] 
    inlists = []
    inurls = []
    indate = []
    inimage = []
    inname = []
  
    for ar in inarticle: 
        inresults.append(ar["title"])
        inlists.append(ar["description"])
        inurls.append(ar["url"])
        indate.append(ar["publishedAt"])
        inimage.append(ar["urlToImage"])
        inname.append(ar["source"])

    intitle = inresults[0]
    indescription = inlists[0]
    inlinks = inurls[0]
    indate = indate[0]
    inimage = inimage[0]
    inname = inname[0]["name"]
    return intitle, indescription, inlinks, indate, inimage, inname