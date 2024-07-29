import re
from geotext import GeoText

def clean_text(input_file, output_file):
    # Define lists of month names and day names
    months = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December',
        'Jan', 'Feb', 'Mar', 'Apr', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    
    days = [
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
        'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'
    ]
    
    # Open the input file and read the content
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Remove URLs
    content = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', content)

    # Remove month names
    for month in months:
        content = re.sub(r'\b' + month + r'\b', '', content, flags=re.IGNORECASE)
    
    # Remove day names
    for day in days:
        content = re.sub(r'\b' + day + r'\b', '', content, flags=re.IGNORECASE)
    
    # Identify and remove location names using GeoText
    places = GeoText(content)
    for city in places.cities:
        content = re.sub(r'\b' + city + r'\b', '', content, flags=re.IGNORECASE)
    for country in places.countries:
        content = re.sub(r'\b' + country + r'\b', '', content, flags=re.IGNORECASE)
    
    # Replace non-alphabetic characters with a space
    content = re.sub(r'[^a-zA-Z]', ' ', content)
    
    # Remove single character alphabets
    content = re.sub(r'\b[a-zA-Z]\b', '', content)
    
    # Replace multiple spaces with a single space
    content = re.sub(r' +', ' ', content)
    
    # Open the output file and write the cleaned content
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(content.strip())

if __name__ == "__main__":
    clean_text('data.txt', 'data1.txt')
