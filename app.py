import todoist_helper as td
# import pandas as pd
import streamlit as st
import altair as alt
import altair_helpers as ah

# Initialize a session state variable that tracks the sidebar state (either 'expanded' or 'collapsed').
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'collapsed'

# Streamlit set_page_config method has a 'initial_sidebar_state' argument that controls sidebar state.
st.set_page_config(initial_sidebar_state=st.session_state.sidebar_state)

## styles
st.markdown("""
<style>
.small-font {
    font-size:10px !important;
}
</style>
""", unsafe_allow_html=True)

# Show title and description of the app.
st.title('Dashboard')
st.sidebar.markdown('Select active projects:')

#     st.experimental_rerun()



def format_task(taskName, taskUrl):
    return '* ' + taskName + '  --> [Link](' + taskUrl + ')'
def stMarkdownPrint(taskName, taskUrl):
    st.markdown(format_task(taskName, taskUrl))
def printTasks(df, style=None):
    taskBlob = '<BR>'.join([format_task(x,y) for x, y in zip(df['content'], df['url'])])
    if style:
        prefix = '<div style="font-size: small">'
        postfix = '</div>'
        st.markdown(prefix+taskBlob+postfix, unsafe_allow_html=True)
    else:
        st.markdown('\n'.join([format_task(x,y) for x, y in zip(df['content'], df['url'])]))

df = td.get_tasks_df()

projOrder = df[['project_name', 'project_order']]
sortProjOrder = projOrder.sort_values(['project_order'])
projects = sortProjOrder['project_name'].unique()

with st.sidebar:
    display_projects = {}
    for p in projects:
        display_projects[p] = st.checkbox(p, value = True)
    
# st.session_state.sidebar_state = 'collapsed'

tasks = df[df['project_name'].isin([key for key in display_projects if display_projects[key]])]

left, right = st.columns(2)

with left:
    'Upcoming Task Density by Priority'
    (heatmap, text) = ah.get_heatmap_with_counts(tasks, 'due_date', 'priority', xTitle=None, yTitle='Pri')
    heatmap + text

with right:
    'Top Priority 1 Tasks'
    top_tasks = tasks[tasks['priority'] == 1].sort_values(by = ['due_date', 'order'], ascending=True).head(3)
    # printTasks(top_tasks, style='small-font')
    printTasks(top_tasks)

with st.expander('Full list of tasks'):
    printTasks(tasks)
