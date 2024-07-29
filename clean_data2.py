import re

def clean_text(input_file, output_file):
    # Open the input file and read the content
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Remove URLs
    content = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', content)
    
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
    clean_text('data.txt', 'data2.txt')
