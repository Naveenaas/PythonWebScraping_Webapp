from urllib.request import urlopen
from requests import get
from bs4 import BeautifulSoup
from pathlib import Path
from argparse import ArgumentParser
from time import sleep
from time import time
from random import randint
from IPython.core.display import clear_output
import pandas as pd
import re

parser = ArgumentParser(description = "Web scraping app to display the ratings of book from goodreads")
parser.add_argument('--genre',action='store', dest='alist', required=True,type=str, nargs='*',
                    default = ["crime","fiction","fantasy"], 
                    help="Enter genre from the given list:biography,contemporary,crime,fiction,fantasy,mystery,romance,thriller")                                 
args = parser.parse_args()
genres = args.alist
#print("Genre type ",type(genres),genres)

namelist=[]
authorlist=[]
ratinglist=[]
numofratingslist=[]
publisedyearlist=[]
imglinklist=[]
bookgenres = []

headers = {"Accept-Language": "en-US, en;q=0.5"}

#genres = ["biography","contemporary","crime","fiction","fantasy","mystery","romance","thriller"]

pages = [i.__str__() for i in range(1,2)]


start_time = time()
requests = 0

#For every genre in genres list
for genre in genres:
    
    #For every page from 1 to 5
    for page in pages:
        
        response = get('https://www.goodreads.com/shelf/show/'+ genre +'?page='+ page, headers = headers)
       
        # Pause the loop
        sleep(randint(8,15))

        # Monitor the requests
        requests += 1
        elapsed_time = time() - start_time
        #print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
        clear_output(wait = True)

        # Throw a warning for non-200 status codes
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))

        # Break the loop if the number of requests is greater than expected
        if requests > 72:
            warn('Number of requests was greater than expected.')  
            break 

        
        bs=BeautifulSoup(response.text,'html.parser')
       
        bookscontainer = bs.find_all('div',class_= 'elementList')

        for book in bookscontainer:

            if book.find('a',class_='bookTitle') is not None:  
                #To retrieve the book names
                name = book.find('a',class_='bookTitle').contents[0]
                name = re.sub("[\(\[].*?[\)\]]", "", name)
                namelist.append(name)
                bookgenres.append(genre)
                #print(name)

            if book.find('a',class_='authorName') is not None:
                #To retrieve the author of the book
                author = book.find('a',class_='authorName').span.text
                authorlist.append(author)
                #print(author)

            if book.find('span',class_='greyText smallText') is not None:
                #To retrieve ratings & Year of publication
                arr = book.find('span',class_='greyText smallText').text.split(" —\n ")
                rating = arr[0][-4:]
                ratinglist.append(float(rating))
                
                ratingnum = re.sub("[^\d]","",arr[1])
                numofratingslist.append(ratingnum)
               
                
                year = re.sub("[^\d]","",arr[2])
                publisedyearlist.append(year)
               
        
                #print(name," ",author," ",ratingnum," ",rating)

            if book.find('a',class_='leftAlignedImage') is not None:
                imglink = book.find('a',class_='leftAlignedImage').img['src']
                imglinklist.append(imglink)
                #print(imglink)
            
            
#end of for loop
            

book_ratings = pd.DataFrame({'Book': namelist,
                              'Author': authorlist,
                              'Genre' : bookgenres,
                              'Year Of publication': publisedyearlist,
                              'Average rating': ratinglist,
                              'Number of ratings': numofratingslist,
                              'BookCover Image': imglinklist})
print(book_ratings.info())
print(book_ratings)
output_csvfile = 'goodreads_ratings.csv'
output_csvdir = Path('csv_output')
output_csvdir.mkdir(parents=True, exist_ok=True)

output_jsonfile = 'goodreads_ratings.json'
output_jsondir = Path('json_output')
output_jsondir.mkdir(parents=True, exist_ok=True)

book_ratings.to_csv(output_csvdir / output_csvfile)
book_ratings.to_json(output_jsondir / output_jsonfile,orient="records",date_format="iso")