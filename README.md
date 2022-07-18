# pyzet

[![Tests](https://github.com/wojdatto/pyzet/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/wojdatto/pyzet/actions/workflows/tests.yml)

---

> "I, of course, do not think everything by myself. It happens mainly
> within the Zettelkasten".

`pyzet` is a CLI tool targeted at note-taking and personal knowledge
management using the Zettelkasten approach with Git repos.

## Installation

Prerequisites:

* Python 3.7+
* Git 2.25+ (but older also should be fine)

Linux, macOS, and Windows are supported.

You can install pyzet with pip:

    pip install pyzet
    pyzet --help

Alternatively, directly from GitHub you can install the newest version
that may contain some yet unreleased changes (you can inspect
[changelog](https://github.com/wojdatto/pyzet/blob/main/CHANGELOG.md)
for more details):

    pip install git+https://github.com/wojdatto/pyzet

> ⚠️\
> `pyzet` is a work in progress, so you may encounter difficulties and
> annoyances while using it. If you have any problem, question, or
> suggestion, feel free to create an issue on GitHub. We have many ideas
> how to expand pyzet, so make sure to go through [opened
> issues](https://github.com/wojdatto/pyzet/issues) first. **Any
> feedback is welcome!**

## Quick start

Create the simplest required config file, and initialize your
Zettelkasten repository.

Linux/macOS:

```bash
mkdir -p ~/.config/pyzet
echo 'repo: ~/zet' > ~/.config/pyzet/pyzet.yaml
pyzet init
```

Windows (with `PowerShell`):

```powershell
mkdir -p ~/.config/pyzet
echo 'repo: ~/zet' | Set-Content ~/.config/pyzet/pyzet.yaml
pyzet init
```

`pyzet --help` will tell you more about available commands.

`pyzet sample-config unix|windows` will show you how you can extend your
config file. You should especially do this when:

1. Your Git executable isn't in the usual default location.
2. You don't want Vim as the text editor used by pyzet.

## Tutorial

You can read the whole tutorial
[here](https://github.com/wojdatto/pyzet/tree/main/docs).

## Summary of commands

```none
$ pyzet -h
usage: pyzet [-h] [-r REPO] [-c CONFIG] [-V] [-v]
             {init,add,edit,rm,show,list,tags,clean,grep,status,pull,push,remote,sample-config} ...

positional arguments:
  {init,add,edit,rm,show,list,tags,clean,grep,status,pull,push,remote,sample-config}
    init                initialize a git ZK repo at configured or given path
    add                 add a new zettel
    edit                edit an existing zettel
    rm                  remove a zettel
    show                print zettel contents
    list                list all zettels
    tags                list all tags and count them
    clean               delete empty folders in 'zettels' folder in ZK repo
    grep                run 'git grep' with some handy flags in ZK repo
    status              run 'git status' in ZK repo
    pull                run 'git pull --rebase' in ZK repo
    push                run 'git push' in ZK repo
    remote              run 'git remote' in ZK repo
    sample-config       produce a sample pyzet.yaml file

options:
  -h, --help            show this help message and exit
  -r REPO, --repo REPO  point to a custom ZK repo
  -c CONFIG, --config CONFIG
                        use an alternative config file
  -V, --version         show program's version number and exit
  -v, --verbose         increase verbosity of the output
```

## Configuration

The basic configuration of pyzet is set via YAML file which should be
placed at `~/.config/pyzet/pyzet.yaml`. However, there is a `--config`
flag that can be used to point to a custom config file using relative or
global path.

Config file contains a set of possible fields of which only `repo` is
required to be set. The remaining ones will use default values if they
are not set in the config file.

### Default config values

On Linux (or actually: "not Windows", so it will trigger also on Mac)
they will be compatible with Ubuntu and possibly some other distros:

    editor: /usr/bin/vim
    git: /usr/bin/git

On Windows the executables installed with Git for Windows are used as
default options:

    editor: C:/Program Files/Git/usr/bin/vim.exe
    git: C:/Program Files/Git/cmd/git.exe

Forward slashes `/` can be used even on Windows. Backslashes `\` or
double backslashes `\\` should also work, but it wasn't thoroughly
tested.

Also, remember that paths cannot include env variables, but you can use
`~` to point to your `$HOME` directory.

An example correct config file:

    repo: ~/zet
    editor: /usr/bin/vim
    git: /usr/bin/git

You can always display a sample config using `pyzet sample-config`
command.

### Support for multiple ZK repos

You can have multiple repos, and only a single config file, because
there is `--repo` flag that you can always set to point to a custom repo
(and possibly, create an alias that includes it). If `--repo` flag is
used, the setting from YAML is ignored.

## Supported editors

Pyzet is a CLI application which cooperates with a text editor of
choice. The best integration can be probably achieved when also using a
CLI text editor.

But this is not necessary. Currently, pyzet can cooperate with different
text editors, even these that have a GUI but the integration is not
ideal.

Below are listed editors that pyzet was tested with. To use a given
editor, add an `editor` field to your config file.

### Linux

The actual testing was done on Ubuntu WSL2 with these CLI editors, and
they work fine:

    editor: vim
    editor: nano

### Windows

On Windows, the following editors seem to work fine:

    editor: vim  # only if running pyzet from Git Bash
    editor: nano # only if running pyzet from Git Bash
    editor: C:/Program Files/Git/usr/bin/vim.exe
    editor: C:/Program Files/Git/usr/bin/nano.exe
    editor: C:/Program Files/Windows NT/Accessories/wordpad.exe
    editor: notepad.exe

#### Partial compatibility

##### Notepad++

Closing a tab is not enough, you have to close the whole program to save
a zettel.

    editor: C:/Program Files/Notepad++/notepad++.exe

##### VS Code

Issues with adding a zettel. If zettel file already exists, then it
seems to work similarly to Notepad++ (you have to close the whole
program to save a zettel):

    editor: C:/Program Files/Microsoft VS Code/Code.exe

### macOS

Not yet tested. CLI editors known from Linux should work fine.

## Manual installation

Manual installation is also possible. Clone the repo and run the install
command. Using virtual environment is advised.

    git clone https://github.com/wojdatto/pyzet
    cd pyzet

Linux:

    python3 -m venv venv
    . venv/bin/activate
    pip install .
    pyzet --help

Windows:

    python -m venv venv
    .\venv\Scripts\activate
    pip install .
    pyzet --help

## Contributing

### Development installation

Development dependencies are stored in `requirements-dev.txt`. To
install the package in editable mode with the dev dependencies run the
following after cloning the repo:

    pip install -e .
    pip install -r requirements-dev.txt

For running tests more easily, you might also want to install `tox`:

    pip install tox

### Running automatic tests

Pyzet uses pytest and tox to run automatic tests. Use `pytest` command
to test against the current Python version, or use `tox` to test against
all supported Python versions (you, of course, have to install them
first). Tox will also allow you to easily measure test coverage along
with generating a coverage report. [Pre-commit](https://pre-commit.com/)
is also configured as one of tox's envs, but it can be run independently
depending on your preference.

Automatic test coverage is good, but still not ideal at this point, and
some commands are only tested manually. This is especially true in case
of commands that require a user input.

Most tests directly use pyzet CLI to run various commands, and then
their output is compared against expected values. `--config` flag comes
in handy there, as it allows to point to different test configs located
inside `testing` folder.

### GitHub Actions

Continuous integration with GitHub Actions is configured for the `main`
branch, `test-me-<any-name>` branches, and for each branch with an
active pull request.

There are two checks:

* `tox` running tests against each supported Python version

* `pre-commit` running with hooks defined in the [config
  file](https://github.com/wojdatto/pyzet/blob/main/.pre-commit-config.yaml)

## Performance

From real world testing, performance of `pyzet` doesn't seem to be a big
issue at this moment.

E.g. `pyzet list` (probably the slowest command) takes ~150 ms in repo
with 500 zettels.

Generally, we focus on using other performant utilities like `git grep`
to do the hard work, and Python is performing a role of a handy
interface.

### Windows users

A significant performance boost can be achieved after moving to
[WSL2](https://docs.microsoft.com/en-us/windows/wsl/install). You have
to run `pyzet` using Python interpreter from Linux, and your zet repo
needs to be placed on the Linux partition.

## Zettel formatting rules and guidelines

Zettels should use Markdown. It is preferred to use consistent flavor of
Markdown like [CommonMark](https://commonmark.org/). Pyzet will parse
zettel's content trying to extract information like title and tags.

In fact, many rules described below are derived from Rob Muhlestein's
ZettelMark specification that can be found
[here](https://github.com/rwxrob/zet/blob/main/20210812154738/README.md),
which is also based on CommonMark.

Some of the rules described below are only guidelines, but some of them
are needed for pyzet to correctly parse zettels.

### General formatting

For a convenient reading of zettels in the source form, it's recommended
to wrap lines. The [common standard](https://youtu.be/_U5heW26fvg) is to
break line after 72 characters.

Ideal zettels shouldn't be too long, and they should be a brief text
description of pretty much anything. Avoid pasting links in the zettel
core content and prefer using references section (described below) for
that.

Pyzet supports tagging zettels with hashtags for easier searching in the
future. For correct parsing, tags should all fit on a single line, so
their number is naturally limited. Ideally they should only use keywords
that are not a part of a zettel itself, so they can help obtaining
non-obvious connections. The tagging rules are described below.

Try to use consistent Markdown formatting. We recommend:

* Use only `*` for bold & italics

* Use only `*` for unordered lists

* If any item of an unordered lists take more than a single line,
  separate all of them with a single blank line

* Use `<>` to show that something is an URL. GitHub and VSCode will
  detect it even without it thanks to
  [GFM](https://github.github.com/gfm/#autolinks-extension-), but this
  is not true for every tool that supports Markdown (i.e. CommonMark
  doesn't support it).

### Title line

The first line of a zettel that should start with `#` and a single
space, and then the title itself. Title line shouldn't have any leading
or trailing spaces.

If wrong formatting is detected, a warning will be raised and pyzet will
show you a raw title line instead of a parsed one.

Ideally, title should not exceed 50 characters. This is because a title
is also a commit message in a Zettelkasten repo, and GitHub will snip
messages longer than 50 characters when displaying commit messages next
to the files. At this point, this is not checked by pyzet, so no warning
will be raised in that case.

```markdown
# Example correct zettel title
```

### References

Pyzet currently doesn't analyze references, but the suggested way to add
them is as follows:

```markdown
Refs:

* <http://example.com/>

* This is an example description\
  <http://described-example.com/>
```

ZettelMark doesn't specify a keyword for a reference block, but we like
`Refs` as it plays nice with `Tags` that will be described next.
However, at this point, it's all up to the user preference.

If there is no URL description, an URL should be simply placed with a
single space between it and `*`.

If an URL have a description, it should go first. A Markdown syntax for
a hard line break (`\`) is used at the end of the description for a
better rendering in the HTML. Then, a link should start from a new line
preceded with two spaces, so it's aligned with the description.

Along with `\`, Markdown supports different syntax for hard breaks:

* two or more spaces
* inserting HTML `<br>` tag

We believe that `\` is superior to both of them, as a significant
trailing whitespace doesn't seem to be a right idea due to many reasons
(e.g. it's very well hidden from you while editing). Also, a good
practice is to avoid using plain HTML in Markdown files which eliminates
approach with `<br>`.

#### References shouldn't be wrapped

Even if a reference line is longer than 72 characters, ZettelMark tells
not to wrap lines in this section, probably for easier parsing. This
doesn't matter as long as `Refs` are not parsed by pyzet, but it seems
like a reasonable rule to follow, so we recommend it:

```markdown
Refs:

* <http://example.com/>

* This is an example of a a very long description for some very interesting link\
  <http://described-example.com/>

* This is an example of a slightly shorter description\
  <http://this-is-a-very-long-example-link-that-also-should-not-be-wrapped.com/>
```

### Tags

Tags are optional, but if they're used, they should be placed as the
last line of a zettel that starts from 4 or more leading spaces (it's
Markdown syntax for a fenced code block that renders as monospaced
font). Each tag should start with `#` and should be separated with a
single space from the next one.

Using small letters and `kebab-case` is recommended as a consistent
tagging style, but it's not forced or checked at this moment. A tag line
can be preceded by `Tags:` and a single blank line to make zettels more
structured.

```markdown
Tags:

    #tag1 #tag2 #another-tag
```

Remember that tags line should end with a newline character, so the
caret is moved to the next line which should be empty. This is by
default assumed by some text editors like Vim, but is probably less
popular in Windows world.

There are different ways to guarantee that file ending is correct, and
one of them is using pre-commit with `end-of-file-fixer` hook that
[comes by default](https://github.com/pre-commit/pre-commit-hooks) with
that tool. It's very easy to setup pre-commit with ZK Git repository, so
we recommend it.

## Inspiration and further reading

The biggest inspiration for this project was Rob Muhlestein
([`@rwxrob`](https://github.com/rwxrob)), and his approach to
Zettelkasten. Probably the best way to get a grasp of it, is to read
about it in [his public Zettelkasten
repo](https://github.com/rwxrob/zet/blob/main/README.md). Rob also
maintains a Bash CLI tool
[`cmd-zet`](https://github.com/rwxrob/cmd-zet).

See also:

* Two essays by the creator of Zettelkasten, Niklas Luhmann\
  <https://luhmann.surge.sh/>

* Even simpler approach to Zettelkasten\
  <https://gsilvapt.me/posts/building-a-zettelkasten-the-simple-way/>

* Similar tool written in Go by the author of the above\
  <https://github.com/gsilvapt/pmz>

* A Zettelkasten tool for people who prefer to have a GUI\
  <https://github.com/Zettlr/Zettlr>

  There is also an [interesting video](https://youtu.be/c5Tst3-zcWI)
  from the author of this tool that describes his vision of
  Zettelkasten.

## License

Unless explicitly stated otherwise, all files in this repository are
licensed under the Apache Software License 2.0:

> Copyright 2021 Tomasz Wojdat
>
> Licensed under the Apache License, Version 2.0 (the "License"); you
> may not use this file except in compliance with the License. You may
> obtain a copy of the License at
>
>     http://www.apache.org/licenses/LICENSE-2.0
>
> Unless required by applicable law or agreed to in writing, software
> distributed under the License is distributed on an "AS IS" BASIS,
> WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
> implied. See the License for the specific language governing
> permissions and limitations under the License.
