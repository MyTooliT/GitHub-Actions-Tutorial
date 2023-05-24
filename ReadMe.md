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

GitHub Actions, like most other CI systems (I know of), reads actions it should execute from [YAML](https://yaml.org) files. These (workflow) files should be stored in the directory `.github/workflows` in the root of the repository.

In our first example we will create a rather minimal version of such a workflow file:

```yaml
on:
  - push

jobs:
  linux:
    runs-on: ubuntu-latest

    steps:
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
