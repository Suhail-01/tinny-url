from flask import Flask, request, redirect, render_template_string
import random
import string

app = Flask(__name__)

class URLShortener:
    NUM_CHARS_SHORT_LINK = 7
    ALPHABET = string.ascii_letters + string.digits

    def __init__(self):
        self.used_links = set()
        self.url_map = {}

    def generate_random_short_url(self):
        while True:
            short_link = ''.join(random.choices(self.ALPHABET, k=self.NUM_CHARS_SHORT_LINK))
            if short_link not in self.used_links:
                self.used_links.add(short_link)
                return short_link

    def create_custom_short_url(self, custom_url):
        if custom_url not in self.used_links:
            self.used_links.add(custom_url)
            return custom_url
        else:
            return None  # Indicates custom URL already in use

    def shorten_url(self, original_url, custom_url=""):
        if custom_url:
            short_url = self.create_custom_short_url(custom_url)
            if not short_url:
                return "Custom URL already in use!"
        else:
            short_url = self.generate_random_short_url()

        self.url_map[short_url] = original_url
        return short_url

    def get_original_url(self, short_url):
        return self.url_map.get(short_url, None)

url_shortener = URLShortener()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form['original_url']
        custom_url = request.form['custom_url']
        short_url = url_shortener.shorten_url(original_url, custom_url)
        if short_url == "Custom URL already in use!":
            return render_template_string(TEMPLATE, error=short_url)
        short_link = request.host_url + short_url
        return render_template_string(TEMPLATE, short_url=short_link)

    return render_template_string(TEMPLATE)

@app.route('/<short_url>')
def redirect_short_url(short_url):
    original_url = url_shortener.get_original_url(short_url)
    if original_url:
        return redirect(original_url)
    return "Short URL not found!", 404

TEMPLATE = '''
<!doctype html>
<title>URL Shortener</title>
<h1>URL Shortener</h1>
<form method=post>
    Original URL: <input type=text name=original_url required><br>
    Custom Short URL (optional): <input type=text name=custom_url><br>
    <input type=submit value=Shorten>
</form>
{% if short_url %}
    <p>Short URL: <a href="{{ short_url }}" target="_blank">{{ short_url }}</a></p>
{% elif error %}
    <p style="color: red;">{{ error }}</p>
{% endif %}
'''

if __name__ == "__main__":
    app.run(debug=True)
