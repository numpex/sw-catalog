# NumPEx Software Catalog

> [!WARNING]  
> Repo under construction - not operational yet.

This repo centralizes the list of projects following the [NumPEx Software Integration guidelines](https://numpex-pc5.gitlabpages.inria.fr/tutorials/projects/guidelines/index.html).
Human-readable version of the catalog is available on this [website](https://numpex-pc5.gitlabpages.inria.fr/tutorials/projects/index.html).

## How to add your software into that catalog ?

*Procedure yet to be documented: should boild down to adding/updating some files and triggering a Pull Request.*

## Repo structure
```bash
.
├── main-list
│   ├── projects-schema.json          
│   └── projects.yml                  => THE LIST CONTAINING ALL PROJECTS
│      
├── README.md
```

## Continous Integration

The _website_update_ workflow is executed each time a change is made in the `main-list` subfolder on the main branch. This workflow does trigger the CI pipeline in project https://gitlab.inria.fr/numpex-pc5/tutorials in order to deploy an updated version of the [website](https://numpex-pc5.gitlabpages.inria.fr/tutorials/projects/index.html).
To make it work :
- On Gitlab, select "Settings -> CI/CD -> Pipeline Trigger Token -> Add New Token' and copy the newly generated token, 
- On Github, select "Settinggs -> Secrets & Variables -> Actions' and then edit the GITLAB_EXADI_TOKEN repository secret, or create it if it does not exist. As secret value, paste the generated token from the previous step
The complete process may take up to a few minutes.
