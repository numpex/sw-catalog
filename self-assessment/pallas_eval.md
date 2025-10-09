# Pallas Package

## Packaging

Software should be packaged (preferably using Spack or Guix package formats). They should be published in public (community controlled) package repositories (Guix-science, etc.).

* [x] Packages exist
* [x] Packages are published in an easily usable repository
* [x] Packages installation is tested on supercomputers
* [x] Packages are available in community repositories
  - Guix https://gitlab.inria.fr/guix-hpc/guix-hpc
* [x] either Guix or Spack packages are available
* [ ] both Guix and Spack packages are available

## Minimal Validation Tests

Software should include minimal validation tests triggered through automated mechanism such as Guix. These tests should be automatic functional tests that do not require specific hardware.

* [x] unit tests exist
* [x] CI exists
* [x] CI runs regularly (each new release)
* [x] CI runs regularly (each new commit in main branch)
  - https://gitlab.inria.fr/pallas/pallas/-/pipelines

## Public Repository

A public repository, must be available for at least the development version of the software, allowing for pull requests to be submitted.

* [x] A repository where sources can be downloaded by anyone
  - https://gitlab.inria.fr/pallas/pallas
* [x] A repository where anyone can submit a modification proposition (pull request)
  - https://github.com/Pallas-Trace/pallas

## Clearly-identified license

Sources should be published under a clearly-identified free software license (preferably with REUSE)

* [x] Licence is clearly stated
* [x] Licence is FLOSS licence (FSF or OSI conformant)
  https://gitlab.inria.fr/pallas/pallas/-/blob/main/LICENSE
* [x] SPDX is used
  - https://spdx.org/licenses/BSD-3-Clause
* [ ] REUSE is used

## Minimal Documentation

Basic documentation should be publicly available to facilitate user understanding and usage of the software.

* [x] Documentation exists
* [x] It is easily browsable online
  - https://pallas.gitlabpages.inria.fr/pallas/

## Open Public Discussion Channel

An open, public discussion channel must be provided that is easily accessible to all potential users. The chosen platform must not require special permissions or memberships that could limit user participation.

* [x] A channel exist
* [x] Anyone can join the discussion channel, free of charge, without invitation
  - https://discord.gg/eKvVcRkMsH

## Metadata

Each repository should include metadata easing integration and publicity on a software list

* [x] The following metadata is available:
  - Package name
  - Description
  - License
  - Documentation URL
  - Discussion channel URL
  - Package repositories URLs
  - Repository URL
  - Autoevaluation using the list of criteria stated here
  - TODO: What more?
* [x] it uses codemeta format (https://codemeta.github.io/user-guide/) supported by Software Heritage & HAL (https://www.softwareheritage.org/2023/04/04/swhid-deposit-hal/)
  - https://gitlab.inria.fr/pallas/pallas/-/blob/main/codemeta.json

## API compatibility information

Each repository should include information enabling downstream users to know which versions they can use

* [x] any API addition or breakage should be documented
* [ ] Semantic Versioning (https://semver.org) is used
* [ ] a policy easing predictability of these aspects for future release is provided (Release schedule, etc.)

## Minimal Performance Tests

Software should include a minimal set of performance tests divided in three categories: single node without specific hardware, single node with specific hardware, multi-nodes. These tests should be automated as much as possible.

* [x] Tests exist
* [ ] Scripts to automate launching the tests on a supercomputer and adaptable for another exist
* [ ] Scripts using a tool easing portability to new HW exist
