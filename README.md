# even_financial_assignment

The first step is to create install sqlite3 and then to create the database called even_finaincial.db where all the tables will be created. There are 4 tables to create: offers, leads, clicks and results_clicked. offers, leads, click are the first 3 tables where the data will be stored from: 
ds_leads.parquet.gzip
ds_clicks.parquet.gzip
ds_offers.parquet.gzip

The next file main.py is a Python script to transfer the data from the gzip files to the tables in the database. The 4th table, results_clicked, will be used to store model batch predicted results from using the Flask app where two model artefacts are deployed. The SQL commands to create the tables are shown below.


create table offers(
	lead_uuid	   varchar(200)
,offer_id			int
,apr			decimal(10, 5)
,lender_id			int
);



create table leads(
	lead_uuid  varchar(200),
requested	decimal(5, 2),
loan_purpose	varchar(200),
credit	varchar(200),
annual_income	decimal(5,2)
);


create table clicks(
offer_id	int,
clicked_at	datetime);



create table results_clicked(
   ...> model_id VARCHAR(200),
   ...> process_time DATETIME,
   ...> request_amt DECIMAL(5,2),
   ...> annual_income DECIMAL(5,2),
   ...> apr DECIMAL(5,2),
   ...> credit_type VARCHAR(200),
   ...> loan_type VARCHAR(200),
   ...> clicked VARCHAR(200))
   ...> ;


The build_model.ipynb is used for data analysis, features engineering, building models and validating/testing the models. From here, the models are then stored as pickles files to be used for deployment. First step of this notebook is extracting the data from the tables and performing merge/join to combine the tables. Then, the next step was doing features engineering to translate the table and the output suitbale for model building. When building the model, I performed GridSearchCV to find the best set of hyperparameters to use for LogisticRegression models. I used two sets of hyperparameters for to have 2 models and then stored those two models as pickle files.


The app.py is used to deploy the model artefacts in the Flask application.It is a web app that produces model predictions upon receiving a POST request. index.html provides the UI template where you pass the values in the form. The model endpoint is also accepted and the batch predicted results are then stored to the results_clicked table in the database. 
