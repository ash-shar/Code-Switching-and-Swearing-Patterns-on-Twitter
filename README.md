# A Study of English-Hindi Code-Switching and Swearing Patterns on Twitter

This github repository contains codes for Abusive Tweet Detection, Location Detection of users and gender detection of users on Twitter. The proposed algorithms are suited for dataset consisting of code-mixed English-Hindi tweets from Indian users and can be extended to other bilingual/multilingual communities.

## Our Main Objective

Swearing is a prevalent phenomenon, in regular conversations as well as on social media. Whether multilinguals have a preference for a language while swearing and if so, what factors influence it, is an interesting question that has intrigued linguists, but large scale studies of multilingual swearing behavior has been impossible due to unavailability of data. In this study with English and Romanized Hindi tweets from multilingual Indian users, for the first time, we show that indeed when people code-switch, there is a strong preference for swearing in the dominant language, i.e. Hindi in this case. We also study the correlations between topic, gender and language preferences while swearing.

## Workshop Paper
Prabhat Agarwal, **Ashish Sharma**, Jeenu Grover, Mayank Sikka, Koustav Rudra and Monojit Choudhury, *I may talk in English but gaali toh Hindi mein hi denge: A study of English-Hindi Code-Switching and Swearing Pattern on Social Networks*, Social Networking Workshop, COMSNETS 2017, 9th International Conference on Communication Systems & Networks.

Presentation Given at the workshop can be found here: [PRESENTATION LINK](https://drive.google.com/open?id=1hYoDDd-djjhypvNas-IztHs2tb66JzFH)

## Prerequisites

- Python 3 (will work with python 2 after minor tweaks)

## Using the detectors

### Abusive Tweet Detector
The overview of our Abusive Tweet Detection algorithm is as follows:

![Abusive Tweet Detection Overview](https://github.com/ash-shar/Code-Switching-and-Swearing-Patterns-on-Twitter/blob/master/Abusive-Tweet-Detection-Overview.PNG?raw=true "Title")

For using this abusive tweet detector, use the function *classifyTweet()* present in [**Abusive_Tweet_Classifier.py**](https://github.com/ash-shar/Code-Switching-and-Swearing-Patterns-on-Twitter/blob/master/Abusive_Tweet_Detector/Abusive_Tweet_Classifier.py)

```
from Abusive_Tweet_Detector import Abusive_Tweet_Classifier

output = Abusive_Tweet_Classifier.classifyTweet("Saala Uss Waqt se 10.2 K MC chutiya Bna Ra","654680949523791872")
# output: [('saala', 'CM', [('saala', 'DM')]), ('chutiya', 'CM', [('chutiya', 'DM')])]
```

The function takes tweet and tweet_id as input and returns a list of abusive words present in a tweet. If the length of the returned list is 0, the tweet is non-abusive and if it is >0, the tweet is abusive. Sample run is at the end of that file.

### Location Detector
The json object returned by Twitter's developer API for users has location information as spefcied by the user. However, some users opt not to specify their location (around 30% in our case). For the ones who specify the location, it is highly unformatted. Some specify only city, some only state, some both. Also, some of them provide random locations.

So, for extracting location out of this, we first created a database of all the cities and states of india and major countries of the world. These were then looked in the location provided by the user and city, state, country, etc. were infered.

For using location detector, use the function *detect_location()* present in [location_detector.py](https://github.com/ash-shar/Code-Switching-and-Swearing-Patterns-on-Twitter/blob/master/Location_Detector/location_detector.py)

```
from Location_Detector import location_detector

output = location_detector.detect_location('i live in jaipur')
# output: {'city': 'jaipur', 'country': 'india', 'state': 'rajasthan'}
```

The function takes a string as input and returns a dictionary with the detected location in its city, state and country values.

### Gender Detector

For detecting gender of the users, we use the fact that male and female names differ considerably in general. We use [NamSorGender API](http://api.namsor.com/) which determines gender of a person on a -1 (Male) to +1 (Female) scale. 

For using gender detector, use the function *detect_gender()* present in [gender_detector.py](https://github.com/ash-shar/Code-Switching-and-Swearing-Patterns-on-Twitter/blob/master/Gender_Detector/gender_detector.py)

```
from Gender_Detector import gender_detector

output = gender_detector.detect_gender('Ashish Sharma', geography = 'in')
# output: Male
```

The function takes name of the person and optionally geography of the person (default: India) as input and returns the detected gender (Male/Female).