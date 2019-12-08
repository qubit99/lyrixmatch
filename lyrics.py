import requests
import re
from bs4 import BeautifulSoup


# List of sites to extract lyrics from
sites = ["azlyrics.com", "genius.com", "metrolyrics.com"]

# Check if `href` contains `azlyrics.com` or not
def azlyrics(href):
	return href and re.compile("azlyrics.com/").search(href)

# Check if `href` contains `genius.com` or not
def genius(href):
	return href and re.compile("genius.com/").search(href)

# Check if `href` contains `metrolyrics.com` or not
def metrolyrics(href):
	return href and re.compile("metrolyrics.com/").search(href)

# Funtion to match the link for each site
site_match = [azlyrics, genius, metrolyrics]


# Get lyrics from `azlyrics.com`
def get_from_azlyrics(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html.parser')

	try:
		mytag = soup.find("div", "ringtone")
		while True:
			mytag = mytag.next_sibling
			if mytag.name and mytag.name == "div":
				break
		return mytag.text
	except:
		return "Not found"

# Get lyrics from `genius.com`
def get_from_genius(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html.parser')

	try:
		mytag = soup.find("div", "lyrics").p
		mytag = mytag.parent
		return mytag.text
	except:
		return "Not found"

# Get lyrics from `metrolyrics.com`
def get_from_metrolyrics(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html.parser')

	try:
		mytag = soup.find_all("p", "verse")
		if len(mytag) == 0:
			return "Not found"
		lyrics = ''
		for lyric in mytag:
			lyrics += lyric.text + '\n\n'
		return lyrics
	except:
		return "Not found"

# List to store the functions to get lyrics from each website
get_from = [get_from_azlyrics, get_from_genius, get_from_metrolyrics]


# Get the song name from user
print("Enter name of a song")
searchstr = input()

# Iterate over all the sites and get the lyrics
for i in range(len(sites)):
	print("Trying " + sites[i] + "...")
	# Google search the lyrics for current site
	url = "https://www.google.com/search?q=" + searchstr + " lyrics " + sites[i]
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html.parser')

	# Find the first anchor tag containing the website link
	anchor = soup.find("a", href=site_match[i])

	# If link not found, move to the next site
	if anchor == None:
		print("Not found")
		continue

	# Get the url of the lyrics
	ref = anchor['href']
	requrl = ref[ref.index("https"):ref.index('&')]
	# print(requrl)

	# Get the lyrics from current site and print
	print(get_from[i](requrl))