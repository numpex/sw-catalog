# NumPEx Software Catalog

This repo centralizes the list of projects following the [NumPEx Software Integration guidelines](https://numpex-pc5.gitlabpages.inria.fr/tutorials/projects/guidelines/index.html).

Human-readable version of the catalog is available on this [website](https://numpex-pc5.gitlabpages.inria.fr/tutorials/projects/index.html).

## How to add your own software into that catalog ?

1. Fork this repo and create a new branch
2. Perform a self assesment of your software module with respect to the [NumPEx Software Guidelines](https://numpex-pc5.gitlabpages.inria.fr/tutorials/projects/guidelines/index.html)
3. Record the result into a markdown file, named after the name of your software module (e.g. `my_module_name.md`) and add this file in the `self-assessment` folder of your fork
4. Update `main-list/projets.json` in your fork, by adding an entry for each package you want to include in the NumPEx SW Catalog:
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

The website generates a human-readable of the SW catalog by dynamically parsing the latest commit for the `projects.json` file in the `main` branch. Please be aware that an incorrect JSON file in the `main` branch may cause erroneous rendering or even undefined behaviour (e.g. webbrowser crash) when users access the catalog page from the website.

Workflow named `ci`  aims to validate the JSON file to be proper JSON, and to check for missing fields. It is triggered for each pull request, and for each commit/ direct push in the repo. **Make sure to fix the JSON file asap** if the CI worklows fails after a commit on the `main` branch.
### How to add a new field to the schema?

The final page, is generated from 2 repositories:

- This `sw-catalog` repo, that holds the data.
- The [`tutorials`](https://gitlab.inria.fr/numpex-pc5/tutorials) repo, that renders the catalog.

To add a new element for all projects:

1. Add a new property to the schema: https://github.com/numpex/sw-catalog/blob/main/main-list/projects-schema.json
2. Fill the property for all projects: https://github.com/numpex/sw-catalog/blob/main/main-list/projects.json
3. Configure the tutorials page to render the new property:
  1. Modify `projects.mjs`: https://gitlab.inria.fr/numpex-pc5/tutorials/-/blob/main/docs/assets/js/projects.mjs
  2. Add the new field to the `typedef Project` (to have the type system properly detect it).
  3. Add a new `dispatch` function to render a new `<li>`, similar to the existing ones.
  4. (Optionally) Change the icon from `class="fas fa-<name>"`, from the list of icons of FontAwesome: https://fontawesome.com/icons/packs/classic

The projects are rendered with the following steps:

1. Hugo renders the main page: https://gitlab.inria.fr/numpex-pc5/tutorials/-/blob/main/docs/content/projects/_index.md
2. The `{{< projects >}}` shortcode calls the following HTML snippet: https://gitlab.inria.fr/numpex-pc5/tutorials/-/blob/main/docs/layouts/shortcodes/projects.html
3. The projects shotcode loads and calls the following Javascript `projects.mjs`: https://gitlab.inria.fr/numpex-pc5/tutorials/-/blob/main/docs/assets/js/projects.mjs

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
