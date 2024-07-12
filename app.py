import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Load the dataset
@st.cache_data
def load_data():
    data = pd.read_csv('Airline_satisfaction.csv')  # Replace with the actual dataset path
    return data

data = load_data()

# Preprocess the dataset
data['Departure Delay'] = data['Departure Delay in Hrs'] > 0
data['Arrival Delay'] = data['Arrival Delay in Hrs'] > 0

# Helper function to convert Yes/No to 1/0
def yes_no_to_numeric(value):
    return 1 if value == "Yes" else 0

# 1. Percentage of satisfied passengers
satisfaction_counts = data['satisfaction'].value_counts(normalize=True) * 100
customer_satisfaction_fig = px.pie(names=satisfaction_counts.index, values=satisfaction_counts.values, title="Percentage of Satisfied Passengers")

# Satisfaction by customer type
customer_type_satisfaction = data.groupby(['Customer Type', 'satisfaction']).size().reset_index(name='counts')
customer_type_satisfaction_fig = px.bar(customer_type_satisfaction, x='Customer Type', y='counts', color='satisfaction', barmode='group', title='Satisfaction by Customer Type')

# Satisfaction by travel type
travel_type_satisfaction = data.groupby(['Type of Travel', 'satisfaction']).size().reset_index(name='counts')
travel_type_satisfaction_fig = px.bar(travel_type_satisfaction, x='Type of Travel', y='counts', color='satisfaction', barmode='group', title='Satisfaction by Travel Type')

# 2. First-time vs Returning Customers
customer_type_counts = data['Customer Type'].value_counts()
customer_type_fig = px.pie(names=customer_type_counts.index, values=customer_type_counts.values, title="First-time vs Returning Customers")
customer_type_bar_fig = px.bar(x=customer_type_counts.index, y=customer_type_counts.values, title="Number of First-time vs Returning Customers")

# 3. Average age of first-time male and female passengers
first_time_male_age = data[(data['Customer Type'] == 'First-time') & (data['Gender'] == 'Male')]['Age'].mean()
first_time_female_age = data[(data['Customer Type'] == 'First-time') & (data['Gender'] == 'Female')]['Age'].mean()

# 4. Passengers with Departure Delay but no Arrival Delay
departure_no_arrival_delay_count = data[(data['DepartureDelay']) & (~data['ArrivalDelay'])].shape[0]

# 5. Passengers in Business class vs Economy class
class_counts = data['Class'].value_counts()
class_counts_fig = px.pie(names=class_counts.index, values=class_counts.values, title="Business vs Economy Class Passengers")

# Streamlit app
st.title("Airline Passenger Satisfaction Dashboard")

st.header("Dataset Overview")
st.dataframe(data.head(100))  # Display the first 100 rows of the dataset

st.header("1. Percentage of Satisfied Passengers")
st.plotly_chart(customer_satisfaction_fig)
st.subheader("Satisfaction by Customer Type")
st.plotly_chart(customer_type_satisfaction_fig)
st.subheader("Satisfaction by Travel Type")
st.plotly_chart(travel_type_satisfaction_fig)

st.header("2. First-time vs Returning Customers")
st.plotly_chart(customer_type_fig)
st.plotly_chart(customer_type_bar_fig)

st.header("3. Average Age of First-time Passengers")
st.write(f"Average age of MALE first-time passengers: {first_time_male_age:.2f}")
st.write(f"Average age of FEMALE first-time passengers: {first_time_female_age:.2f}")

st.header("4. Passengers with Departure Delay but No Arrival Delay")
st.write(f"Number of passengers with Departure Delay but no Arrival Delay: {departure_no_arrival_delay_count}")

st.header("5. Passengers in Business vs Economy Class")
st.plotly_chart(class_counts_fig)
