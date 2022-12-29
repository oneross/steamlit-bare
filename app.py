# import todoist_helper as td
# import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import altair as alt
import altair_helpers as ah



# Initialize a session state variable that tracks the sidebar state (either 'expanded' or 'collapsed').
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'collapsed'

# Streamlit set_page_config method has a 'initial_sidebar_state' argument that controls sidebar state.
st.set_page_config(initial_sidebar_state=st.session_state.sidebar_state, layout='wide')

# Show title and description of the app.
st.title('Dashboard')
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

# with st.sidebar:
#     display_projects = {}
#     display_tags = {}
#     with st.expander('Projects'):
#         for p in projects:
#             display_projects[p] = st.checkbox(p, value = True)
#     with st.expander('Tags'):
#         for t in tags:
#             display_tags[t] = st.checkbox(t, value = True)
    
left, right = st.columns(2)

with left:
    components.iframe(src='https://todoist.com/app/filter/268907551', height=500)

with right:
    components.iframe(src='https://todoist.com/app/filter/2327135248', height=500)


'---\nHello world!\n---'
