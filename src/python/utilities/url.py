from urllib.parse import urlparse


def is_valid_url(possible_url: str) -> bool:
    try:
        result = urlparse(possible_url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
