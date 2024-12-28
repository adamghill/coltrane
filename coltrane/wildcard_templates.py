from dataclasses import dataclass


@dataclass
class PathRanking:
    """Store a path with its score based on where the wildcard is in the path."""

    path: str

    def __init__(self, path: str):
        self.path = path
        self.score = self.score_path()

    def score_path(self):
        total_score = 0
        path = self.path.replace(".html", "")

        for idx, path_piece in enumerate(path.split("/")):
            path_idx = len(path.split("/")) - idx

            if path_piece == "*":
                # Inflate wildcards to ensure they are sorted as expected
                total_score += path_idx * 100
            else:
                total_score += path_idx

        return total_score

    def __str__(self):
        return f"{self.path} ({self.score})"


def _sort_potential_templates(template_paths):
    """Sort template paths based on where the wildcard is in the directory."""

    rankings = []

    for path in template_paths:
        rankings.append(PathRanking(path))

    rankings = sorted(rankings, key=lambda r: r.score, reverse=False)

    return [r.path for r in rankings]


def get_potential_wildcard_templates(slug: str) -> list[str]:
    """Get a list of potential wildcard HTML templates based on the slug."""

    wildcard_paths = []

    slug_pieces = slug.split("/")
    slug_pieces_count = len(slug_pieces)

    for outer_idx, _ in enumerate(slug_pieces):
        for inner_idx, _ in enumerate(slug_pieces):
            new_slug_pieces = []

            if outer_idx == inner_idx:
                new_slug_pieces.extend(slug_pieces[:outer_idx])
                new_slug_pieces.extend("*")
                new_slug_pieces.extend(slug_pieces[outer_idx + 1 :])

                wildcard_paths.append(new_slug_pieces)
            elif outer_idx < inner_idx and outer_idx > 0:
                new_slug_pieces.extend(slug_pieces[:outer_idx])
                new_slug_pieces.extend("*" * (slug_pieces_count - outer_idx))

                wildcard_paths.append(new_slug_pieces)
            elif outer_idx > inner_idx and (slug_pieces_count - outer_idx - 1) > 0:
                new_slug_pieces.extend("*" * (slug_pieces_count - outer_idx - 1))
                new_slug_pieces.extend(slug_pieces[outer_idx : outer_idx + 1])
                new_slug_pieces.extend("*" * (slug_pieces_count - outer_idx - 1))

                wildcard_paths.append(new_slug_pieces)

    # Add a catch-all for everything
    # Not needed if there are no potential sub-directories
    if slug_pieces_count > 1:
        new_slug_pieces = []

        for _ in range(slug_pieces_count):
            new_slug_pieces.append("*")

        wildcard_paths.insert(0, new_slug_pieces)

    potential_templates = []

    #  Convert the arrays of paths to paths and add to the list of potential templates
    for wildcard_option in wildcard_paths:
        wildcard_option_path = "/".join(wildcard_option)
        wildcard_option_path = f"{wildcard_option_path}.html"

        potential_templates.append(wildcard_option_path)

    potential_templates = _sort_potential_templates(potential_templates)

    return potential_templates
