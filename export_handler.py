import json
from fpdf import FPDF
import markdown
import html

class ExportHandler:
    @staticmethod
    def to_pdf(document, critiques):
        pdf = FPDF()
        pdf.add_page()
        
        # Set up fonts
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Document Critique Report", ln=True)
        
        # Document content
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Original Document:", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 10, document.content)
        
        # Critiques
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Critiques:", ln=True)
        
        for critique in critiques:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, f"Critic: {critique.critic.name}", ln=True)
            pdf.set_font("Arial", "", 11)
            pdf.multi_cell(0, 10, critique.feedback)
            pdf.ln(5)
        
        return pdf.output(dest='S').encode('latin1')
    
    @staticmethod
    def to_html(document, critiques):
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Document Critique Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .section {{ margin-bottom: 30px; }}
                .critic-name {{ font-weight: bold; color: #444; }}
            </style>
        </head>
        <body>
            <h1>Document Critique Report</h1>
            
            <div class="section">
                <h2>Original Document:</h2>
                {markdown.markdown(document.content)}
            </div>
            
            <div class="section">
                <h2>Critiques:</h2>
                {''.join([f'''
                <div class="critique">
                    <p class="critic-name">Critic: {html.escape(critique.critic.name)}</p>
                    <p>{html.escape(critique.feedback).replace(chr(10), '<br>')}</p>
                </div>
                ''' for critique in critiques])}
            </div>
        </body>
        </html>
        """
        return html_content
    
    @staticmethod
    def to_json(document, critiques):
        data = {
            'document': {
                'id': document.id,
                'content': document.content,
                'created_at': document.created_at.isoformat(),
                'critique_mode': document.critique_mode
            },
            'critiques': [{
                'critic_name': critique.critic.name,
                'feedback': critique.feedback,
                'created_at': critique.created_at.isoformat()
            } for critique in critiques]
        }
        return json.dumps(data, indent=2)
