import base64
import logging
from pathlib import Path
from typing import Optional, Union

from retry import retry
from requests.exceptions import RequestException
from github import Github
from github.ContentFile import ContentFile
from github.GithubException import GithubException
from github.Repository import Repository
from github.PullRequest import PullRequest

from .errors import GithubBranchExistError

_EXCEPTIONS = (GithubException, RequestException)


def _decode_base64_str_to_str(s: str) -> str:
    return str(base64.b64decode(bytes(s, encoding='gbk')), encoding='gbk')


def _get_ref(branch_name: str, with_refs_prefix: bool = True) -> str:
    res = 'heads/' + branch_name
    if with_refs_prefix:
        res = 'refs/' + res
    return res


def _check_exists(repo: Repository, branch_name: str, rel_path: Path,
                  is_dir: bool) -> bool:
    branch = repo.get_branch(branch_name)
    tree = repo.get_git_tree(branch.commit.sha, recursive=True).tree
    target_tree_paths = list(filter(lambda v: v.path == str(rel_path), tree))
    assert len(target_tree_paths) < 2
    if not target_tree_paths:
        return False
    return (target_tree_paths[0].type != 'tree') ^ is_dir


@retry(_EXCEPTIONS, tries=5, delay=1)
def check_exists(repo: Repository, branch_name: str, rel_path: Path,
                 is_dir: bool) -> bool:
    """Check if a relative path exists in the github repo

    Args:
        repo (Repository): A Github repo instance.
        branch_name (str): The target branch name.
        rel_path (Path): The relative path to check.
        is_dir (bool): If the target is a directory.

    Returns:
        bool: True if the target exists.
    """
    return _check_exists(repo, branch_name, rel_path, is_dir)


@retry(_EXCEPTIONS, tries=5, delay=1)
def create_branch_from_master(repo: Repository,
                              branch_name: str,
                              master_branch_name: str = 'master'):
    """Create a new branch from master

    Args:
        repo (Repository): A Github repo instance.
        branch_name (str): The name of the new branch.
        master_branch_name (str, optional): Master branch name. Defaults to 'master'.
    """
    branches = repo.get_branches()
    branch_names = [branch.name for branch in branches]
    if branch_name in branch_names:
        raise GithubBranchExistError
    master_branch = repo.get_branch(master_branch_name)
    repo.create_git_ref(
        ref=_get_ref(branch_name), sha=master_branch.commit.sha)


@retry(_EXCEPTIONS, tries=5, delay=1)
def delete_branch(repo: Repository,
                  branch_name: str,
                  should_check_exist: bool = True) -> bool:
    """Delete a branch

    Args:
        repo (Repository): A Github repo instance.
        branch_name (str): The name of the branch to delete.
        should_check_exist (bool, optional): Firstly check existence if true. Defaults to True.

    Returns:
        bool: Whether it was successfully deleted. (Only works when `should_check_exist` is `True`)
    """
    if should_check_exist:
        branches = repo.get_branches()
        if (not any([branch.name == branch_name for branch in branches])):
            logging.warning('Cannot find the branch {}, skip deleting.'.format(
                branch_name))
            return False
    git_ref = repo.get_git_ref(_get_ref(branch_name, with_refs_prefix=False))
    git_ref.delete()
    return True


@retry(_EXCEPTIONS, tries=5, delay=1)
def merge_branch_to_master(repo: Repository,
                           branch_name: str,
                           commit_message: str,
                           master_branch_name: str = 'master',
                           merge_method: str = 'squash') -> str:
    """Merge a branch to master with a PR created

    Args:
        repo (Repository): A Github repo instance.
        branch_name (str): The name of the branch to merge.
        commit_message (str): The commit message.
        master_branch_name (str, optional): Master branch name. Defaults to 'master'.
        merge_method (str, optional): Merge method used. Defaults to 'squash'. For more details:
            https://docs.github.com/cn/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github

    Returns:
        str: The URL of the PR created.
    """
    pr: PullRequest = repo.create_pull(
        title=commit_message,
        body='',
        head=branch_name,
        base=master_branch_name)
    pr.merge(commit_title=commit_message, merge_method=merge_method)
    return pr.url


