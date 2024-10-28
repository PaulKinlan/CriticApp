import google.generativeai as genai
import os

class GeminiHandler:
    def __init__(self):
        api_key = os.environ.get('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def generate_critique(self, document_text, persona, mode='detailed'):
        try:
            if mode == 'quick':
                prompt = f"""
                You are acting as a critic with the following persona:
                {persona}
                
                Please provide a brief, high-level critique of the following document in 2-3 sentences:
                {document_text}
                
                Focus on the most important points that align with your persona's perspective.
                Keep the feedback concise but meaningful.
                """
            else:  # detailed mode
                prompt = f"""
                You are acting as a critic with the following persona:
                {persona}
                
                Please provide a comprehensive critique of the following document:
                {document_text}
                
                Structure your critique as follows:
                1. Overall Assessment (2-3 sentences)
                2. Key Strengths (2-3 points)
                3. Areas for Improvement (2-3 points)
                4. Specific Recommendations (2-3 actionable suggestions)
                
                Focus on providing constructive feedback that aligns with your persona's perspective.
                """
            
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating critique: {str(e)}"
