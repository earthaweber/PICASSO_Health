ABOUT:
This code was prepared for the article: Modelling PM2.5 Reduction Scenarios for Future Cardiopulmonary Disease Reduction.

CONTACT: 

If you have problems or questions direct them to this e-mail: e.d.c.weber@uu.nl

OPERATING INSTRUCTIONS:

DATA 
In order to sucessfully run the GBD 2019 model you will need data from the following resources: 

- MRBRT Curves (disease specific and downloadable from the IHME website [
](https://ghdx.healthdata.org/record/ihme-data/global-burden-disease-study-2019-gbd-2019-particulate-matter-risk-curves))
-TMREL also from above link
- Optional: Population Datasets (in the most recent version of the GBD outcomes like stroke and IHD no longer have age separated MRBRT curves) for SSP2 these are obtained here: https://iiasa.ac.at/news/feb-2024/population-and-human-capital-projections-to-2100

The data we used as input data are listed in the file PM2_5_2050_Data where we have generated the Ind_PM variable with the WHO HOMEs Model, and the Out_PM with the TM5-FAAST model. The sum of these two variables are called Tot_PM.  The TM5-FAAST model was written by a team of other researchers (https://tm5-fasst.jrc.ec.europa.eu/) and in collaboration the PBL IMAGE team has created their own version compatible with the IMAGE model thus is not shared here but questions can be directed to the PBL IMAGE team or the corresponding author at: e.d.c.weber@uu.nl if data is needed for your own projects or additional data is required for the interpretation of this study. 

FUNCTIONS 
Before running the code, be sure to run the functions within the function file first, adapt the functions to fit the name of the different data (eg. MRBRT curves) associated with the different health outcomes. Note that for the GBD 2019 version of the Stroke and Ischemic Heart Disease code you will need a dataset that has the breakdown of the population into 5 year age groups, however in the newer version of the GBD study this is no longer required so the code for COPD can simply be used without the dataset with the population age breakdown. 

BUGS AND TROUBLESHOOTING STEPS 
There are some issues that often appear if the data structure is not in the format that the code is designed for (for example in my main analysis my results are stored in lists however to turn it into a table to be exported it needs to be stored in the working directory as a dataframe).

POTENTIAL FUTURE IMPROVEMENTS
At the beginning this code was designed to only analize one health outcome (Ischemic Heart Disease) a potential improvement to make it more efficient at analyzing multiple outcomes would be to introduce for loops (especially now that the age groupings are dropped for the newer versions of MRBRT curves for ISHD and Stroke) to automatically be able to analyze multiple health outcomes in one run. 
