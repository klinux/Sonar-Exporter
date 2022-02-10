from prometheus_client.core import GaugeMetricFamily

def make_metrics(measures):
    label_list = ['projectKey']
    
    list_metrics = []
    for measure in measures.project_measures:

        projectKey = measure['project']
        label_values = [projectKey]

        for metric in measure['metrics']:

            metric_key = metric['key']
            metric_description = metric['description']
            metric_value = metric['value']

            gauge = GaugeMetricFamily(
                name=f"sonar_{metric_key}",
                documentation=metric_description,
                labels=label_list
            )

            gauge.add_metric(
                labels=label_values,
                value=metric_value
            )

            list_metrics.append(gauge)
    
    return list_metrics