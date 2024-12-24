import requests
import pandas as pd
from bs4 import BeautifulSoup
import os

# from dotenv import load_dotenv
# load_dotenv()




class SongExtracter:
    def __init__(self):
        
        self.API_KEY =os.getenv("MY_API_KEY")
        self.CX ="b0a5c1b510456457b"

    def get_search_result(self, query="aadat by atif aslam", max_results=5):
        """
        Fetches the search results from the Google Custom Search API.
        Returns two DataFrames: one for basic song data and another for detailed song data.
        """
        api_url = f"https://customsearch.googleapis.com/customsearch/v1?q={query}&key={self.API_KEY}&cx={self.CX}"
        response = requests.get(api_url)
        
        if response.status_code != 200:
            print(f"Failed to fetch results. Status code: {response.status_code}")
            print(f"Response content: {response.text}")
                  
            return pd.DataFrame(), pd.DataFrame()
        
        basic_data = []
        data = response.json()

        for idx, item in enumerate(data.get("items", [])):
            title = item['title']
            desc = item['snippet']
            link = item['link']
            img = item.get('pagemap', {}).get('cse_image', [{}])[0].get('src', '')

            # title = title.strip("Mp3")
            # title = title.strip("Mp3")
            # title = title.strip("Download")
            title = title.strip("Download Mp3")
            title = title.strip("PenduJatt")

            song_details = self.get_song_details(link)
            if not song_details:
                continue
            
            # Append to basic data
            basic_data.append({
                'id': idx + 1,
                'title': title,
                'img': img,
                'audioSource': song_details.get('Audio Source', ''),
                'singer': song_details.get('Singer', ''),
                'duration': song_details.get('Duration', ''),
                'releasedOn': song_details.get('Released on', ''),
            })

            
            if len(basic_data) >= max_results:
                break
        
        
        
        return  basic_data

    def get_song_details(self, url):
        """
        Scrapes song details and the audio source from the given URL.
        Returns a dictionary of song details.
        """
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to scrape URL: {url}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        song_link = soup.find('source')
        details_div = soup.find_all('p', class_='title')

        if not song_link or not details_div:
            return None

        audio_src = song_link.get('src', '')
        details = {detail.text.split(':')[0].strip(): detail.text.split(':', 1)[1].strip() for detail in details_div}
        details['Audio Source'] = audio_src

        return details
    
