import requests
from bs4 import BeautifulSoup
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SearchResult:
    def __init__(self):
        self.API_KEY = "AIzaSyAey5h4mFIeiFS2qJyK5tzNnckgHK4RcOc"
        self.SEARCH_ENGINE_ID = "43dbcb78258c74a8e"

    def retry_request(self, url, retries=1, delay=1):
        """Makes a GET request with retries on failure."""
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



    def google_custom_search(self, query, max_results=5):
        """Fetch search results continuously and yield them."""
        api_url = "https://customsearch.googleapis.com/customsearch/v1"
        params = {"q": query, "key": self.API_KEY, "cx": self.SEARCH_ENGINE_ID}

        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()
            yield from self.json_into_dict(data, max_results)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching search results: {e}")
            return

    def json_into_dict(self, data, max_results):
        """Process JSON response and yield results one by one."""
        if not data or "items" not in data:
            logger.warning("No results found in the API response.")
            return

        count = 0
        for idx, item in enumerate(data.get("items", [])):
            title = item.get("title", "No Title")
            title = title.replace("PenduJatt", "").replace("Download", "").replace("Mp3", "")

            link = item.get("link", "No Link")
            snippet = item.get("snippet", "No Description")
            thumbnail_url = item.get("pagemap", {}).get("cse_thumbnail", [{}])[0].get("src", "No Thumbnail")
            cover_image_url = item.get("pagemap", {}).get("cse_image", [{}])[0].get("src", "No Cover Image")

            song_details = self.scrapper(link)
            if not song_details:
                continue

            yield {
                 'id': idx + 1,
                "title": title,
                "link": link,
                "description": snippet,
                "thumbnail": thumbnail_url,
                "image": cover_image_url,
                "audio_source": song_details.get("Audio Source", ""),
                "singer": song_details.get("Singer", ""),
                "duration": song_details.get("Duration", ""),
                "released_on": song_details.get("Released on", ""),
            }

            count += 1
            if count >= max_results:
                break

    def scrapper(self, url):
        """Scrape song details and audio source from the given URL."""
        response = self.retry_request(url)
        if not response or response.status_code != 200:
            logger.error(f"Failed to scrape URL: {url}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        song_link = soup.find("source")
        details_div = soup.find_all("p", class_="title")

        if not song_link or not details_div:
            return None

        try:
            audio_src = song_link.get("src", "")
            details = {
                detail.text.split(":")[0].strip(): detail.text.split(":", 1)[1].strip()
                for detail in details_div
            }
            details["Audio Source"] = audio_src
            return details
        except Exception as e:
            logger.error(f"Error parsing details from URL {url}: {e}")
            return None


# # Example Usage
# if __name__ == "__main__":
    
#     sr = SearchResult()
#     query = "kaise hua"
#     max_results = 5
    
    
#     for idx, song in enumerate(sr.google_custom_search(query, max_results=max_results), start=1):
        
#         # print(f"{idx}. {song['title']} - {song['singer']}")
#         print(song['title'])

        

if __name__ == "__main__":
    sr = SearchResult()
    query = "kaise hua"
    max_results = 5

    logger.info(f"Fetching top {max_results} results for query: {query}")
    for idx, song in enumerate(sr.google_custom_search(query, max_results=max_results), start=1):
        print(f"{idx}. {song['title']} by {song['singer']}")
