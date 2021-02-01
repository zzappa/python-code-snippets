from typing import Tuple
from urllib.parse import urlparse


class Proxy:
    """Class to validate and construct valid proxy."""
    def __init__(self,
                 login: str,
                 password: str,
                 site_url: str) -> None:
        self._site_url = site_url
        self._login = login
        self._password = password
        self._protocol, self._host = self._parse_url()

    def _parse_url(self) -> Tuple[str, str]:
        """Method to parse url that raises an error if not all qualifying_attrs
        could be parsed.
        :returns: scheme and netloc"""
        qualifying_attrs = ('scheme', 'netloc')
        tokens = urlparse(self._site_url)
        if all([getattr(tokens, attr) for attr in qualifying_attrs]):
            return tokens.scheme, tokens.netloc
        else:
            raise KeyError("URL is invalid.")

    def construct(self) -> str:
        """Method that construct proxy by template and returns valid proxy.
        :returns: protocol and proxy url"""
        url = f'{self._protocol}://{self._login}:{self._password}@{self._host}'
        return url
