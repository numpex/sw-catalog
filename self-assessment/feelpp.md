# Feel++ Package

## Description

Feel++ is an open-source, high-performance C++ framework for solving complex PDE and ODE-based mathematical models using advanced Galerkin methods (finite element, discontinuous Galerkin, and spectral methods) and efficient reduced-order modeling (ROM) techniques, including Reduced Basis (RB), Proper Orthogonal Decomposition (POD), and Empirical Interpolation Methods (EIM). It features specialized application toolboxes (CFD, CSM, FSI, thermoelectric, Maxwell), modern parallel computing with seamless Python integration (Pybind11), and extensive DevOps support (CI/CD, benchmarking, and containers). Feel++ is used in academia and industry for multiphysics simulations, inverse problems, uncertainty quantification, data assimilation, and machine learning applications.

## Packaging

Software should be packaged (preferably using Spack or Guix package formats). They should be published in public (community controlled) package repositories (Guix-science, etc.).

* [x] Packages exist
* [x] Packages published in easily usable repositories
* [ ] Packages installation tested on supercomputers
* [x] Packages available in community repositories
  * Spack: https://github.com/numpex/spack.numpex/blob/main/packages/feelpp/package.py
  * Guix: https://gitlab.inria.fr/numpex-pc5/wp3/guix-hpc/-/blob/feelpp/guix-hpc/packages/math.scm?ref_type=heads
  * Docker: https://github.com/feelpp/feelpp/pkgs/container/feelpp
  * Apptainer: https://github.com/feelpp/feelpp/pkgs/container/feelpp

Available packages:

* Debian
* Ubuntu
* Fedora
* Spack
* GUIX-HPC

## Minimal Validation Tests

Software should include minimal validation tests triggered through automated mechanism such as Guix. These tests should be automatic functional tests that do not require specific hardware.

* [x] Unit tests exist
* [x] CI exists
* [x] CI runs regularly (each new release)
* [x] CI runs regularly (each commit)

## Public Repository

A public repository, must be available for at least the development version of the software, allowing for pull requests to be submitted.

* [x] Publicly available source repository
* [x] Supports contribution via pull requests

Repository: https://github.com/feelpp/feelpp

## Clearly-identified license

Sources should be published under a clearly-identified free software license (preferably with REUSE)

* [x] License clearly stated
* [x] FLOSS license (FSF/OSI conformant)
* [ ] SPDX is used
* [ ] REUSE is used
  * OSS:: LGPL v*
  * OSS:: GPL v*

## Minimal Documentation

Basic documentation should be publicly available to facilitate user understanding and usage of the software.

* [x] Documentation exists
* [x] Easily browsable online
  * https://docs.feelpp.org

## Open Public Discussion Channel

An open, public discussion channel must be provided that is easily accessible to all potential users. The chosen platform must not require special permissions or memberships that could limit user participation.

* [x] Channel exists
* [x] Freely joinable without invitation
  * Slack (https://feelpp.slack.com)
  * GitHub Discussions (https://github.com/feelpp/discussions)

## Metadata

Each repository should include metadata easing integration and publicity on a software list.

* [x] The following metadata is available:
  * Software name: ✅
  * Description: ✅
  * License: ✅
  * Documentation URL: ✅
  * Discussion channel URL: ✅
  * Package repositories URLs: ✅
  * Repository URL: ✅
  * Autoevaluation using the list of criteria stated here: ✅
* [ ] Uses codemeta format

## API Compatibility Information

Each repository should include information enabling downstream users to know which versions they can use

* [x] API changes documented
* [x] Semantic Versioning used
* [ ] Clear release policy

## Minimal Performance Tests

Software should include a minimal set of performance tests divided in three categories: single node without specific hardware, single node with specific hardware, multi-nodes. These tests should be automated as much as possible.

* [x] Tests exist
* [x] Scripts to automate tests on supercomputers
* [ ] Scripts/tools easing portability to new hardware
