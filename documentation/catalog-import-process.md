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

This file must contains one `projects` property, which is an array of mapping objects. Each mapping object have the following properties:


- `source` : mandatory -  the URL or local path to the JSON file to be used a source for projects metadata. A local path should be expressed in the form `local:path/relative/to/the/root/of/the/Git/repo/file_name.json` - attempts to escape out of the Git repo are detected and flagged as errors.
   The source JSON file may contain either one JSON object or an array of JSON objects. In the latter case, the script loops over every JSON object sequentially, and for each:
   1.  applies the mapping for that object according to `mappingRef` or `fields` (see below)
   2.  updates the corresponding project in the NumPEx software catalog
- `name` : optional - the name of the project to be updated in in the NumPEx software catalog. If this property is omitted, the script searches for a property called `name` across the fields fetched from the JSON source during the mapping step, and uses its value instead. See note 3 below.
- `mappingRef` : optional - the URL of a standard mapping among the following ones:

   | URL | Comment |
   | --- | --- |
   | `https://numpex.github.io/sw-catalog/mappings/codemeta-v2-v3.json` | Standard mapping for [Codemeta file v2 or v3 adhering to the NumPEx conventions](./codemeta-mapping.md) | 

- `fields` : optional - the definition for a custom mapping, consisting in an object including multiple string properties:
   - on left side, name of the NumPex catalog property to be fetched from the JSON source - must be one of these: `name`, `documentation`, `description`, `discussion`, `guix_package` or `spack_package`. 
   - on right side, value of the property is a [Jq](https://jqlang.org/) query to be applied on the JSON source in order to retrieve the corresponding NumPEx property. Note that Jq supports complex queries, possibly much more powerful than just selecting one specific field from the JSON source - see a tutorial [here](https://www.baeldung.com/linux/jq-command-json).

   Missing NumPEx catalog properties will not be fetched from the JSON source. If they are defined in `projects.json` their value will be preserved. If not, they will stay undefined.
- `allow` : optional - specifies whether this mapping object is allowed to create new projects in the NumPEx software catalog (`"create"`),  to update existing ones (`"update"`), or both (`"both"`). Default value is `"update"`.
- `_comment` : optional - human-readable comments, ignored by the script.

> [!Note]
>1. Each mapping object must contain at least one of the two optional properties `mappingRef` and `fields`. In case both properties are defined, then the custom mapping defined in `fields` takes precedence. 
>
>2. Multiple mapping objects may refer to the same project (i.e. have an identical `name` property).  This can be useful if you want to combine multiple metadata sources for your project. The script does process the mapping objects in their order of appearance in the `mapping.json` file - if the same NumPEx Catalog property is mapped multiple times for a given project, the latter mapping overrides earlier ones.
>
>3. It is also possible to have a single `source` file aggregating metadata for multiple projects. You only need to omit the `name` property in the mapping object, to structure the `source` file as an array of objects, one per project, and then rely on the mapping process to correctly fetch the `name` for each project.



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

And before initiating the _pull request_, you must also update the `main-list/mapping.json` file in you fork, adding a new mapping object for your project in the `projects` array, like this:
~~~~json
{
  "projects": [
    {
      "name": "My Super Software",
      "source": "https://url.to.your.repo/codemeta.json",
      "allow": "update",
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
This gives the instructions to the CI system where to fetch the metadata for your project, and how to retrieve the fields needed for the SW Catalog. Especially:
- The fact that neither `guix_package` nor `spack_package` properties are defined indicates that these properties will not be updated automatically ; the values you manually edited in `main-list/mapping.json` are preserved.
- The `allow` property tells the script that we expect an existing entry with that name to be already present in the `main-list/projects.json`, and that an error shall be triggered otherwise. That prevents an incorrect behaviour in case someone would latter delete the project entry in the `main-list/projects.json` but forget to delete the correspond entry in `mapping.json` : without that protection the script would silently create a new entry with the specified `fields` mapping, leading to incomplete presentation of the project in the catalog.

After the submission is accepted, **automatic updates of the SW Catalog with the latest versions of your source metadata file will be performed daily.**

> [!Note]
> 1. If something goes wrong during an update (e.g. network failure), the values you have edited in `main-list/projets.json` are used as backup. 
> It's therefore recommended to put some default text, rather than leaving an empty string.