@retry(_EXCEPTIONS, tries=5, delay=1)
def get_file_content(repo: Repository,
                     branch_name: str,
                     rel_path: Path,
                     should_check_exist: bool = True) -> Optional[str]:
    """Get the file content with relative path from the Github repo

    Args:
        repo (Repository): A Github repo instance.
        branch_name (str): The source branch name.
        rel_path (Path): The relative path to the target file.
        should_check_exist (bool, optional): Firstly check existence if true. Defaults to True.

    Returns:
        Optional[str]: The file content. If `should_check_exist` is `True` and the file does not
        exist, `None` will be returned.
    """
    if should_check_exist and not _check_exists(
            repo, branch_name, rel_path, is_dir=False):
        logging.warning('The file {} does not exist.'.format(rel_path))
        return None
    content_file: ContentFile = repo.get_contents(
        str(rel_path), ref=_get_ref(branch_name))
    content_str = _decode_base64_str_to_str(content_file.content)
    return content_str


@retry(_EXCEPTIONS, tries=5, delay=1)
def create_file(repo: Repository,
                rel_path: Path,
                content: Union[str, bytes],
                commit_message: str,
                branch_name: str,
                should_check_exist: bool = True) -> bool:
    """Create a file on the Github repo

    Args:
        repo (Repository): A Github repo instance.
        rel_path (Path): The relative file path on the repo to create.
        content (Union[str, bytes]): The file content.
        commit_message (str): The commit message.
        branch_name (str): The target branch name.
        should_check_exist (bool, optional): Firstly check existence if true. Defaults to True.

    Returns:
        bool: Whether it was successfully created. (Only works when `should_check_exist` is `True`)
    """
    if should_check_exist and _check_exists(
            repo, branch_name, rel_path, is_dir=False):
        logging.warning(
            '{} exists on github repo, skip uploading.'.format(rel_path))
        return False
    content_file: ContentFile = repo.create_file(
        path=str(rel_path),
        message=commit_message,
        content=content,
        branch=branch_name)['content']
    logging.debug('Successfully upload to github {} .'.format(
        content_file.path))
    return True


@retry(_EXCEPTIONS, tries=5, delay=1)
def delete_file(repo: Repository,
                rel_path: Path,
                commit_message: str,
                branch_name: str,
                should_check_exist: bool = True) -> bool:
    """Delete a file on the Github repo

    Args:
        repo (Repository): A Github repo instance.
        rel_path (Path): The relative file path on the repo to delete.
        commit_message (str): The commit message.
        branch_name (str): The target branch name.
        should_check_exist (bool, optional): Firstly check existence if true. Defaults to True.

    Returns:
        bool: Whether it was successfully deleted. (Only works when `should_check_exist` is `True`)
    """
    if should_check_exist and not check_exists(
            repo, branch_name, rel_path, is_dir=False):
        logging.warning(
            '{} does not exist on github repo, skip deleting.'.format(
                rel_path))
        return False
    content_file: ContentFile = repo.get_contents(
        str(rel_path), ref=_get_ref(branch_name))
    repo.delete_file(
        path=str(rel_path),
        message=commit_message,
        sha=content_file.sha,
        branch=branch_name)
    logging.debug('Successfully delete {} on github.'.format(rel_path))
    return True


def get_cdn_github_url(repo: Repository, rel_path: Path,
                       branch_name='master') -> str:
    """Get the corresponding CDN url for a relative path on the Github repo

    Args:
        repo (Repository): A Github repo instance.
        rel_path (Path): The relative path to the target.
        branch_name (str, optional): The target branch name. Defaults to 'master'.

    Returns:
        str: The corresponding CDN url.
    """
    cdn_github_url = 'https://cdn.jsdelivr.net/gh/{user}/{repo}@{branch}/{path}'.format(
        user=repo.owner.login,
        repo=repo.name,
        branch=branch_name,
        path=str(rel_path),
    )
    logging.debug('Got CDN github url {} .'.format(cdn_github_url))
    return cdn_github_url


@retry(_EXCEPTIONS, tries=5, delay=1)
def get_github_repo(token: str, repo_name: str) -> Repository:
    """Get a Github Repository instance by token and repo name

    Args:
        token (str): The Github token.
        repo_name (str): The repo name.

    Returns:
        Repository: The Github Repository instance.
    """
    github_ctx = Github(token)
    github_user = github_ctx.get_user()
    github_repo = github_user.get_repo(repo_name)
    return github_repo
