from typing import Annotated, Dict, Generator, Optional, Union

import msgspec

from coltrane.config.paths import get_redirects_json


class Redirect(msgspec.Struct):
    """Data for a redirect"""

    to_url: Optional[str] = msgspec.field(name="url")
    permanent: bool = False
    from_url: str = ""


def get_redirects() -> Generator[Redirect, None, None]:
    redirects_json_path = get_redirects_json()

    if not redirects_json_path.exists():
        return

    with redirects_json_path as f:
        paths = msgspec.json.decode(f.read_bytes(), type=Annotated[Dict[str, Union[str, Redirect]], msgspec.Meta()])

        for from_url, to_url in paths.items():
            if from_url.startswith("/"):
                from_url = from_url[1:]  # noqa: PLW2901

            if isinstance(to_url, Redirect):
                redirect = to_url
                redirect.from_url = from_url
            else:
                redirect = Redirect(from_url=from_url, to_url=to_url, permanent=False)

            yield redirect
