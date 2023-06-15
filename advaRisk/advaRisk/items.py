# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy


class ColConversion:
    """
        In the below dictionary the keys are standard form given in website
        so values are new variable or keys in the desired output dictionary
    """
    cols = {
        'CIN':                      'cin',
        'Company Name':             'cname',
        'Company Status':           'status',
        'Registration Number':      'reg_number',
        'Company Category':         'company_cat',
        'Company Sub Category':     'company_sub_cat',
        'Class of Company':         'class_of_company',
        'Date of Incorporation':    'date_of_incorp',
        'Age of Company':           'age_of_company',
        'Activity':                 'activity'
    }


class CompanyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
