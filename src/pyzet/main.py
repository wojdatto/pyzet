from __future__ import annotations

import argparse
import io
import itertools
import logging
import shutil
import subprocess
import sys
from argparse import ArgumentParser, Namespace
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pyzet.constants as const
from pyzet.zettel import get_zettel, get_zettels


@dataclass
class Config:
    repo_path: Path = const.DEFAULT_REPO_PATH
    editor: Path = const.VIM_WIN_PATH


def main(argv: list[str] | None = None) -> int:
    _configure_console_print_utf8()
    logging.basicConfig(level=logging.INFO)

    parser = _get_parser()
    args = parser.parse_args(argv)

    try:
        return _parse_args(args)
    except NotImplementedError:
        parser.print_usage()
        return 0


def _configure_console_print_utf8() -> None:
    # https://stackoverflow.com/a/60634040/14458327
    if isinstance(sys.stdout, io.TextIOWrapper):
        # if statement is needed to satisfy mypy
        # https://github.com/python/typeshed/issues/3049
        sys.stdout.reconfigure(encoding="utf-8")


def _get_parser() -> ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pyzet", formatter_class=argparse.RawTextHelpFormatter
    )

    # https://stackoverflow.com/a/8521644/812183
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {const.VERSION}",
    )

    parser.add_argument("-r", "--repo", help="path to point to any zet repo")

    subparsers = parser.add_subparsers(dest="command")

    status_parser = subparsers.add_parser(
        "status",
        help="run `git status` in zet repo,\nuse `--` before including git options",
    )
    _add_git_cmd_options(status_parser, "status")

    list_parser = subparsers.add_parser("list", help="list zettels in given repo")
    list_parser.add_argument(
        "-p",
        "--pretty",
        action="store_true",
        help="use prettier format for printing date and time",
    )
    list_parser.add_argument(
        "-r",
        "--reverse",
        action="store_true",
        help="reverse the output (so the newest are first)",
    )

    tags_parser = subparsers.add_parser("tags", help="list tags in given repo")
    tags_parser.add_argument(
        "-r",
        "--reverse",
        action="store_true",
        help="reverse the output to be descending",
    )
    tags_parser.add_argument(
        "--count",
        action="store_true",
        help="count the total number of all tags in zet repo (non-unique)",
    )

    show_parser = subparsers.add_parser("show", help="print zettel contents")
    show_parser.add_argument(
        "id",
        nargs="?",
        help="zettel id, by default shows zettel with the newest timestamp",
    )

    clean_parser = subparsers.add_parser(
        "clean", help="delete empty folders in zet repo"
    )
    clean_parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="list what will be deleted, but don't delete it",
    )

    subparsers.add_parser("add", help="add a new zettel")

    edit_parser = subparsers.add_parser("edit", help="edit a zettel")
    edit_parser.add_argument(
        "id",
        nargs="?",
        help="zettel id, by default edits zettel with the newest timestamp",
    )

    remove_parser = subparsers.add_parser("rm", help="remove a zettel")
    remove_parser.add_argument("id", nargs=1, help="zettel id (timestamp)")

    grep_parser = subparsers.add_parser("grep", help="run `grep -rni` in zet repo")
    grep_parser.add_argument(
        "pattern",
        nargs=1,
        help="grep pattern, letter case is ignored",
    )

    subparsers.add_parser("pull", help="run `git pull --rebase` in zet repo")

    push_parser = subparsers.add_parser(
        "push",
        help="run `git push` in zet repo,\nuse `--` before including git options",
    )
    _add_git_cmd_options(push_parser, "push")

    return parser


def _add_git_cmd_options(parser: ArgumentParser, cmd_name: str) -> None:
    parser.add_argument(
        "options",
        action="store",
        type=str,
        nargs="*",
        default=[],
        help=f"`git {cmd_name}` options, use `--` before including them",
    )


def _parse_args(args: Namespace) -> int:
    config = _get_config(args.repo)
    id_: str | None
    try:
        # show & edit use nargs="?" which makes it str, rather than single elem list
        if args.command in ("show", "edit"):
            id_ = args.id
        else:
            id_ = args.id[0]
    except AttributeError:
        pass  # command that doesn't use `id` was executed
    else:
        return _parse_args_with_id(id_, args.command, config)
    return _parse_args_without_id(args, config)


def _get_config(args_repo_path: str) -> Config:
    """Gets config values from CLI or from default value and validates them."""
    config = Config()
    if args_repo_path:
        config.repo_path = Path(args_repo_path)
    if not config.repo_path.is_dir():
        raise SystemExit(
            "ERROR: wrong repo path. "
            f"Create folder `{config.repo_path}` or use `--repo` flag."
        )
    return config


def _parse_args_with_id(id_: str | None, command: str, config: Config) -> int:
    if id_ is None:
        id_ = _get_last_zettel_id(config.repo_path)

    _validate_id(id_, command, config)

    if command == "show":
        return show_zettel(id_, config.repo_path)

    if command == "edit":
        return edit_zettel(id_, config.repo_path, config.editor)

    if command == "rm":
        return remove_zettel(id_, config.repo_path)

    raise NotImplementedError


