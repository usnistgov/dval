## 18summer-1.4-alpha  (v2018.7.11)

* Fix bugs occuring when running unittest discover 
* Fix division by zero in normalize method
* Add an option in pipelines validation to skip the rank validation
* objectDetectionAP metric now supports str parsed arrays as an input

## 18summer-1.3-alpha  (v2018.7.05)

* Fix Pipelines schema full validation
* Fix categorical targets validation
* Handle the case where test data and ground truth have different shapes

## 18summer-1.2-alpha  (v2018.7.02)

* Allow duplicate primitives in steps
* Add TA3 Task1 validation
* Fix some bugs

## 18summer-1.1-alpha  (v2018.6.27)

* Add transformed and normalized scores and baseline scores


## 18summer-1.0-alpha  (v2018.6.10)
First release for *Summer 2018 Evaluation* Validation and Scoring

* Add a CHANGELOG.md file tracking version changes.
* Support for MIT-LL data specification v3.1
* Support for v3.1 metrics and metric parameters
  * f1 parameter
  * score on all targets
* Added new metrics precision and recall (object metric still TBD)
* Task 2 scoring - summer 2018 specification
* Support for metalearning format pipelines


## v2018.4.28
Last release according to *February 2018* Evaluation standards.

Released on April 4th 2018

* Added post-search validation
* Added test script generation
