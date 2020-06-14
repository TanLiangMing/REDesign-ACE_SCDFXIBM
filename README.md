# RE Design Acclimatisation Conditioning Engine (ACE)

Team RE Design's proposed solution for SCDF X IBM Lifesavers' Innovation Challenge: Call for Code 2020.

## Contents

1. [Introduction](#introduction)
1. [Demo video](#demo-video)
1. [The architecture](#the-architecture)
1. [Project roadmap](#project-roadmap)
1. [Getting started](#getting-started)
1. [Running the tests](#running-the-tests)
1. [Live demo](#live-demo)
1. [Built with](#built-with)
1. [Authors](#authors)
1. [Acknowledgments](#acknowledgments)
1. [References](#references)

## Introduction

### What's the problem?

Climate change is inevitable, with projected increase in temperatures leading to phenomena such as the Urban Heat Island effect. This leads to an environment and climate where it is increasingly physically challenging for First Responders to train and operate to maximum efficiency and performance. How might SCDF leverage wearables or other technologies to provide relief or enhancement in harsh operating conditions and maximise the safety, health and performance of First Responders during training and operations?

### How can technology help?

Heat strain is a significant safety concern especially in the SCDF's line of work, worsened by projected environmental temperature increases. Not only is heat strain a safety concern, it also negatively affects performance and judgement [[1](#references)]. It is therefore crucial to monitor for signs of heat strain.

Currently, there are plenty of existing wearable technology to measure heat strain indicators, namely Hexoskin (Carré Technologies Inc., Montreal, Que., Canada), LifeMonitor EQ02 (Equivital, Cambridge, UK), BioHarness 3.0 (Zephr Performance Systems, Annapolis, Md., USA), Questemp II (3M, St. Paul, Minn., USA), BioNomadix (BIOPAC Systems, Inc., Goleta, Calif., USA), BioRadio (Great Lakes Neurotechnologies, Cleveland, Ohio, USA).

However most systems lack proper interpretation of physiological data to identify the signs and symptoms of excessive heat strain and merely displays what data it collects. Furthermore, they do not take into consideration the possible effects of climate change [[2](#references)].

### The idea

First Responders may face an increasing physical challenge because of the increased environmental temperature (ET) and humidity (EH), which affects their physiological and psychological states both before and during operations. ET and EH are thus critical factors to take into consideration to maximise safety and performance.

Since the SCDF is currently looking into integrating Equivital EQ02 LifeMonitor with wearable sensors in the Heat Strain Monitor System (HSM) [[3](#references)], we intend to leverage on this and build a more powerful model with the data collected from this system.

Our idea would be implemented in 2 phases: Training Phase, and Mission Phase.

**Training Phase**:
Individual physiological data (heart rate, core temperature [derive from skin temperature], breathing rate) from the wearable, as well as environmental data (ET and EH) from a WBGT device, would be captured and stored securely on IBM Cloud Object Storage after training. Our machine learning model, Acclimatisation Conditioning Engine (ACE), would then process the data via clustering and a time series analysis. A global threshold for each of the physiological data for a given environmental data would first be derived for anomaly detection. Our models will also learn the time-to-fatigue, which is how long a person can safely maintain their level of exertion, given their current vital signs and the prevailing environmental conditions. Following that, when sufficient data is collected, a personal threshold would be derived by giving individual data a higher weightage in the calculations.

**Mission Phase**:
The central hub would continue to monitor the soldiers' conditions. All soldiers would have a "health bar". When an anomaly is detected, be it during training or when soldiers are deployed, the central hub would notify the ground commander and HQ in the form of a depleting health bar, changing from green to yellow or red, depending on the number of thresholds breached by anomalous physiological data received. The estimated time-to-fatigue would also be displayed.

With this, both the ground commander and HQ can monitor the situation of all soldiers accurately as the model does not depend on a fixed index, but instead generates personal thresholds based on individualised data. Considering the highly volatile weather due to climate change, our customised thresholds provide a more accurate estimation of the soldiers' current "health".

## Demo video

[![Watch the video](https://github.com/Code-and-Response/Liquid-Prep/blob/master/images/IBM-interview-video-image.png)](https://youtu.be/vOgCOoy_Bx0)

## The architecture

![Architecture](Architecture.png)

1. EQ02 Life Monitor measures and transmits vitals information over wireless data link
2. Watson Internet of Things platform processes and visualises the information 
3. Watson Cloudant stores the information as a database on the cloud
4. Watson Studio utilizes Jupyter notebook to process the data and train the anomaly detection model

![Iot](Watson IoT platform.JPG)

![Cloudant](Cloudant Database.JPG)

## Project roadmap

![Roadmap](Roadmap.jpg)

## Getting started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Create a new Notebook on IBM Watson Studio and Import Packages 
```bash
import numpy as np
import pandas as pd
import matplotlib as plt
import types
import io
from botocore.client import Config
import ibm_boto3
import seaborn as sb
```

### Installing

Upload the following .csv files under examples/res to your Asset folder
  1. 5 sets of training dataset (SCDF_dataset1.csv -  SCDF_dataset5.csv)
  2. 1 set of test dataset: (SCDF_dataset_test1.csv)

Include a cell to store your IBM Watson Studio credentials in a dictionary. The format is as follows: 

```bash
credentials = {
    'IAM_SERVICE_ID': '*****',
    'IBM_API_KEY_ID': '*****',
    'ENDPOINT': 'https://s3-api.us-geo.objectstorage.service.networklayer.com',
    'IBM_AUTH_ENDPOINT': 'https://iam.cloud.ibm.com/oidc/token',
    'BUCKET': '*****'
}
```
For easier access to the 5 training datasets:

```bash
n_datasets = 5
dfs = []

for i in range(n_datasets):
    body = client.get_object(Bucket=credentials['BUCKET'],Key='SCDF_dataset%i.csv'%(i+1))['Body']
    # add missing __iter__ method, so pandas accepts body as file-like object
    if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )
    df_time = pd.read_csv(body, header=0, parse_dates=[0], index_col=0, squeeze=True)
    dfs.append(df_time.copy())
```
We have provided 5 sets of training datasets (5 training datasets each having differing environmental conditions) 
and 1 set of test dataset in the .csv format. 
The datasets are created by us to simulate real life conditions that vary with external temperature and humidity 
These files would be used primarily to build the anomaly detection model as a proof of concept.

## Running the tests

In our code, we experimented with 3 different sliding windows of duration (10min, 30min and 1 hour).
X contains 5 sets of data obtained from trainings under different 5 environmental conditions.

  1. Using df_10min and df_30min, we can calculate the average data (E.g Ext temp, Humidity etc) 
     over a 10min and 30min window respectively
  ```bash
  # Extract the Features from the Data
  X = pd.DataFrame(df_10min[["Ext Temp", "Humidity", "Core Temp", "Heart Rate", "Breathing Rate", "PSI"]])

  # Extract the Features from the Data
  X = pd.DataFrame(df_30min[["Ext Temp", "Humidity", "Core Temp", "Heart Rate", "Breathing Rate", "PSI"]])
  ```

  2. Local Outlier Factor was chosen as our anomaly detection algorithm where the local deviation in density 
     of a datapoint is measured with respect to its neighbours. An anomaly is then flagged if the datapoint 
     is sufficiently isolated compared to its neighbouring points. This trained model allows us to flag datapoint 
     as anomalous during operations and trainings if the datapoint collected deviates significantly from the 
     data points of other trainings under similar environmental conditions.
  
  ```bash
  # Create Anomaly Detection Model using LocalOutlierFactor
  lof = LocalOutlierFactor(n_neighbors = num_neighbors, contamination = cont_fraction)
  ```
  
  3. Num_neighbours refer to the number of nearest neighbours whose density will be compared with the new 
     datapoint. cont_fraction is set at a small value of 0.00025 as an example as we expect training to be 
     conducted in a safe environment. These 2 parameters can be further optimised with other data collected 
     in SCDF. As an example, we have set the parameters as 10 and 0.00025 for num_neighbours and cont_fractions. 
     
  ```bash
  # Set the Parameters for Neighborhood
  num_neighbors = 10      # Number of Neighbors
  cont_fraction = 0.00025    # Fraction of Anomalies
  ```
 
 4. The model is then fitted onto data obtained from training. 
  
  ```bash
  # Fit the Model on the Data and Predict Anomalies
  lof.fit(X)
  ```
  
 5. After the model is built, we load the test dataset (SCDF_dataset_test1.csv) and use the model to 
    predict the anomalies of the test dataset. 
  
  ```bash
  #Load test dataset
  body = client.get_object(Bucket=credentials['BUCKET'],Key='SCDF_dataset_test1.csv')['Body']
  # add missing __iter__ method, so pandas accepts body as file-like object
  if not hasattr(body, "__iter__"): body.__iter__ = types.MethodType( __iter__, body )
  real_time_data = pd.read_csv(body,  header=0, parse_dates=[0], index_col=0, squeeze=True)
  real_time_data.head()
  anomaly_or_not = clf.predict(real_time_data)
  ```
  
  6. A warning would only be detected if 10 consecutive anomalies are detected. This value can be changed 
     accordingly to tune the sensitivity of the detection system.
     
  ```bash
  counter = 0
  counterLimit = 10

  for i in range(0, anomaly_or_not.size):
      if (anomaly_or_not[i] == -1):
        counter += 1
          if counter >= counterLimit:
              print("Limit has been reach at datapoint", i, "at time =", i*5, "s")
      else:
          counter = 0
   ```
### Interpreting the results
The main advantage of our model is that it allows commanders to accurately estimate the time-to-fatigue 
of the responders in an operation

Anomaly Detection Model

| Situation | Window | Anomaly detected | Time-to-fatigue/min |
| --- | --- | --- | --- |
| 1 | 10 min | Y | <10 |
|   | 30 min | Y |
| 2 | 10 min | Y | <10 |
|   | 30 min | N |
| 3 | 10 min | N | <30 |
|   | 30 min | Y |
| 4 | 10 min | N | <30 |
|   | 30 min | N |     |


Our model is novel because it creates a cluster of normal data points for every set of environmental conditions. 
This allows us to easily flag anomalous data points pertaining to the specific environmental condition. However, 
our model will only work well if the model has been trained with a good range of different environmental conditions. 
Otherwise, an anomaly might be flagged because of anomalous environmental conditions and not because of anomalous 
vital signs.



  
### Break down into end to end tests

Explain what these tests test and why, if you were using something like `mocha` for instnance

```bash
npm install mocha --save-dev
vi test/test.js
./node_modules/mocha/bin/mocha
```

### And coding style tests

Explain what these tests test and why, if you chose `eslint` for example

```bash
npm install eslint --save-dev
npx eslint --init
npx eslint sample-file.js
```

## Live demo

You can find a running system to test at [callforcode.mybluemix.net](http://callforcode.mybluemix.net/)

## Built with

* [IBM Cloudant](https://cloud.ibm.com/catalog?search=cloudant#search_results) - The NoSQL database used
* [IBM Cloud Functions](https://cloud.ibm.com/catalog?search=cloud%20functions#search_results) - The compute platform for handing logic
* [IBM API Connect](https://cloud.ibm.com/catalog?search=api%20connect#search_results) - The web framework used
* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Authors

* **Tan Liang Ming** - *Leader*
* **Loh Aik Hui**
* **Matthew Loo Jun Kuan**
* **Neo Lin How, Anthony**
* **Victor Gwee De Ming**

## Acknowledgments

* Based on [Billie Thompson's README template](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2).

## References
1. Flouris, A. D., Dinas, P. C., Ioannou, L. G., Nybo, L., Havenith, G., Kenny, G. P., & Kjellstrom, T. (2018). Workers' health and productivity under occupational heat strain: a systematic review and meta-analysis. The Lancet Planetary Health, 2(12), e521-e531.
2. Notley, S. R., Flouris, A. D., & Kenny, G. P. (2018). On the use of wearable physiological monitors to assess heat strain during occupational heat stress. Applied physiology, nutrition, and metabolism = Physiologie appliquee, nutrition et metabolisme, 43(9), 869–881. doi:10.1139/apnm-2018-0173
3. SCDF (2018). REaction, Rescuers in action. https://www.scdf.gov.sg/docs/default-source/sgfpc-library/sgfpc/reaction-publication-2018-(november-edition).pdf
