# -*- coding: utf-8 -*-
"""
    Routes for the website
"""
import os
import codecs
import feedparser
from pygments.formatters import HtmlFormatter
from flask import render_template, Markup, abort, safe_join, request, flash
from markdown import markdown
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.extra import ExtraExtension
from contact import ContactForm
from app import app


# For restructured text
#from docutils.core import publish_parts

#@app.template_filter('rst')
#def rst_filter(text):
#    return Markup(publish_parts(source=text, writer_name='html')['body'])

@app.template_filter('markdown')
def markdown_filter(text):
    """ Convert markdown to html """
    return Markup(markdown(text, extensions=[CodeHiliteExtension(linenums=False, css_class='highlight'), ExtraExtension()]))

@app.route('/pygments.css')
def pygments_css():
    formatter = HtmlFormatter(style='monokai', nobackground=True)
    defs = formatter.get_style_defs('.highlight')
    return defs, 200, {'Content-Type': 'text/css'}

@app.route('/')
def index():
    feed = feedparser.parse('https://archwomen.org/blog/feed.atom').entries
    return render_template('index.html', entries=feed[0:6], title='Home')

@app.route('/contact/', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST' and form.validate():
        msg = render_template("email.txt",
                        name=form.name.data,
                        email=form.email.data,
                        subject=form.subject.data,
                        message=form.message.data)
        p = os.popen("/usr/bin/sendmail -f contact@archwomen.org -t -i", "w")
        p.write(msg)
        status = ip.close()
        if status:
            flash(u"%s"%(status))
        flash("Your message has been sent. Thank you!", "success")
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                ))
    return render_template('contact.html', form=form)

@app.route('/blog/<year>/<month>/<day>/<slug>/')
def blog_page(year, month, day, slug):
    page = 'app/content/posts/%s-%s-%s-%s%s'%(year, month, day, slug, '.md')
    if os.path.isfile(page):
        with codecs.open(page, encoding='utf-8', mode='r+') as f:
            content = f.read()
            return render_template('page.html', page_html=content, title=slug)
    else:
        abort(404)

@app.route('/<path:webpage>/')
def page(webpage):
    page = 'app/content/pages/%s%s'%(webpage, '.md')
    if os.path.isfile(page):
        with codecs.open(page, encoding='utf-8', mode='r+') as f:
            content = f.read()
            return render_template('page.html', page_html=content, title=webpage)
    else:
        abort(404)

@app.route('/blog/feed')
@app.route('/blog/feed.atom')
def feed():
    xml = render_template('atom.xml', **locals())
    return app.response_class(xml, mimetype='application/atom+xml')

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404
