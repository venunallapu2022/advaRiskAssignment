from fastapi import FastAPI, HTTPException
from mongodb import MongoDB

"""
    FastAPI is a python framework that produces a RESTAPI
    here we are acessing data from FASTAPI from Mongo DB 
    on remote server
"""
app = FastAPI()


mongo = MongoDB()


@app.get("/")
async def root():
    companies = mongo.find_many_from_mongo()
    return companies


@app.get("/query/{query}")
def get_company_by_query(query: str):
    """
            This method takes query and passes desired output
    """
    company = mongo.find_from_mongo_by_query(eval(query))
    if len(company) == 0:
        raise HTTPException(status_code=500, detail="Data not found")
    return company


@app.get("/companies")
def get_companies():
    """
            This method access all the data of collection
    """
    movies = mongo.find_many_from_mongo()
    return movies


@app.get("/company_name/{company_name}")
def get_company_by_name(company_name: str):
    """
            This method filter DB based on company name and return output of
            that company
    """
    company = mongo.find_from_mongo_by_name(company_name)
    if len(company) == 0:
        raise HTTPException(status_code=500, detail="Company not found")
    return company


@app.get("/city/{city_name}")
def get_company_by_city(city_name: str):
    """
            This method filter DB based on city name where company located
            and return output of that company
    """
    company = mongo.find_from_mongo_by_city(city_name)
    if len(company) == 0:
        raise HTTPException(status_code=500, detail="Company not found")
    return company


@app.get("/status/{status}")
def get_company_by_status(status: str):
    """
            This method filter DB based on company working status
            and return output of that company
    """
    company = mongo.find_from_mongo_by_status(status)
    if len(company) == 0:
        raise HTTPException(status_code=500, detail="Company not found")
    return company
