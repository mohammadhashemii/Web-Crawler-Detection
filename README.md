# Web Crawler Detection
This work is the final project of [Rahnema College](https://rahnemacollege.com/courses/machine_learning_fundamental) Machine Leaning internship program.
The aim of this project is to train an unsupervised model in order to recognize the web requests given to [Sanjagh Website](https://sanjagh.pro) are crawlers or not.
Finally, for taking advantage of this work, we had to create and develope a web application for production phase.


## Dataset

The dataset has been obtained from the Sanjagh server logs. Altough it cannot be publicly released, a tiny sample of can be found in `output.log`. In case you are intersted in the complete dataset, you can use any other nginx log servers available in the world wide internet.

A sample record structure is as follows:

`207.213.193.143 [2021-5-12T5:6:0.0+0430] [Get /cdn/profiles/1026106239] 304 0 [[Googlebot-Image/1.0]] 32`


## Project phases

| Phase | Description |
|--|--|
| [*EDA*](https://github.com/mohammadhashemii/Web-Crawler-Detection#EDA) | Exploratory Data Analysis and Feature Engineering  |
| [*Baseline Models*](https://github.com/mohammadhashemii/Web-Crawler-Detection#Baseline-Models) | Train some common and baseline clustring models for anomaly detection |

## EDA

In this phase we just got to know the data better! We exploratary searched about useful information in the dataset and tried to extract appropriate clues from it. It is highly recommended to run the `01_sanjaghDatasetEDA.ipynb` to see what we have exactly done in this part.

Then we had to create and generate some features. Here is the list of the features we have used:

| Feature | Description |
|--|--|
| *Click rate* | Higher click rate can only be achieved by an automated script  |
| *STD of path’s depth* | Deeper requests usually indicates a human user |
| *Percentage of 4xx status codes* | Usually higher for crawlers as there is higher chances of hitting an outdated or deleted pages |
| *Percentage of 3xx status codes* | Indicates redirected requests|
| *Percentage of HTTP HEAD requests* | Usually higher for crawlers as there is higher chances of hitting an outdated or deleted pages |
| *Percentage of image requests* | Web crawlers usually ignore images |
| *Average & sum of response_length & response_time* | Human users retrieve info from the web via browser, so it forces the user’s session to request additional resource automatically |
| *Set the user agent attributes* | Browser - OS - is_bot - is_pc |
| *Average of time between requests* | Is more for human requets |

## Baseline models

The baseline models we decided to use are [IsolationForest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html) and [LocalOutlierFactor](http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.LocalOutlierFactor.html)
