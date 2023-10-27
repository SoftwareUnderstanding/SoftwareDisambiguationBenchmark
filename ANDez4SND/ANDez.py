######################################################################################
# ANDez is an open-source framework that integrates the workflows of several high-performing machine learning methods 
# for classification and clustering in author name disambiguation.
# ANDez was developed under a grant from the National Science Foundation 
# (NSF NCSES Award # 1917663: Creating a Data Quality Control Framework for Producing New Personnel-Based S&E Indicators) 
# and its supplementary fund program, Research Experiences for Undergraduates (REU).
#
# Author:
# 1. Jinseok Kim (Ph.D.): Institute for Social Research and School of Information, University of Michian Ann Arbor
# 2. Jenna Kim: School of Information Sciences, University of Illinois at Urbana-Champaign
#
######################################################################################


# NOTE: Run this script with 'procedures.py', 'modules.py', 'cluevalmetrics.py'
#       after placing all the files in the same directory


import time
import uuid
from datetime import timedelta

from procedures import *

''' measure start time '''
start_time = time.time()


################# set parameters #################
"""
For details on parameter choices during disambiguation, see a paper below
(1) Kim, J., & Kim, J. (2020). Effect of forename string on author name disambiguation.
    Journal of the Association for Information Science and Technology, 71(7), 839-855
(2) Kim, J., Kim, J., & Owen-Smith, J. (2019). Generating automatically labeled data for
    author name disambiguation: an iterative clustering method. Scientometrics, 118(1), 253-280.
(3) Kim, J., & Owen-Smith, J. (2020). Model Reuse in Machine Learning for Author Name Disambiguation:
    An Exploration of Transfer Learning. IEEE Access, 8, 188378-188389. doi:10.1109/ACCESS.2020.3031112
"""


### Select model training or application ###

"""
Two options: 
(1) train and save a model : "train"
(2) apply the trained model on test data: "predict"
"""

model_usage = "train"


###################################################
##########  Parameters for the case (1)  ##########
###################################################
"""
If you want to train and save a model,
you can change values of the follwing parameters
before you run the main code
"""

### 1-1. Type in file names ###

"""
Input files are required to be prepared in a specific format
(1) signature file: instance id, paper id, author byline position, name string, affiliation, etc. 
(2) record file: paper id, publication year, venue name, author list, title, etc.
                > Author names in the author list are seperated by vertical bar
(3) cluster file: cluster id and instance id list
                > Instance ids in instance id list are separated by vertical bar
Each file is created in .txt and columns are separated by tab.
Please see the example files provided with this code set. 
"""

train_instance_file = "signatures_train.txt"
train_cluster_file  = "clusters_train.txt"
train_record_file   = "records_ml.txt"

test_instance_file  = "signatures_test.txt"
test_cluster_file   = "clusters_test.txt"
test_record_file    = "records_ml.txt"


### 1-2. Choose a blocking method ###

"""
Blocking is a step to collate name instances to be compared with each other
The blocking method selected here is applied to both training and test data

Three options are available
(1) first_initial: name instances that have the same surname and first forename initial are compared
        e.g., 'kim, jinseok' vs 'kim, j' > They share 'kim, j'
(2) full_name: name instances that have the same string are compared
        e.g., 'kim, jinseok' vs 'kim, jinseok' > They share 'kim, jinseok'
(3) forename_strip: name instances that have the same surname and n characters of forename are compared
        e.g., 'kim, jinseok' vs 'kim, jin s' > They share 'kim, jin' (if n == 3)

For more details on blocking and 3 options, see the paper below
    Kim, J., & Kim, J. (2020). Effect of forename string on author name disambiguation.
        Journal of the Association for Information Science and Technology, 71(7), 839-855. doi:10.1002/asi.24298
"""

blocking_method = "full_name"


### 1-3. Choose a similarity calculation metric ###

"""
(1) cos: cosine similarity
(2) jac: Jaccard similarity
(3) jrw: Jaro-Winkler similarity

"""

similarity_metric = "cos"      


### 1-4. Choose a classifier for pairwise similarity comparison ###

"""
(1) GB: Gradient Boosting
(2) RF: Random Forests
(3) LR: Logistic Regression
(4) NB: Naive Bays;
(5) SVM: Support Vector Machine
(6) DT: Decision Tree;

Choice of multiple classifier names available: e.g., classifier_lists = ['LR', 'RF', 'SVM']
URLs for details on each clssifier are available in procedures.py

"""

classifier_name_list = ['RF']


### 1-5. 10-fold cross validation is performed? ###

"""
(1) 1: yes
(2) 0: no

"""

cross_validation = 0


### 1-6. produce classification results? ###

"""
(1) 1: yes -> classification performance is evaluated on labeled test data
              and classification report is produced for precision, recall, and f1-score
(2) 0: no

"""

conduct_classification = 1   


### 1-7. Choose a clustering algorithm ###

