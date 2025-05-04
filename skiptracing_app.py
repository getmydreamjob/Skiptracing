import streamlit as st
import requests
import json

# Set up the RapidAPI credentials
RAPIDAPI_KEY = '68efe57bd5mshbb02503559ba90ep1e59bbjsn18b931a07505'
API_URL = "https://skip-tracing-working-api.p.rapidapi.com/search/byaddress"

# Define headers for the RapidAPI request
headers = {
    'x-rapidapi-key': RAPIDAPI_KEY,
    'x-rapidapi-host': "skip-tracing-working-api.p.rapidapi.com"
}

# Function to get skiptracing results
def get_skiptracing_info(street, citystatezip):
    params = {
        'street': street,
        'citystatezip': citystatezip,
        'page': '1'
    }

    # Send the request to the API
    response = requests.get(API_URL, headers=headers, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        raw_data = response.json()  # Parse the JSON data
        st.write("Raw API Response:")  # Display raw response
        st.json(raw_data)  # Show the full response as JSON for debugging

        # Check if the response contains 'data' and it's not empty
        if 'data' in raw_data and raw_data['data']:
            return raw_data  # Return the data if present
        else:
            st.warning("No data found for the given address.")  # If no data is found
            return None
    else:
        st.error(f"Error fetching data from the API. Status Code: {response.status_code}")
        return None

# Streamlit App Layout
def main():
    st.title('Skiptracing Tool')
    
    st.write("""
    This is a simple skiptracing app that uses RapidAPI to fetch phone numbers and other available details
    for a given property address. Please manually input the full address (street, city, state, ZIP).
    """)

    # Input for street address
    street = st.text_input("Enter Street Address (e.g., 123 Main)", "")
    citystatezip = st.text_input("Enter City, State, ZIP", "")

    if st.button("Get Skiptrace Info"):
        if street and citystatezip:
            st.write(f"Searching for information on: **{street}, {citystatezip}**")
            data = get_skiptracing_info(street, citystatezip)
            
            if data:
                # If data is found, display relevant information
                if 'phoneNumbers' in data['data'][0]:
                    st.subheader("Phone Numbers:")
                    for phone in data['data'][0]['phoneNumbers']:
                        st.write(phone['number'])
                else:
                    st.warning("No phone numbers found.")
        else:
            st.warning("Please enter both street address and city, state, ZIP.")

if __name__ == "__main__":
    main()
