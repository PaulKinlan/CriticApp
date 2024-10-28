from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from models import Critic, Document, Critique
from gemini_handler import GeminiHandler
import markdown

gemini = GeminiHandler()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/critics', methods=['GET', 'POST'])
def critics():
    if request.method == 'POST':
        name = request.form.get('name')
        persona = request.form.get('persona')
        
        if name and persona:
            critic = Critic(name=name, persona=persona)
            db.session.add(critic)
            db.session.commit()
            flash('Critic added successfully!', 'success')
        
    critics = Critic.query.filter_by(active=True).all()
    return render_template('critics.html', critics=critics)

@app.route('/critics/delete/<int:id>')
def delete_critic(id):
    critic = Critic.query.get_or_404(id)
    critic.active = False
    db.session.commit()
    flash('Critic deleted successfully!', 'success')
    return redirect(url_for('critics'))

@app.route('/document', methods=['GET', 'POST'])
def document():
    if request.method == 'POST':
        content = request.form.get('content')
        if content:
            document = Document(content=content)
            db.session.add(document)
            db.session.commit()
            
            critics = Critic.query.filter_by(active=True).all()
            for critic in critics:
                feedback = gemini.generate_critique(content, critic.persona)
                critique = Critique(
                    document_id=document.id,
                    critic_id=critic.id,
                    feedback=feedback
                )
                db.session.add(critique)
            
            db.session.commit()
            flash('Document submitted and critiques generated!', 'success')
            return redirect(url_for('document', doc_id=document.id))
    
    doc_id = request.args.get('doc_id')
    if doc_id:
        document = Document.query.get_or_404(doc_id)
        return render_template('document.html', 
                            document=document,
                            content_html=markdown.markdown(document.content))
    
    return render_template('document.html')

@app.route('/history')
def history():
    documents = Document.query.order_by(Document.created_at.desc()).all()
    return render_template('history.html', documents=documents)
