import streamlit as st
import pandas as pd
from PIL import Image
import ocr
import outputter
from config import logos_dir
# Load the logo from the file
logo = Image.open(f'{logos_dir}/ptcl.png')

# Display the logo in the sidebar
st.sidebar.image(logo, use_column_width=False)

# Load the DataFrame from the CSV file
df = pd.read_csv('output.csv')

# Sidebar controls
st.sidebar.header('Control Buttons')
run_ocr = st.sidebar.button('RUN OCR', key='run_ocr')
generate_csv = st.sidebar.button('Generate CSV', key='generate_csv')
# browse_images = st.sidebar.button('Browse Images', key='browse_images')

st.sidebar.header('Data Types')
show_comments = st.sidebar.checkbox('Comments', value=True, key='show_comments')
show_replies = st.sidebar.checkbox('Replies', value=True, key='show_replies')
show_time = st.sidebar.checkbox('Time', value=True, key='show_time')

# Run maintain.py when the OCR button is clicked
if run_ocr:
    # st.write('Running OCR...')
    ocr.ocr()  # assuming maintain.py has a function called run()
    # st.write('OCR completed.')

# Run outputter.py when the Generate CSV button is clicked
if generate_csv:
    # st.write('Generating CSV...')
    outputter.outputter()  # assuming outputter.py has a function called run()
    # st.write('CSV generation completed.')

# Filter the DataFrame based on the checkboxes
if not show_comments:
    df = df.loc[:, ~df.columns.str.contains('Comments')]
if not show_replies:
    df = df.loc[:, ~df.columns.str.contains('Replies')]
if not show_time:
    df = df.loc[:, ~df.columns.str.contains('Time')]
st.header('Select Groups')
# Define the networks and accounts
networks = ['facebook', 'twitter', 'instagram', 'linkedin']
accounts = ['Ufone', 'Upaisa', 'Corporate']

# Create a row of logos and checkboxes
logos_and_checkboxes = st.columns(len(networks))
checkboxes_dict = {}
for i, network in enumerate(networks):
    logo = Image.open(f'{logos_dir}/{network.lower()}.png')
    logos_and_checkboxes[i].image(logo, use_column_width=False)
    checkbox = logos_and_checkboxes[i].checkbox(network, value=True, key=f'{network}_checkbox')  # Added a unique key for each checkbox
    checkboxes_dict[network] = checkbox

# Create checkboxes for the accounts in the sidebar
st.sidebar.header('Choose Accounts')
account_checkboxes_dict = {}
for account in accounts:
    checkbox = st.sidebar.checkbox(account, value=True, key=f'{account}_checkbox')  # Added a unique key for each checkbox
    account_checkboxes_dict[account] = checkbox

# Filter the DataFrame based on the checkboxes at the bottom
for network, checkbox in checkboxes_dict.items():
    if not checkbox:
        df = df.loc[:, ~df.columns.str.contains(network)]

# Filter the DataFrame based on the account checkboxes
for account, checkbox in account_checkboxes_dict.items():
    if not checkbox:
        df = df.loc[:, ~df.columns.str.contains(account)]

# Main DataFrame display
st.dataframe(df)
