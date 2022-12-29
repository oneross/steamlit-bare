from todoist_api_python.api_async import TodoistAPIAsync
from todoist_api_python.api import TodoistAPI
from secret import TODOIST_API_TOKEN

# from beautiful_date import *
from datetime import datetime
from dateutil import relativedelta as durd

import pandas as pd


## Utility function
class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

## Delta calculation and display logic for Age    
def get_age(date_string, from_date = datetime.now()):
#     print(date_string, from_date)
    dt = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    delta = durd.relativedelta(from_date, dt)
    if delta.years >= 1:
        description = '1+ years'
        sort_order = 0
    elif delta.months >= 3:
        description = '3+ months'
        sort_order = 1
    elif delta.months >= 1:
        description = '1+ months'
        sort_order = 2
    elif delta.days >= 14:
        description = '2+ weeks'
        sort_order = 3
    elif delta.days >= 7:
        description = '1+ weeks'
        sort_order = 4
    elif delta.days >= 3:
        description = '3+ days'
        sort_order = 5
    elif delta.days >= 1:
        description = '1+ days'
        sort_order = 6
    else:
        description = '<1 day'
        sort_order = 7
        
    ## Approximate, doesn't account for varying month lengths, leap years, etc.
    age_in_days = (365 * delta.years) + (30 * delta.months) + (delta.days)
        
    result = {'description': description,
              'sort_order': sort_order,
              'age_in_days': age_in_days}
    age = dotdict(result)
    
    return age

## 
def get_due_description(date_string, from_date = datetime.now()):
    dt = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    delta = durd.relativedelta(dt, from_date)
    if delta.years >= 1:
        description = '1+ years'
        sort_order = 7
    elif delta.months >= 3:
        description = '3+ months'
        sort_order = 6
    elif delta.months >= 1:
        description = '1+ months'
        sort_order = 5
    elif delta.days >= 14:
        description = '2+ weeks'
        sort_order = 4
    elif delta.days >= 7:
        description = '1+ weeks'
        sort_order = 3
    elif delta.days >= 3:
        description = '3+ days'
        sort_order = 2
    elif delta.days >= 1:
        description = '1+ days'
        sort_order = 1
    else:
        description = '<1 day'
        sort_order = 0
        
    due_in_days = (365 * delta.years) + (30 * delta.months) + (delta.days)
        
    result = {'description': description,
              'sort_order': sort_order,
              'age_in_days': due_in_days}
    due_description = dotdict(result)
    
    return due_description

def get_descendent_count(task, tasks):
    node_id = task.id
    direct_descendents = [t for t in tasks if t.parent_id == node_id]
    if direct_descendents:
        number_direct_descendents = len(direct_descendents)
        descendents_childcounts = [get_descendent_count(d, tasks) for d in direct_descendents]
        number_descendents_descendents = sum(descendents_childcounts)
        descendent_count = number_direct_descendents + number_descendents_descendents
    else:
        descendent_count = 0
    
    return descendent_count

def get_display_hierarchy(task):
    if hasattr(task, 'Section'):
        section_appendix = '/' + task.Section.name
    else:
        section_appendix = ''
    result = task.Project.name + section_appendix + ': '
    return result

def get_project_by_id(project_id, projects):
    result = [p for p in projects if p.id == project_id][0]
    return result

def get_section_by_id(section_id, sections):
    result = [s for s in sections if s.id == section_id][0]
    return result

def get_task_by_id(task_id, tasks):
    result = [t for t in tasks if t.id == task_id][0]
    return result

# Fetch tasks synchronously
def get_tasks_sync(filterString):
    api = TodoistAPI(TODOIST_API_TOKEN)
    try:
        projects = api.get_projects()
        sections = api.get_sections()
        if filter:
            tasks = api.get_tasks(filter=filterString)
        else:
            tasks = api.get_tasks()
        
        for task in tasks:
            task.Age = get_age(task.created_at)
            
            # due = get_due_description(task.Due.) ##due date differently formatted, more difficult
            
            task.Project = get_project_by_id(task.project_id, projects)
            if task.section_id:
                task.Section = get_section_by_id(task.section_id, sections)
            task.display_hierarchy = get_display_hierarchy(task)
            task.descendent_count = get_descendent_count(task, tasks)
        return(tasks)
    except Exception as error:
        print(error)
        
import copy
def objToDict(inputObj):
    d = copy.copy(inputObj).__dict__
    for key in d:
        try:
            dummy = d[key].__dict__
            d[key] = objToDict(d[key])
        except:
            pass
    return d

def get_tasks_dict(filterString):
    tasks = get_tasks_sync(filterString)
    dictTasks = [objToDict(t) for t in tasks]
    return dictTasks

## adjust priority... grrr
def reverse_priority(x):
    if x == 1:
        result = 4
    elif x == 2:
        result = 3
    elif x == 3:
        result = 2
    elif x == 4:
        result = 1
    else:
        pass
    return result
def better_reverse_priority(x):
    result = 5-x
    return result

def get_tasks_df(filter=None):
    dictTasks = get_tasks_dict(filter)
    df = pd.json_normalize(dictTasks)
    oldColumnNames = df.columns
    newColumnNames = [c.replace('.','_').lower() for c in oldColumnNames]
    for i in range(len(oldColumnNames)):
        oldName = oldColumnNames[i]
        newName = newColumnNames[i]
        df.rename(columns = {oldName:newName}, inplace = True)
    
    df['priority'] = df['priority'].apply(lambda x: reverse_priority(x))
    return df

