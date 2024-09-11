#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "typer",
#   "batchpr@git+https://github.com/astrofrog/batchpr",
#   "cruft@git+https://github.com/Cadair/cruft@patch-p1",
# ]
# ///
"""
This script runs cruft update on all templated sponsored affiliated packages and opens PRs.

The main usecase for this script is when the CI files have been updated as
Github actions can't modify the Github actions workflow files.

You can run this script with:

   pipx run ./all_update.py --help
"""

import os
from typing import Annotated, Optional

from batchpr import Updater
from cruft import update
import typer


ALL_REPOS = (
    "sunpy/sunpy",
    "sunpy/ndcube",
    "sunpy/sunkit-magex",
    "sunpy/streamtracer",
    "sunpy/sunkit-dem",
    "sunpy/mpl-animators",
    "sunpy/sunkit-image",
    "sunpy/sunkit-pyvista",
    "sunpy/sunpy-soar",
)


class CruftUpdater(Updater):

    def process_repo(self):
        ret = update(skip_apply_ask=True, refresh_private_variables=True)
        if not ret:
            self.error(f"Cruft update failed for {self.repo}")
            return False
        self.add(".")
        return True

    @property
    def commit_message(self):
        return "Update cruft with batchpr"

    @property
    def branch_name(self):
        return 'cruft-manual-update'

    @property
    def pull_request_title(self):
        return "Updates from package template"

    @property
    def pull_request_body(self):
        return "This PR has been generated by a script, it should update the repo with the latest changes from the package template."


def run_multi_updater(
    github_token: Annotated[str, typer.Option(envvar="GITHUB_TOKEN")],
    repos: Annotated[list[str], typer.Option()] = ALL_REPOS,
    dry_run: bool = False,
    verbose: bool = False
):
    """
    Run the Cruft Updater script against all repos.

    The GITHUB_TOKEN should be a Personal Access Token (classic) with the workflow permission and public_repo permissions.
    """
    helper = CruftUpdater(token=os.environ["GITHUB_TOKEN"], dry_run=dry_run, verbose=verbose)
    for repo in repos:
        helper.run(repo)


if __name__ == "__main__":
    typer.run(run_multi_updater)