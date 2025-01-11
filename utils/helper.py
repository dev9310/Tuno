import requests
import pandas as pd
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import time
import logging
from supabase import create_client
from django.http import JsonResponse

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SongExtractor:
    def __init__(self):
        self.API_KEY = os.getenv("MY_API_KEY", "default_api_key")  # Google API key from environment
        self.CX = os.getenv("CUSTOM_SEARCH_CX", "default_cx")  # Custom Search Engine ID

    def retry_request(self, url, retries=3, delay=2):
        """
        Makes a GET request with retries on failure.
        """
        for attempt in range(retries):
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    return response
                logger.warning(f"Attempt {attempt + 1} failed with status {response.status_code}")
            except requests.exceptions.RequestException as e:
                logger.error(f"Attempt {attempt + 1} failed with error: {e}")
            time.sleep(delay)
        return None

    def get_search_result(self, query="aadat by atif aslam", max_results=5):
        """
        Fetches search results from the Google Custom Search API.
        Returns a list containing song data dictionaries.
        """
        api_url = f"https://customsearch.googleapis.com/customsearch/v1?q={query}&key={self.API_KEY}&cx={self.CX}"
        response = self.retry_request(api_url)
        print(api_url)

        if not response or response.status_code != 200:
            try:
                error = response.json().get('error', {}).get('message', 'Unknown error')
                logger.error(f"API Error: {error}")
            except Exception:
                logger.error("Failed to fetch results and parse error.")
            return []

        data = response.json()
        results = []

        for idx, item in enumerate(data.get("items", [])):
            title = item['title']
            desc = item['snippet']
            link = item['link']
            img = item.get('pagemap', {}).get('cse_image', [{}])[0].get('src', '')

            # Clean up the title
            title = title.replace("PenduJatt", "").replace("Download", "").replace("Mp3", "")
            logger.info(f"Fetching details for: {title}")

            # Get song details
            song_details = self.get_song_details(link)
            if not song_details:
                continue

            # Append to results
            results.append({
                'id': idx + 1,
                'title': title,
                'image': img,
                'description': desc,
                'audio_source': song_details.get('Audio Source', ''),
                'singer': song_details.get('Singer', ''),
                'duration': song_details.get('Duration', ''),
                'released_on': song_details.get('Released on', ''),
            })

            # Stop if max_results is reached
            if len(results) >= max_results:
                break

        return results

    def get_song_details(self, url):
        """
        Scrapes song details and the audio source from the given URL.
        Returns a dictionary of song details.
        """
        response = self.retry_request(url)

        if not response or response.status_code != 200:
            logger.error(f"Failed to scrape URL: {url}")
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        song_link = soup.find('source')
        details_div = soup.find_all('p', class_='title')

        if not song_link or not details_div:
            logger.warning(f"Details not found for URL: {url}")
            return None

        try:
            audio_src = song_link.get('src', '')
            details = {
                detail.text.split(':')[0].strip(): detail.text.split(':', 1)[1].strip()
                for detail in details_div
            }
            details['Audio Source'] = audio_src
            return details
        except Exception as e:
            logger.error(f"Error parsing details from URL {url}: {e}")
            return None

class DBManager:
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL', 'default_supabase_url')
        self.supabase_key = os.getenv('SUPABASE_API', 'default_supabase_key')
        self.supabase = self.get_supabase_client()


    def get_supabase_client(self):
        
        return create_client(self.supabase_url, self.supabase_key)

    def fetch_data(self):
        """
        Fetches data from Supabase table `Home_song` and returns it as a JSON-like dict.
        """
        supabase = self.get_supabase_client()
        try:
            response = supabase.table("Home_song").select("*").limit(10).execute()
            if 'error' in response:  # Adjusted to check for 'error' in the response
                logger.error(f"Supabase Error: {response['error']}")
                return {"error": response['error']}
            
            return response.data  # Return the raw data
        
        
        except Exception as e:
            logger.error(f"Unexpected error fetching data: {e}")
            return {"error": "Internal server error"}
        


def get_supabase_client():
    supabase_url = os.getenv('SUPABASE_URL', 'default_supabase_url')
    supabase_key = os.getenv('SUPABASE_API', 'default_supabase_key')
    return create_client(supabase_url, supabase_key)


# # Example Usage
# if __name__ == "__main__":
#     # # Initialize Supabase client
#     # db = DBManager()
#     # supabase = db.get_supabase_client()

#     # # Example to fetch data from Supabase
#     # try:
#     #     response = supabase.table("Home_song").select("*").execute()
#     #     print(response.data)
#     # except Exception as e:
#     #     logger.error(f"Error fetching data from Supabase: {e}")

#     # # Example to fetch and process song search results
#     # # extractor = SongExtractor()
#     # # results = extractor.get_search_result(query="aadat by atif aslam", max_results=5)

#     # # if results:
#     # #     print(pd.DataFrame(results))
#     # else:
#     #     logger.error("No results found or an error occurred.")
#     supa =  DBManager()
    
#     print(supa.fetch_data())