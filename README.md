
# Companies Incorporated In India

The Objective is to Perform a web scraping on the [companies](https://www.zaubacorp.com/company-list) website and to perform data cleaning, data ingestion and data retrieval.In this project I have used [scrapy](https://docs.scrapy.org/en/latest/) framework for data scraping and data ingestion and [fastAPI](https://fastapi.tiangolo.com/lo/) for accessing data.

`prerequesite tools: 
  python3, 
  mongodb(specifically mongosh,mongodb server)
`

If mongodb is not installed in your pc then create a mongo db cloud account and access [atlas](https://studio3t.com/knowledge-base/articles/connect-to-mongodb-atlas/).
## Code Deployment

Code Deployment involves few steps for Data scraping, Data ingestion and accessibility.

## step1:

Create a virtual environment, activate it and install packages from `Pipfile`.We can use
following cmds that will activate and install requirded packages.
```bash
  pip install pipenv
  pipenv shell
  pipenv install
```

##  step2:

Run the scrapy cmd to scrape the data from [website](https://www.zaubacorp.com/company-list).
make sure current dir in this [path](https://github.com/venunallapu2022/advaRiskAssignment/tree/main/advaRisk) before running scrapy cmd.here the spider name is `companies`.

```bash
  scrapy crawl companies
```
The data will be ingested in the mongodb database.here i have given local connection and we can also ingest data remotely to db.

## step3:

Now the last and final part that is accessing data.There are two ways provided to access the data from MongoDB.one is running `python scripts` and other is using `fastAPI`

make sure current dir in this [dbpath](https://github.com/venunallapu2022/advaRiskAssignment/tree/main/advaRisk/advaRisk) before running database scripts.

## Method 1 - Python Script and Input file
we give our query inside a [input.json](https://github.com/venunallapu2022/advaRiskAssignment/blob/main/advaRisk/advaRisk/input.json) and then run python run cmd to run pipeline script

```bash
  python pipelines.py
```

sample query we can write in [input.json](https://github.com/venunallapu2022/advaRiskAssignment/blob/main/advaRisk/advaRisk/input.json)

```bash
  {'company_address.city':'jaipur'}
```

## Method 2 - FastAPI UI
we can use fastAPI for accessing data from mongodb.[FastAPI](https://fastapi.tiangolo.com/lo/) is a modern web framework for building RESTful APIs in Python.we can connect mongodb server with fastAPI to access the data. To start fastAPI we have to run following cmd

```bash
  uvicorn main:app
```

Now the fastAPI gets hosted at [localhost](http://127.0.0.1:8000/) and to interact with data, we need to access [localhost/docs](http://127.0.0.1:8000/docs).

In the fastAPI UI we can access data with query,city name,company name and id.
 we need to select particular option and use `Try It Out`.

sample example input to access data by [query](http://127.0.0.1:8000/docs#/default/get_company_by_query_query__query__get):
```bash
  {'status':'active'}
```
```bash
  {'company_address.city':'jaipur'}
```

sample example input  to access data by [city_name](http://127.0.0.1:8000/docs#/default/get_company_by_city_city__city_name__get):
```bash
  jaipur
```

sample example input  to access data by [company_name](http://127.0.0.1:8000/docs#/default/get_company_by_name_company_name__company_name__get):
```bash
  awign enterprises private limited
```


sample example input  to access data by [companystatus](http://127.0.0.1:8000/docs#/default/get_company_by_status_status__status__get):
```bash
  active
```

### Delete data from data base

If we want to delete all ingested data from mongodb we can run [mongogb](https://github.com/venunallapu2022/advaRiskAssignment/blob/main/advaRisk/advaRisk/mongodb.py) script
```bash
  python mongodb.py
```










## Data Model

Here I Have used [Embedded](https://www.mongodb.com/docs/manual/core/data-model-design/#std-label-data-modeling-embedding) data model Because, For many use cases in MongoDB the denormalized data model is optimal.


![App Screenshot](https://github.com/venunallapu2022/advaRiskAssignment/blob/main/datamodel.png)
