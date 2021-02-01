from typing import Any, Dict, List, Tuple, Union
import logging

from proxy_rotator.proxy import Proxy


class ProxyManager:
    """Class for managing proxies. Can be instantiated only with valid settings.
    Can manage proxy rotation by using various strategies.
    Currently all proxies will rotate in endless circle."""

    def __new__(cls, settings: Union[Dict[str, Any], None], raw_proxy_list):
        """Method that instantiates new object only with valid setting.
        In case of wrong settings (either without 'is_using_proxy' key,
        or not a dict) ProxyManager would be substituted by EmptyProxyManager."""
        if isinstance(settings, dict) and settings.get("is_using_proxy"):
            return object.__new__(cls)
        return EmptyProxyManager()

    def __init__(self, settings: Dict[str, Any], raw_proxy_list):
        self.raw_proxy_list = raw_proxy_list
        self._proxy_rotator = ProxyRotator(self.raw_proxy_list)

    def _get_proxy_list(self) -> List[str]:
        """Method that returns a list of valid proxies.
        :return list with proxies.
        """
        proxy_list = []

        for login, password, site_url in self.raw_proxy_list:
            proxy = Proxy(site_url=site_url, login=login, password=password)
            proxy_list.append(proxy.construct())

        return proxy_list

    def get_proxy(self) -> str:
        """
        Method that returns a proxy.
        :return: proxy: valid proxy
        """
        current_proxy = next(self._proxy_rotator)
        return current_proxy


class EmptyProxyManager:
    """Class that is used when ProxyManager shouldn't be instantiated."""

    def get_proxy(self):
        """Stub for get_proxy method of ProxyManager."""
        return None


class ProxyRotator:

    def __init__(self, proxies: list) -> None:
        self._proxies = self.rotate_proxies_in_unlimited_circle(proxies)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._proxies)

    @staticmethod
    def rotate_proxies_in_unlimited_circle(proxies: List) -> Dict[str, Any]:
        """Function to rotate proxies endlessly.
        :param: proxies: list with proxies
        """
        while True:
            for proxy in proxies:
                yield proxy
