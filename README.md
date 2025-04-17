# NumPEx Software Catalog

This repo centralizes the list of projects following the [NumPEx Software Integration guidelines](https://numpex-pc5.gitlabpages.inria.fr/tutorials/projects/guidelines/index.html).

Human-readable version of the catalog is available on this [website](https://numpex-pc5.gitlabpages.inria.fr/tutorials/projects/index.html).

## How to add your own software into that catalog ?

1. Fork this repo and create a new branch
2. Perform a self assesment of your software module with respect to the [NumPEx Software Guidelines](https://numpex-pc5.gitlabpages.inria.fr/tutorials/projects/guidelines/index.html)
3. Record the result into a markdown file, named after the name of your software module (e.g. `my_module_name.md`) and add this file in the `self-assessment` folder of your fork
4. Update `main-list\projets.json` in your fork, by adding an entry for each package you want to include in the NumPEx SW Catalog:
~~~~json
  {
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod\ntempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim\nveniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea\ncommodo consequat. Duis aute irure dolor in reprehenderit in voluptate\nvelit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat\ncupidatat non proident, sunt in culpa qui officia deserunt mollit anim id\nest laborum.\n",
    "discussion": "https://example.com/discussion",
    "documentation": "https://example.com/",
    "guix_package": "https://example.com/guix",
    "name": "My Super Software",
    "spack_package": "https://example.com/spack"
  }
~~~~
5. Initiate a _pull request_ for your changes
6. After screening and evaluation by NumPEx team, your software will be added into the catalog.

## Information for Maintainers

Workflow named `ci`  and will validate the JSON file to be proper JSON, and check for missing fields. It is triggered for each pull request, and for each commit/ direct push in the repo. 

Please be aware that an incorrect JSON file in the `main` branch may cause erroneous rendering or even undefined behaviour when the catalog is displayed on the website.
**Make sure to fix the JSON file asap** if the CI worklows fails after a commit on the `main` branch.

## Repo structure
```bash
.
|
├── main-list
│   ├── projects-schema.json  
│   └── projects.json                  => THE LIST CONTAINING ALL PROJECTS
|
├── self-assessment                    => THE FOLDER CENTRALIZING SELF-ASSESSMENTS
│   ├── some-sw-module.md
│   └── another_module.md             
|
├── .github
│   └── workflows                      => CI WORKFLOWS
|
├── README.md
````
