$PROJECT = 'pdfstream'
$ACTIVITIES = [
    'changelog',  # Uses files in the news folder to create a changelog for release
    'tag',  # Creates a tag for the new version number
    'push_tag',  # Pushes the tag up to the $TAG_REMOTE
    'pypi',  # Sends the package to pypi
    'conda_forge',  # Creates a PR into your package's feedstock
    'ghrelease'  # Creates a Github release entry for the new tag
]
$CHANGELOG_FILENAME = 'CHANGELOG.rst'  # Filename for the changelog
$CHANGELOG_TEMPLATE = 'TEMPLATE.rst'  # Filename for the news template
$PUSH_TAG_REMOTE = 'git@github.com:st3107/pdfstream.git'  # Repo to push tags to

$GITHUB_ORG = 'st3107'  # Github org for Github releases and conda-forge
$GITHUB_REPO = 'pdfstream'  # Github repo for Github releases  and conda-forge
