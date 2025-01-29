import os
import requests
import csv
import pandas as pd
from io import StringIO
import api_keys

class RedcapApiHandler:
    def __init__(self, site):
        self.site = site
        self.url = 'https://redcap.core.wits.ac.za/redcap/api/'

    def export_from_redcap(self, csv_out=None):
        report_ids = {'ethiopia': 63427, 'nigeria': 0}
        api_key = api_keys.GetApiKey(self.site)
        #print(api_key)
        #exit()
        report_id = report_ids[self.site]
        data = {
            'token': api_key,
            'content': 'report',
            'action': 'export',
            'format': 'csv',
            'report_id': report_id,
            'type': 'flat', # check if correct
            'csvDelimiter': '\t',
            'rawOrLabel': 'raw',
            'rawOrLabelHeaders': 'raw',
            'exportCheckboxLabel': 'false',
            'returnFormat': 'json'
        }
        r = requests.post(self.url,data=data)
        df = pd.read_csv(StringIO(r.text), low_memory=False, sep='\t')
        if csv_out:
            df.to_csv(csv_out, index=False, sep='\t')
        return df
    
    def get_exceptions_from_redcap(self):
        report_ids = {'ethiopia': 63660, 'nigeria': 0} # ethiopia currently has 63660, why 63427
        site_ids = {'ethiopia': 1, 'nigeria': 2}
        report_id = report_ids[self.site]
        site_id = site_ids[self.site]

        api_key = api_keys.GetApiKey('exceptions')
        url = 'https://redcap.core.wits.ac.za/redcap/api/'

        data = {
            'token': api_key,
            'content': 'report',
            'format': 'csv',
            'report_id': report_id,
            'rawOrLabel': 'raw',
            'rawOrLabelHeaders': 'raw',
            'exportCheckboxLabel': 'false',
            'returnFormat': 'json'
        }

        r = requests.post(url, data)

        if r.text == '\n':
            df = pd.DataFrame(columns = ['study_id','Data Field'])
            df.set_index('study_id', inplace=True)
        else:
            df = pd.read_csv(StringIO(r.text),index_col='study_id')
            df = df[df['is_correct'].notna() | df['comment'].notna() | df['new_value'].notna()]
            df = df[df['site'] == site_id]
            df = df[['data_field']]
            df.rename(columns={'data_field': 'Data Field'}, inplace=True)
        return df





