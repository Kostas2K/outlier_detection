# About this project

There is an abundance of resources, from books to academic articles on anomaly detection (or outlier detection as our focus here). In this example we use some random generated data of refund requests from a media company about some sports programs and detect any activities that can be considered fraudulent. This is widely seen in financial companies and organisations, such as detecting suspicious activities on credit card activities, but we use as an example a sports subscription platform by giving some examples of how it could be used in the media sector to reduce income losses, or increase the total revenue. 

Instead of detecting outliers by by customer payments, a media company is looking how the frequency and total amount ofthe customers' requested refunds can cause concerns of illegal activities. Moreover, because most of the media companies' customer base is through subscriptions, the importance of big media events is also added in the potential features.

## Data fields definition

The initial fields in the original dataset, before creating new features are:

![alt text](image.png)

## Features definition

| Term | Definition |
|------|------------|
| Viewing Frequency | Number of times a user watches content within a period. |
| Viewing Time (Seconds) | Total time spent watching content, measured in seconds. |
| Inlier | A data point that fits within the expected distribution. |
| Outlier | A data point that deviates significantly from the expected distribution. |


## Criteria for setting up alerts

| Alert  | Definition |
|------|------------|
| Maximum total refund amount | Highest total amount for a refund request on a particular day |
| Detected outlier | Record detected as outlier by using methods, such as Isolation Forest or KNN |

# Storing the results

The final stage is using the google.cloud library to import the outliers scores as potentially being used as stream processing when outliers are shown in the alerts set-up.




