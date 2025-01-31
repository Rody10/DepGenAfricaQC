import pandas as pd
import csv
import os

class BranchingLogicHandler:
    def __init__(self, data, site):
        self.data = data.set_index('study_id')
        self.site = site

    def get_missing_ids(self, input_df):
        if input_df.size == 0: return

        # Get all study_ids with missing values for each column
        output_df = input_df[input_df == True].dropna(how='all').stack().to_frame().reset_index()
        output_df.rename(columns={'level_1':'Data Field'}, inplace=True)
        output_df = output_df[['study_id', 'Data Field']]

        return output_df
    
    def check_participant_information(self):
        col_names = self.data.columns[(self.data.columns.str.contains('study_id'))|
                                      (self.data.columns.str.contains('clinician_name'))|
                                      (self.data.columns.str.contains('country'))|
                                      (self.data.columns.str.contains('lang_used_nigeria'))|
                                      (self.data.columns.str.contains('other_lang_used_nigeria'))|
                                      (self.data.columns.str.contains('study_site_nigeria'))|
                                      (self.data.columns.str.contains('study_site_ethiopia'))|
                                      (self.data.columns.str.contains('urban_or_rural'))|
                                      (self.data.columns.str.contains('dates_conversions_notes_ethiopia'))|
                                      (self.data.columns.str.contains('enrolment_date'))|
                                      (self.data.columns.str.contains('date_of_birth_known'))|
                                      (self.data.columns.str.contains('date_of_birth'))|
                                      (self.data.columns.str.contains('estimated_date_of_birth'))|
                                      (self.data.columns.str.contains('age_at_data_collection'))|
                                      (self.data.columns.str.contains('estimated_age_at_data_collection'))|
                                      (self.data.columns.str.contains('age_comment'))|
                                      (self.data.columns.str.contains('sex'))|
                                      (self.data.columns.str.contains('ethnicity_ethiopia'))|
                                      (self.data.columns.str.contains('other_ethnicity_ethiopia'))|
                                      (self.data.columns.str.contains('ethnicity_nigeria'))|
                                      (self.data.columns.str.contains('other_ethnicity_nigeria'))|
                                      (self.data.columns.str.contains('father_ethnicity_nigeria'))|
                                      (self.data.columns.str.contains('father_ethnicity_other_nigeria'))|
                                      (self.data.columns.str.contains('father_ethnicity_ethiopia'))|
                                      (self.data.columns.str.contains('other_father_ethnicity_ethiopia'))|
                                      (self.data.columns.str.contains('mother_ethnicity_nigeria'))|
                                      (self.data.columns.str.contains('mother_ethnicity_nigeria_other'))|
                                      (self.data.columns.str.contains('mother_ethnicity_ethiopia'))|
                                      (self.data.columns.str.contains('mother_ethnicity_ethiopia_other'))|
                                      (self.data.columns.str.contains('first_language_nigeria'))|
                                      (self.data.columns.str.contains('other_first_language_nigeria'))|
                                      (self.data.columns.str.contains('first_language_ethiopia'))|
                                      (self.data.columns.str.contains('other_language_ethiopia'))|
                                      (self.data.columns.str.contains('father_first_language_nigeria'))|
                                      (self.data.columns.str.contains('father_first_language_nigeria_other'))|
                                      (self.data.columns.str.contains('mother_first_language_nigeria'))|
                                      (self.data.columns.str.contains('mother_first_language_nigeria_other'))|
                                      (self.data.columns.str.contains('father_first_language_ethiopia'))|
                                      (self.data.columns.str.contains('father_first_language_ethiopia_other'))|
                                      (self.data.columns.str.contains('mother_first_language_ethiopiay'))|
                                      (self.data.columns.str.contains('mother_first_language_ethiopia_other'))]
        df = pd.DataFrame(index=self.data.index)
        for col in sorted(col_names.to_list()):
            if col in self.ignored_cols: continue

            elif col == 'study_id' or col == 'clinician_name' or col == 'urban_or_rural' or col == 'enrolment_date' or col == 'date_of_birth_known':
                mask = (self.data[col].isna())

            mask = self.data[col].isna()

            df[col] = mask.to_frame().values

        return self.get_missing_ids(df) # finish implementation
                            


ignored_cols = []
        

    
    



