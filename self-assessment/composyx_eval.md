# Composyx Package

## 1. Packaging

Software should be packaged (Spack and/or Guix package formats). They should be published in  public (community controlled) package repositories (Guix-science, etc.).
- [x] Packages exist
- [x] Packages are published in an easily usable repository
- [x] Packages installation is tested on supercomputers
- [x] Packages are available in community repositories
- [x] Either Guix or Spack packages are available
  - Guix https://gitlab.inria.fr/guix-hpc/guix-hpc
  - Spack https://github.com/spack/spack/
- [x] Both Guix and Spack packages are available

## 2. Minimal Validation Tests

Software should include minimal validation tests triggered through automated mechanism such as Guix. These tests should be automatic functional tests that do not require specific hardware.
- [x] Unit tests exist
- [x] CI exists
- [x] CI runs regularly (each new release)
- [x] CI runs regularly (each new commit in main branch)
  - https://gitlab.inria.fr/composyx/composyx/-/pipelines

## 3. Public Repository

A public repository, must be available for at least the development version of the software, allowing for pull requests to be submitted.
- [x] A repository where sources can be downloaded by anyone
- [x] A repository where anyone can submit a modification proposition (pull request)

## 4. Clearly-identified license

Sources published under a clearly-identified free software license (preferably with REUSE).
- [x] Licence is clearly stated
- [x] Licence is FLOSS licence (FSF or OSI conformant)
- [ ] SPDX is used (https://spdx.dev)
- [ ] REUSE is used (https://reuse.software)

## 5. Minimal Documentation

Basic documentation should be publicly available to facilitate user understanding and usage of the software.
- [x] Documentation exists
- [x] It is easily discoverable and browsable online
  - https://composyx.gitlabpages.inria.fr/composyx/

## 6. Open Public Discussion Channel

An open, public discussion channel must be provided that is easily accessible to all potential users. The chosen platform must not require special permissions or memberships that could limit user participation.
- [x] A channel exist
- [ ] Anyone can join the discussion channel, free of charge

## 7. Metadata

Each repository should include metadata easing integration and publicity on a software list.
- [x] The following metadata is available:
	* Package name
	* Description
	* License
	* Documentation URL
	* Package repositories URLs
	* Repository URL
- [ ] It uses codemeta format (https://codemeta.github.io/user-guide/) supported by Software Heritage & HAL (https://www.softwareheritage.org/2023/04/04/swhid-deposit-hal/)

## 8. API compatibility information

Each repository should include information enabling downstream users to know which versions they can use.
- [x] Any API addition or breakage should be documented
- [ ] Semantic Versioning (https://semver.org) is used
- [ ] A policy easing predictability of these aspects for future release is provided (Release schedule, support policy for previous releases)

## 9. Minimal Performance Tests

Software should include a minimal set of performance tests divided in three categories: single node without specific hardware, single node with specific hardware, multi-nodes. These tests should be automated as much as possible.
- [x] Tests exist
- [x] Scripts to automate launching the tests on a supercomputer and adaptable for another exist
- [ ] Scripts using a tool easing portability to new HW exist
  - https://composyx.gitlabpages.inria.fr/bench/weekly_results.html
