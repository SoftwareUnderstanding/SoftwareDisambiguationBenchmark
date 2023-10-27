The files within this folder were utilized during the CZI hackathon to showcase the application of machine learning techniques for clustering ambiguous software names. This particular dataset, containing the software name 'prism', was generously provided by Dr. Kai Li from the University of Tennessee.

To rapidly process the raw input into suitable formats for disambiguation, Perl was employed. Given the limited time, this allowed for a quick implementation. The clustering based on machine learning was facilitated using ANDez, an open-source tool for author name disambiguation, created by Dr. Jinseok Kim from the University of Michigan.

Though adjustments were made to the code to better suit the nuances of software name data, the function names remained consistent. As a result, there might be discrepancies between the output names and the feature names from the input data. It's worth noting that the initial data was enhanced by including duplicate entries with a minimal label set (oversampling) to optimize the machine learning algorithms' performance.

Future updates will see the Perl code files being refined, consolidated, and enhanced for a more user-friendly experience.

Should there be any queries, please reach out to Jinseok Kim at jinseokk@umich.edu