import logging
from pathlib import Path
from typing import TYPE_CHECKING

from django.template.library import InvalidTemplateLibrary, import_library

from coltrane.module_finder import is_dj_angles_installed

if TYPE_CHECKING:
    from coltrane.config.coltrane import Config

logger = logging.getLogger(__name__)


class TemplatesConfigurator:
    def __init__(self, config: "Config", *args, **kwargs):
        self.config = config

    def _get_template_tag_module_name(self, file: Path) -> str:
        """
        Get a dot notation module name if a particular file path is a template tag.
        """

        base_dir = self.config.base_dir

        # TODO: Cleaner way to convert a string path to a module dot notation?
        module_name = str(file)

        if str(base_dir) != ".":
            module_name = module_name.replace(str(base_dir), "")

        module_name = module_name.replace("/", ".")

        if module_name.startswith("."):
            module_name = module_name[1:]

        if module_name.endswith(".py"):
            module_name = module_name[:-3]
        else:
            raise InvalidTemplateLibrary()

        import_library(module_name)

        return module_name

    def get_settings(self) -> list[dict]:
        """
        Gets default template settings, including templates and built-in template tags.
        """

        template_dirs = []
        templatetags_dirs = [self.config.base_dir / "templatetags"]

        if self.config.has_custom_sites:
            # Add the base directory so that overriden `include` and `static` templatetags will
            # automatically allow per-site templates to be used.
            # This is in lieu of adding template directories for each site's template folders here
            # which would also "work", but would require templates to live in another sub-directory under
            # `templates` like a normal Django app which is sub-optimal, aka not what I wanted to happen.
            template_dirs.extend([self.config.base_dir, self.config.base_dir / "templates"])

            # Add each site's templatetag folders
            for site in self.config.sites:
                templatetags_dirs.append(self.config.base_dir / site.folder / "templatetags")
        else:
            template_dirs.append(self.config.base_dir / "templates")

        template_tags = []

        for templatetags_dir in templatetags_dirs:
            if templatetags_dir.exists():
                for template_tag_path in templatetags_dir.rglob("*.py"):
                    if template_tag_path.is_file():
                        try:
                            module_name = self._get_template_tag_module_name(template_tag_path)
                            template_tags.append(module_name)
                        except InvalidTemplateLibrary as e:
                            logger.debug(e)

        builtins = [
            "django.contrib.humanize.templatetags.humanize",
            "django.templatetags.static",
            "coltrane.templatetags.coltrane_tags",  # this needs to be last so it overrides the Django templatetags
        ]
        builtins.extend(template_tags)

        template_settings = {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "APP_DIRS": True,
            "DIRS": template_dirs,
            "OPTIONS": {
                "builtins": builtins,
                "context_processors": [
                    "django.template.context_processors.request",
                    "django.template.context_processors.debug",
                    "django.template.context_processors.static",
                    "coltrane.context_processors.coltrane",
                ],
            },
        }

        if is_dj_angles_installed():
            del template_settings["APP_DIRS"]

            if self.config.is_debug:
                template_settings["OPTIONS"]["loaders"] = [
                    "dj_angles.template_loader.Loader",
                    "django.template.loaders.filesystem.Loader",
                    "django.template.loaders.app_directories.Loader",
                ]
            else:
                template_settings["OPTIONS"]["loaders"] = [
                    (
                        "django.template.loaders.cached.Loader",
                        [
                            "dj_angles.template_loader.Loader",
                            "django.template.loaders.filesystem.Loader",
                            "django.template.loaders.app_directories.Loader",
                        ],
                    )
                ]

        return [template_settings]
