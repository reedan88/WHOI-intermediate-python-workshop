---
title: "Getting Started"
---

This page walks you through everything you need to do **before Session 1**.
Please finish it at least a day ahead. The downloads are large, and we will
**not** have time to troubleshoot installations during the workshop.

It takes about 30 to 45 minutes, most of it waiting for downloads. Use a
reliable internet connection (not a conference hotspot), and plug in your
laptop.

::::::::::::::::::::::::::::::::::::: checklist

## What you need

- A laptop running **Windows, macOS, or Linux** that you are allowed to
  install software on. If it is managed by your institution, see the
  troubleshooting notes at the bottom of this page.
- About **5 GB of free disk space** and, we recommend, **8 GB of memory (RAM)**.
  The notebook loads a full deployment of instrument data.
- Three tools, which this page helps you install:
  1. **git**, for version control
  2. **uv**, which installs Python and manages your packages
  3. A free [GitHub](https://github.com/signup) account
- The **workshop starter files** (a notebook and two data files, about
  1 GB in total).

You do **not** need to install Python, Jupyter, Anaconda, or conda
separately. `uv` takes care of Python and every package we use.

::::::::::::::::::::::::::::::::::::::::::::::::

## Step 0: Open a terminal

Most of the commands on this page are typed into a **terminal**, a window
where you type commands instead of clicking. Copy each command exactly, press
Enter, and wait for it to finish before typing the next one.

- **Windows:** use **Git Bash**, a terminal that is installed together with
  git in Step 1. Open the Start menu, type `Git Bash`, and open it. Use Git Bash
  for every command in this workshop (not PowerShell or Command Prompt), so
  that the commands are the same on Windows, macOS, and Linux. Because Git Bash
  comes with git, **Windows users should do Step 1 first.**
- **macOS:** press `Cmd` + `Space`, type `Terminal`, and press Enter.
- **Linux:** press `Ctrl` + `Alt` + `T`, or search your applications for
  "Terminal".

## Step 1: Install git

:::::::::::::::: spoiler

### Windows

Download and run the installer from
[git-scm.com/download/win](https://git-scm.com/download/win), accepting the
default options. This installs both git and **Git Bash**. (If you use WinGet,
running `winget install --id Git.Git -e` in PowerShell does the same thing.)

When it finishes, open **Git Bash** from the Start menu. Type all the
commands on this page there. You can also right-click inside any folder in
File Explorer and choose **Open Git Bash here** (on Windows 11 it may be under
**Show more options**), which opens Git Bash already in that folder.

::::::::::::::::::::::::

:::::::::::::::: spoiler

### macOS

Git is often already installed. Type `git --version` in Terminal. If git is
missing, macOS offers to install the "command line developer tools"; accept
the offer and wait for it to finish.

::::::::::::::::::::::::

:::::::::::::::: spoiler

### Linux

Install git with your package manager, for example `sudo apt install git`
(Debian, Ubuntu) or `sudo dnf install git` (Fedora).

::::::::::::::::::::::::

On macOS and Linux, close your terminal and open a new one. On Windows, you
are already in Git Bash. Check that it worked:

```bash
git --version
```

```output
git version 2.47.0
```

Your version number will differ. Any recent version is fine.

Next, tell git who you are. Git stamps this on every commit you make, and
it will refuse to commit in Session 2 without it. Use your own name and
email:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.org"
```

## Step 2: Create a GitHub account

If you do not already have one, create a free account at
[github.com/signup](https://github.com/signup). Session 2 is about building
a repository you can share, and GitHub is where most people host one.

## Step 3: Install uv

[uv](https://docs.astral.sh/uv/) is the one tool we use for Python itself,
for environments, and for packages.

:::::::::::::::: spoiler

### Windows

In Git Bash, run:

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

This uses Windows' built-in PowerShell only to run uv's installer; you keep
typing in Git Bash. Or, if you use WinGet, run
`winget install --id=astral-sh.uv -e` in Git Bash instead.

::::::::::::::::::::::::

:::::::::::::::: spoiler

### macOS

In Terminal, run:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Or, if you use Homebrew: `brew install uv`.

::::::::::::::::::::::::

:::::::::::::::: spoiler

### Linux

In a terminal, run:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

::::::::::::::::::::::::

**Close your terminal (on Windows, every Git Bash window) and open a new
one.** This step is easy to skip and
the most common reason for a "command not found" error right after
installing. Then check that uv works:

```bash
uv --version
```

```output
uv 0.11.32
```

Your version number will differ. Any recent version is fine.

## Step 4: Download the starter files

Download **`starter-files.zip`** from the lesson's
[Releases page](https://github.com/WHOIGit/WHOI-intermediate-python-workshop/releases/latest)
and unzip it to a folder you will be able to find again, for example a new
folder called `workshop` in your Documents folder.

::::::::::::::::::::::::::::::::::::: caution

Use the zip file from the **Releases** page. Do not use GitHub's green
"Code → Download ZIP" button for this: it does not include the large data
files.

::::::::::::::::::::::::::::::::::::::::::::::::

After unzipping you should have:

```text
starter-files/
├── README.md
├── first_analysis.ipynb
└── data/
    ├── gi01sumo_nsif_ctd.nc
    └── gi01sumo_nsif_dosta.nc
```

The two `.nc` files are real
[OOI](https://oceanobservatories.org/) data, so they are large: roughly
120 MB for the CTD file and 800 MB for the DOSTA file. If either file is
only a few hundred **bytes**, you have a text placeholder and not the data.
Download the zip again.

## Step 5: Run the dress rehearsal

This step downloads every package we use, so that the workshop itself does not
have to. It also proves that your setup works end to end.

**1.** In your terminal, move into the `starter-files` folder. Replace the
path below with wherever you unzipped it:

```bash
cd ~/Documents/workshop/starter-files
```

On Windows, Git Bash understands `~` as your user folder (`C:\Users\yourname`)
and uses forward slashes. If your Documents folder is synced by OneDrive, the
path is probably `~/OneDrive/Documents/workshop/starter-files`. A drive letter
is written like `/c/`, for example `/c/Users/yourname/Documents`. The easiest
route is to open the `starter-files` folder in File Explorer and choose
**Open Git Bash here**.

**2.** Start JupyterLab with all the packages the workshop uses:

```bash
uv run --no-project --with jupyterlab --with xarray --with netCDF4 --with pandas --with numpy --with matplotlib jupyter lab
```

The first time, this prints many "Downloading..." lines and can take several
minutes. That is normal. When it finishes, JupyterLab opens in your web
browser. If no browser window appears, look in the terminal for a line
starting with `http://localhost:8888/lab?token=` and copy that whole address
into your browser.

**3.** In JupyterLab, open `first_analysis.ipynb` from the file list on the
left. Click the first cell and press `Shift` + `Enter` to run it, then do the
same for the second cell. Neither should print an error.

**4.** Click an empty cell at the bottom, type the following, and press
`Shift` + `Enter`:

```python
print(ctd.sizes)
print(dosta.sizes)
```

You should see two lines, each reporting a number of points along `time`,
something like `Frozen({'time': 1234567})`. The numbers will differ from this
example; what matters is that both lines print and neither is an error.

**5.** To shut JupyterLab down, go back to the terminal and press `Ctrl` + `C`.
If it asks whether to shut down, type `y` and press Enter.

**6.** Run the command from step 2 again. This time JupyterLab should start
within a few seconds, because uv reuses what it already downloaded.

::::::::::::::::::::::::::::::::::::: discussion

### What do `--no-project` and `--with` mean?

`--with jupyterlab` (and the others) asks uv to build a temporary environment
that contains those packages and run the command inside it. `--no-project`
tells uv not to look for a `pyproject.toml` in the current folder, because you
have not made a project yet. In Session 2 you will create one, and it will
record these packages for you.

::::::::::::::::::::::::::::::::::::::::::::::::

## Step 6 (optional): Pick an editor

You can do the whole workshop in JupyterLab. If you already prefer another
editor, such as VS Code or PyCharm, that is fine too. VS Code with its Python
and Jupyter extensions works well for editing the `.py` modules you will
write next to your notebook.

## You are ready when...

::::::::::::::::::::::::::::::::::::: checklist

- `git --version` prints a version number
- `git config --global user.name` prints your name
- `uv --version` prints a version number
- You can log in to GitHub
- You launched JupyterLab from the `starter-files` folder, ran the first two
  cells of `first_analysis.ipynb`, and `print(ctd.sizes)` worked

::::::::::::::::::::::::::::::::::::::::::::::::

If something on the list does not work and the troubleshooting notes below
do not fix it, email the instructors **before** the workshop. We would much
rather sort it out beforehand.

## Troubleshooting

**`uv: command not found`.** Close every terminal window (on Windows, every
Git Bash window) and open a new one. The installer changes your search path,
and only new terminals see the change.

**The download stalls, fails, or is blocked.** Institutional networks and VPNs
sometimes block software downloads. Try again off the VPN, or on a different
network. If you are on a managed laptop, your IT group may need to allow
downloads from `astral.sh`, `pypi.org`, `files.pythonhosted.org`, and
`github.com`. If you cannot install software at all, tell the instructors
right away so we can find a workaround.

**Windows: the uv install command says running scripts is disabled.** The
install command above already bypasses that setting for this one command. If
your organization blocks it anyway, use the `winget` command instead, or ask
your IT group.

**JupyterLab does not open in a browser.** Copy the `http://localhost:8888/...`
address from the terminal and paste it into your browser. If port 8888 is
already in use, JupyterLab picks the next free port and prints that address.

**`FileNotFoundError: ... data/gi01sumo_nsif_ctd.nc`.** JupyterLab was started
from the wrong folder. Press `Ctrl` + `C` in the terminal, `cd` into the folder
that contains both `first_analysis.ipynb` and the `data` folder, and run the
launch command again.

**The `.nc` files are tiny (a few hundred bytes).** They are placeholders. See
Step 4.

**The kernel died or the computer ran out of memory.** Close other programs,
especially web browsers with many tabs, and run the cells again. If it keeps
happening, tell the instructors which computer and how much memory it has.

**Something else.** Copy the full error message from the terminal and send
it to the instructors. A screenshot of the whole terminal window is even better.
