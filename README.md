# NumPEx Software Catalog

> [!WARNING]  
> Repo under construction - not operational yet.

This repo centralizes the list of projects following the [NumPEx Software Integration guidelines](https://numpex-pc5.gitlabpages.inria.fr/tutorials/projects/guidelines/index.html).
Human-readable version of the catalog is available on this [website](https://numpex-pc5.gitlabpages.inria.fr/tutorials/projects/index.html).

## How to add your software into that catalog ?

*Procedure yet to be documented: should boil down to adding/updating some files and triggering a Pull Request.*
1. Perform a self assesment of your software module with respect to the [NumPEx Software Guidelines](https://numpex-pc5.gitlabpages.inria.fr/tutorials/projects/guidelines/index.html)
2. Record the result into a markdown file, named after the name of your software module (e.g. `my_module_name.md`) and add this file in the `self-assessment` folder
3. Update `main-list\projets.json` by adding an entry for each package you want to include in the NumPEx SW Catalog:
~~~~json
  {
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod\ntempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim\nveniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea\ncommodo consequat. Duis aute irure dolor in reprehenderit in voluptate\nvelit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat\ncupidatat non proident, sunt in culpa qui officia deserunt mollit anim id\nest laborum.\n",
    "discussion": "https://example.com/discussion",
    "documentation": "https://example.com/",
    "guix_package": "https://example.com/guix",
    "name": "Fake554",
    "spack_package": "https://example.com/spack"
  }
~~~~
5. Make a _pull request_ for your changes
6. After screening and validation, your software will be added in the catalog.

## Repo structure
```bash
.
├── main-list
│   ├── projects-schema.json  
│   └── projects.json                  => THE LIST CONTAINING ALL PROJECTS
|
├── self-assessment
│   ├── projects-schema.json
│   └── projects.json                  => THE LIST CONTAINING ALL PROJECTS
|
├── README.md
```

