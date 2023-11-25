from application import app
from flask import render_template, url_for, redirect,flash, get_flashed_messages, request
from application.models import Reviews, Sales
from application import db
from sqlalchemy import func
from datetime import datetime, timedelta
import json
import pandas as pd

@app.route('/reviews')
def review():
    data = Reviews.query.all()
   
    for review in data:
        review.product_quality = '&#9733; ' * review.product_quality
        review.shipping_time = '&#9733; ' * review.shipping_time
        review.shipping_quality = '&#9733; ' * review.shipping_quality
        review.contact_quality = '&#9733; ' * review.contact_quality

    
    return render_template('review.html', data=data)

@app.route('/sales')
def sales():
    data = Sales.query.all()
    return render_template('sales.html', data=data)

@app.route('/load_review')
def load_review():
    try:
        df = pd.read_csv("application/data/data_reviews1.csv")
        df.to_sql('reviews', con=db.engine, if_exists='replace', index=False)
        flash('Dane wczytane do bazy danych!', 'success')
    except Exception as e:
        flash(f'Błąd podczas wczytywania danych: {str(e)}', 'danger')

    return redirect(url_for('review'))

@app.route('/load_sales')
def load_sales():
    try:
        df = pd.read_csv("application/data/sales_data.csv")
        df.to_sql('sales', con=db.engine, if_exists='replace', index=False)
        flash('Dane wczytane do bazy danych!', 'success')
    except Exception as e:
        flash(f'Błąd podczas wczytywania danych: {str(e)}', 'danger')

    return redirect(url_for('sales'))


@app.route('/reviews/dashboard')
def reviews_dashboard():
    avg_product_quality = db.session.query(func.avg(Reviews.product_quality)).scalar()
    avg_shipping_quality = db.session.query(func.avg(Reviews.shipping_quality)).scalar()
    avg_shipping_time = db.session.query(func.avg(Reviews.shipping_time)).scalar()
    avg_contact_quality = db.session.query(func.avg(Reviews.contact_quality)).scalar()


    chart_data = {
        'labels': ['Product Quality', 'Shipping Quality', 'Shipping Time', 'Contact with seller'],
        'data': [avg_product_quality, avg_shipping_quality, avg_shipping_time, avg_contact_quality]
    }

    return render_template('rdashboard.html', chart_data=chart_data)

@app.route('/sales/dashboard')
def sales_dashboard():
    time_range = request.args.get('time-range', '1w') 


    reference_date = datetime(2023, 1, 1)

    try:
        if time_range == '1w':
            sales_data = Sales.query.filter(Sales.date >= reference_date - timedelta(weeks=1)).all()
        elif time_range == '1m':
            sales_data = Sales.query.filter(Sales.date >= reference_date - timedelta(weeks=4)).all()
        elif time_range == '6m':
            sales_data = Sales.query.filter(Sales.date >= reference_date - timedelta(weeks=26)).all()
        elif time_range == '1y':
            sales_data = Sales.query.filter(Sales.date >= reference_date - timedelta(weeks=52)).all()

        dates = [str(sale.date) for sale in sales_data]
        quantities = [sale.quantity for sale in sales_data]

        return render_template('sdashboard.html', dates=dates, quantities=quantities)
    except Exception as e:
        print(f"Error: {e}")
        return render_template('error.html', error_message="An error occurred while processing the request.")

if __name__ == '__main__':
    app.run(debug=True)