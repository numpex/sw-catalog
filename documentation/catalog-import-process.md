# Automatic Import & Update Process for the NumPEx Catalog

## Process Overview

The NumPEx software catalog primarily consists in a `main-list/projects.json`  file containing a set of properties (e.g. description, link to documentation, to guix package...) for every project included in the catalog.

The Automatic Import & Update Process makes it possible, for given projects, to fetch these metadata (or a subset of these metadata) from external JSON sources, such as Codemeta files. The two objectives are:
- to avoid duplicating the information for projects already having a JSON metadata file available
- to avoid need for manual updates of the NumPEx catalog to keep in sync with evolutions of the JSON metadata file 

How does it work ?

- A specific configuration file called `main-list/mapping.json` defines for each project the location of the external JSON source to be fetched, and specifies how to map the metadata contained in this external source to NumPEx catalog properties.
- A Python script (`update_projects.py`) is able to collect all the external metadata as defined in `mapping.json` and to update the `projects.json` file accordingly, either in-place or in a specified output file.
- The CI system triggers this script at any change in either `mapping.json` or `projects.json` and also one time daily in order to capture potential changes in external JSON sources. Output is directed to the `projects-generated.json` file, which is the one used by [HTML renderer](https://numpex-pc5.gitlabpages.inria.fr/tutorials/projects/catalog/index.html) to visualise the NumPEx Catalaog.
- Users wanting to add a new project into the SW Catalog can either:
   1. edit the `mapping.json` file and run the script in-place to create an entry for the project into `projects.json`  - this suits very well the situation where all the catalog properties can be fetched from an external JSON source
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

This workflow ensures a good separation between human & machine edition :
- `mapping.json` is only human-edited
- `projects.json` is either human-edited or updated by script, upon human request & under human supervision
- `projects-generated.json` is only machine-edited by CI system

The commit history of each file is kept clean and we have good separation between intentional changes and automatic updates.

## Format of the `mapping.json` file

This file lust contains one `projects` property, which is an array of mapping objects. Each mapping object have the following properties:

- `name` : mandatory - the name of the project (used to match entries in `projects.json`)
- `source` : mandatory -  the URL of the external JSON metadata file.
- `mappingRef` : optional - the URL of a standard mapping among the following ones:

   | URL | Comment |
   | --- | --- |
   | `https://numpex.github.io/sw-catalog/mappings/codemeta-v2-v3.json` | Standard mapping for [Codemeta file v2 or v3 adhering to the NumPEx conventions](./codemeta-mapping.md) | 

- `fields` : optional - the definition for a custom mapping, consisting in an object including multiple string properties:
   - on left side, name of the NumPex catalog property to be fetched form the external JSON source - must be one of these: `documentation`, `description`, `discussion`, `guix_package` or `spack_package`. 
   - on right side, value of the property is a [Jq](https://jqlang.org/) query to be applied on the external JSON source in order to retrieve the corresponding NumPEx property. Note that [Jq](https://jqlang.org/) supports complex queries, much more powerful than just selecting one specific field from the extternal JSON source - see a tutorial [here](https://www.baeldung.com/linux/jq-command-json).

   Missing NumPEx catalog properties will not be fetched from the external JSON source. If they are defined in `projects.json` their value will be preserved. If not, they will stay undefined.

> [!Note]
>1. Each mapping object must contain at least one of the two optional properties `mappingRef` and `fields`. In case both optional properties are defined, then the custom mapping defined in `fields` takes precedence.
>
>2. Multiple mapping objects may refer to the same project (i.e. have an identical `name` property).  This can be useful if you want to combine multiple metadata sources for your project. The script will process the mapping objects in their order of appearance in the `mapping.json` file - if the same NumPEx Catalog property is mapped multiple times, the latter one overrides earlier > ones.


## Usage Examples 
### Standard mapping
See [README](../README.md#what-if-you-already-have-a-codemeta-file-for-your-software-).

###  Custom mapping
Let's assume for the sake of example that:
- your project has a Codemeta file including fields `description`, `buildInstructions` and `issueTracker`,
- you would like to use content of these Codemeta fields to fill in the `description`, `documentation` and `discussion` fields of the SW Catalog (respectively)
- you would like that the other fields of the SW Catalog (`guix_package` and `spack_package`) are managed in the classic way, via `projects.json`.

Then in the step 4 of the [submission workflow](../README.md#how-to-submit-your-own-software-into-the-sw-catalog-), when editing `main-list/projects.json` in your fork, you just need to fill in the `guix_package` and `spack_package` fields, you can leave the other fields empty (or put some default text, see note 1 below):
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
This gives the instructions to the CI system where to fetch the metadata for your project, and how to retrieve each field needed for the SW Catalog. The fact that neither `guix_package` nor `spack_package` properties are defined indicates that these properties shall not be updated automatically ; the values you manually edited in `main-list/mapping.json` are preserved.

After the submission is accepted, **automatic updates of the SW Catalog with the latest versions of your source metadata file will be performed daily.**

> [!Note]
> 1. If something goes wrong during an update (e.g. network failure), the values you have edited in `main-list/projets.json` are used as backup. 
> It's therefore recommended to put some default text, rather than leaving an empty string.


