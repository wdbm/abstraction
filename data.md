# data

# feature scaling

Standardization of datasets is a common requirement for many machine learning estimators implemented in the scikit; they might behave badly if the individual features do not more or less look like standard normally-distributed data: Gaussian with zero mean and unit variance -- often called a standard scores. Many machine learning algorithms assume that all features are centered around zero and have variance of the same order. A feature with a variance that is orders of magnitude larger that others might dominate the objective function and make the estimator unable to learn from other features. The scikit function `scale` provides a quick way to perform this operation on a single array-like dataset.

# data sets sources

- <https://www.kaggle.com/>
- <https://www.reddit.com/r/datasets/>

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

Curated conversation data sourced from Reddit is used for the conversation analysis and modelling. Specifically, conversational exchanges on Reddit are recorded. An exchange consists of an utterance and a response to the utterance, together with associated data, such as references and timestamps. A submission to Reddit is considered as an utterance and a comment on the submission is considered as a response to the utterance. The utterance is assumed to be of good quality and the response is assumed to be appropriate to the utterance based on the crowd-curated quality assessment inherent in Reddit.
