from base64 import b64decode
import os

class Base64ToPDF:
    def __init__(self, save_path):
        """
        Initializes the class with the path where the PDF file will be saved.
        """
        self.save_path = save_path
 
    def clean_base64_string(self, base64_string):
        """
        Removes invalid characters and the Data URL prefix from a base64 string.
        """
        if base64_string.startswith('data:application/pdf;base64,'):
            base64_string = base64_string.replace('data:application/pdf;base64,', '')
        return ''.join(filter(lambda x: x in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=', base64_string))
 
    def convert_from_base64(self, base64_data):
        """
        Converts a cleaned base64 string into a PDF file.
        """
        cleaned_data = self.clean_base64_string(base64_data)
        file_bytes = b64decode(cleaned_data, validate=True)
        if file_bytes[0:4] != b"%PDF":
            raise ValueError("Missing the PDF file signature")
        with open(self.save_path, "wb") as f:
            f.write(file_bytes)
       