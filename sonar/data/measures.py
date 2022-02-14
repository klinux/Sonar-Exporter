from copy import copy
from urllib import response
from sonar.data.projects import get_list_projects


permitted_metrics = [

    # Size
    'ncloc',
    'lines',
    'classes',
    'functions',
    'files',
    'directories',

    # Reliability
    'bugs',
    'reliability_rating',
    'reliability_remediation_effort',

    # Maintainability
    'code_smells',
    'development_cost',
    'effort_to_reach_maintainability_rating_a',
    'sqale_index',
    'sqale_rating',

    # Security
    'security_hotspots',
    'security_rating',
    'security_remediation_effort',

    # Complexity
    'complexity',
    'cognitive_complexity',

    # Coverage
    'lines_to_cover',
    'line_coverage',
    'uncovered_lines',
    'branch_coverage',
    'conditions_to_cover',
    'uncovered_conditions',

    # Duplications
    'duplicated_lines',

    # Issues
    'violations',
    'open_issues',
    'reopened_issues',
    'confirmed_issues',
    'false_positive_issues',
    'wont_fix_issues',
]


class Measures(object):
    def __init__(self, sonar):
        all_projects, _, _ = get_list_projects(sonar)
        all_metrics = get_all_metrics(sonar)
       
        self.project_measures = get_project_measures(sonar, all_projects, all_metrics)

def get_project_measures(sonar, all_projects, all_metrics):
    all_measures = []
    for project in all_projects:
        all_measures.append(get_project_measure(sonar, project, all_metrics))
    return all_measures

def get_project_measure(sonar, projectKey, all_metrics):
    url = f"{sonar.server}/api/measures/component"

    params = {
        'component': projectKey,
        'metricKeys': ",".join(permitted_metrics)
    }

    print(params)

    response = sonar.req.do_get(url, params)
    if response.status_code != 200:
        return None
    raw_data = response.json()
    
    component = raw_data['component']

    measure = {}
    measure['project'] = component['key']
    measure['metrics'] = []

    for item in component['measures']:    
        if item['metric'] in all_metrics:
            metric = copy(all_metrics[item['metric']])
            metric['value'] = item['value']
            measure['metrics'].append(metric)

    return measure

def get_all_metrics(sonar):
    url = f"{sonar.server}/api/metrics/search"

    response = sonar.req.do_get(url)
    if response.status_code != 200:
        return []

    raw_data = response.json()
    
    metric_dict = {}
    for metric in raw_data['metrics']:
        metric_dict[metric['key']] = metric_info(metric)
        
    return metric_dict

def metric_info(metric):
    return {
        'key': metric['key'],
        'description': metric['name']
    }