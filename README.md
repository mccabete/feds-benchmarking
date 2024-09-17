# Documentation: VEDA Polygon Evaluation and Comparison (PEC)

Author: Katrina Sharonin

## Statement of Need

* What: The VEDA PEC is designed to accelerate comparison of [FEDS fire parimeter datasets, + link to API documentation: https://nasa-impact.github.io/veda-docs/example-notebooks/wfs.html, to reference fire perimeters datasets.]. [Why do we need it?, why should we compare fire perimeters to other datasets?. You want a full paragraph explaining the motivations for building what you have built before you go into what you have built.]
    * Users should only need to interact with the library with the `BLANK_PEC_Outline.ipynb`; all python scripts are used as abstractions [This should be in installation instructions, not a statement of need]
    * Reference datasets can be a predefined option (i.e. already saved to a URL in MAAP) or can be user uploaded/defined [Again, not a statement of need, move to new "features" section]
    * Calculations include: Ratio, Accuracy, Precision, Recall, IOU, F1, and Symmetric Ratio [why would we need these/ want these?, add bullet to features section]
    * Currently most support exists for the firenrt perimeter collection; seeking community feedback for new datasets [not a statement of need. put into upcoming features]
    * Dumps outputs in convenient formats for research uses and archiving [informal tone, list formats, and move to "features" section]
* Why [use this tool]: rather than force users to re-implement comparisons/calculations on their own for research, this add-on quickly lets users feed in datasets of interest and pump out analysis. More time can be spent on dataset selection and output analysis, rather than implementing/testing software [This is why we should automate things, but not why we should comepare perimeters. You titled this repo "benchmarking" but so far have not mentioned it.]
* Who [is this built for, or "intended audience" or "intended user community"]: MAAP users and Earth science research community. 

## Installation Instructions
1. Conda enviornment: please run the env-feds bash script to generate the `env-feds` conda enviornment
    * Required packages: glob, sys, logging, pandas, geopandas, pyproj, owslib, datetime, functools, boto3, fsspec, matplotlib
    * TODO: make a bash/conf script for this repo to install
2. Edit/Make a copy of the `BLANK_PEC_Outline.ipynb`
3. Make sure the selected ipynb kernel is the `env-feds` enviornment (and/or
4. Follow instructions in the notebook for quickstart; you only need to modify inputs in the section `User Inputs for Comparison: time, bbox, VEDA set, reference set` 
5.  

## Example Usage: 
* See `DEMO_PEC_Outline.ipynb` for a full demonstration with the Kincade Fire

## Testing:
* This module implements strict argument catches to block users from accessing un-implemented features
* TBD for unit testing

## Upcoming features:
* Output formats + plotting persistence
* Additional pre-defined datasets for comparison
* Potential community-shared datasets (i.e. uploaded by non-admin user, public to all to try using)

## Key Files/Classes
* `Input_VEDA.py`: class representing a dataset input from VEDA either from API or a hard-coded path in the MAAP enviornment
* `Input_Reference`: class representing a dataset input from a predefined source (e.g. NIFC interagency perimeters) or a user input sourced from a MAAP path
* `Output_Calculation.py`: class representing an output for each Input_VEDA and Input_Reference run together; holds calculations and capable of printing/plotting/serializing data
* `Utilities.py`: misc functions for various operations
* `PEC_Outline.ipynb`: notebook demonstrating how to set up inputs and use class, assumes user has NASA MAAP acccess
* `PEC_Scratchwork.ipynb`: misc work

## Contribution/Reporting
* Contact ksharonin@berkeley.edu / katrina.sharonin@nasa.gov for support/issues/feedback
 
