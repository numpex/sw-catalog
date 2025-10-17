# Using Codemeta to feed the NumPEx Software Catalog
![Static Badge](https://img.shields.io/badge/Status-Draft-orange?style=for-the-badge)

**NumPEx Software Catalog** is a living list software projects adhering to the [NumPEx software integration guidelines](https://numpex-pc5.gitlabpages.inria.fr/tutorials/projects/guidelines/index.html). 

This document provides recommendations for creating the CodeMeta file for your project so that it can be automatically imported into the Software Catalog. In particular, it defines conventions to map CodeMeta properties to the NumPEx catalog properties in a uniform and consistent manner across all projects.

The guidelines cover both general project metadata (such as project name & description) and related resources (such as documentation, discussion forums, software packages). For the latter, the `relatedLink` property of Codemeta is used to specify URLs to external resources. Each entry in `relatedLink` is represented as a `Role` object, with a `roleName` indicating the type of resource and a `url` pointing to its location.

Following these conventions ensures that metadata for the NumPEx projects is both human-readable and machine-actionable, with a consistent & uniform structure allowing the Software Catalog to automatically import, validate, and present project information in a standardized way.


## Requirements

### 1. Context
- The `@context` property of the Codemeta file **shall** include the standard CodeMeta context: `"https://w3id.org/codemeta/3.0"` or `"https://doi.org/10.5063/schema/codemeta-2.0"` depending on the selected version.

- To use the NumPEx-specific roles (see [below](#4-related-links)), the context **shall** define the `numpex-catalog` namespace pointing to the terms file:
````json
"numpex-catalog": "https://.../terms"
````
### 2. Type

- The `@type` property of the Codemeta file **shall** be set to `"SoftwareSourceCode"`.

### 3. General Project Metadat


- The `description` property of the Codemeta file **shall** provide a textual description of the project:

    | ParentType | Property | Type | Description
    |---|---|---|---|
    | schema:Thing |description | Text | A description of the item.

### 4. Related Links

- The `relatedLink` property of the Codemeta file **may** include an array of `Role` objects, each representing a URL to a project-related resource.

- Each `Role` object **shall** include:

   - `roleName` — specifying the type of resource, prefixed with `numpex-catalog:`.
   - `url` — specifying the full URL of the resource.

- Below the list of standard Roles:

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