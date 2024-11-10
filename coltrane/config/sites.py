from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Site:
    name: str
    hosts: List[str] = field(default_factory=lambda: [])

    def has_host(self, request_host: str) -> bool:
        for host in self.hosts:
            if host.lower() == request_host.lower():
                return True

        return False

    @property
    def folder(self):
        return self.name

    def __str__(self):
        return self.name


@dataclass
class Sites:
    def __init__(self, sites: Dict):
        self.sites = []

        for name, hosts in sites.items():
            self.sites.append(Site(name, hosts))

    def get_site(self, request) -> Optional[Site]:
        request_host = request.headers.get("X-Forwarded-Host") or request.headers.get("Host")

        for site in self.sites:
            if site.has_host(request_host):
                return site
