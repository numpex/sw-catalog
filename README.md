# NumPEx Software Catalog

This repo centralizes the list of projects following the [NumPEx Software Integration guidelines](https://numpex-pc5.gitlabpages.inria.fr/tutorials/projects/guidelines/index.html).

Human-readable version of the SW catalog is available on this [website](https://numpex-pc5.gitlabpages.inria.fr/tutorials/projects/index.html).

## How to submit your own software into the SW Catalog ?

1. Fork this repo and create a new branch
2. Perform a self assesment of your software module with respect to the [NumPEx Software Guidelines](https://numpex-pc5.gitlabpages.inria.fr/tutorials/projects/guidelines/index.html)
3. Record the result into a markdown file, named after the name of your software module (e.g. `my_module_name.md`) and add this file in the `self-assessment` folder of your fork
4. Update `main-list/projets.json` in your fork, by adding an entry for each package you want to include in the NumPEx SW Catalog:
~~~~json
  {
    "name": "My Super Software",
    "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod\ntempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim\nveniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea\ncommodo consequat. Duis aute irure dolor in reprehenderit in voluptate\nvelit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat\ncupidatat non proident, sunt in culpa qui officia deserunt mollit anim id\nest laborum.\n",
    "discussion": "https://example.com/discussion",
    "documentation": "https://example.com/",
    "guix_package": "https://example.com/guix",
    "spack_package": "https://example.com/spack"
  }
~~~~
5. Initiate a _pull request_ for your changes
6. After screening and evaluation by NumPEx team, your software will be added into the catalog.


> [!IMPORTANT]
> Don't forget to reapply the same process again when some of the fields need to be updated to reflect the latest evolutions of your software !
> The next section describes a solution that supports automatic updates of your SW Catalog entry without any user intervention.

## What if you already have Codemeta file (or alike) for your software ?

In case some of the fields expected for the SW Catalog are already documented at another place, for instance a Codemeta file contained in your project repo, we offer a solution to avoid any duplication or redundant typing, and to enable automatic updates.

Let's assume for the sake of example that:
- your project has already a Codemeta file including fields `description`, `buildInstructions` and `issueTracker`,
- you would like to use content of these Codemeta fields to fill in the `description`, `documentation` and `discussion` fields of the SW Catalog (respectively)
- you would like that the other fields of the SW Catalog (`guix_package` and `spack_package`) are managed in the classic way, via `projects.json`

Then in the step 4 of the submission workflow, when editing `main-list/projets.json` in your fork, you just need to fill in the `guix_package` and `spack_package` fields, you can leave the other fields empty (or put some default text - see note 1 below):
~~~~json
  {
    "name": "My Super Software",
    "description": "",
    "discussion": "",
    "documentation": "",
    "guix_package": "https://example.com/guix",
    "spack_package": "https://example.com/spack"
  }
~~~~

And before initiating the _pull request_, you must also update the `main-list/mapping.json` file in you fork, adding a new item for your project in the `projects` array, like this:
~~~~json
{
  "projects": [
    {
      "name": "My Super Software",
      "source": "https://url.to.your.repo/codemeta.json",
      "fields": 
        {
          "description":  ".description",
		  "discussion":   ".issueTracker",
		  "documentation":  ".buildInstructions"
        }
    }
  ]
}
~~~~
This gives the instructions to the CI system where to fetch the metadata for your project, and how to retrieve each field needed for the SW Catalog. The string values on the right side are [Jq](https://jqlang.org/) queries that will be applied to your Codemeta file, the result of the query being used to fill in the field of the SW Catalog mentionned on the left side.

**Automatic updates of the SW Catalog with the latest versions of the source meta data will be performed daily.**

> [!Note]
> 1. If something goes wrong during an update (e.g. network failure), the values you have edited in `main-list/projets.json` will be used as backup. 
> It's thererfore recommended to put some default text in it, rather than leaving an empty string.
> 2. We are agnostic to Codemeta ; same process can be applied with any JSON file stored at a public URL.
> 3. [Jq](https://jqlang.org/) supports complex queries, much more powerful than just selecting one field from your Codemeta file - see a tutorial [here](https://www.baeldung.com/linux/jq-command-json).
> 4. The same project can appear multiple times in the `main-list/mapping.json` file  in case you want to combine multiple metadata sources for your project. If the same SW Catalog field is updated from multiple entries, the latter one overrides earlier ones.

## Information for Maintainers

### How does it work ? 

The website generates a human-readable of the SW catalog by dynamically parsing the latest commit for the `main-list/projects-generated.json` file in the `main` branch. 
Please be aware that unexpected content in this file may cause erroneous rendering or even undefined behaviour (e.g. webbrowser crash) when users access the catalog page from the website. **Make sure to fix any problem in that file asap**.

As it name suggests, the `projects-generated.json` file is generated by the CI system, by applying all the updates specified in `main-list/mapping.json` to the (human-edited) file `main-list/projects.json`.

Following workflows are implemented:
- In a pull request: validate the format of `projects.json`, try to regenerate the `projects-generated.json` and validate the format of `projects-generated.json`
- When pushing to main: same + commit the new version of `projects-generated.json`
- Periodically: same + commit the latest update of `projects-generated.json` in a new branch & issue a PR (if needed)

### What are the conditions to accept a PR ?

Currently the conditions are very loose; we only check:
1. that the self-assesment file is provided
2. that there is no obvious typo in the description or project name
3. that the format of the file is valid (done by CI workflow)

### How to add a new field to the schema ?

The final HTML page, is generated from 2 repositories:

- This `sw-catalog` repo, that holds the metadata.
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
```
.
|
├── main-list
│   ├── projects-schema.json           => JSON SCHEMA
│   ├── mapping-schema.json            => JSON SCHEMA
│   ├── projects-generated.json        => THE GENERATED CATALOG - DON'T TOUCH
│   ├── mappings.json                  => INSTRUCTIONS FOR FETCHING FROM EXTERNAL JSON FILES - HUMAN EDITABLE
│   └── projects.json                  => THE LIST OF PROJECTS - HUMAN EDITABLE
|
├── self-assessment                    => THE FOLDER CENTRALIZING SELF-ASSESSMENTS
│   ├── some-sw-module.md
│   └── another_module.md
|
├── scripts                            => THE FOLDER FOR SCRIPTS
|
├── .github
│   └── workflows                      => CI WORKFLOWS
|
├── README.md
````
