from bs4 import BeautifulSoup
import json
from urllib.request import Request
from urllib.request import urlopen

class MetaCriticScraper:
	def __init__(self, url):
		self.game = {'url': '',
					 'image': '',
					 'title': '',
					 'description': '',
					 'platform': '',
					 'publisher': '',
					 'release_date': '',
					 'critic_score': '',
					 'critic_outof': '',
					 'critic_count': '',
					 'user_score': '',
					 'user_count': '',
					 'developer': '',
					 'genre': '',
					 'rating': '',
					 'nplayer': ''
					}
		
		try:
			req = Request(url)
			req.add_unredirected_header('User-Agent','Mozilla/5.0')
			metacritic_url = urlopen(req, timeout = 10)
			self.game['url'] = metacritic_url.geturl()
			html = metacritic_url.read()
			self.soup = BeautifulSoup(html,'html.parser')
			self.scrape()
		except:
			pass
	
	def scrape(self):
		# Get Title and Platform. If site changes and we can't find the right divs or classes
		# skip and leave these values as empty strings
		try:
			product_title_div = self.soup.find("div", class_="product_title")
			self.game['title'] = product_title_div.a.text.strip()
			#self.game['platform'] = product_title_div.span.a.text.strip()
		except:
			print("WARNING: Problem getting title and platform information")
			pass
			
		# Get publisher and release date. 
		try:
			self.game['publisher'] = self.soup.find("li", class_="summary_detail publisher").a.text.strip()
		except:
			print("WARNING: Problem getting publisher and release date information")
			pass

		try:
			self.game['release_date'] = self.soup.find("li", class_="summary_detail release_data").find("span", class_="data").text.strip()
			#datetime.strptime(release_date.strip(), "%b %d, %Y")
		except:
			print("WARNING: Problem getting publisher and release date information")
			pass
			
		# Get critic information
		try:
			res = self.soup.find("script",type="application/ld+json")
			#print(res.string)
			js = json.loads(res.string)
			self.game['image'] = js['image']
			self.game['platform'] = js['gamePlatform']
			self.game['description'] = js['description']
			self.game['critic_score'] = js['aggregateRating']['ratingValue']
			self.game['critic_count'] = js['aggregateRating']['ratingCount']
		except Exception as e:
			print(e)
			print("WARNING: Problem getting critic score information")
			pass
			
		# Get user information
		try:
			users = self.soup.find("div", class_="details side_details")
			#self.game['user_score'] = users.find("span", class_="score_value").text.strip()
			self.game['user_score'] = users.find("div", class_="metascore_w").text.strip()
			raw_users_count = users.find("span", class_="count").a.text
			user_count = ''
			for c in raw_users_count:
				if c.isdigit(): user_count += c
			self.game['user_count'] = user_count.strip()
		except:
			print("WARNING: Problem getting user score information")
			pass
				
		# Get remaining information
		try:
			product_info = self.soup.find("div", class_="section product_details").find("div", class_="details side_details")
			self.game['developer'] = product_info.find("li", class_="summary_detail developer").find("span", class_="data").text.strip()
			#self.game['genre'] = product_info.find("li", class_="summary_detail product_genre").find("span", class_="data").text.strip()
		except:
			print("WARNING: Problem getting miscellaneous game information")
			pass

		try:
			product_info = self.soup.find("div", class_="section product_details").find("div", class_="details side_details")
			self.game['genre'] = [item.string.strip() for item in list(product_info.find("li", class_="summary_detail product_genre").find_all("span", class_="data")) if item.string is not None]
		except:
			print("WARNING: Problem getting miscellaneous game information")
			pass

		try:
			product_info = self.soup.find("div", class_="section product_details").find("div", class_="details side_details")			
			self.game['rating'] = product_info.find("li", class_="summary_detail product_rating").find("span", class_="data").text.strip()
		except:
			print("WARNING: Problem getting miscellaneous game information")
			pass

		try:
			product_info = self.soup.find("div", class_="section product_details").find("div", class_="details side_details")
			self.game['nplayer'] = product_info.find("li", class_ = "summary_detail product_players").find("span", class_="data").text.strip()
		except:
			print("WARNING: Problem getting miscellaneous game information")
			pass
 
		"""try:
			product_info = self.soup.find("div", class_="section product_details").find("div", class_="details side_details")
			
			self.game['developer'] = product_info.find("li", class_="summary_detail developer").find("span", class_="data").text.strip()
			# self.game['genre'] = product_info.find("li", class_="summary_detail product_genre").find("span", class_="data").text.strip()
			self.game['genre'] = [item.string.strip() for item in list(product_info.find("li", class_="summary_detail product_genre").find_all("span", class_="data"))]
			# self.game['genre'] = product_info.find("li", class_="summary_detail product_genre").find_all("span", class_="data").text.strip()
			self.game['rating'] = product_info.find("li", class_="summary_detail product_rating").find("span", class_="data").text.strip()
		except:
			print("WARNING: Problem getting miscellaneous game information")
			pass"""