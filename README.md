## MediaConnect Easy Dashboard Maker

This script will quickly make a CloudWatch dashboard for one, tagged, or all MediaConnect flows in found in your current AWS Account and Region. 

![chart1](https://github.com/aws-samples/mediaconnect-dashboard-maker/blob/main/exampledash.jpg)

The dashboard will have widgets for the most common and useful service metrics.

Remember to alter the time interval (granularity)  and time span (longevity)  of the chart to fit your workdlow.

High resolution metrics at 1s intervals exist for most MediaConnect metrics. Short -interval metrics are not retained very long. 
Use longer-interval metrics for larger timespans.
_

### You can invoke this script directly in your AWS CLI or CloudShell prompt by copying and pastig this one line below:

```
python3 -c "$(curl -fsSL https://raw.githubusercontent.com/aws-samples/mediaconnect-dashboard-maker/main/MediaConnect_dashmaker_v07.py)"
```

===============

### For more AWS Media Services dashboard scripts, see the [AWS Blog Post here](https://aws-blogs-prod.amazon.com/media/cs-quick-and-easy-media-services-dashboards/)
