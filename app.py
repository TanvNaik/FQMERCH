from flask import Flask, redirect, render_template, url_for, session
import razorpay, sys
from karma import app
from karma.pages.forms import AddressForm


if __name__ == "__main__":
    app.run(debug=True)
