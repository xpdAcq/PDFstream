$PROJECT = 'pdfstream'
$ACTIVITIES = [
    'version_bump', # Changes the version number in various source files (setup.py, __init__.py, etc)
    'changelog',  # Uses files in the news folder to create a changelog for release
    'tag',  # Creates a tag for the new version number
    'push_tag',  # Pushes the tag up to the $TAG_REMOTE
    'ghrelease',  # Creates a Github release entry for the new tag
    'pypi',  # Sends the package to pypi
]

$VERSION_BUMP_PATTERNS = [
    ('pdfstream/__init__.py', '__version__\s*=.*', "__version__ = '$VERSION'"),
    ('setup.py', 'version\s*=.*,', "version='$VERSION',")
]

$CHANGELOG_FILENAME = 'CHANGELOG.rst'  # Filename for the changelog
$CHANGELOG_TEMPLATE = 'TEMPLATE.rst'  # Filename for the news template
$TAG_REMOTE = 'git@github.com:st3107/pdfstream.git'  # Repo to push tags to

$GITHUB_ORG = 'st3107'  # Github org for Github releases and conda-forge
$GITHUB_REPO = 'pdfstream'  # Github repo for Github releases  and conda-forge
