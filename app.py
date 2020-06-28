from flask import Flask, jsonify
import requests
import re
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
  return 'Get lyrics by sending a GET request to /lyrics/search_query'
  
@app.route('/lyrics/<search>')
def get_lyrics(search):
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
		print(soup.prettify())

		try:
			mytag = soup.find("div", "ringtone")
			print(mytag)
			while True:
				mytag = mytag.next_sibling
				if mytag.name and mytag.name == "div":
					break
			return mytag.text
		except Exception as e:
			print(e)
			return "Not found", 404

	# Get lyrics from `genius.com`
	def get_from_genius(url):
		r = requests.get(url)
		soup = BeautifulSoup(r.content, 'html.parser')

		try:
			mytag = soup.find("div", "lyrics").p
			mytag = mytag.parent
			return mytag.text
		except:
			return "Not found", 404

	# Get lyrics from `metrolyrics.com`
	def get_from_metrolyrics(url):
		r = requests.get(url)
		soup = BeautifulSoup(r.content, 'html.parser')

		try:
			mytag = soup.find_all("p", "verse")
			if len(mytag) == 0:
				return "Not found", 404
			lyrics = ''
			for lyric in mytag:
				lyrics += lyric.text + '\n\n'
			return lyrics
		except:
			return "Not found", 404

	# List to store the functions to get lyrics from each website
	get_from = [get_from_azlyrics, get_from_genius, get_from_metrolyrics]


	# Get the song name from user
	# print("Enter name of a song")
	searchstr = search

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
			print("Not found on " + sites[i]), 404
			continue

		# Get the url of the lyrics
		ref = anchor['href']
		requrl = ref[ref.index("https"):ref.index('&')]
		print(requrl)

		# Get the lyrics from current site and print
		return jsonify({"lyrics": get_from[i](requrl)})

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
