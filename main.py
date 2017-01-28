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
import cgi

#html header setting error color and title
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
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

mainpage = """
<form method="post">
    <table>
        <tbody>
            <tr>
                <td><label for="username">Username</label></td>
                <td><input name="username" type="text" value="%(username)s" required>
                <span class="error">%(error_username)s</span>
            </tr>
            <tr>
                <td><label for="password">Password</label></td>
                <td><input name="password" type="password" value="" required>
                <span class="error">%(error_password)s</span>
            </tr>
            <tr>
                <td><label for="verify">Verify Password</label></td>
                <td><input name="verify" type="password" value="" required>
                <span class="error">%(error_verify)s</span>
            </tr>
            <tr>
                <td><label for="email">Email (optional)</label></td>
                <td><input name="email" type=text value=%(email)s>
                <span class="error">%(error_email)s</span>
            </tr>
        </tbody>
    </table>
    <input type="submit">
</form>
"""

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        title = "Welcome"
        display_title = ""
        username = self.request.get("username")
        welcome = "<h1>Welcome, " + cgi.escape(username, quote=True) + "!</h1>"

        content = page_header%{"title":title, "display_title":display_title} + welcome + page_footer

        self.response.write(content)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        title = "Signup"
        display_title = "Signup"
        username = ""
        email = ""
        error_username = ""
        error_password = ""
        error_verify = ""
        error_email = ""

        content = page_header%{"title":title, "display_title":display_title} + mainpage%{"username":username, "email":email, "error_username":error_username, "error_password":error_password, "error_verify":error_verify, "error_email":error_email} + page_footer

        self.response.write(content)


    def post(self):
        title = "Signup"
        display_title = "Signup"
        username = self.request.get("username")
        email = self.request.get("email")
        password = self.request.get("password")
        verify = self.request.get("verify")
        error_username = ""
        error_password = ""
        error_verify = ""
        error_email = ""
        error = True

        content = page_header%{"title":title, "display_title":display_title} + mainpage%{"username":cgi.escape(username, quote = True), "email":cgi.escape(email, quote = True), "error_username":error_username, "error_password":error_password, "error_verify":error_verify, "error_email":error_email} + page_footer

        if error == False:
            self.redirect("/welcome?username=" + username)
        else:
            self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
