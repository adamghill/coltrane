import logging
from enum import Enum
from os import environ
from pathlib import Path
from typing import Optional, get_type_hints

import msgspec
from django.http import HttpRequest
from django.template.loader import select_template

from coltrane.config.coltrane.configurators.templates import TemplatesConfigurator

logger = logging.getLogger(__name__)


def get_default_mistune_plugins():
    return [
        "strikethrough",
        "footnotes",
        "table",
        "task_lists",
        "def_list",
        "abbr",
        "mark",
        "insert",
        "superscript",
        "subscript",
    ]


class Base(msgspec.Struct, forbid_unknown_fields=True, dict=True):
    pass


class Coltrane(Base):
    site_url: Optional[str] = None
    is_secure: bool = False
    extra_file_names: list[str] = msgspec.field(default_factory=list)
    data_json5: bool = False
    disable_wildcard_templates: bool = False
    content_directory: str = "content"
    data_directory: str = "data"
    description: Optional[str] = None
    title: Optional[str] = None
    mistune_plugins: list[str] = msgspec.field(default_factory=get_default_mistune_plugins)


class Redirect(Base):
    from_url: str
    to_url: str
    permanent: bool = False


class Site(Base):
    folder: str
    hosts: list[str]

    def has_host(self, request_host: Optional[str]) -> bool:
        if not request_host:
            logger.warning("The host for the request could not be determined")

        for host in self.hosts:
            if host == "*" or (request_host and host.lower() == request_host.lower()):
                return True

        return False

    @property
    def config(self) -> "Config":
        return self._config

    @config.setter
    def config(self, value: "Config"):
        self._config = value

    @property
    def is_custom(self):
        return self.config.has_custom_sites and self.folder != ""

    def get_template_name(self, template_name: str, *, verify: bool = True):
        # print("testt----template_name 1", template_name)

        if template_name in ["coltrane/content.html", "coltrane/base.html"]:
            return template_name

        if self.is_custom:
            template_name = f"{self.config.base_dir}/{self.folder}/templates/{template_name}"

        # print("testt----template_name 2", template_name)

        if verify:
            # print("test---go here")
            selected_template = select_template([template_name])
            template_name = selected_template.template.name

            # print("testt----template_name 3", template_name)

        # print("testt----template_name 4", template_name)

        return template_name

    # def get_template(self, template_name: str):
    #     template_name = self.get_template_name(template_name)
    #     selected_template = select_template([template_name])

    #     return selected_template.template.name


class Config(Base):
    class SiteType(Enum):
        BASE = 1
        SITES = 2

    base_dir: Path = msgspec.field(default_factory=lambda: Path("."))
    """The base directory for the project."""

    site_type: SiteType = SiteType.BASE
    """Whether the project uses a `sites` structure or not."""

    is_debug: bool = False
    """Whether the project is in debug mode."""

    config_file_name: Optional[str] = None
    """The name of the configuration file. Defaults to coltrane.toml."""

    coltrane: Coltrane = msgspec.field(default_factory=Coltrane)
    redirects: list[Redirect] = msgspec.field(default_factory=list)
    sites: list[Site] = msgspec.field(default_factory=lambda: [Site(folder="", hosts=["*"])])

    @property
    def config_file_path(self):
        return self._config_file_path

    @config_file_path.setter
    def config_file_path(self, value):
        self._config_file_path = value

        # TODO: Handle this a little more elegantly
        if str(self._config_file_path).startswith("sites/") or "/sites/" in str(self._config_file_path):
            self.site_type = Config.SiteType.SITES

    @property
    def has_custom_sites(self) -> bool:
        return self.site_type == Config.SiteType.SITES

    def get_site(self, request: HttpRequest) -> Site:
        request_host = request.headers.get("X-Forwarded-Host") or request.headers.get("Host")

        for site in self.sites:
            if site.has_host(request_host):
                return site

        raise AssertionError(f"Missing default site; current sites: {self.sites}")

    def get_templates_settings(self) -> list[dict]:
        return TemplatesConfigurator(self).get_settings()

    def update_from_settings(self):
        # TODO: Parse Django settings and add them to coltrane here?
        pass

    def update_from_env(self):
        """Override coltrane.coltrane config with environment variables"""

        type_hints = get_type_hints(self.coltrane)

        for key in environ.keys():
            if key.startswith("COLTRANE_"):
                coltrane_key = key.replace("COLTRANE_", "").lower()
                value = environ[key]

                if hasattr(self.coltrane, coltrane_key):
                    if coltrane_key in type_hints:
                        key_type = type_hints[coltrane_key]

                        if hasattr(key_type, "__origin__"):
                            if key_type.__origin__ is list:
                                value = value.split(",")
                        elif isinstance(value, str) and key_type is bool:
                            value = "true" == value.lower()

                        setattr(self.coltrane, coltrane_key, value)

    def __post_init__(self):
        """Called after the object has been instantiated."""

        for site in self.sites:
            site.config = self

        self.update_from_settings()  # this is currently a no-op
        self.update_from_env()
