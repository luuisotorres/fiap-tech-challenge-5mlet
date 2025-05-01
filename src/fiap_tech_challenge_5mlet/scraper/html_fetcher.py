import os
import requests


def fetch_or_cache(url: str, cache_filename: str,
                   cache_dir: str = "cache") -> str:
    """
    Fetches HTML from a URL and caches it locally.
    If the cache file exists, it loads from the cache instead.

    Args:
        url (str): The URL to fetch.
        cache_filename (str): The filename to use for the cached HTML.
        cache_dir (str): The directory to store cache files. Defaults to
                         "cache".

    Returns:
        str: HTML content from the cache or freshly fetched.
    """
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, cache_filename)

    if os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            print(f"[CACHE] Loaded: {cache_filename}")
            return f.read()

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        html = response.text

        with open(cache_path, "w", encoding="utf-8") as f:
            f.write(html)
            print(f"[FETCHED] Cached: {cache_filename}")

        return html
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch {url}: {str(e)}")
