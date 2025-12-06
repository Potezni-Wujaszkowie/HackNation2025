# https://github.com/KashmalaJamshaid/Web-scraping-using-python-and-beautifulsoup/blob/main/Web_Scraping_using_python_and_beautifulsoup.ipynb

import BeautifulSoup
import urllib.request as ur

url_input = "https://kolagospodynwiejskich.org/2025/11/17/racuszki-gruszkowo-dyniowe-z-mieta-i-cynamonem/"
print("The website link that you entered is:", url_input)

def main():
  url =  ur.urlopen(url_input)
  htmlSource = url.read()
  url.close()
  soup = BeautifulSoup(htmlSource)
  print('\n The alt tag along with the text in the web page')
  imgs = soup.find_all('img', alt=True)
  for img in imgs:
    print(img, "\n") 

if __name__ == '__main__':
  main()