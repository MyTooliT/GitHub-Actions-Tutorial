---
title: GitLab CI/CD-Tutorial
author: IFT
description: Very basic tutorial on how to use GitHub Actions based in part on [GitLab CI Tutorial](https://git.ift.tuwien.ac.at/lab/ift/sis/gitlab-ci-tutorial)
---

# GitHub Actions Tutorial

**Disclaimer:** While I worked with multiple CI systems (Circle CI, Jenkins, GitHub Actions, GitLab CI, Travis) in the past, I was never more than a user of these systems. Therefore I would recommend to **take all information below with a grain** (or multiple kilos 😅) **of salt**.

## Usual Tasks of CI(/CD) Systems

- **Code analysis** (e.g type checking, style checks)
- **Test** execution
- **Software packaging** (compilation)
- Building **documentation** (e.g. HTML/PDF documentation)
- **Deployment**:
  - Store packages/documentation at correct location
  - Start/stop (web) services

## Hello World

GitHub Actions, like most other CI systems (I know of), reads actions/commands it should execute from [YAML](https://yaml.org) files. These (workflow) files are stored in the directory `.github/workflows` in the root of the repository.

In our first example we will create a rather minimal version of such a workflow file:

```yaml
on:
  # Execute workflow every time we push changes to remote
  - push

jobs:
  linux:
    # Execute actions/command on latest Ubuntu version
    # For more information on available “runners”, please take
    # a look here:
    # https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners#supported-runners-and-hardware-resources
    runs-on: ubuntu-latest

    # A workflow contains multiple steps (actions/commands), which are
    # executed after each other. Our workflow contains only a single step.
    steps:
      # In this step we use the key `run` to execute the command `printf` and
      # print the text “Hello, World” to the (standard output)
      - run: printf 'Hello, World\n'
```

To execute the workflow above we need to follow the steps below:

1. Create a Git repository
2. Store the YAML content above in the file `hello.yaml` in the directory `.github/workflows`
3. Create a commit containing `hello.yaml`
4. Publish the repository at [GitHub](https://github.com)

After you followed the steps above you should be able to see the execution of the CI run in the repository web page under the tab **“Actions”**:

<img src="Pictures/Hello World Run.webp" alt="Hello World Run" width="600"/>

After you click on the commit message – “CI: Add “Hello World” workflow” in the example above – GitHub should show you are more detailed description about the workflow run:

<img src="Pictures/Hello World Details.webp" alt="Hello World Details" width="600"/>

The picture above shows us that out workflow contains exactly one job called `linux`. We now click on the job to see a detailed view of the job output:

<img src="Pictures/Hello World Output.webp" alt="Hello World Output" width="600"/>

The “Set up job” section tells us some information about the runner (computer that executed the job). For example, we can see that the operating system of the runner is Ubuntu `22.04.2`, because we used the value `ubuntu-latest` for the key `runs-on`.

The section “Run printf 'Hello, World\n'” shows us the output of our only workflow step. Just like we expected the shell command we used (`printf …`) prints the text “Hello, World”.

### Describing a Workflow

While navigating the workflow and the output for our small example was reasonable, it makes sense to describe

- the workflow,
- the jobs (that are part of a workflow) and
- the steps (that are part of a job)

further. To do that we can use the key `name`. Let us add some basic description to our “Hello World” workflow:

```yaml
name: Hello World

on:
  - push

jobs:
  linux:
    name: 🐧 Ubuntu
    runs-on: ubuntu-latest

    steps:
      - name: Print “Hello, World”
        run: printf 'Hello, World\n'
```

After we commit and push our changes the list of workflows:

<img src="Pictures/Hello World Workflows.webp" alt="Hello World Workflows" width="300"/>

the job name:

<img src="Pictures/Hello World Job.webp" alt="Hello World Job" width="250"/>

and our job step:

<img src="Pictures/Hello World Step.webp" alt="Hello World Step" width="350"/>

displays the name we provided.

## Command Return Values & Failing Jobs

In our “Hello World” example, everything worked as expected and hence the CI run finished with the status “passed” displaying a green checkmark. How does a certain (test) command then tell that something went wrong. The usual way is the return value of the command, also often called **exit or status** value. The status value is a number that will/should be

- **`0`** if everything **worked as expected** or
- **any other number than `0`** (often `1`) if the command did **not finish successfully**.

Usually you can also **tell certain errors apart from their return value**. For example most shells return `127` if a command was not found.

There are even two simple commands `false` and `true` that do nothing except for setting the status value to:

- `0`: `true` and
- `1`: `false`.

These values might be **inverted to what you expect from other programming languages** like C, where `0` represents false and all other numbers represent true.

If you want to set the exit value in a program yourself you can usually use a function called `exit` or something similar. For example, you can use the following line of Python code to write your own version of the command `false`:

```py
exit(1)
```

Now lets add a new workflow called “Return Values” that we store in a file called `return.yaml` in the directory `.github/workflows`:

```yaml
name: Return Values

on:
  - push

jobs:
  linux:
    name: 🐧 Ubuntu
    runs-on: ubuntu-latest

    steps:
      - name: Execute command that sets return value to 1
        # Quotes are required, since the text `false` represent the
        # **boolean value “false”**. The text `"false"` (with quotes)
        # on the other hand represent the **string `false`**.
        run: "false"
```

After we push our changes we see that there are now two workflows listed under the “Actions” tab of the repository page:

<img src="Pictures/Multiple Workflows.webp" alt="Multiple Workflows" width="300"/>

> **Note:** Workflows are independent of each other, which makes them ideal for doing tasks that are quite different. For example you can use a workflow that builds and deploys documentation, while another workflow tests the software.

While the workflow “Hello World” finished successfully, just like before, the workflow “Return Values” failed as we expected:

<img src="Pictures/Overall Status.webp" alt="Overall Status" width="300"/>

We take a closer look and see that the step “Execute command that sets return value to 1” did indeed set the exit value to 1:

<img src="Pictures/Return Value False.webp" alt="Return Value False" width="450"/>

## Multiple Steps

Since we now know how we can write a basic workflow containing a single step it is time to look at how we can execute jobs after each other. For that purpose we remove `hello.yaml` and `return.yaml` and add a new workflow called `multiple steps.yaml` in the directory `.github/workflows`:

```yaml
name: Sequential Execution

on:
  - push

jobs:
  linux:
    name: 🐧 Ubuntu
    runs-on: ubuntu-latest

    steps:
      - name: Works
        run: "true"

      - name: Fails
        run: "false"

      - name: Works too
        run: "true"
```

As you can see this workflow contains three jobs called

- “Works”,
- “Fails” and
- “Works too”.

These steps will be executed one after each other. The whole job will fail after the first step that fails. Steps after the first failed step will not be executed. We can see that, if we take a look at the output of our job:

<img src="Pictures/Multiple Steps.webp" alt="Multiple Steps" width="200"/>

## Checking Source Code

Since we are already a little familiar with GitHub Actions it is time to move to our first example that might also be useful in our own projects.

To increase the quality of the code we write we can use (static) **source code checkers** that analyze code and provide suggestions to make it better. In the text below we will write some Python code and then use the style checker [Flake8](https://flake8.pycqa.org) to analyze it.

First we store the simple code for a “Hello World” program below:

```py
import math

print("Hello, World!")
```

in a file called `source.py` in the root of our repository. To check the file locally we install `flake8` with `pip`:

```sh
pip install flake8
```

and then execute the command:

```sh
flake8
```

in the root of the repo. The output of the command:

```
./source.py:1:1: F401 'math' imported but unused
```

will tell us that the first line in our source code is more or less useless. Great! Now it is time to move the check for our source code into a GitHub Actions workflow. For that purpose we store the following code in `check.yaml` in the directory `.github/workflows` and remove `multiple steps.yaml`.

```yaml
name: Check Code

on:
  - push

jobs:
  linux:
    name: 🐧 Ubuntu
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Install Flake8
        run: python3 -m pip install flake8

      - name: Check code with Flake8
        run: flake8 .
```

Compared to our previous examples, we notice the new key `uses` in the “Checkout code” step. Here we use the [Checkout “action” provided by GitHub](https://github.com/actions/checkout) instead of relying on a Shell command (key `run`), like we did previously. As you might expect the `checkout` action clones the repository to the current runner, i.e. the computer that executes the workflow.

> **Note:** Usually it makes sense to prefer one of the many [available actions](https://github.com/marketplace?category=&query=&type=actions) to writing the Shell commands yourself, unless your code is trivial. Using “custom” actions usually has the advantages, that you
>
> - receive bug fixes for free and
> - do not need to tailor your code for the [different operating systems of the runner images](https://github.com/actions/runner-images#available-images).

After we commit our files and push the changes, the job “🐧 Ubuntu” in the workflow “Check Code” should fail:

<img src="Pictures/Failed Run Flake8.webp" alt="Failed Run Flake8" width="400"/>

Now it is time to fix `source.py`:

```sh
print("Hello, World!")
```

and check that the workflow runs successfully after we push the changes:

<img src="Pictures/Successfull Run Flake8.webp" alt="Successfull Run Flake8" width="300"/>

## Multiple Jobs

Until now we only used a single job. Often you want to run **multiple things in parallel**. For that purpose you can use an additional job. Let us extend our example from before. This time we also check the code with [mypy][], a static type checker for Python code. We now store the following code in the file `source.py`:

[mypy]: http://mypy-lang.org

```py
def add(*numbers: float) -> None:
    print(f"{' + '.join(map(str, numbers))} = {sum(numbers)}")


add(1, 2, 3)
add(4, 5, '6')  # Argument 3 has incorrect type
```

In the last line of the code above the third argument to `add` is incorrect (`str` instead of `float`). We can find this bug if we just run the code directly:

```sh
python source.py
```

and see that the script fails with a `TypeError`:

```
1 + 2 + 3 = 6
Traceback (most recent call last):
  File "source.py", line 6, in <module>
    add(4, 5, '6')  # Argument 3 has incorrect type
    ^^^^^^^^^^^^^^
  File "source.py", line 2, in add
    print(f"{' + '.join(map(str, numbers))} = {sum(numbers)}")
                                               ^^^^^^^^^^^^
TypeError: unsupported operand type(s) for +: 'int' and 'str'
```

However, you usually want to find such errors even before you start a script. Sometimes a **buggy line of code might only be executed under some special circumstances**. In this case you might assume that the code works perfectly fine, even though it contains a serious bug.

To detect such problems, even before you start a script, you can use **static type checkers** like [mypy][]:

```sh
pip install mypy
```

We first check our script locally:

```sh
mypy source.py
```

and see the following helpful output:

```
source.py:6: error: Argument 3 to "add" has incompatible type "str"; expected "float"  [arg-type]
Found 1 error in 1 file (checked 1 source file)
```

Now it is time to automate the type checking process. While we could use the same job to run both `flake8` and `mypy` we will use two jobs to run these tools in parallel. For our tiny amount of code this might not make much sense, but if your code base is getting bigger running things in parallel might save quite some time.

We update `check.yaml`:

```yaml
name: Check Code

on:
  - push

jobs:
  linux:
    name: 🐧 Flake8
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Install Flake8
        run: python3 -m pip install flake8

      - name: Check code with Flake8
        run: flake8 .

  windows:
    name: 🪟 Mypy
    runs-on: windows-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Install mypy
        run: python3 -m pip install mypy

      - name: Check code with mypy
        run: mypy source.py
```

Here we used a Windows runner for mypy, not because it makes much sense, but just to show how we can change the runner image, if we want to use a different operating system to execute the code.

> **Note:** If you do not care about the operating system it makes sense to use a Linux runner. Not only do Linux runners usually start faster, they [are also cheaper](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions#minute-multipliers) compared to Windows and especially macOS runners, if you use them (in a private repository).

Now it is time to commit our changes (to `source.py` & `check.yaml`) and push the changes to the remote repository. If we take a look at the latest run of the “Check Code” workflow we see the two independent jobs:

<img src="Pictures/Failed Run mypy.webp" alt="Failed Run mypy" width="350"/>

As expected the job `🪟 Mypy` failed, because of the bug in the last line of the script. Flake8 on the other hand was perfectly happy how we formatted/structured the Python code. In a last step we fix the bug in `source.py`:

```py
add(4, 5, 6)  # Argument 3 has correct type
```

and commit the fixed code. After that both jobs run successfully:

<img src="Pictures/Successfull Run mypy.webp" alt="Successfull Run mypy" width="350"/>

## Using Multiple Software Versions

Sometimes you might want to use the same steps in a job, but use different software (versions) to execute the steps. For example, you might want to change the operating systems or use different Python versions to test software. While you could just copy and paste code and change minor parts of the copied YAML code this can get unwieldy soon. To improve this situation GitHub Actions supports the [`matrix` keyword to define job variations](https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs).

In the following example we will check if the modified Python code (`source.py`):

```py
from pathlib import Path

example_path = Path("some") / "directory" / "something.txt"
example_path_changed_stem = example_path.with_stem("something else")

print(f"Original:     {example_path}")
print(f"Changed stem: {example_path_changed_stem}")
```

works on

- Linux,
- macOS and
- Windows

using the Python versions:

- `3.8`,
- `3.9`,
- `3.10`, and
- `3.11`.

For that purpose we update `test.yaml`:

```yaml
name: Check Code

on:
  - push

jobs:
  os-python-matrix:
    strategy:
      matrix:
        os:
          - name: macos
            icon: 🍏
          - name: ubuntu
            icon: 🐧
          - name: windows
            icon: 🪟
        python-version:
          - "3.8"
          - "3.9"
          - "3.10"
          - "3.11"

    runs-on: ${{ matrix.os.name }}-latest
    name: ${{ matrix.os.icon }} Python ${{ matrix.python-version }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Run example script
        run: python source.py # Fails on Python 3.8
```

We use the key `os-python-matrix` (you can choose any non-reserved name here) to define a matrix containing

- three list elements below the key `os` and
- four elements below the key `python-version`.

This means that GitHub Actions will create 12 jobs (3·4), where `os` and `python-version` will store every possible combination of the list values. For example, the first job will store the dictionary:

```yaml
name: mac
icon: 🍏
```

in `os` while `python-version` will store the string:

```yaml
"3.8"
```

To access the values of the matrix we use the [expression](https://docs.github.com/en/actions/learn-github-actions/expressions) syntax `${{ variable }}`.

This way we can make the value of the following variables dynamic:

- `runs-on` to change the used operating system
- `python-version` in the [Setup Python](https://github.com/actions/setup-python) action to change the used Python version

After we deploy our updates we see that from the 12 jobs:

<img src="Pictures/Job Matrix.webp" alt="Job Matrix" width="150"/>

the job that uses Python `3.8` on Linux failed. The other jobs on Linux finished successfully. The jobs on the other operating systems were canceled, because of the failure of the Linux job.

If we take a closer look at the failed job “🐧 Python 3.8” we see that the `Path` class in Python `3.8` does not support the method `with_stem`

<img src="Pictures/AttributeError Path.webp" alt="Attribute Error Path Object" width="500"/>

To fix this problem we decide to not support Python 3.8 with our script and just remove the line:

```yaml
- "3.8"
```

from `test.yaml`. After we do that we see that out code runs successfully for all of the remaining 9 OS/Python combinations:

<img src="Pictures/Job Matrix Fixed.webp" alt="Job Matrix Fixed" width="150"/>

## ToDo

- [ ] Combined Actions
- [ ] Dependent jobs (`needs` keyword)