def _get_last_zettel_id(repo_path: Path) -> str:
    return get_zettels(Path(repo_path, const.ZETDIR), is_reversed=True)[0].id_


def _parse_args_without_id(args: Namespace, config: Config) -> int:
    if args.command == "add":
        return add_zettel(config)

    if args.command == "list":
        return list_zettels(
            config.repo_path, is_pretty=args.pretty, is_reversed=args.reverse
        )

    if args.command == "tags":
        if args.count:
            return count_tags(config.repo_path)
        return list_tags(config.repo_path, is_reversed=args.reverse)

    if args.command == "grep":
        return call_grep(config.repo_path, args.pattern[0])

    if args.command in ("status", "push"):
        return call_git(config.repo_path, args.command, args.options)

    if args.command == "pull":
        # `--rebase` is used to maintain a linear history without merges, as this
        # seems to be a reasonable approach in zet repo that is usually personal
        return call_git(config.repo_path, "pull", ["--rebase"])

    if args.command == "clean":
        return clean_zet_repo(config.repo_path, is_dry_run=args.dry_run)

    raise NotImplementedError


def _validate_id(id_: str, command: str, config: Config) -> None:
    zettel_dir = Path(config.repo_path, const.ZETDIR, id_)
    if not zettel_dir.is_dir():
        raise SystemExit(f"ERROR: folder {id_} doesn't exist")
    if not Path(zettel_dir, const.ZETTEL_FILENAME).is_file():
        if command == "rm":
            raise SystemExit(
                f"ERROR: {const.ZETTEL_FILENAME} in {id_} doesn't exist. "
                "Use `pyzet clean` to remove empty folder"
            )
        raise SystemExit(f"ERROR: {const.ZETTEL_FILENAME} in {id_} doesn't exist")


def call_git(path: Path, command: str, options: list[str]) -> int:
    subprocess.run(
        [_get_git_cmd().as_posix(), "-C", path.as_posix(), command, *options]
    )
    return 0


def call_grep(path: Path, pattern: str) -> int:
    """Calls grep with recursive search and with ignoring letter case."""
    # `--color=auto` colors the output, e.g. shows found matched with red font.
    # It's a default setting in Ubuntu's .bashrc
    subprocess.run(
        [
            _get_grep_cmd().as_posix(),
            "--color=auto",
            "-rni",
            pattern,
            Path(path, const.ZETDIR).as_posix(),
        ]
    )
    return 0


def list_zettels(path: Path, is_pretty: bool, is_reversed: bool) -> int:
    for zettel in get_zettels(Path(path, const.ZETDIR), is_reversed):
        representation = zettel.timestamp if is_pretty else zettel.id_
        print(f"{representation} - {zettel.title}")
    return 0


def list_tags(path: Path, is_reversed: bool) -> int:
    zettels = get_zettels(Path(path, const.ZETDIR))
    all_tags = itertools.chain(*[t for t in [z.tags for z in zettels]])

    # chain is reverse sorted for correct alphabetical displaying for the same
    # tag counts as Counter's most_common() method remembers the insertion order
    tags = Counter(sorted(all_tags, reverse=True))

    target = tags.most_common() if is_reversed else reversed(tags.most_common())
    [print(f"{occurrences}\t#{tag}") for tag, occurrences in target]
    return 0


def count_tags(path: Path) -> int:
    print(sum(len(zettel.tags) for zettel in get_zettels(Path(path, const.ZETDIR))))
    return 0


def show_zettel(id_: str, repo_path: Path) -> int:
    """Prints zettel text prepended with centered ID as a header."""
    print(f" {id_} ".center(const.ZETTEL_WIDTH, "="))
    zettel_path = Path(repo_path, const.ZETDIR, id_, const.ZETTEL_FILENAME)
    with open(zettel_path, "r", encoding="utf-8") as file:
        print(file.read(), end="")
    return 0


def clean_zet_repo(repo_path: Path, is_dry_run: bool) -> int:
    for item in sorted(Path(repo_path, const.ZETDIR).iterdir(), reverse=True):
        if item.is_dir() and _is_empty(item):
            if is_dry_run:
                print(f"will delete {item.name}")
            else:
                print(f"deleting {item.name}")
                item.rmdir()
    return 0


def _is_empty(folder: Path) -> bool:
    # https://stackoverflow.com/a/54216885/14458327
    return not any(Path(folder).iterdir())


def add_zettel(config: Config) -> int:
    """Adds zettel and commits the changes with zettel title as the commit message."""
    id_ = datetime.utcnow().strftime(const.ZULU_DATETIME_FORMAT)

    zettel_dir = Path(config.repo_path, const.ZETDIR, id_)
    zettel_dir.mkdir(parents=True, exist_ok=True)

    zettel_path = Path(zettel_dir, const.ZETTEL_FILENAME)

    with open(zettel_path, "w+") as file:
        file.write("")

    _open_file(zettel_path, config.editor)
    logging.info(f"{id_} was created")

    try:
        zettel = get_zettel(zettel_path.parent)
    except ValueError:
        logging.info("Adding zettel aborted, cleaning up...")
        zettel_path.unlink()
        zettel_dir.rmdir()
    else:
        _commit_zettel(config.repo_path, zettel_path, zettel.title)
    return 0


