## MediaConnect Easy Dashboard Maker

This script will quickly make a CloudWatch dashboard for one, tagged, or all MediaConnect flows located in your current AWS Account and Region. 

![chart1](https://github.com/aws-samples/mediaconnect-dashboard-maker/blob/main/exampledash.jpg)

The new dashboard includes widgets for the most common & useful service metrics. 
*Remember* to update the time interval (granularity)  and time span (longevity)  of the chart to fit your workflow.

High resolution metrics at 1s intervals exist for most MediaConnect metrics. 
Short -interval metrics are not retained very long (3 hours). Refer to [the documentation](https://aws.amazon.com/cloudwatch/faqs/#:~:text=The%20retention%20period%20is%2015,hour%20available%20for%2015%20months) for roll-up intervals. 

Refer to the "Denitions" widget for explanations of the metrics used, and the retention intervals for past data points.

[Definitions](https://raw.githubusercontent.com/aws-samples/mediaconnect-dashboard-maker/main/definitions.jpg)
- -  

### You can invoke this script directly in your AWS CLI or CloudShell prompt by copying and pasting this one line below:

```
python3 -c "$(curl -fsSL https://raw.githubusercontent.com/aws-samples/mediaconnect-dashboard-maker/main/MediaConnect_dashmaker_v07.py)"
```

===============
### For more information on MediaConnect mertrics, see the [MediaConnect documentation](https://docs.aws.amazon.com/mediaconnect/latest/ug/monitor-with-cloudwatch-metrics-source-health.html)

_ _ 
### For more AWS Media Services dashboard scripts, see the [AWS Blog Post here](https://aws.amazon.com/blogs/media/cs-quick-and-easy-media-services-dashboards/)
