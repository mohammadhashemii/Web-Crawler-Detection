# Web Crawler Detection
This work is the final project of [Rahnema College](https://rahnemacollege.com/courses/machine_learning_fundamental) Machine Leaning internship program.
The aim of this project is to train an unsupervised model in order to recognize the web requests given to [Sanjagh Website](https://sanjagh.pro) are crawlers or not.
Finally, for taking advantage of this work, we had to create and develop a web application for production phase. Reach the webpage by clicking this link: [Demo](http://157.90.221.151:3000/)

We highly recommend you to see the presentation slides [here](https://github.com/mohammadhashemii/Web-Crawler-Detection/tree/master/presentation) to get a better intuition of what we have done.

## Dataset

The dataset has been obtained from the Sanjagh server logs. Although it cannot be publicly released, a tiny sample of can be found in [`output.log`](https://github.com/mohammadhashemii/Web-Crawler-Detection/blob/master/dataset/output.log). In case you are interested in the complete dataset, you can use any other nginx log servers available in the world-wide internet.

A sample record structure is as follows:

`207.213.193.143 [2021-5-12T5:6:0.0+0430] [Get /cdn/profiles/1026106239] 304 0 [[Googlebot-Image/1.0]] 32`


## Project phases

| Phase | Description |
|--|--|
| [*EDA*](https://github.com/mohammadhashemii/Web-Crawler-Detection#EDA) | Exploratory Data Analysis and Feature Engineering.  |
| [*Baseline Models*](https://github.com/mohammadhashemii/Web-Crawler-Detection#Baseline-Models) | Train some common and baseline Clustering models for anomaly detection. |
| [*Advanced Models*](https://github.com/mohammadhashemii/Web-Crawler-Detection#Advanced-Models) | Auto encoders are used! |
| [*Demo*](https://github.com/mohammadhashemii/Web-Crawler-Detection#Evaluation) | A simple demo webpage developed.|

## EDA

In this phase we just got to know the data better! We exploratory searched about useful information in the dataset and tried to extract appropriate clues from it. It is highly recommended running the `01_sanjaghDatasetEDA.ipynb` in [notebooks/](https://github.com/mohammadhashemii/Web-Crawler-Detection/tree/master/notebooks) to see what we have exactly done in this part.

Then we had to create and generate some features per session. These features can be modified in `my_utils.py` in [utils/](https://github.com/mohammadhashemii/Web-Crawler-Detection/tree/master/utils) Here is the list of the features we have used:

| Features per session | Description |
|--|--|
| *Click rate* | Higher click rate can only be achieved by an automated script. |
| *STD of path’s depth* | Deeper requests usually indicates a human user |
| *Percentage of 4xx status codes* | Usually higher for crawlers as there is higher chances of hitting an outdated or deleted pages. |
| *Percentage of 3xx status codes* | Indicates redirected requests|
| *Percentage of HTTP HEAD requests* | Usually higher for crawlers as there is higher chances of hitting an outdated or deleted pages. |
| *Percentage of image requests* | Web crawlers usually ignore images |
| *Average & sum of response_length & response_time* | Human users retrieve info from the web via browser, so it forces the user’s session to request additional resource automatically.|
| *Set the user agent attributes* | Browser - OS - is_bot - is_pc |
| *Average of time between requests* | Is more for human requests |
| *Number of *robots.txt* requests* | Crawlers wants to know the limitations! |
| *Percentage of consecutive repeated requests* | Crawlers wants to know the limitations! |

## Baseline models

The baseline models we decided to use are [IsolationForest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html) and [LocalOutlierFactor](http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.LocalOutlierFactor.html).

### IsolationForest

The Isolation Forest is a technique for the detection of outlier samples. Since outliers have features X that differ significantly from most of the samples, they are isolated earlier in the hierarchy of a decision tree. Outliers are detected by setting a threshold on the mean length (number of splits) from the top of the tree downwards. The Scikit-learn implementation provides a score for each sample that increases from -1 to +1 with the number of splits. The sample with lower score are likely to be outliers. The outlier threshold on the score must be set by the user.

![](https://github.com/mohammadhashemii/Web-Crawler-Detection/blob/master/images/IsolationForestScore.png)

And then for better visualization, we applied PCA with 3 components to see how outilers and inliers are seperated.

![](https://github.com/mohammadhashemii/Web-Crawler-Detection/blob/master/images/PCA.png)


### LocalOutlierFactor

The anomaly score of each sample is called Local Outlier Factor. It measures the local deviation of density of a given sample with respect to its neighbors. It is local in that the anomaly score depends on how isolated the object is with respect to the surrounding neighborhood. More precisely, locality is given by k-nearest neighbors, whose distance is used to estimate the local density. By comparing the local density of a sample to the local densities of its neighbors, one can identify samples that have a substantially lower density than their neighbors. These are considered outliers.

But the results of IsolationForest were more accurate.

## Advanced Models

One of the most promising methods for unsupervised task is Auto encoders. We got the best results for that.

### Auto encoders

It is a neural network architecture capable of discovering structure within data in order to develop a compressed representation of the input. Applications: anomaly detection, data denoising and ... . 
 
 ![](https://github.com/mohammadhashemii/Web-Crawler-Detection/blob/master/images/autoencoder.png)

 The training configuration we use is as follows. These can be modified in `configs.py` which can be found in [configs/](https://github.com/mohammadhashemii/Web-Crawler-Detection/tree/master/configs).

 | Setting | Type |
|--|--|
| *Optimizer* | Adam |
| *Loss* | MSE |
| *Activations* | ReLu |
| *# of epochs* | 20|
| *Batch size* | 64 |
| *Percentage of image requests* | Web crawlers usually ignore images |

Additionally, multiple architectures have been tested and the comparison of them is shown below:

 | # of neurons | Train loss | Test loss |
|--|--|--|
| *[15, 7, 15]* | 0.42 | 0.48 |
| ***[15, 3, 15]*** | 0.28 | 0.39 |
| *[15, 7, 3, 7, 15]* | 0.29 | 0.43 |
| *[15, 7, 7, 7, 15]* | 0.31 | 0.42 |

As for all the unsupervised algorithms an anomaly score threshold should be selected, after many experiments, the MSE threshold which fits best for the dataset is 0.26. But you can modify it based on your own dataset in `configs.py` which can be found in [configs/](https://github.com/mohammadhashemii/Web-Crawler-Detection/tree/master/configs). Also we evaluated our models and it can be checked thorough presentation slides in [presentation/](https://github.com/mohammadhashemii/Web-Crawler-Detection/tree/master/presentation).

## Demo

We have used [Flask](https://flask.palletsprojects.com/en/2.0.x/) and [React](https://reactjs.org) to develop a webpage for our project. Firstly check it [here](http://157.90.221.151:3000/). In case you are interested in running the webpage locally follow the steps below:

### How to run

The whole source code of the webpage can be found in [App/](https://github.com/mohammadhashemii/Web-Crawler-Detection/tree/master/App). Firstly, clone the repository and run the commands below:

1. Clone the repo:

```
git clone https://github.com/mohammadhashemii/Web-Crawler-Detection
cd Web-Crawler-Detection
```

2. Run the backend:

```
cd backend
pip install flask flask-cors
python app.py
```

3. Run the frontend:

```
cd frontend
npm install
npm start
```