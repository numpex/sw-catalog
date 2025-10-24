# Using Codemeta to feed the NumPEx Software Catalog
![Static Badge](https://img.shields.io/badge/Status-Draft-orange?style=for-the-badge)

**NumPEx Software Catalog** is a living list of software projects adhering to the [NumPEx software integration guidelines](https://numpex-pc5.gitlabpages.inria.fr/tutorials/projects/guidelines/index.html). 

This document provides recommendations for creating the CodeMeta file for your project to enable automatic import into the NumPEx Software Catalog. It defines conventions for structuring Codemeta files so that they contain all the information required by the catalog, in a uniform and consistent manner across projects.

Some catalog fields can be populated directly from existing CodeMeta properties, while others, for which no direct Codemeta property exists, will be searched in a  custom  `numpex-catalog:annotatedLink` property. Each entry in `annotatedLink` is a structured object containing:
- `url`: the link to the resource
- `roleName`: a controlled vocabulary value indicating the type of resource (e.g., `numpex-catalog:guix_package`)

Following these conventions ensures that metadata for NumPEx projects is both human-readable and machine-actionable, while maintaining a consistent and uniform structure of Codemeta file. Standard Codemeta tools can still validate and process the properties they recognize, and the NumPEx catalog importer can interpret `annotatedLink` objects to populate the corresponding catalog fields automatically.

## Requirements on Codemeta file

### 1. Context
- The `@context` property of the Codemeta file **shall** include:
    1. the standard CodeMeta context: `"https://w3id.org/codemeta/3.0"` or `"https://doi.org/10.5063/schema/codemeta-2.0"` depending on the selected Codemeta version,
    2. the `numpex-catalog` namespace required to identify the custom NumPex vocabulary,
    3. the definition of the `Role`, `roleName`and `url` terms, required to describe [annotated links](#4-annotated-links).


    An example of complete context would therefore looks like this:
````json
"@context": [
  "https://doi.org/10.5063/schema/codemeta-2.0",
  {
    "numpex-catalog": "https://numpex.github.io/sw-catalog/terms-1.0/index.jsonld#",
    "Role": "https://schema.org/Role",
    "roleName": "https://schema.org/roleName",
    "url": "https://schema.org/url"
  }
]
````
### 2. Type

- The `@type` property of the Codemeta file **shall** be set to either `"SoftwareSourceCode"` or `"SoftwareApplication"`.

### 3. Description


- The `description` property of the Codemeta file **shall** provide a textual description of the project:

    | ParentType | Property | Type | Description
    |---|---|---|---|
    | schema:Thing |description | Text | A description of the item.

### 4. Annotated Links

- The Codemeta file **may** include a custom `numpex-catalog:annotatedLink` property. 
- When present, this property **shall** contain an array of `Role` objects, each including folliowing properties:
   - `roleName` — specifying the type of resource,
   - `url` — specifying the full URL of the resource.

- The following additional requirements apply to the `numpex-catalog:annotatedLink` property:

    | Role              | Requirement                                                                                                                                                                             | Example                                                                                                                       |
    | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
    | **Documentation** | If a project documentation exists, the `annotatedLink` property **shall** include a `Role` object with `roleName` `"numpex-catalog:documentation"`. The `url` **shall** point to the project documentation.                          | `json { "@type": "Role", "roleName": "numpex-catalog:documentation", "url": "https://example.com/supercomputesim/docs" }`                    |
    | **Discussion**    | If a project discussion forum or mailing list exists, the `annotatedLink` property  **shall** include a `Role` object with `roleName` `"numpex-catalog:discussion"`. The `url` **shall** point to the forum or mailing list.          | `json { "@type": "Role", "roleName": "numpex-catalog:discussion", "url": "https://forum.example.com/supercomputesim" }`      |
    | **Guix Package**  | If a Guix package exists, the `annotatedLink` property **shall** include a `Role` object with `roleName` `"numpex-catalog:guix_package"`. The `url` **shall** point to the Guix package recipe.     | `json { "@type": "Role", "roleName": "numpex-catalog:guix_package", "url": "https://guix.example.com/supercomputesim.scm" }`     |
    | **Spack Package** | If a Spack package exists, the `annotatedLink` property  **shall** include a `Role` object with `roleName` `"numpex-catalog:spack_package"`. The `url` **shall** point to the Spack package recipe.  | `json { "@type": "Role", "roleName": "numpex-catalog:spack_package", "url": "https://spack.example.com/supercomputesim.py" }`  |

- For maximum interoperability, the Codemeta file **may** also include a `relatedLink` property (part of standard Codemeta schema) duplicating some or all of the URLs listed in the `annotatedLink` property. Standard Codemeta tools will look into the `relatedLink` property[^1], while the NumPEx software catalog importer is using the `numpex-catalog:annotatedLink` property.

## A minimal Codemeta file example 

~~~~json
{
  "@context": [
    "https://doi.org/10.5063/schema/codemeta-2.0",
     {
       "numpex-catalog": "https://numpex.github.io/sw-catalog/terms-1.0/index.jsonld#",
       "Role": "https://schema.org/Role",
       "roleName": "https://schema.org/roleName",
       "url": "https://schema.org/url"
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
    "affiliation": {
      "@type": "Organization",
      "name": "National HPC Lab"
    }
  },
  "codeRepository": "https://gitlab.com/hpc/supercomputesim",
  "numpex-catalog:annotatedLink": [
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
      "url": "https://guix.example.com/supercomputesim.scm" 
    },
    { 
      "@type": "Role",
      "roleName": "numpex-catalog:spack_package",
      "url": "https://spack.example.com/supercomputesim.py" 
    }
  ]
}
~~~~

The two snippets specifically added for NumPEx catalog are :
- The additional definitions in `@context`
- The `numpex-catalog:annotatedLink` property

[^1]: however due to the lack of semantics associated to the individual URLs, we can hardly imagine any useful processing of the `relatedLink` property, except presenting all the links "in bulk" to the user. That was the main reason for introducing annotated links.

