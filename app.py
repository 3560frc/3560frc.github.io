from flask import render_template
from flask_frozen import Freezer
from flask import Flask
from flask import abort
import json

with open('pages.json', 'r') as file:
    pages = json.load(file)

app = Flask(__name__)
app.config['FREEZE'] = True
freezer = Freezer(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def page(path):
    page_html = None
    for page in pages:
        if pages[page]['path'] == path:
            page_html = page + '.html'
    if not page_html:
        abort(404)
    return render_template(page_html, pages=dict(pages))


@freezer.register_generator
def page():
    for page in pages:
        yield {'path': pages[page]['path']}

if __name__ == '__main__':
    if app.config['FREEZE']:
        freezer.freeze()
    else:
        app.run()