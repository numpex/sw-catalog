# Using Codemeta to feed the NumPEx Software Catalog
![Static Badge](https://img.shields.io/badge/Status-Draft-orange?style=for-the-badge)

**NumPEx Software Catalog** is a living list of software projects adhering to the [NumPEx software integration guidelines](https://numpex-pc5.gitlabpages.inria.fr/tutorials/projects/guidelines/index.html). 

This document provides recommendations for creating the CodeMeta file for your project so that it can be automatically imported into the NumPEx Software Catalog. In particular, it defines conventions to map CodeMeta properties to the NumPEx Software Catalog properties in a uniform and consistent manner across all projects.

The guidelines cover both general project metadata (such as project name & description) and related resources (such as documentation, discussion forums, software packages). For the latter, the `relatedLink` property of Codemeta is used to specify URLs to external resources. Each entry in `relatedLink` is represented as a `Role` object, with a `roleName` indicating the type of resource and a `url` pointing to its location.

Following these conventions ensures that metadata for the NumPEx projects is both human-readable and machine-actionable, and with a consistent & uniform structure allowing the Software Catalog to automatically import, validate, and present project information in a standardized way.


## Requirements on Codemeta file

### 1. Context
- The `@context` property of the Codemeta file **shall** include:
    1. the standard CodeMeta context: `"https://w3id.org/codemeta/3.0"` or `"https://doi.org/10.5063/schema/codemeta-2.0"` depending on the selected Codemeta version,
    2. the definition of the `Role` and `roleName` terms, required to describe related resources,
    3. the `numpex-catalog` namespace required to identify the custom role names used [below](#4-related-links) in this document.

    An example of complete context would therefore looks like this:
````json
"@context": [
  "https://doi.org/10.5063/schema/codemeta-2.0",
  {
    "Role": "https://schema.org/Role",
    "roleName": "https://schema.org/roleName",
    "numpex-catalog": "https://.../terms/"
  }
]
````
### 2. Type

- The `@type` property of the Codemeta file **shall** be set to `"SoftwareSourceCode"`.

### 3. Description


- The `description` property of the Codemeta file **shall** provide a textual description of the project:

    | ParentType | Property | Type | Description
    |---|---|---|---|
    | schema:Thing |description | Text | A description of the item.

### 4. Related Links

- The `relatedLink` property of the Codemeta file **may** include an array of `Role` objects, each representing a URL to a project-related resource.

- Each `Role` object **shall** include:

   - `roleName` — specifying the type of resource, prefixed with `numpex-catalog:`.
   - `url` — specifying the full URL of the resource.

- The following `Role` objects **may** be used:

    | Role              | Requirement                                                                                                                                                                             | Example                                                                                                                       |
    | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
    | **Documentation** | If a project documentation exists, the CodeMeta file **shall** include a `Role` object with `roleName` `"numpex-catalog:documentation"`. The `url` **shall** point to the project documentation.                          | `json { "@type": "Role", "roleName": "numpex-catalog:documentation", "url": "https://example.com/supercomputesim/docs" }`                    |
    | **Discussion**    | If a project discussion forum or mailing list exists, the CodeMeta file **shall** include a `Role` object with `roleName` `"numpex-catalog:discussion"`. The `url` **shall** point to the forum or mailing list.          | `json { "@type": "Role", "roleName": "numpex-catalog:discussion", "url": "https://forum.example.com/supercomputesim" }`      |
    | **Guix Package**  | If a Guix package exists, the CodeMeta file **shall** include a `Role` object with `roleName` `"numpex-catalog:guix_package"`. The `url` **shall** point to the Guix package recipe.     | `json { "@type": "Role", "roleName": "numpex-catalog:guix_package", "url": "https://guix.example.com/supercomputesim.scm" }`     |
    | **Spack Package** | If a Spack package exists, the CodeMeta file **shall** include a `Role` object with `roleName` `"numpex-catalog:spack_package"`. The `url` **shall** point to the Spack package recipe.  | `json { "@type": "Role", "roleName": "numpex-catalog:spack_package", "url": "https://spack.example.com/supercomputesim.py" }`   |


## A minimal Codemeta file example 

~~~~json
{
  "@context": [
    "https://doi.org/10.5063/schema/codemeta-2.0",
    {
      "Role": "https://schema.org/Role",
      "roleName": "https://schema.org/roleName",
      "numpex-catalog": "https://.../terms"
    }
  ],
  "@type": "SoftwareSourceCode",
  "name": "SuperComputeSim",
  "description": "A high-performance simulation toolkit for supercomputers.",
  "version": "2.3.1",
  "license": "https://spdx.org/licenses/MIT",
  "programmingLanguage": "C++",
  "author": {
    "@type": "Person",
    "name": "Alice Dupont",
    "affiliation": "National HPC Lab"
  },
  "codeRepository": "https://gitlab.com/hpc/supercomputesim",
  "relatedLink": [
    {
      "@type": "Role",
      "roleName": "numpex-catalog:documentation",
      "url": "https://example.com/supercomputesim/docs"
    },
    {
      "@type": "Role",
      "roleName": "numpex-catalog:discussion",
      "url": "https://forum.example.com/supercomputesim"
    },
    {
      "@type": "Role",
      "roleName": "numpex-catalog:guix_package",
      "url": "https://guix.example.com/supercomputesim"
    },
    {
      "@type": "Role",
      "roleName": "numpex-catalog:spack_package",
      "url": "https://spack.example.com/supercomputesim"
    }
  ]
}
~~~~