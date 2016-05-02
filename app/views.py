# -*- coding: utf-8 -*-
"""
    Routes for the website
"""
import os.path
from pygments.formatters import HtmlFormatter
from flask import render_template, Markup, abort, safe_join, request, flash
from flask_mail import Message, Mail
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from contact import ContactForm
from app import app
 
mail = Mail()

app.secret_key = 'development key'
 
app.config["MAIL_SERVER"] = "smtp.zoho.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'admin@archwomen.org'
app.config["MAIL_PASSWORD"] = 'your-password'
 
mail.init_app(app)

# For restructured text
#from docutils.core import publish_parts

#@app.template_filter('rst')
#def rst_filter(text):
#    return Markup(publish_parts(source=text, writer_name='html')['body'])

@app.template_filter('markdown')
def markdown_filter(text):
    """ Convert markdown to html """
    return Markup(markdown(text, extensions=[CodeHiliteExtension(linenums=True, css_class='highlight'), ExtraExtension()]))

@app.route('/')
def index():
    return render_template('index.html', title='Home')

#@app.route('/contact', methods=['POST'])
#def contact():
#    msg = Message(form.subject.data, sender='contact@archwomen.org', recipients=['admin@archwomen.org'])
#    msg.body = """
#    From: %s <%s>
#    %s
#    """ % (form.name.data, form.email.data, form.message.data)
#    mail.send(msg)
#    return 'Form posted.'

@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact.html', form=form)
        else:
            msg = Message(form.subject.data, sender='contact@archwomen.org', recipients=['admin@archwomen.org'])
            msg.body = """
            From: %s &lt;%s&gt;
            %s
            """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)
            return render_template('contact.html', success=True)
    elif request.method == 'GET':
        return render_template('contact.html', form=form)

@app.route('/pygments.css')
def pygments_css():
    formatter = HtmlFormatter(style='monokai', linenos='table', nobackground=True)
    defs = formatter.get_style_defs('.highlight')
    return defs, 200, {'Content-Type': 'text/css'}

#@app.route('/<path:webpage>/')
#def page(webpage):
#    page = 'app/content/pages/%s%s'%(webpage, '.md')
#    if os.path.isfile(page):
#        with open(page, 'r') as f:
#            content = f.read()
#            return render_template('page.html', page_html=content, title=webpage)
#    else:
#        return render_template('page.html', page_html=webpage, title="test")
#        #abort(404)

@app.route('/feed')
@app.route('/feed.atom')
def feed():
    xml = render_template('atom.xml', **locals())
    return app.response_class(xml, mimetype='application/atom+xml')

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404