def edit_zettel(id_: str, repo_path: Path, editor: Path) -> int:
    """Edits zettel and commits the changes with `ED:` in the commit message."""
    zettel_path = Path(repo_path, const.ZETDIR, id_, const.ZETTEL_FILENAME)
    _open_file(zettel_path, editor)

    try:
        zettel = get_zettel(zettel_path.parent)
    except ValueError:
        logging.info("Editing zettel aborted, restoring the version from git...")
        subprocess.run(
            [
                _get_git_cmd().as_posix(),
                "-C",
                repo_path.as_posix(),
                "restore",
                zettel_path.as_posix(),
            ]
        )
    else:
        if _check_for_file_changes(zettel_path, repo_path):
            _commit_zettel(
                repo_path,
                zettel_path,
                _get_edit_commit_msg(zettel_path, zettel.title, repo_path),
            )
            logging.info(f"{id_} was edited")
        else:
            logging.info(f"{id_} wasn't modified")
    return 0


def _get_edit_commit_msg(zettel_path: Path, title: str, repo_path: Path) -> str:
    if _check_for_file_in_git(zettel_path, repo_path):
        return f"ED: {title}"
    return title


def _check_for_file_in_git(filepath: Path, repo_path: Path) -> bool:
    """Returns True if a file was committed to git."""
    git_log_output = subprocess.run(
        [
            _get_git_cmd().as_posix(),
            "-C",
            repo_path.as_posix(),
            "log",
            filepath.as_posix(),
        ],
        capture_output=True,
        check=True,
    ).stdout
    # If `git log` output is empty, the file wasn't committed
    return git_log_output != b""


def _check_for_file_changes(filepath: Path, repo_path: Path) -> bool:
    """Returns True if a file was modified in a working dir."""
    git_cmd = _get_git_cmd().as_posix()

    # Run `git add` to avoid false negatives, as `git diff --staged` is used for
    # detection. This is important when there are external factors that impact the
    # committing process (like pre-commit).
    subprocess.run([git_cmd, "-C", repo_path.as_posix(), "add", filepath.as_posix()])

    git_diff_output = subprocess.run(
        [git_cmd, "-C", repo_path.as_posix(), "diff", "--staged", filepath.as_posix()],
        capture_output=True,
        check=True,
    ).stdout
    # If `git diff` output is empty, the file wasn't modified
    return git_diff_output != b""


def _open_file(filename: Path, editor: Path) -> None:
    if sys.platform == "win32":
        subprocess.run([editor.as_posix(), filename.as_posix()])
    else:
        vim_path = shutil.which("vi")

        if vim_path is None:
            raise SystemExit("ERROR: `vi` cannot be found by `which` command")

        opener = "open" if sys.platform == "darwin" else vim_path
        subprocess.run([opener, filename])


def remove_zettel(id_: str, repo_path: Path) -> int:
    """Removes zettel and commits the changes with `RM:` in the commit message."""
    if input(f"{id_} will be deleted. Are you sure? (y/N): ") != "y":
        raise SystemExit("aborting")
    zettel_path = Path(repo_path, const.ZETDIR, id_, const.ZETTEL_FILENAME)
    zettel = get_zettel(zettel_path.parent)

    zettel_path.unlink()
    logging.info(f"{id_} was removed")
    _commit_zettel(repo_path, zettel_path, f"RM: {zettel.title}")

    # If dir is removed before committing, git raises a warning that dir doesn't exist
    zettel_path.parent.rmdir()

    return 0


def _commit_zettel(repo_path: Path, zettel_path: Path, message: str) -> None:
    git_cmd = _get_git_cmd()
    subprocess.run(
        [git_cmd.as_posix(), "-C", repo_path.as_posix(), "add", zettel_path.as_posix()]
    )
    subprocess.run(
        [git_cmd.as_posix(), "-C", repo_path.as_posix(), "commit", "-m", message]
    )


def _get_git_cmd() -> Path:
    git_path = shutil.which("git")
    if not git_path:
        raise SystemExit("ERROR: `git` cannot be found by `which` command")
    return Path(git_path)


def _get_grep_cmd() -> Path:
    if sys.platform == "win32":
        grep_path = shutil.which(const.GREP_WIN_PATH)
        if not grep_path:
            raise SystemExit(
                "ERROR: `grep` cannot be found. Do you have Git for Windows"
                " installed in the default location?"
            )
    else:
        grep_path = shutil.which("grep")
        if not grep_path:
            raise SystemExit("ERROR: `grep` cannot be found by `which` command")
    return Path(grep_path)
