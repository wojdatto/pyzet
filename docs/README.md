# Pyzet tutorial

## Disclaimer for Windows user

This instruction is written with a Linux user in mind. If you're on
Windows, and you don't want to use
[WSL2](https://docs.microsoft.com/en-us/windows/wsl/install), you can
still follow it, but it will be much easier, if you do it using Git Bash
that comes with Git for Windows. With that, all commands will be very
similar, and the main difference will be the location of your home
folder. On Linux, it's by default:

    $ echo $HOME
    /home/<your-username>

And on Git Bash it will be shown as:

    $ echo $HOME
    /c/Users/<your-username>

which is very Git Bash specific and won't work if put it in the config
file.

Generally, in your config file you can use Windows-like path, but we
suggest to use forward slashes `/` rather than backslashes `\` or double
backslashes `\\`, because it wasn't thoroughly tested.

Home directory written with this is mind should look like this:

    C:/Users/<your-username>

## Installation

If you haven't already, install pyzet using one of the methods described
in the [main readme](https://github.com/wojdatto/pyzet#installation),
e.g.:

    pip install pyzet

Now, run `pyzet` command to see if it is installed correctly. You should
see a usage hint:

    $ pyzet
    usage: pyzet [-h] <here will a list of flags and available commands>

For more detailed information, you can always use `--help` flag: `pyzet
-h`.

## Initial configuration

Let's start by initializing our Zettelkasten repository:

    $ pyzet init
    ERROR: config file at '/home/<your-username>/.config/pyzet/pyzet.yaml' not found.
    Add it or use '--config' flag.

Whoops! If you saw a similar error, it means that you haven't used the
quick start commands provided in the [main
readme](https://github.com/wojdatto/pyzet#quick-start). Otherwise,
please feel free to skip to the next section.

We have to create a config file at `~/.config/pyzet/pyzet.yaml`.

Let's create the simplest config file possible that will contain only a
single line:

    repo: ~/zet

E.g. you should be able to quickly do it with these two commands:

    mkdir -p ~/.config/pyzet
    echo 'repo: ~/zet' > ~/.config/pyzet/pyzet.yaml

Now, the command from above should work:

    $ pyzet init
    Initialized empty Git repository in /home/<your-username>/zet/.git/

## Zettelkasten with Git

The idea behind pyzet is that each ZK repository is also a Git
repository to have ZK history under control. It also opens an ability to
easily backup it to any Git hosting of your choice.

To use some of the Git interaction commands you have it set up correctly
(at the beginning, setting [commit name and
email](https://git-scm.com/book/en/v2/Getting-Started-First-Time-Git-Setup)
will be enough).

Probably, a convenient approach for creating a Git remote is to create a
private `zet` repository on any online Git hosting of your choice. Then,
you can easily point to it with this command:

    pyzet remote add origin https://some-git-hosting/your-username/zet

Its equivalent is going directly to `~/zet` folder and executing `git
remote add...` command.

If the above command doesn't work for you, your Git executable is
probably installed in some non-default location for your system. Example
error in such situation:

    ERROR: '/usr/bin/git' cannot be found.

To tell pyzet where to look, you need to add another line to the config
file:

    git: <path-to-your-git-executable>

If your Git executable in on `PATH`, the following should work for you:

    git: git

Pyzet comes with a few more commands that allow for easier interaction
with Git, and they will be discussed later in this tutorial.

## Basic interaction with zettels

Now, you can proceed with adding your first zettel with `pyzet add`.

The text editor should open. By default, it will be Vim. If you prefer
something else, you can add another line to the config file:

    editor: <path-to-your-editor>

However, not every editor might work seamlessly with pyzet. In the [main
readme](https://github.com/wojdatto/pyzet#supported-editors) you can see
a list of editors with some comments about their compatibility.

Once you're happy with the text editor, add some example text using
[Markdown](https://commonmark.org/) syntax:

```markdown
# This is my first zettel created with pyzet

The above line is the title of this zettel, and this is part of
its contents. It's a good practice to wrap lines like that, so zettels
are easier to read in the terminal.

Refs:

* This way you can add links\
  <https://github.com/wojdatto/pyzet>

Tags:

    #tutorial
```

You can see that we used a special syntax to add a link. You can read
more about it in the [main
readme](https://github.com/wojdatto/pyzet#references), but note that at
this point it's only a convention.

Save the file and exit from your editor. You should see a similar
output:

    $ pyzet add
    20220126232605 was created
    [main (root-commit) 7d40260] This is my first zettel created with pyzet
    1 file changed, 14 insertions(+)
    create mode 100644 zettels/20220126232605/README.md

Now, you can run `pyzet show` to see your zettel:

    $ pyzet show
    ============================ 20220126232605 ============================
    # This is my first zettel created with pyzet

    The above line is the title of this zettel, and this is part of
    its contents. It's a good practice to wrap lines like that, so zettels
    are easier to read in the terminal.

    Refs:

    * This way you can add links\
      <https://github.com/wojdatto/pyzet>

    Tags:

        #tutorial

If you made a typo, you can edit your zettel with `pyzet edit` command.

Now, let's make a second zettel with `pyzet add`:

```markdown
# This is my second zettel

A short one :D

Tags:

    #tutorial #example-tag
```

Again, you can show it with `pyzet show`:

    $ pyzet show
    ============================ 20220123233028 ============================
    # This is my second zettel

    A short one :D

    Tags:

        #tutorial #example-tag

You might ask, "well, how can I show the first zettel now?". The
behavior of `pyzet show` is simple: by default it shows the zettel with
the highest ID (i.e. the latest one). To see older zettels, you have to
provide an ID.

But how can you obtain the ID of the first zettel? It's a pretty long
number, right?

The simplest way is to show a list of all zettels, and copy it. You can
do it with `pyzet list`:

    $ pyzet list
    20220126232605 -- This is my first zettel created with pyzet
    20220126232716 -- This is my second zettel

BTW, these numbers are not random. They actually follow special
timestamp format that consists of the current year, month, day, hour,
minute, and second in this very exact order. The hour, though, will most
likely not match your local time. This is done on purpose -- we use
UTC+0 to make sure that each ID is unique (at least, as long as you
don't try to create multiple zettels at the same second :p)

You can see that my ID of the first zettel was `20220126232605`. We can
now paste it to the `show` command:

    $ pyzet show 20220126232605
    ============================ 20220126232605 ============================
    # This is my first zettel created with pyzet
    <snip>

We mentioned that you can edit a zettel with `pyzet edit` command. As
you might guess, it also works with the last zettel by default, and you
need to provide an ID to edit an older zettel.

## Rage quit option

If you ever mess up during the editing of your zettel or you would like
to cancel adding of the new zettel, there is always a way to withdraw --
just remove *everything* from a zettel. This aborts the adding/editing
process making no actual changes on the drive, and in the Git repo.

## Tags

As you might saw, we added some tags in our zettels. There is a `pyzet
tags` command that allows you to interact with them:

    $ pyzet tags
    1       #example-tag
    2       #tutorial

The number shows how many times each tag was used in your Zettelkasten
repository. You can use it to maintain more coherent tag naming over
time. There are also some additional options, you can see them with
`pyzet tags -h` (and this is true for almost every command, BTW).

## Removing zettels

There is also `pyzet rm` command that allows you to remove a zettel.
It's a bit different: you have to provide the ID each time, even for the
newest zettel, e.g. to remove my second zettel we should run the
following:

    $ pyzet rm 20220126232716
    20220126232716 will be deleted including all files that might be inside. Are you sure? (y/N): y
    /home/<your-username>/zet/zettels/20220126232716/README.md was removed
    [main 009b935] RM: This is my second zettel
    1 file changed, 7 deletions(-)
    delete mode 100644 zettels/20220126232716/README.md
    /home/<your-username>/zet/zettels/20220126232716 was removed

As you can see, we had to confirm the deletion with `y` (capitalization
matters). Pressing `Enter` or any other key will abort the process.

Because pyzet uses Git, the removed zettel is still available in the Git
history. In order to completely remove it, you need to purge it
completely from the Git history which means that you need to rewrite it
(i.e. remove any commit that involved adding/editing such zettel, and
rebase commits that happened later.)

## More interaction with Git repo

Pyzet ships with a few commands that make it easier to interact with a
Git repo. However, the work is always done by Git executable itself --
pyzet just calls it with the correct parameters.

The simplest command is `pyzet status` -- it just runs `git status` in
your ZK repo:

    $ pyzet status
    On branch main
    nothing to commit, working tree clean

### Push and pull from Git remote

For the remaining Git-interaction commands, you have to make sure that
your Git configuration including name, email, and remote is correct.

Once you're ready, you can try out these commands:

* `pyzet push` -- runs `git push` in your ZK repo
* `pyzet pull` -- runs `git pull` in your ZK repo

By default, these commands probably won't work for you because you have
to tell Git which remote branch it should track. If you're new to Git,
you can check the [official
tutorial](https://git-scm.com/book/en/v2/Git-Branching-Remote-Branches).

### Passing flags to Git interaction commands

You have to note that there is a special syntax for passing flags to Git
interaction commands. A flag is an argument that starts with either a
single dash `-` or a double dash `--`, e.g. `-f` / `--force` for Git
force push to a remote.

To pass these flags to a Git executable you have to tell pyzet not to
parse them on its own.

It can be done by adding a special pseudo-argument `--` before passing
any of the flags that should be passed directly to Git (you can find
more details about it in the [argparse
docs](https://docs.python.org/3/library/argparse.html#arguments-containing)).

E.g. to do the mentioned force push with `pyzet push` you have to:

    pyzet push -- -f

Note that there is some freedom regarding the exact placement of `--`
argument.

E.g. we can bring back `pyzet remote` command. To add a new remote we
used the following command:

    pyzet remote add origin https://some-git-hosting/your-username/zet

And to add a `--tags` flag to `pyzet remote add` you have to use either
of the following:

    pyzet remote add origin -- --tags https://some-git-hosting/your-username/zet
    pyzet remote add -- origin --tags https://some-git-hosting/your-username/zet
    pyzet remote -- add origin --tags https://some-git-hosting/your-username/zet

At the end, the only thing to remember is to include `--` before any
**Git flag**, but after the main action keyword (here: `remote`). So,
the following **won't** work:

    pyzet remote add origin --tags -- https://some-git-hosting/your-username/zet
    pyzet -- remote add origin --tags https://some-git-hosting/your-username/zet

### Git interaction summary

Overall, Git integration is very simple, because pyzet don't want to
complicate Git-related stuff more than it's needed. We think that one
branch is enough, and for more sophisticated Git-related work you can
just `cd ~/zet`, and run Git commands directly.

Below, there is also a description of `pyzet grep` command which is the
last one directly interacting with Git.

## Search for anything using grep

Grep is your friend when you try to look for something in your ZK repo.
`pyzet grep` command works by running `git grep` with some handy default
flags.

Unlike `pyzet remote|status|push|pull`, this command offers some
additional options, and you can check them out with `pyzet grep --help`.

Of course, you can still pass custom options directly to `git grep` with
`--`, as it was described earlier.

Also, remember that `pyzet grep` will by default look only in files that
are already tracked by Git.

### Simple example

Now, let's try running a grep search in our repo. Let's use `zettel` as
a search pattern:

    $ pyzet grep zettel
    20220123233028/README.md
    # This is my second zettel

    20220126232605/README.md
    # This is my first zettel created with pyzet
    The above line is the title of this zettel, and this is part of
    its contents. It's a good practice to wrap lines like that, so zettels

As you can see, we've got three matches in our two files. In your
output, you should also see some nice coloring (e.g. matched pattern
colored with red) if only your terminal configuration supports it.

### Passing multiple patterns

One of nice features of `pyzet grep` is the ability to provide multiple
patterns, one after another. In such case, the output will include only
zettels which contain all of provided patterns in their content.

E.g. by looking for both `zettel` and `part` only one of our zettels
will be listed:

    $ pyzet grep zettel part
    20220126232605/README.md
    # This is my first zettel created with pyzet
    The above line is the title of this zettel, and this is part of
    its contents. It's a good practice to wrap lines like that, so zettels

This will be especially helpful in bigger Zettelkasten repos, where
there are a lot of zettels, and you would like to limit the number of
matches.

However, you have to remember that your patterns need to go one after
another, e.g this will work:

    $ pyzet grep --line-number zettel part
    20220126232605/README.md
    1:# This is my first zettel created with pyzet
    3:The above line is the title of this zettel, and this is part of
    4:its contents. It's a good practice to wrap lines like that, so zettels

And this will also work, but only if you don't pass custom parameters
with `--`:

    $ pyzet grep zettel part --line-number
    20220126232605/README.md
    1:# This is my first zettel created with pyzet
    3:The above line is the title of this zettel, and this is part of
    4:its contents. It's a good practice to wrap lines like that, so zettels

With `--`, argument parser raises an exception:

    $ pyzet grep zettel part --line-number -- --no-color
    pyzet: error: unrecognized arguments: -- --no-color

And this won't work either because grep patterns were split:

    $ pyzet grep zettel --line-number part
    pyzet: error: unrecognized arguments: part

### Grep and `.gitattributes`

You might come into a situation in which `pyzet grep` shows you results
from files that you are not interested in, e.g. SVG graphics which are
not binary and contain a lot of correct English words. It is possible to
filter these results out by telling Git to treat these files like
binary. This can be done by creating a `.gitattributes` file in your ZK
repo. E.g. to filter out SVG, use the following syntax.

    *.svg binary

You can find more information about it in [Git
Docs](https://git-scm.com/docs/gitattributes#_using_macro_attributes).

## Clean command

The last command to go through is `pyzet clean`. It works a bit
similarly to `git clean` but targets a very specific use case: it
removes empty folders at your ZK repo.

Let's try it. At first, let's create an empty folder with `mkdir
~/zet/zettels/test`. Now, we can run the command:

    $ pyzet clean
    will delete test
    Use '--force' to proceed with deletion

Let's do as asked:

    $ pyzet clean --force
    deleting test

And the folder was removed. If you ever happen to have an empty folder
that matches the timestamp syntax used by pyzet, `pyzet list` output
will show a warning about it. We can simulate it:

Let's remove `REAMDE.md` from our only zettel:

    rm ~/zet/zettels/20220126232605/README.md

And now, list the zettels:

    $ pyzet list
    WARNING: empty zet folder 20220126232605 detected
    ERROR: there are no zettels at given repo.

Now you can just run `pyzet clean --force` to get rid of this warning.

## Summary

This concludes the tutorial. It should give you a basic idea how to use
pyzet, and create your own ZK repository with it.

If you're new to the Zettelkasten, it might be helpful to read more
about it. We suggest to go through *Inspiration and further reading*
section in the [main
readme](https://github.com/wojdatto/pyzet#inspiration-and-further-reading).

If you have any problem, question, or suggestion, feel free to create an
issue on GitHub. We have many ideas how to expand pyzet, so make sure to
go through [opened issues](https://github.com/wojdatto/pyzet/issues)
first. **Any feedback is welcome!**
