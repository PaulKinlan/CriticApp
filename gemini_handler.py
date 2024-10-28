import google.generativeai as genai
import os

class GeminiHandler:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_critique(self, document_text, persona):
        try:
            prompt = f"""
            You are acting as a critic with the following persona:
            {persona}
            
            Please provide a detailed critique of the following document:
            {document_text}
            
            Focus on providing constructive feedback that aligns with your persona's perspective.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating critique: {str(e)}"
