from flask import render_template

class HomeController:
    def renderHome(self):
        return render_template('index.html')