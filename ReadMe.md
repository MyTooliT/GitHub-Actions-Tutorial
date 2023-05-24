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

GitHub Actions, like most other CI systems (I know of), reads actions it should execute from [YAML](https://yaml.org) files.
