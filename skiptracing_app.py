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

    response = requests.get(API_URL, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()  # Return the parsed JSON response
    else:
        st.error("Error fetching data from the API. Please try again.")
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
                # Check if the API returned any records
                if 'data' in data and data['data']:
                    st.subheader("Skiptrace Results:")
                    st.json(data)  # Display the full response in JSON format for now

                    # Example of extracting and displaying relevant details from the data
                    if 'phoneNumbers' in data['data'][0]:
                        st.subheader("Phone Numbers:")
                        for phone in data['data'][0]['phoneNumbers']:
                            st.write(phone['number'])
                    else:
                        st.warning("No phone numbers found.")

                    # Display other available information if necessary
                    if 'otherDetails' in data['data'][0]:
                        st.subheader("Other Available Details:")
                        st.write(data['data'][0]['otherDetails'])

                else:
                    st.warning("No skiptracing data found for the given address.")
        else:
            st.warning("Please enter both street address and city, state, ZIP.")

if __name__ == "__main__":
    main()