"""
Clustering is a process of an algorithm to collate name instances into clusters
(1) hier: hierarchical agglomerative clustering
        -> NOTE! you must change below options < clusterer_blocking_on = 1, cluster_count = None >
        -> This process is implemented by the BEARD library for computational efficiency as introduced in
           Louppe, G., Al-Natsheh, H. T., Susik, M., & Maguire, E. J. (2016).
           Ethnicity Sensitive Author Disambiguation Using Semi-supervised Learning.
           Knowledge Engineering and Semantic Web, Kesw 2016, 649, 272-287. 

(2) db: DBSCAN
(3) spectral: spectral
(4) kmeans: K-Means
(5) agg: agglomerative clustering: change below options <clusterer_blocking_on = 0, cluster_count = integer number>

URLs for details on each clssifier are available in modules.py

"""

clustering_algorithm = "hier"

cluster_blocking_on = 1 # 1 for clustering with blocking applied (hierarchical); 0 for other clustering methods

cluster_count = None    # "None" for hierarchical clustering; integer(e.g., 1000) for DBSCAN, spectral, KMeans or agglomerative
    

### 1-8. If 'hier' is chosen, what is a threshold value? ###

"""
Set a threshold value to filter instance pairs to be put into the same cluster
between 0 and 1
A threshold value is a distance, i.e., 1 - similarity score, between name instances.
E.g., A threshold value of 0.3 is roughly equal to 70 % of probability of name instances
      referring to the same author entity
The lower the threshold value is, the higher the precision score is.

"""

threshold_list = [0.1, 0.5, 10] # [0] if clustering algorithms other than 'hier' are used
    
    # <- if various thresholds need to be used, put a starting threshold, an end threshold, and a number of samples in the list
    # e.g., [0.1, 0.3, 5]: this generates a list of thresholds [0.1, 0.15, 0.2, 0.25, 0.3]


### 1-9. Which clustering evaluation metric do you want to use? ###

"""
(1) cluster-f: cluster-f precision/recall/f1
(2) k-metric: k-metric precision/recall/f1
(3) split-lump: splitting & lumping error precision/recall/f1
(4) pairwise-f: paired precision/recall/f1    
(5) b-cubed: b3 precision/recall/f1  

For more details on clustering evaluation metrics, see a paper below
Kim, J. (2019). A fast and integrative algorithm for clustering performance evaluation
    in author name disambiguation. Scientometrics, 120(2), 661-681. 

"""

clustering_metric = "b-cubed" 


### 1-10. Would you like to assign a distinct identifier to each cluster? ###

"""
enable_cluster_id = True
enable_cluster_id = False 

The parameter enable_cluster_id controls whether a unique identifier is 
assigned to each cluster within the namespace "550e8400-e29b-41d4-a716-44665544abcd".
This can be useful for tracking individual clusters throughout an analysis. 
To enable cluster ID, set enable_cluster_id to True. The output file includes 
IDs in the first column and cluster lists in the second column with a tab as a delimiter. 
To disable cluster ID, set enable_cluster_id to False.

The namespace used in this script is a UUID (Universally Unique Identifier) 
generated with the value '550e8400-e29b-41d4-a716-44665544abcd'. A UUID is a 128-bit
identifier that is globally unique and can be used to prevent naming conflicts 
between different systems or entities. This namespace is used to create deterministic 
UUIDs using the uuid5() function from the uuid module, which takes a namespace and 
a name as input and generates a UUID based on them. 

"""

enable_cluster_id = True
cluster_id_namespace = uuid.UUID('550e8400-e29b-41d4-a716-44665544abcd')


###################################################
##########  Parameters for the case (2)  ##########
###################################################

"""
If you want to use the trained model for prediction,
you can change values of the follwing parameters
before you run the main code
"""

### 2-1. Type in file names ###

"""
Input files are required to be prepared in a specific format
(1) signature file: instance id, paper id, author byline position, name string, affiliation, etc. 
(2) record file: paper id, publication year, venue name, author list, title, etc.
                > Author names in the author list are seperated by vertical bar
(3) cluster file: No cluster file is provided. Clustering evaluation is unavailable.
Each file is created in .txt and columns are separated by tab.
Please see the example files provided with this code set. 
"""

predict_instance_file  = "signatures_test.txt"
predict_record_file    = "records.txt"
predict_cluster_file   = None


### 2-2. Choose a classifier for loading trained model ###

"""
(1) LR: Logistic Regression
(2) NB: Naive Bays
(3) SVM: Support Vector Machine
(4) DT: Decision Tree
(5) GB: Gradient Boosting
(6) RF: Random Forests

Choice of multiple classifier names available: e.g., classifier_lists = ['LR', 'RF', 'SVM']
URLs for details on each clssifier are available in procedures.py
"""

classifiers_list = ['RF']


### 2-3. Choose a blocking method ###

