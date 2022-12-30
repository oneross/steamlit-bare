import streamlit as st
import streamlit.components.v1 as components
from dashboard import todoist_helper as th

###
# Filter definitions
###

photoURL = 'https://images.unsplash.com/photo-1568849676085-51415703900f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=774&q=80'

class DotDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

dFilters = {
    'mit':  '(2 days & p1) | (today & p2) | (7 days & @deadline)',
    'tod':  'today | overdue',
    'tom':  'tomorrow',
    'work': '(no due date & @work & !p4) | (2 days & @work) | (no due date & ##Work & !p4) | (2 days & ##Work) | (7 days & @work & @deadline) | (7 days & ##Work & @deadline)'
}
filter = DotDict(dFilters)

###
# pull tasks
###

mit = th.get_tasks_sync(filter.mit)
tod = th.get_tasks_sync(filter.tod)
tom = th.get_tasks_sync(filter.tom)
work = th.get_tasks_sync(filter.work)


# Initialize a session state variable that tracks the sidebar state (either 'expanded' or 'collapsed').
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'collapsed'

# Streamlit set_page_config method has a 'initial_sidebar_state' argument that controls sidebar state.
st.set_page_config(initial_sidebar_state=st.session_state.sidebar_state, layout='wide')

# Show title and description of the app.
st.sidebar.markdown('Settings:')

#     st.experimental_rerun()

def hasSharedElement(listX, listY):
    result = set(listX) and set(listY)
    return result

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
    
left, center, right = st.columns(3)

left.metric(label='MITs', value = len(mit), delta=3-len(mit))
center.metric(label = 'Work', value = len(work), delta = 5-len(work))
right.image(photoURL)

def md_blob(list):
    result = '\n'.join(['- {}'.format(th.get_task_display(i)) for i in list])
    return result

left.markdown(md_blob(mit))

top5work = th.get_sorted_top_x(work, 3)
center.markdown(md_blob(top5work))


# with right:
#     components.iframe(src='https://todoist.com/app/filter/268907551', height=500)
#     components.iframe(src='https://todoist.com/app/filter/2327135248', height=500)


'---\nHello world!\n---'
