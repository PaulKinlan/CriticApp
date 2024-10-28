# Document Critique System

A web application for document critique using configurable AI personas powered by Flask and Google Gemini. The system provides intelligent feedback on documents through customizable AI critics with different expertise and perspectives.

## Features

- **AI-Powered Document Analysis**: Utilizes Google Gemini AI to generate insightful critiques
- **Customizable Critics**: Create and manage AI critics with unique personas and expertise
- **Critique Templates**: Pre-built templates for common use cases (Academic, Technical, Content, etc.)
- **Multiple Analysis Modes**: Choose between quick review or detailed analysis
- **Export Options**: Export critiques in multiple formats (PDF, HTML, JSON)
- **User Authentication**: Secure multi-user system with personal document spaces
- **Markdown Support**: Rich text formatting for both documents and critique feedback

## Prerequisites

- Python 3.11 or higher
- PostgreSQL database
- Google Gemini API key

## Setup and Installation

1. Clone the repository from Replit
2. Install required dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

3. Set up environment variables:
   - `GOOGLE_API_KEY`: Your Google Gemini API key
   - `FLASK_SECRET_KEY`: Secret key for Flask sessions
   - Database configuration (if not using Replit's provided database):
     - `DATABASE_URL` or individual components:
       - `PGHOST`
       - `PGPORT`
       - `PGDATABASE`
       - `PGUSER`
       - `PGPASSWORD`

4. Initialize the database:
   ```bash
   python
   from app import app, db
   with app.app_context():
       db.create_all()
   ```

## Usage

1. **User Registration and Login**
   - Register a new account with email and password
   - Login to access the system features

2. **Managing Critics**
   - Create custom critics with unique personas
   - Use pre-built templates for common critique scenarios
   - Manage and delete critics as needed

3. **Document Submission**
   - Submit documents in Markdown format
   - Choose between quick review or detailed analysis
   - View generated critiques from all active critics

4. **Viewing Results**
   - Access critique results with formatted feedback
   - Export critiques in various formats
   - Review previous submissions in the history section

## Features in Detail

### Critic Templates
- Academic Reviewer: Focuses on research methodology and academic rigor
- Technical Editor: Reviews technical accuracy and clarity
- Content Strategist: Analyzes content effectiveness
- Writing Style Expert: Evaluates tone and narrative flow
- Grammar Expert: Reviews technical correctness and structure

### Analysis Modes
1. **Quick Review**
   - Brief, high-level critique
   - Focus on key points
   - Ideal for quick feedback

2. **Detailed Analysis**
   - Comprehensive feedback
   - Structured analysis with multiple sections
   - In-depth recommendations

### Export Formats
- **PDF**: Professional formatted document
- **HTML**: Web-friendly format with styling
- **JSON**: Structured data for programmatic use

## Deployment

The application is deployed on Replit and can be accessed at:
[https://your-replit-url.replit.app](https://your-replit-url.replit.app)

To deploy your own instance:
1. Fork the project on Replit
2. Configure the required environment variables
3. Run the application using the provided run configuration

## Security Considerations

- Passwords are securely hashed using Werkzeug's security features
- User data is isolated - users can only access their own documents and critics
- API keys and sensitive data are stored as environment variables
- Session management handled by Flask-Login

## License

This project is open source and available under the MIT License.
