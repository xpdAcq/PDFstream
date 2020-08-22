$PROJECT = 'pdfstream'
$ACTIVITIES = [
    'version_bump',
    'changelog',
    'tag',
    'push_tag',
    'ghrelease',
    'pypi',
]

$VERSION_BUMP_PATTERNS = [
    ('pdfstream/__init__.py', '__version__\s*=.*', "__version__ = '$VERSION'"),
    ('setup.py', 'version\s*=.*,', "version='$VERSION',")
]

$CHANGELOG_FILENAME = 'CHANGELOG.rst'
$CHANGELOG_TEMPLATE = 'TEMPLATE.rst'
$TAG_REMOTE = 'git@github.com:st3107/pdfstream.git'

$GITHUB_ORG = 'st3107'
$GITHUB_REPO = 'pdfstream'
