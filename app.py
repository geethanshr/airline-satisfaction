import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Load the dataset
df = pd.read_csv("Airline_satisfaction.csv")

# Dataset preview
st.header("Dataset Preview")
st.write("Here's a preview of the dataset used for analysis:")
st.dataframe(df.head(20))

# Question 1: Percentage of satisfied passengers
st.header("1. Percentage of Satisfied Passengers")
satisfaction_counts = df['Satisfaction'].value_counts(normalize=True) * 100

fig_satisfaction = px.bar(satisfaction_counts, x=satisfaction_counts.index, y=satisfaction_counts.values, labels={'x': 'Satisfaction', 'y': 'Percentage'}, title="Percentage of Satisfied Passengers")
fig_satisfaction.update_layout(xaxis_tickangle=0)  # Ensuring horizontal x-axis labels
st.plotly_chart(fig_satisfaction)


col1, col2, col3 = st.columns(3)
col1.metric("Satisfied Passengers:", satisfaction_counts['Satisfied'])
if 'Satisfied' in satisfaction_counts.index:
    st.write("Satisfied Passengers:", satisfaction_counts['Satisfied'], "%")
if 'Neutral or unsatisfied' in satisfaction_counts.index:
    st.write("Neutral or Unsatisfied Passengers:", satisfaction_counts['Neutral or unsatisfied'], "%")

st.subheader("Satisfaction by Customer Type")
customer_satisfaction = df.groupby('Customer Type')['Satisfaction'].value_counts(normalize=True).unstack().fillna(0) * 100
fig_customer_satisfaction = px.bar(customer_satisfaction, x=customer_satisfaction.index, y=customer_satisfaction.columns, barmode='group', labels={'x': 'Customer Type', 'value': 'Percentage'}, title="Satisfaction by Customer Type")
fig_customer_satisfaction.update_layout(xaxis_tickangle=0)  # Ensuring horizontal x-axis labels
st.plotly_chart(fig_customer_satisfaction)

st.subheader("Satisfaction by Travel Type")
travel_satisfaction = df.groupby('Type of Travel')['Satisfaction'].value_counts(normalize=True).unstack().fillna(0) * 100
fig_travel_satisfaction = px.bar(travel_satisfaction, x=travel_satisfaction.index, y=travel_satisfaction.columns, barmode='group', labels={'x': 'Travel Type', 'value': 'Percentage'}, title="Satisfaction by Travel Type")
fig_travel_satisfaction.update_layout(xaxis_tickangle=0)  # Ensuring horizontal x-axis labels
st.plotly_chart(fig_travel_satisfaction)

# Question 2: First-time vs Returning Customers
st.header("2. First-time vs Returning Customers")
customer_type_counts = df['Customer Type'].value_counts()
customer_type_percentage = df['Customer Type'].value_counts(normalize=True) * 100

fig_pie = px.pie(values=customer_type_percentage, names=customer_type_percentage.index, title="Customer Type Percentage")
st.plotly_chart(fig_pie)

fig_bar = px.bar(x=customer_type_counts.index, y=customer_type_counts.values, labels={'x': 'Customer Type', 'y': 'Count'}, title="Customer Type Count")
fig_bar.update_layout(xaxis_tickangle=0)  # Ensuring horizontal x-axis labels
st.plotly_chart(fig_bar)

# Question 3: Average age of first-time male and female passengers
st.header("3. Average Age of First-time Male and Female Passengers")
first_time_male_age = df[(df['Customer Type'] == 'First-time') & (df['Gender'] == 'Male')]['Age'].mean()
first_time_female_age = df[(df['Customer Type'] == 'First-time') & (df['Gender'] == 'Female')]['Age'].mean()
st.write("Average Age of First-time Male Passengers:", first_time_male_age)
st.write("Average Age of First-time Female Passengers:", first_time_female_age)

# Question 4: Departure Delay but no Arrival Delay
st.header("4. Passengers with Departure Delay but No Arrival Delay")
departure_but_no_arrival_delay = df[(df['Departure Delay'] > 0) & (df['Arrival Delay'] == 0)].shape[0]
st.write("Number of Passengers with Departure Delay but No Arrival Delay:", departure_but_no_arrival_delay)

# Question 5: Business vs Economy Class Passengers
st.header("5. Business vs Economy Class Passengers")
class_counts = df['Class'].value_counts()
fig_class = px.bar(x=class_counts.index, y=class_counts.values, labels={'x': 'Class', 'y': 'Count'}, title="Class Distribution")
fig_class.update_layout(xaxis_tickangle=0)  # Ensuring horizontal x-axis labels
st.plotly_chart(fig_class)


