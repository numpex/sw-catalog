# SPM Package

## Packaging

Software should be packaged (preferably using Spack or Guix package formats). Packages should be published in public, community-controlled repositories.

* [x] SPM is distributed as a bundled component of PaStiX packages
* [x] The PaStiX packages are published in easily usable repositories
* [x] Package installation is tested on supercomputers
  - SPM is built as part of the scheduled PaStiX benchmark CI on the
    PlaFRIM supercomputer, in a reproducible Guix environment:
    https://gitlab.inria.fr/solverstack/pastix/-/blob/master/.gitlab/benchmark.yml
* [x] Indirect packages are available in community repositories
  - Homebrew PaStiX formula: https://gitlab.inria.fr/solverstack/brew-repo/-/blob/master/Formula/pastix.rb
  - Spack PaStiX package: https://github.com/spack/spack-packages/blob/develop/repos/spack_repo/builtin/packages/pastix/package.py
  - Guix-HPC SolverStack packages: https://gitlab.inria.fr/guix-hpc/guix-hpc/-/blob/master/guix-hpc/packages/solverstack.scm
* [ ] A standalone SPM package is available in Guix or Spack
* [ ] Standalone SPM packages are available in both Guix and Spack

## Minimal Validation Tests

Software should include minimal validation tests triggered through an automated mechanism. These tests should be automatic functional tests that do not require specific hardware.

* [x] Unit and functional tests exist
  - https://gitlab.inria.fr/solverstack/spm/-/tree/master/tests
* [x] Continuous integration exists
  - https://gitlab.inria.fr/solverstack/spm/-/pipelines
* [x] CI tests shared-memory and distributed-memory configurations
* [x] CI tests the C, Fortran, and Python interfaces
* [x] CI runs for changes to the repository

## Public Repository

A public repository must be available for at least the development version of the software and allow modification proposals to be submitted.

* [x] Sources can be downloaded by anyone
  - https://gitlab.inria.fr/solverstack/spm
* [x] Anyone can fork the repository and submit a merge request
  - https://gitlab.inria.fr/solverstack/spm/-/forks/new
  - A free GitLab account is required to submit a merge request.

## Clearly Identified License

Sources should be published under a clearly identified free-software license, preferably using REUSE.

* [x] The license is clearly stated
* [x] The license is a FLOSS license: CeCILL 2.0
  - https://gitlab.inria.fr/solverstack/spm/-/blob/master/LICENSE
* [x] The CodeMeta metadata uses the SPDX license identifier
  - https://gitlab.inria.fr/solverstack/spm/-/blob/master/codemeta.json
* [ ] SPDX identifiers are present in every source file
* [ ] REUSE is used

## Minimal Documentation

Basic documentation should be publicly available to facilitate understanding and use of the software.

* [x] User and API documentation exists
* [x] Documentation is browsable online
  - https://solverstack.gitlabpages.inria.fr/spm/
* [x] Build and installation instructions are provided
  - https://gitlab.inria.fr/solverstack/spm/-/blob/master/README.md

## Open Public Discussion Channel

An open, public discussion channel should be easily accessible to all potential users without special permission or invitation.

* [x] A public issue tracker exists
  - https://gitlab.inria.fr/solverstack/spm/-/issues
* [x] Anyone can read it and join through a free account without invitation

## Metadata

Each repository should include metadata easing integration and publicity in software catalogs.

* [x] The repository contains CodeMeta metadata
  - https://gitlab.inria.fr/solverstack/spm/-/blob/master/codemeta.json
* [x] The metadata includes the package name, description, version, license, repository, documentation, discussion channel, CI, languages, and supported operating systems
* [ ] The metadata includes direct package-repository URLs; SPM is currently packaged indirectly through PaStiX
* [x] The metadata follows the NumPEx CodeMeta conventions
* [x] This self-assessment records the project's status against the NumPEx criteria

## API Compatibility Information

Each repository should include information enabling downstream users to determine which versions they can use.

* [x] API additions, deprecations, and relevant compatibility changes are documented in the changelog
  - https://gitlab.inria.fr/solverstack/spm/-/blob/master/ChangeLog.md
* [ ] A formal semantic-versioning policy is documented
* [ ] A release schedule or formal compatibility policy is provided

## Minimal Performance Tests

Software should include a minimal set of performance tests for single-node and multi-node configurations, automated as much as possible.

* [ ] Single-node performance tests exist
* [ ] Accelerator-specific performance tests exist
* [ ] Multi-node performance tests exist
* [ ] Portable scripts automate performance testing

SPM currently prioritizes a portable API and simple sparse-matrix interfaces rather than performance, as stated in its README.
