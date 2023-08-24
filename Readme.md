# Covid19EventDrivenPython

The intent of this repo is based on a coding challenge from several years ago.
The main caveat is that I did not undertake this until after the original challenge was over.
I still wanted to code it as a way to help show unassisted, individual effort to make an event-driven, cloud-based solution using an unfamiliar language.

## AWS Resources Used

- DynamoDb - this is used to store the status of the run and the csv data in the database.
- S3 - this is used to store the raw csv/txt files pulled down from the two different URLs.
- Lambda - these are used to perform all the data fetches, comparisons, etc.  They are the individual workers for the process.
- Step Functions - two step functions were used as targets of the EventBridge events.
- EventBridge - two event buses were used for processing.
- SNS - used to notify any subscribers of the result.  In this case, I used a personal email address to get verification emails.

## Process Flow

As previously noted, there are two EventBridge and Step Functions used to complete this.
The first EventBridge event bus is a daily schedule that simply pushes and event to the first step function.
The first step function checks the run status of the previous day, and if it failed, it will push an event to the second EventBridge with the file name(s) needing processing.
The rest of the step function will then pull the new data from the sources and writes the file up to an S3 bucket.
Another event is then published to that second EventBridge with the new file names.

The second step function has the responsibility of reading the individual files from the S3 bucket, comparing the data between them, and making appropriate updates in DynamoDb.
One change that I went with that was not really covered by the challenge was that I included logic to retroactively update information in the event that the data publisher changed information of old records.
One the data has been written to DynamoDb, the result of that lambda will then be pushed to DynamoDb as a separate record reflecting the success of the run.
Lastly, the result will be pushed to an SNS topic such that any subscribers will get the result of the job.

## Upload

This repo wasn't created until August 2023, which may seem odd.
There are a few reasons for this.
The main reason is that I wanted to make a personal Github account that would be used to better show the work I have done. 

Before uploading the code, I actually went back through and reread the functions I hadn't touched in about 2 years.
Even with the time that has passed, the code still holds up well and was able to function when I initiated the first step function.
Note, by functioning I mean that the entire process completed successfully as I wanted to ensure what I was uploading was still working as intended.