from flask import Flask, redirect, render_template, url_for

from karma import app


if __name__ == "__main__":
    app.run(debug=True)