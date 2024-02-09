## MediaConnect Easy Dashboard Maker

This script will quickly make a CloudWatch dashboard for one, tagged, or all MediaConnect flows in found in your current AWS Account and Region. 

The dashboard will have widgets for the most common and useful service metrics.

Remember to alter the time interval (granularity)  and time span (longevity)  of the chart to fit your workdlow.

High resolution metrics at 1s intervals exist for most MediaConnect metrics.

Short -interval metrics are not retained very long.  Use longer-interval metrics for larger timespans.

You can invoke this script directly in your AWS CLI or CloudShell prompt by copying and pastig this one line below:

XXX
