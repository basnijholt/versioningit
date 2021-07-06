from datetime import datetime, timezone
from pathlib import Path
import shutil
import subprocess
from typing import Any, Dict
import pytest
from versioningit.core import VCSDescription
from versioningit.errors import NoTagError, NotVCSError
from versioningit.git import describe_git

pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="Git not installed")

BUILD_DATE = datetime(2038, 1, 19, 3, 14, 7, tzinfo=timezone.utc)

DATA_DIR = Path(__file__).with_name("data")


@pytest.mark.parametrize(
    "repo,params,description",
    [
        (
            "exact",
            {},
            VCSDescription(
                tag="v0.1.0",
                state="exact",
                branch="master",
                fields={
                    "distance": 0,
                    "rev": "002a8cf",
                    "revision": "002a8cf62e16f1b22c5869479a5ba7cac7c19fbc",
                    "author_date": datetime(2021, 7, 4, 4, 8, 20, tzinfo=timezone.utc),
                    "committer_date": datetime(
                        2021, 7, 4, 4, 9, 33, tzinfo=timezone.utc
                    ),
                    "build_date": BUILD_DATE,
                    "vcs": "g",
                    "vcs_name": "git",
                },
            ),
        ),
        (
            "distance",
            {},
            VCSDescription(
                tag="v0.1.0",
                state="distance",
                branch="master",
                fields={
                    "distance": 1,
                    "rev": "d735ad7",
                    "revision": "d735ad70269a40b26c56eea540a9e4a50c48b36a",
                    "author_date": datetime(2021, 7, 4, 4, 11, 57, tzinfo=timezone.utc),
                    "committer_date": datetime(
                        2021, 7, 4, 4, 11, 57, tzinfo=timezone.utc
                    ),
                    "build_date": BUILD_DATE,
                    "vcs": "g",
                    "vcs_name": "git",
                },
            ),
        ),
        (
            "distance-dirty",
            {},
            VCSDescription(
                tag="v0.1.0",
                state="distance-dirty",
                branch="master",
                fields={
                    "distance": 1,
                    "rev": "d735ad7",
                    "revision": "d735ad70269a40b26c56eea540a9e4a50c48b36a",
                    "author_date": datetime(2021, 7, 4, 4, 11, 57, tzinfo=timezone.utc),
                    "committer_date": datetime(
                        2021, 7, 4, 4, 11, 57, tzinfo=timezone.utc
                    ),
                    "build_date": BUILD_DATE,
                    "vcs": "g",
                    "vcs_name": "git",
                },
            ),
        ),
        (
            "default-tag",
            {"default-tag": "v0.0.0"},
            VCSDescription(
                tag="v0.0.0",
                state="distance",
                branch="master",
                fields={
                    "distance": 2,
                    "rev": "2b9cc67",
                    "revision": "2b9cc67944ff8e70163441a55be4596147f82df7",
                    "author_date": datetime(
                        2021, 7, 5, 23, 32, 45, tzinfo=timezone.utc
                    ),
                    "committer_date": datetime(
                        2021, 7, 5, 23, 32, 45, tzinfo=timezone.utc
                    ),
                    "build_date": BUILD_DATE,
                    "vcs": "g",
                    "vcs_name": "git",
                },
            ),
        ),
        (
            "match",
            {"match": ["v*"]},
            VCSDescription(
                tag="v0.1.0",
                state="distance",
                branch="master",
                fields={
                    "distance": 2,
                    "rev": "56fd4b6",
                    "revision": "56fd4b64151218b0339fcf0f5ffca4f5cbfd64b3",
                    "author_date": datetime(
                        2021, 7, 6, 16, 27, 48, tzinfo=timezone.utc
                    ),
                    "committer_date": datetime(
                        2021, 7, 6, 16, 27, 48, tzinfo=timezone.utc
                    ),
                    "build_date": BUILD_DATE,
                    "vcs": "g",
                    "vcs_name": "git",
                },
            ),
        ),
        (
            "match",
            {},
            VCSDescription(
                tag="0.2.0",
                state="exact",
                branch="master",
                fields={
                    "distance": 0,
                    "rev": "56fd4b6",
                    "revision": "56fd4b64151218b0339fcf0f5ffca4f5cbfd64b3",
                    "author_date": datetime(
                        2021, 7, 6, 16, 27, 48, tzinfo=timezone.utc
                    ),
                    "committer_date": datetime(
                        2021, 7, 6, 16, 27, 48, tzinfo=timezone.utc
                    ),
                    "build_date": BUILD_DATE,
                    "vcs": "g",
                    "vcs_name": "git",
                },
            ),
        ),
        (
            "exclude",
            {"exclude": ["v*"]},
            VCSDescription(
                tag="0.1.0",
                state="distance",
                branch="master",
                fields={
                    "distance": 2,
                    "rev": "f0e0d90",
                    "revision": "f0e0d900fdd146d6c1c5ec202eebe37cd8f3d000",
                    "author_date": datetime(
                        2021, 7, 6, 16, 27, 48, tzinfo=timezone.utc
                    ),
                    "committer_date": datetime(
                        2021, 7, 6, 16, 29, 54, tzinfo=timezone.utc
                    ),
                    "build_date": BUILD_DATE,
                    "vcs": "g",
                    "vcs_name": "git",
                },
            ),
        ),
        (
            "exclude",
            {},
            VCSDescription(
                tag="v0.2.0",
                state="exact",
                branch="master",
                fields={
                    "distance": 0,
                    "rev": "f0e0d90",
                    "revision": "f0e0d900fdd146d6c1c5ec202eebe37cd8f3d000",
                    "author_date": datetime(
                        2021, 7, 6, 16, 27, 48, tzinfo=timezone.utc
                    ),
                    "committer_date": datetime(
                        2021, 7, 6, 16, 29, 54, tzinfo=timezone.utc
                    ),
                    "build_date": BUILD_DATE,
                    "vcs": "g",
                    "vcs_name": "git",
                },
            ),
        ),
        (
            "detached-exact",
            {},
            VCSDescription(
                tag="v0.1.0",
                state="exact",
                branch=None,
                fields={
                    "distance": 0,
                    "rev": "002a8cf",
                    "revision": "002a8cf62e16f1b22c5869479a5ba7cac7c19fbc",
                    "author_date": datetime(2021, 7, 4, 4, 8, 20, tzinfo=timezone.utc),
                    "committer_date": datetime(
                        2021, 7, 4, 4, 9, 33, tzinfo=timezone.utc
                    ),
                    "build_date": BUILD_DATE,
                    "vcs": "g",
                    "vcs_name": "git",
                },
            ),
        ),
    ],
)
def test_describe_git(
    repo: str, params: Dict[str, Any], description: VCSDescription, tmp_path: Path
) -> None:
    shutil.unpack_archive(
        str(DATA_DIR / "repos" / "git" / f"{repo}.zip"), str(tmp_path)
    )
    desc = describe_git(project_dir=tmp_path, **params)
    assert desc == description
    for date in ["author_date", "committer_date", "build_date"]:
        assert desc.fields[date].tzinfo is timezone.utc


def test_describe_git_no_tag(tmp_path: Path) -> None:
    shutil.unpack_archive(
        str(DATA_DIR / "repos" / "git" / "default-tag.zip"), str(tmp_path)
    )
    with pytest.raises(NoTagError) as excinfo:
        describe_git(project_dir=tmp_path)
    assert str(excinfo.value) == "`git describe` could not find a tag"


def test_describe_git_no_repo(tmp_path: Path) -> None:
    with pytest.raises(NotVCSError) as excinfo:
        describe_git(project_dir=tmp_path)
    assert str(excinfo.value) == f"{tmp_path} is not a Git repository"


def test_describe_git_no_commits(tmp_path: Path) -> None:
    subprocess.run(["git", "-C", str(tmp_path), "init"], check=True)
    with pytest.raises(NoTagError, match=r"^`git describe` command failed: "):
        describe_git(project_dir=tmp_path)