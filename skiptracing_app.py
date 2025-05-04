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

        # Check if the response contains 'PropertyDetails'
        if 'PropertyDetails' in raw_data:
            property_details = raw_data['PropertyDetails']
            st.subheader("Property Details")
            for key, value in property_details.items():
                st.write(f"**{key}**: {value}")

        # Check if the response contains 'PeopleDetails' and display phone numbers
        if 'PeopleDetails' in raw_data:
            st.subheader("People Associated with this Property")
            for person in raw_data['PeopleDetails']:
                st.write(f"**Name**: {person['Name']}")
                st.write(f"**Age**: {person['Age']}")
                st.write(f"**Lives in**: {person['Lives in']}")
                
                if person['Phone']:  # If phone numbers are available
                    st.write("**Phone Numbers**:")
                    for phone in person['Phone']:
                        st.write(phone)
                else:
                    st.write("No phone numbers found.")
                
                st.write(f"[More Details](https://www.fastpeoplesearch.com/{person['Link']}")  # Link to person's details
        else:
            st.warning("No people details found for this address.")
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
                pass  # Data is already displayed by the `get_skiptracing_info()` function
        else:
            st.warning("Please enter both street address and city, state, ZIP.")

if __name__ == "__main__":
    main()
