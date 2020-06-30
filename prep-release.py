"""Prepare for the conda release."""
import typing as tp
from pathlib import Path

import yaml

import versioneer


def main():
    """Prepare for the release."""
    make_meta_yaml()
    return


def make_meta_yaml():
    """Make the meta.ymal in conda-recipe before the release."""
    with Path('./conda-recipe/meta-template.yaml').open('r') as f:
        dct = yaml.safe_load(f)
    dct['package']['version'] = versioneer.get_version()
    path = next(Path("./dist").glob("*.tar.gz"))
    if path.exists():
        dct['source']['path'] = str(Path('..').joinpath(path))
    else:
        raise FileNotFoundError("No such file: {}".format(path))
    dct['build']['script'] = "{{{{ PYTHON }}}} -m pip install {{{{ SRC_DIR }}}}/{} --no-deps " \
                             "-vv".format(path.name)
    dct['requirements']['run'] = _get_requirements(".")
    with Path('./conda-recipe/meta.yaml').open('w') as f:
        yaml.safe_dump(dct, f)
    return


def _get_requirements(here: str) -> tp.List[str]:
    """Get the current version using versioneer."""
    with open(Path(here).joinpath('requirements/run.txt')) as requirements_file:
        # Parse requirements.txt, ignoring any commented-out lines.
        return [
            line for line in requirements_file.read().splitlines()
            if not line.startswith('#')
        ]


if __name__ == "__main__":
    main()
