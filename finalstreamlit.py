import streamlit as st
import requests
import random
import pandas as pd
import plotly.express as px

# Function to fetch country information from Wikipedia API
def fetch_country_info(country_name):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{country_name}"
    response = requests.get(url)
    data = response.json()
    return data

def get_country_images(country):
    # Unsplash API endpoint
    endpoint = "https://api.unsplash.com/photos/random"
    
    # Parameters for the Unsplash API request
    params = {
        "query": country,
        "orientation": "landscape",
        "count": 2
    }
    
    # Unsplash API access key
    access_key = "fQOXSOIh51DigtPMCzMWxaK1fafQYj-VGr3V2zOSHxk"
    
    # Make the Unsplash API request
    headers = {"Authorization": f"Client-ID {access_key}"}
    response = requests.get(endpoint, params=params, headers=headers)
    data = response.json()
    
    # Extract the image URLs from the response
    image_urls = []
    for photo in data:
        image_url = photo["urls"]["regular"]
        image_urls.append(image_url)
    
    # Return two random image URLs
    return random.sample(image_urls, 2)

def get_country_population(country_name):
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    response = requests.get(url)
    data = response.json()

    if 'population' in data[0]:
        return data[0]['population']
    else:
        return 'Population data not found'

def get_country_capital(country_name):
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    response = requests.get(url)
    data = response.json()
    capital = data[0]['capital']
    return ', '.join(capital)

def get_country_currency(country_name):
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    response = requests.get(url)
    data = response.json()
    currency = data[0]['currencies']
    return ', '.join(currency)

def get_country_language(country_name):
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    response = requests.get(url)
    data = response.json()
    language = data[0]['languages']
    return ', '.join(language)

def get_city_coordinates(city_name, country_name):
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {
        "city": city_name, country_name: country_name,
        "format": "json",
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    if data:
        return (float(data[0]["lat"]), float(data[0]["lon"]))
    else:
        return None

def get_top_5_countries():
    url = "https://restcountries.com/v3.1/all"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    df = df.nlargest(5, ['population'])
    return df

# Main function to run the app
def main():

    st.title("Country Info App")
    
    # Get list of countries
    countries = ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia", "Comoros", "Congo", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Côte d'Ivoire", "DR Congo", "Denmark", "Djibouti", "Dominica", "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Tajikistan", "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"]
    
    # Display dropdown to select country
    selected_country = st.selectbox("Select a country", countries, index=countries.index("United States"))
    
    # Fetch country information
    country_info = fetch_country_info(selected_country)
    
    # Display country information
    if 'extract' in country_info:
        st.markdown(country_info['extract'])
    else:
        st.error("Sorry, no information available for this country.")

    col1, col2, col3 = st.columns(3)

    # Display images of the country
    left_image_url, right_image_url = get_country_images(selected_country)
    col1.image(left_image_url, width=200)
    col3.image(right_image_url, width=200)

    # Display the capital of the country
    capital = get_country_capital(selected_country)
    col2.write(f"Capital: {capital}")

    #display population of the country
    population = get_country_population(selected_country)
    if selected_country == "United States":
        population = "331,449,281"
    col2.write(f"Population: {population}")
    
    # Display the currency of the country
    currency = get_country_currency(selected_country)
    col2.write(f"Currency: {currency}")

    #display the language of the country
    language = get_country_language(selected_country)
    col2.write(f"Language: {language}")
    
    # Display the coordinates of the capital
    coordinates = get_city_coordinates(capital, country_name=selected_country)
    #display bar chart

    df = pd.DataFrame({
        "col1": [coordinates[0]],
        "col2": [coordinates[1]],
        "col3": [800]
    })

    st.map(df, latitude='col1', longitude='col2', size='col3')

    st.write("Population by Country")
     # Get the top 5 countries with the highest population
    top_5_countries = get_top_5_countries()
    # Extract country names and populations
    countries = [country['name']['common'] for index, country in top_5_countries.iterrows()]
    populations = top_5_countries['population'].values
    # Display donut chart
    chart = px.pie(top_5_countries, values='population', names=countries, title='Top 5 Countries by Population')
    st.plotly_chart(chart)

# Run the app
if __name__ == "__main__":
    main()
