from flask import Flask, render_template, request
import datetime
import sqlite3
import pickle
import os
import json
app = Flask(__name__)
pwd = os.getcwd()
database_name = "even_financial.db"

with open(pwd+'/credit_dictionary.json') as json_file:
    credit_dict=json.load(json_file)

with open(pwd+'/loan_purpose_dictionary.json') as json_file:
    loan_purpose_dict=json.load(json_file)


def log_sqlite_table(metadata):
    try:
        sqliteConnection = sqlite3.connect(database_name)
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")
        sqlite_insert_query = """INSERT INTO results_clicked(model_id, process_time, request_amt, annual_income, apr, 
        credit_type, loan_type, clicked) VALUES(?, ?, ?, ?, ?, ?, ?, ?) """
        insert_values=(str(metadata['model_id']), str(metadata['process_time']), str(metadata['request_amt']), str(metadata['annual_income']), str(metadata['apr']), str(metadata['credit_type']), str(metadata['loan_type']), str(metadata['clicked']))
        cursor.execute(sqlite_insert_query,insert_values)
        sqliteConnection.commit()
        print("Record inserted successfully into SqliteDb_developers table")
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        requested_amt = float(request.form['Requested_Amount'])
        annual_income = float(request.form['Annual_Income'])
        apr = float(request.form['apr'])
        credit = request.form['Credit']
        credit_val = list(credit_dict.keys())[list(credit_dict.values()).index(credit)]
        loan_purpose = request.form['Loan_Purpose']
        loan_val = list(loan_purpose_dict.keys())[list(loan_purpose_dict.values()).index(loan_purpose)]
        lr_model = request.form['model_type']
        if lr_model == 'logistic_regr_1':
            model = pickle.load(open('first_logistic_regression_modl.pkl', 'rb'))
            model_id = "12345_logistic_regr_1"
        else:
            model = pickle.load(open('second_logistic_regression_modl.pkl', 'rb'))
            model_id = "67890_logistic_regr_2"
        X_input = [requested_amt,int(loan_val),int(credit_val),annual_income,apr]
        prediction = model.predict([X_input])
        output=round(prediction[0], 2)
        output_dict = {'0': 'Sorry, an offer is not clicked', '1': 'Congratulations, the offer is clicked'}
        batch_dict = {'0': 'Not clicked', '1': 'Clicked'}
        message = output_dict[str(output.item())]
        process_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        metadata_dict = {'model_id':model_id,'request_amt': requested_amt, 'annual_income':annual_income,
                       'apr': apr, 'credit_type':credit, 'loan_type':loan_purpose,'clicked':batch_dict[str(output.item())],
                       'process_time': process_time}
        log_sqlite_table(metadata_dict)
        return render_template('index.html',prediction_text=message)
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
