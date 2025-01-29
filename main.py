from data_analyser import DataAnalyser
from redcap_api_handler import RedcapApiHandler
from datetime import datetime

import xlsxwriter
import pandas as pd

def main():
    outputDir = './resources/'
    datestr = datetime.today().strftime('%Y%m%d')
    sites = ['ethiopia', 'nigeria'] 
    site = sites[0] # dealing with ethiopia for now
    csv = outputDir + 'data_{}_{}.csv'.format(site, datestr)
    print(csv)
    data = RedcapApiHandler(site).export_from_redcap(csv)
    # try writing data to csv
    data.to_csv(csv, index=False)
    print('successfully saved data to csv file')
    # Generate outliers
    outliers_writer = pd.ExcelWriter(outputDir + 'outliers_{}_{}.xlsx'.format(site, datestr), engine='xlsxwriter')
    DataAnalyser(outputDir, data, site).write_outliers_report(outliers_writer)
    outliers_writer.close() #outliers_writer.save()

if __name__ == '__main__':
    main()

