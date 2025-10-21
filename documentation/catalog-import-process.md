# Automatic Import & Update Process for the NumPEx Catalog

## Process Overview

The NumPEx software catalog primarily consists in a `main-list/projects.json`  file containing a set of properties (e.g. description, link to documentation, to guix package...) for every project included in the catalog.

The Automatic Import & Update Process makes it possible, for given projects, to fetch these metadata (or a subset of these metadata) from external JSON sources, such as Codemeta files. The two objectives are:
- to avoid duplicating the information for projects already having a JSON metadata file available
- to avoid need for manual updates of the NumPEx catalog in case the JSON metadata file evolves

How does it work ?

- A specific configuration file called `main-list/mapping.json` specifies for each project the location of the external JSON source to be fetched, and how to map the metadata contained in this external source to NumPEx catalog properties.
- A Python script (`update_projects.py`) is able to collect all the external metadata as defined in `mapping.json` and to update the `projects.json` file accordingly, either in place or in a specified output file.
- The CI system triggers this script at any change in either `mapping.json` or `projects.json` + one time daily (in order to capture potential changes in external JSON sources). Output is directed to the `projects-generated.json` file, which is the one used by [HTML renderer](https://numpex-pc5.gitlabpages.inria.fr/tutorials/projects/catalog/index.html) to visualise the NumPEx Catalaog.
- Users wanting to add a new project into the SW Catalog can either:
   1. edit the `mapping.json` and use the script in-place to create an entry for the project into `projects.json`  - this suits very well the situation where all the catalog properties can be fetched from an external JSON source
   2. create manually an entry for the project in `projects.json` and edit the `mapping.json` to configure future updates - this corresponds to the case where only some catalog properties can be fetched from an external source, whereas others have to be manually provided.


The overall workflow is shown in the diagram below:
~~~~mermaid
flowchart LR
    %% Step 1: Manual update 
    subgraph Step1a["Manual Edit & import"]
        M["Manual Edition"]
        A["projects.json"]
        F["mapping.json"]
        Script["Update Script"]
        M --> A
        M --> F
        A --> Script
        F --> Script
        Script --> A_updated["Updated projects.json (same file)"]
    end

    %% Step 2: CI Generation
    subgraph Step2["CI System (on changes + daily)"]
        A_latest["projects.json"]
        F2["mapping.json"]
        Script2["Update Script"]
        A_generated["projects-generated.json"]
        A_latest --> Script2
        F2 --> Script2
        Script2 --> A_generated
    end

    %% Step 3: Web Visualization
    subgraph Step3["Visualization"]
        A_generated2["projects-generated.json"]
        VizTool["HTML Renderer"]
        Result["Displayed catalog"]
        A_generated2 --> VizTool --> Result
    end

    %% Overall flow
    A_updated --> A_latest
    A_generated --> A_generated2
~~~~

## Format of the `mapping.json` file
## Example with custom mapping
Let's assume for the sake of example that:
- your project has a Codemeta file including fields `description`, `buildInstructions` and `issueTracker`,
- you would like to use content of these Codemeta fields to fill in the `description`, `documentation` and `discussion` fields of the SW Catalog (respectively)
- you would like that the other fields of the SW Catalog (`guix_package` and `spack_package`) are managed in the classic way, via `projects.json`.

Then in the step 4 of the submission workflow, when editing `main-list/projects.json` in your fork, you just need to fill in the `guix_package` and `spack_package` fields, you can leave the other fields empty (or put some default text - see note 1 below):
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
This gives the instructions to the CI system where to fetch the metadata for your project, and how to retrieve each field needed for the SW Catalog. The string values on the right side are [Jq](https://jqlang.org/) queries that will be applied to your Codemeta file, the result of the query being used to fill in the field of the SW Catalog mentionned on the left side. The fact that neither `guix_package` nor `spack_package` properties are defined indicates that these properties shall never updated automatically ; the values you manually edited in `main-list/mapping.json` are preserved.

After the submission is accepted, **automatic updates of the SW Catalog with the latest versions of your source metadata file will be performed daily.**

> [!Note]
> 1. If something goes wrong during an update (e.g. network failure), the values you have edited in `main-list/projets.json` are used as backup. 
> It's therefore recommended to put some default text, rather than leaving an empty string.
> 2. We are agnostic to Codemeta ; same process can be applied with any JSON file stored at a public URL.
> 3. [Jq](https://jqlang.org/) supports complex queries, much more powerful than just selecting one field from your Codemeta file - see a tutorial [here](https://www.baeldung.com/linux/jq-command-json).
> 4. The same project can appear multiple times in the `main-list/mapping.json` file  in case you want to combine multiple metadata sources for your project. If the same SW Catalog field is updated from multiple entries, the latter one overrides earlier ones.
