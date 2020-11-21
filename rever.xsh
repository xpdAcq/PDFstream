from rever.activity import activity
from pathlib import Path


@activity
def conda_release():
    $PYTHON release.py
    cd rever
    if Path($FORGE_REPO).is_dir():
        rm -rf $FORGE_REPO
    gh repo clone $FORGE_ORG/$FORGE_REPO
    cd $FORGE_REPO
    git checkout master
    git reset --hard origin/master
    git checkout -b $VERSION
    cp -Rv ../recipe/* recipe/
    conda smithy rerender --feedstock_directory .
    git add .
    git commit -m "MNT: Re-rendered"
    git push origin $VERSION --force
    gh pr create --title $VERSION --body "New release using rever"
    cd ../..

@activity
def build_docs():
    make -C docs html


$PROJECT = 'pdfstream'
$ACTIVITIES = [
    'version_bump',
    'changelog',
    'tag',
    'push_tag',
    'ghrelease',
    'pypi',
    'conda_release'
]

$VERSION_BUMP_PATTERNS = [
    ('pdfstream/__init__.py', r'__version__\s*=.*', "__version__ = '$VERSION'"),
    ('setup.py', r'version\s*=.*,', "version='$VERSION',")
]

$CHANGELOG_FILENAME = 'CHANGELOG.rst'
$CHANGELOG_TEMPLATE = 'TEMPLATE.rst'
$TAG_REMOTE = 'git@github.com:st3107/pdfstream.git'

$GITHUB_ORG = 'st3107'
$GITHUB_REPO = 'pdfstream'

$FORGE_ORG = 'nsls-ii-forge'
$FORGE_REPO = 'pdfstream-feedstock'

$SPHINX_HOST_DIR = 'docs/build'
$GHPAGES_REPO = 'git@github.com:st3107/pdfstream.git'
$GHPAGES_BRANCH = 'gh-pages'
$GHPAGES_COPY = (
    ('$SPHINX_HOST_DIR/html', '$GHPAGES_REPO_DIR'),
)
