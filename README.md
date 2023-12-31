# Software Name Disambiguation Benchmark

Software names are challenging to link together: tools may use different variations (e.g., SPSS, statistical package for social sciences), they may contain typos (e.g., pandas, panda) or may share the same name (e.g., packages sharing a name in Pypi and CRAN or GitHub).

In this project we aim to create a benchmark to validate clustering approaches for tool disambiguation. The benchmark includes challenging tool mentions (extracted from the CZI dataset) validated by different annotators, as well as an initial clustering analysis. 

## Methodology
This will describe how we have managed to identify problematic instances. This has been accomplished by two different means:
    - By looking into those that have many URLs are associated with each tool.
    - Bu looking into tools with many variations, which may be difficult to cluster together.

For the benchmark, each mention variation was populated by sampling 5 papers from CZI, and validating them manually. Each paper was enriched from OpenAlex with concepts and authors

## Outcomes
- First version of the benchmark (111 mention variations from 15 different groups)
- An additional 500 hand annotated mentions for the `PRISM` tool prpovided by Kai Li.
- First results bu Jinseok, using the [ANDez](https://codeocean.com/capsule/3498527/tree/v1). See README in the `/ANDez4SND` folder
- An enrichment notebook that finds variations of a given mention in CZI, samples 5 publications and enriches them with OpenAlex authors and concepts (with confidence > 0.5)

## Next steps
- Merge Kai Li's 500 annotation benchmark in the benchmark (in the `to_merge` folder)
- Merge additional 120 mentions for the tool `star` (in the `to_merge` folder)
- Include data from Scicrunch annotators (see [10.5281/zenodo.10048228](http://doi.org/10.5281/zenodo.10048228))
- Include problematic annotations from SoftwareKG (https://data.gesis.org/softwarekg/)
- Include the disambiguation data from [CZI](https://datadryad.org/stash/dataset/doi:10.5061/dryad.6wwpzgn2c)
- Remove mentions from repeated papers from the benchmark.

## Contributing
If you want to collaborate, please open an issue or do a pull request to the main branch of the repository.

## About this project

This repository was developed as part of the [Mapping the Impact of Research Software in Science](https://github.com/chanzuckerberg/software-impact-hackathon-2023) hackathon hosted by the Chan Zuckerberg Initiative (CZI). By participating in this hackathon, owners of this repository acknowledge the following:
1. The code for this project is hosted by the project contributors in a repository created from a template generated by CZI. The purpose of this template is to help ensure that repositories adhere to the hackathon’s project naming conventions and licensing recommendations.  CZI does not claim any ownership or intellectual property on the outputs of the hackathon. This repository allows the contributing teams to maintain ownership of code after the project, and indicates that the code produced is not a CZI product, and CZI does not assume responsibility for assuring the legality, usability, safety, or security of the code produced.
2. This project is published under a MIT license.

## Code of Conduct

Contributions to this project are subject to CZI’s Contributor Covenant [code of conduct](https://github.com/chanzuckerberg/.github/blob/master/CODE_OF_CONDUCT.md). By participating, contributors are expected to uphold this code of conduct. 

## Reporting Security Issues

If you believe you have found a security issue, please responsibly disclose by contacting the repository owner via the ‘security’ tab above.

## Contributors
**Project lead**: Daniel Garijo

**Hackathon Participants**: Daniel Garijo, Jinseok Kim

**Contributors**: Anita Brandowski, Kai Li and  Ana-Maria Istrate
