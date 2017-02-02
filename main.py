#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import jinja2
import cgi
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
PASS_RE = re.compile(r"^.{3,20}$")

def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    return PASS_RE.match(password)

def valid_email(email):
    return EMAIL_RE.match(email)


#html header setting error color and title
def buildHeader(title = "Signup", display_title="Signup"):
    page_header = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>%(title)s</title>
        <style type="text/css">
            .error {
                color: red;
            }
        </style>
    </head>
    <body>
        <h1>
            <a href="/">%(display_title)s</a>
        </h1>
    """%{"title":title, "display_title":display_title}
    return page_header

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class WelcomeHandler(Handler):
    def get(self):

        username = self.request.get("username")
        #welcome = "<h1>Welcome, " + cgi.escape(username, quote=True) + "!</h1>"

        #content = buildHeader("Welcome", "") + welcome + page_footer

        self.render("welcome_page.html", username = cgi.escape(username, quote = True), title = "Welcome")


class MainHandler(Handler):
    def get(self):
        title = "Signup"
        display_title = "Signup"

        self.render("signup_page.html", title = "Signup", display_title = "Signup")

        #content = buildHeader() + buildMainPage() + page_footer

        #self.write(content)


    def post(self):
        title = "Signup"
        display_title = "Signup"
        username = self.request.get("username")
        email = self.request.get("email")
        password = self.request.get("password")
        verify = self.request.get("verify")
        error = False

        if username and valid_username(username):
            error_username = ""
        else:
            error = True
            error_username = "That's not a valid username"

        if password and valid_password(password):
            error_password = ""
        else:
            error = True
            error_password = "That's not a valid password"

        if verify and password == verify:
            error_verify = ""
        else:
            error = True
            error_verify = "Password and Verify Password must match"

        if (not email) or valid_email(email):
            error_email = ""
        else:
            error = True
            error_email = "That's not a valid email"

        #content = buildHeader() + buildMainPage(cgi.escape(username, quote=True), cgi.escape(email, quote=True), error_username, error_password, error_verify, error_email) + page_footer

        if error == False:
            self.redirect("/welcome?username=" + username)
        else:
            self.render("signup_page.html",
                        title = "Signup",
                        display_title = "Signup",
                        username = cgi.escape(username, quote=True),
                        email = cgi.escape(email, quote=True),
                        error_username = error_username,
                        error_password = error_password,
                        error_verify = error_verify,
                        error_email = error_email)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
