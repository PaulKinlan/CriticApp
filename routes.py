from flask import render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db
from models import User, Critic, Document, Critique, CriticTemplate
from gemini_handler import GeminiHandler
from export_handler import ExportHandler
import markdown
from io import BytesIO

gemini = GeminiHandler()

@app.template_filter('markdown')
def markdown_filter(text):
    return markdown.markdown(text)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return render_template('register.html')
            
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return render_template('register.html')
        
        user = User()
        user.username = username
        user.email = email
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

def initialize_templates():
    if CriticTemplate.query.count() == 0:
        default_templates = [
            {
                'name': 'Academic Reviewer',
                'category': 'academic',
                'description': 'Provides scholarly analysis with focus on research methodology and academic rigor',
                'persona': '''I am an experienced academic reviewer with expertise in research methodology and scholarly writing. 
                I focus on the clarity of arguments, proper citation of sources, and adherence to academic standards. 
                My feedback emphasizes theoretical framework, methodology, and contribution to the field.'''
            },
            {
                'name': 'Technical Editor',
                'category': 'technical',
                'description': 'Reviews technical documentation with emphasis on accuracy and clarity',
                'persona': '''As a technical editor, I specialize in reviewing technical documentation, code explanations, and technical specifications. 
                I focus on technical accuracy, clarity of explanations, and proper use of technical terminology. 
                I ensure that technical concepts are explained clearly for the target audience.'''
            },
            {
                'name': 'Content Strategist',
                'category': 'content',
                'description': 'Analyzes content effectiveness and alignment with communication goals',
                'persona': '''I am a content strategist with expertise in digital communication and audience engagement. 
                I evaluate content for its strategic value, audience alignment, and effectiveness in achieving communication goals. 
                My feedback focuses on content structure, messaging, and audience impact.'''
            },
            {
                'name': 'Writing Style Expert',
                'category': 'style',
                'description': 'Focuses on writing style, tone, and narrative flow',
                'persona': '''As a writing style expert, I analyze the rhetorical elements of writing including tone, voice, and narrative flow. 
                I focus on stylistic choices, sentence variety, and overall readability. 
                My feedback aims to enhance the writing's impact while maintaining the author's unique voice.'''
            },
            {
                'name': 'Grammar and Structure Expert',
                'category': 'grammar',
                'description': 'Reviews grammar, syntax, and document structure',
                'persona': '''I specialize in reviewing grammar, syntax, and document structure. 
                I focus on technical correctness, clarity of expression, and logical organization. 
                My feedback ensures that the writing is polished, professional, and well-structured.'''
            }
        ]
        
        for template_data in default_templates:
            template = CriticTemplate()
            template.name = template_data['name']
            template.category = template_data['category']
            template.description = template_data['description']
            template.persona = template_data['persona']
            db.session.add(template)
        
        db.session.commit()

with app.app_context():
    initialize_templates()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/critics', methods=['GET', 'POST'])
@login_required
def critics():
    if request.method == 'POST':
        name = request.form.get('name')
        persona = request.form.get('persona')
        template_id = request.form.get('template_id')
        
        if template_id:
            template = CriticTemplate.query.get(template_id)
            if template:
                name = name or template.name
                persona = template.persona
        
        if name and persona:
            critic = Critic()
            critic.name = name
            critic.persona = persona
            critic.user_id = current_user.id
            db.session.add(critic)
            db.session.commit()
            flash('Critic added successfully!', 'success')
    
    critics = Critic.query.filter_by(active=True, user_id=current_user.id).all()
    templates = CriticTemplate.query.all()
    return render_template('critics.html', critics=critics, templates=templates)

@app.route('/critics/delete/<int:id>')
@login_required
def delete_critic(id):
    critic = Critic.query.get_or_404(id)
    if critic.user_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('critics'))
    
    critic.active = False
    db.session.commit()
    flash('Critic deleted successfully!', 'success')
    return redirect(url_for('critics'))

@app.route('/templates', methods=['GET', 'POST'])
@login_required
def templates():
    if request.method == 'POST':
        name = request.form.get('name')
        persona = request.form.get('persona')
        category = request.form.get('category')
        description = request.form.get('description')
        
        if all([name, persona, category, description]):
            template = CriticTemplate()
            template.name = name
            template.persona = persona
            template.category = category
            template.description = description
            db.session.add(template)
            db.session.commit()
            flash('Template added successfully!', 'success')
    
    templates = CriticTemplate.query.all()
    return render_template('templates.html', templates=templates)

@app.route('/templates/delete/<int:id>')
@login_required
def delete_template(id):
    template = CriticTemplate.query.get_or_404(id)
    db.session.delete(template)
    db.session.commit()
    flash('Template deleted successfully!', 'success')
    return redirect(url_for('templates'))

@app.route('/templates/use/<int:id>')
@login_required
def use_template(id):
    template = CriticTemplate.query.get_or_404(id)
    critic = Critic()
    critic.name = template.name
    critic.persona = template.persona
    critic.user_id = current_user.id
    db.session.add(critic)
    db.session.commit()
    flash(f'Critic created from template: {template.name}', 'success')
    return redirect(url_for('critics'))

@app.route('/document', methods=['GET', 'POST'])
@login_required
def document():
    if request.method == 'POST':
        content = request.form.get('content')
        mode = request.form.get('mode', 'detailed')
        
        if content:
            document = Document()
            document.content = content
            document.critique_mode = mode
            document.user_id = current_user.id
            db.session.add(document)
            db.session.commit()
            
            critics = Critic.query.filter_by(active=True, user_id=current_user.id).all()
            for critic in critics:
                feedback = gemini.generate_critique(content, critic.persona, mode)
                critique = Critique()
                critique.document_id = document.id
                critique.critic_id = critic.id
                critique.feedback = feedback
                db.session.add(critique)
            
            db.session.commit()
            flash('Document submitted and critiques generated!', 'success')
            return redirect(url_for('document', doc_id=document.id))
    
    doc_id = request.args.get('doc_id')
    if doc_id:
        document = Document.query.get_or_404(doc_id)
        if document.user_id != current_user.id:
            flash('Access denied', 'danger')
            return redirect(url_for('document'))
        
        return render_template('document.html', document=document)
    
    return render_template('document.html')

@app.route('/history')
@login_required
def history():
    documents = Document.query.filter_by(user_id=current_user.id).order_by(Document.created_at.desc()).all()
    return render_template('history.html', documents=documents)

@app.route('/export/<int:doc_id>/<format>')
@login_required
def export_document(doc_id, format):
    document = Document.query.get_or_404(doc_id)
    if document.user_id != current_user.id:
        flash('Access denied', 'danger')
        return redirect(url_for('history'))
    
    critiques = document.critiques
    
    if format == 'pdf':
        pdf_content = ExportHandler.to_pdf(document, critiques)
        buffer = BytesIO(pdf_content)
        return send_file(
            buffer,
            download_name=f'critique_report_{doc_id}.pdf',
            mimetype='application/pdf'
        )
    
    elif format == 'html':
        html_content = ExportHandler.to_html(document, critiques)
        buffer = BytesIO(html_content.encode())
        return send_file(
            buffer,
            download_name=f'critique_report_{doc_id}.html',
            mimetype='text/html'
        )
    
    elif format == 'json':
        json_content = ExportHandler.to_json(document, critiques)
        buffer = BytesIO(json_content.encode())
        return send_file(
            buffer,
            download_name=f'critique_report_{doc_id}.json',
            mimetype='application/json'
        )
    
    return "Invalid format", 400
