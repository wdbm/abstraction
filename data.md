# data

# feature scaling

Standardisation of datasets is a common requirement for many machine learning estimators implemented in the scikit; they might behave badly if the individual features do not more or less look like standard normally-distributed data: Gaussian with zero mean and unit variance -- often called a standard scores. Many machine learning algorithms assume that all features are centered around zero and have variance of the same order. A feature with a variance that is orders of magnitude larger that others might dominate the objective function and make the estimator unable to learn from other features. The scikit function `scale` provides a quick way to perform this operation on a single array-like dataset.

# imputation

Imputation is the process of replacing missing data with substituted values. There are various methods to impute missing values. Sometimes it is better to remove null values directly and sometimes it is better to use sophisticated mining techniques to impute the values. Initially, why data is missing should be investigated, there should be an analysis of the distribution of missing data and then an imputation strategy should be selected that yields the least biased estimates.

Listwise (complete case) deletion excludes an entire record from analysis if any single value of the record is missing. This affects the statistical power of the tests conducted because statistical power relies in part on sample size. Listwise deletion is problematic when the reasons for data being missing are not random and can result in a bias in data findings.

A global constant can be used in place of a missing value. This makes the distinction between empty and missing values. Empty values can be vital for an analysis. If the missing values of a vital variable cannot be differentiated from "empty" then they can be categorised as a different value from the rest of the data set using a global constant such as "NA".

Domain knowledge can be used to replace the missing value. Experts can suggest a reasonable value for missing data.

Attribute mean or median (for numerical data) or mode (for categorical data) can be used to replace missing data. This reduces the variability of the data, which weakens the correlation estimates.

An indicator variable can be used for missing values.

A data-mining algorithm can be used to predict a probably value for the missing value.

# SUSY Data Set

- <https://archive.ics.uci.edu/ml/datasets/SUSY>
- <http://arxiv.org/abs/1402.4735>

The SUSY Data Set is a classification problem to distinguish between a signal process which produces supersymmetric particles and a background process which does not. In the data, the first column is the class label (1 for signal, 0 for background), followed by 18 features (8 low-level features and 10 high-level features):

- lepton 1 pT
- lepton 1 eta
- lepton 1 phi
- lepton 2 pT
- lepton 2 eta
- lepton 2 phi
- missing energy magnitude
- missing energy phi
- MET_rel
- axial MET
- M_R
- M_TR_2
- R
- MT2
- S_R
- M_Delta_R
- dPhi_r_b
- cos(theta_r1)

This data has been produced by MadGraph5 Monte Carlo simulations of 8 TeV proton collisions, with showering and hadronisation performed by Pythia 6 and detector response simulated by Delphes. The first 8 features are kinematic properties measured by simulated particle detectors. The next 10 features are functions of the first 8 features; they are high-level features derived by physicists to help discriminate between the two classes. There are 46% positive examples in the SUSY data set. The features were standardised over the entire training/testing sets with mean zero and standard deviation one, except for those features with values strictly greater than zero; these were scaled such that the mean value was one.

# curated conversation data

Curated conversation exchange data sourced from Reddit is used for the conversation analysis and modelling. An exchange consists of an utterance and a response to the utterance, together with associated data, such as references and timestamps. A submission to Reddit is considered as an utterance and a comment on the submission is considered as a response to the utterance. The utterance is assumed to be of good quality and the response is assumed to be appropriate to the utterance based on the crowd-curated quality assessment inherent in Reddit.