"""
Blocking is a step to collate name instances to be compared with each other
The blocking method selected here is applied to both training and test data

Three options are available
(1) first_initial: name instances that have the same surname and first forename initial are compared
        e.g., 'kim, jinseok' vs 'kim, j' > They share 'kim, j'
(2) full_name: name instances that have the same string are compared
        e.g., 'kim, jinseok' vs 'kim, jinseok' > They share 'kim, jinseok'
(3) forename_strip: name instances that have the same surname and n characters of forename are compared
        e.g., 'kim, jinseok' vs 'kim, jin s' > They share 'kim, jin' (if n == 3)

For more details on blocking and 3 options, see the paper below
    Kim, J., & Kim, J. (2020). Effect of forename string on author name disambiguation.
        Journal of the Association for Information Science and Technology, 71(7), 839-855. doi:10.1002/asi.24298
"""

blocking_method_name = "full_name"


### 2-4. Choose a clustering algorithm ###

"""
Clustering is a process of an algorithm to collate name instances into clusters
(1) hier: hierarchical agglomerative clustering
        -> NOTE! you must change below options < clusterer_blocking_on = 1, cluster_count = None >
        -> This process is implemented by the BEARD library for computational efficiency as introduced in
           Louppe, G., Al-Natsheh, H. T., Susik, M., & Maguire, E. J. (2016).
           Ethnicity Sensitive Author Disambiguation Using Semi-supervised Learning.
           Knowledge Engineering and Semantic Web, Kesw 2016, 649, 272-287. 

(2) db: DBSCAN
(3) spectral: spectral
(4) kmeans: K-Means
(5) agg: agglomerative clustering: change below options <clusterer_blocking_on = 0, cluster_count = integer number>

URLs for details on each clssifier are available in modules.py
"""

clustering_algorithm_name = "hier"

clusters_blocking_on = 1    # 1 for clustering with blocking applied (hierarchical); 0 for other clustering methods

clusters_count = None       # "None" for hierarchical clustering; integer(e.g., 1000) for DBSCAN, spectral, KMeans or agglomerative
   
    
### 2-5. If 'hier' is selected, what is the best threshold value? ###

"""
Set the best threshold value to filter instance pairs to be put into the same cluster
between 0 and 1
A threshold value is a distance, i.e., 1 - similarity score, between name instances.
E.g., A threshold value of 0.3 is roughly equal to 70 % of probability of name instances
      referring to the same author entity
The lower the threshold value is, the higher the precision score is.
"""

best_threshold = [0.35]     # [0] if clustering algorithms other than 'hier' are used


### 2-6. Would you like to assign a distinct identifier to each cluster? ###

"""
enable_cluster_id = True
enable_cluster_id = False 

The parameter enable_cluster_id controls whether a unique identifier is 
assigned to each cluster within the namespace "550e8400-e29b-41d4-a716-44665544abcd".
This can be useful for tracking individual clusters throughout an analysis. 
To enable cluster ID, set enable_cluster_id to True. The output file includes 
IDs in the first column and cluster lists in the second column with a tab as a delimiter. 
To disable cluster ID, set enable_cluster_id to False.

The namespace used in this script is a UUID (Universally Unique Identifier) 
generated with the value '550e8400-e29b-41d4-a716-44665544abcd'. A UUID is a 128-bit
identifier that is globally unique and can be used to prevent naming conflicts 
between different systems or entities. This namespace is used to create deterministic 
UUIDs using the uuid5() function from the uuid module, which takes a namespace and 
a name as input and generates a UUID based on them. 
"""

enable_clusters_id = False
clusters_id_namespace = uuid.UUID('550e8400-e29b-41d4-a716-44665544abcd')
 
    
    
###################################################
###############    Run Main Code    ###############
###################################################

if __name__ == "__main__":
    
    if model_usage == "train":      
        
        model_train_save(train_instance_file,
                         train_cluster_file,
                         train_record_file,
                         test_instance_file,
                         test_record_file,
                         blocking_method        = blocking_method,
                         similarity_metric      = similarity_metric,
                         classifier_name_list   = classifier_name_list,
                         cluster_file_test      = test_cluster_file,
                         cross_validation       = cross_validation,
                         conduct_classification = conduct_classification,
                         clustering_algorithm   = clustering_algorithm,
                         cluster_blocking_on    = cluster_blocking_on,
                         cluster_count          = cluster_count,
                         threshold_list         = threshold_list,
                         clustering_metric      = clustering_metric,
                         enable_cluster_id      = enable_cluster_id,
                         cluster_id_namespace   = cluster_id_namespace)
    
    elif model_usage == "predict": 
        
        model_inference(predict_instance_file,
                        predict_record_file,
                        blocking_method        = blocking_method_name,
                        classifier_name_list   = classifiers_list,
                        cluster_file_test      = predict_cluster_file,
                        clustering_algorithm   = clustering_algorithm_name,
                        cluster_blocking_on    = clusters_blocking_on,
                        cluster_count          = clusters_count,
                        threshold_list         = best_threshold,
                        enable_cluster_id      = enable_clusters_id,
                        cluster_id_namespace   = clusters_id_namespace)
        
    else:
        
        print("Wrong value for 'model_usage' parameter. Please provide the correct one: 'train' or 'predict'.")
        

        
''' measure finish time '''
elapsed_time_secs = time.time() - start_time
msg = "\nrun time: %s secs" % timedelta(seconds=round(elapsed_time_secs))
print(msg)

### The end of line ###
