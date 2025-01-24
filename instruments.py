import pandas as pd

class Instruments:
    def __init__(self, data):
        self.data = data

    def get_participant_information(self):
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
        col_names= col_names.insert(0,'study_id')
        participant_information = self.data[col_names]
        return participant_information
                                       

    def get_participant_screening(self):
        col_names = self.data.columns[(self.data.columns.str.contains('cidi_')) |
                                      (self.data.columns.str.contains('consent')) |
                                      (self.data.columns.str.contains('participant_consent_note')) |
                                      (self.data.columns.str.contains('case_')) |
                                      (self.data.columns.str.contains('cidi_')) |
                                      (self.data.columns.str.contains('control_')) |
                                      (self.data.columns.str.contains('scan_'))]
        col_names= col_names.insert(0,'study_id')
        participant_screening = self.data[col_names]
        return participant_screening

    def get_alcohol_use_disorders_identification_test(self):
        col_names = self.data.columns[(self.data.columns.str.contains('audit_'))]
        col_names= col_names.insert(0,'study_id')
        alcohol_use_disorders_identification_test = self.data[col_names]
        return alcohol_use_disorders_identification_test

    def get_alcohol_smoking_and_substance_involvement_screening_test(self):
        col_names = self.data.columns[(self.data.columns.str.contains('assist_')) |
                                      (self.data.columns.str.contains('tramadol')) |
                                      (self.data.columns.str.contains('morphine')) |
                                      (self.data.columns.str.contains('pethidine')) |
                                      (self.data.columns.str.contains('other_drug_injection')) |
                                      (self.data.columns.str.contains('other_drug_injection_specify')) |
                                      (self.data.columns.str.contains('important_note'))]
        col_names= col_names.insert(0,'study_id')
        alcohol_smoking_and_substance_involvement_screening_test = self.data[col_names]
        return alcohol_smoking_and_substance_involvement_screening_test

    def get_clinical_global_impression(self):
        col_names = self.data.columns[(self.data.columns.str.contains('cgi_')) |
                                      (self.data.columns.str.contains('clinician_additional_information'))]
        col_names= col_names.insert(0,'study_id')
        clinical_global_impression = self.data[col_names]
        return clinical_global_impression
        

    def get_history_of_antidepressant_use(self):
        col_names = self.data.columns[(self.data.columns.str.contains('antidepressant_'))]
        col_names= col_names.insert(0,'study_id')
        history_of_antidepressant_use = self.data[col_names]
        return history_of_antidepressant_use

    def get_morisky_medication_adherence_scale(self):
        col_names = self.data.columns[(self.data.columns.str.contains('mmas_'))]
        col_names= col_names.insert(0,'study_id')
        morisky_medication_adherence_scale = self.data[col_names]
        return morisky_medication_adherence_scale

    def get_antidepressant_side_effects(self):
        col_names = self.data.columns[(self.data.columns.str.contains('glad_')) |
                                      (self.data.columns.str.contains('sideeffect_')) |
                                      (self.data.columns.str.contains('rsideeffect_')) |
                                      (self.data.columns.str.contains('fast_')) |
                                      (self.data.columns.str.contains('ledto_')) |
                                      (self.data.columns.str.contains('treated_')) |
                                      (self.data.columns.str.contains('glad_worstaspect_sideeffects_')) |
                                      (self.data.columns.str.contains('glad_worstaspect_sideeffects_other'))]
        col_names= col_names.insert(0,'study_id')
        antidepressant_side_effects = self.data[col_names]
        return antidepressant_side_effects

    def get_health_history(self):
        col_names = self.data.columns[(self.data.columns.str.contains('health_'))]
        col_names= col_names.insert(0,'study_id')
        health_history = self.data[col_names]
        return health_history

    def get_sociodemographic_status(self):
        col_names = self.data.columns[(self.data.columns.str.contains('name_of_research_assistant')) |
                                      (self.data.columns.str.contains('had_formal_education')) |
                                      (self.data.columns.str.contains('highest_level_education')) |
                                      (self.data.columns.str.contains('father_had_formal_education')) |
                                      (self.data.columns.str.contains('father_highest_level_of_education')) |
                                      (self.data.columns.str.contains('mother_had_formal_education')) |
                                      (self.data.columns.str.contains('mother_highest_level_of_education')) |
                                      (self.data.columns.str.contains('current_employment_status')) |
                                      (self.data.columns.str.contains('empl_days_work')) |
                                      (self.data.columns.str.contains('marital_status')) |
                                      (self.data.columns.str.contains('household_size')) |
                                      (self.data.columns.str.contains('number_of_rooms'))]
        col_names= col_names.insert(0,'study_id')
        sociodemographic_status = self.data[col_names]
        return sociodemographic_status
    
    def get_asset_register(self):
        col_names = self.data.columns[(self.data.columns.str.contains('asset_'))]
        col_names= col_names.insert(0,'study_id')
        asset_register = self.data[col_names]
        return asset_register

    def get_household_food_insecurity_access_scale_measurement_tool(self):
        col_names = self.data.columns[(self.data.columns.str.contains('hfias_'))]
        col_names= col_names.insert(0,'study_id')
        asset_register = self.data[col_names]
        return asset_register

    def get_oslo_3_item_social_support_scale(self):
        col_names = self.data.columns[(self.data.columns.str.contains('social_')) ]
        col_names= col_names.insert(0,'study_id')
        oslo_3_item_social_support_scale = self.data[col_names]
        return oslo_3_item_social_support_scale

    def get_world_health_organization_disability_assessment_schedule(self):
        col_names = self.data.columns[(self.data.columns.str.contains('disability_')) ]
        col_names= col_names.insert(0,'study_id')
        world_health_organization_disability_assessment_schedule = self.data[col_names]
        return world_health_organization_disability_assessment_schedule

    def get_phq9(self):
        col_names = self.data.columns[(self.data.columns.str.contains('phq9_')) ]
        col_names= col_names.insert(0,'study_id')
        phq9 = self.data[col_names]
        return phq9

    def get_gad7(self):
        col_names = self.data.columns[(self.data.columns.str.contains('gad7_')) ]
        col_names= col_names.insert(0,'study_id')
        gad7 = self.data[col_names]
        return gad7

    def get_life_events_scale(self):
        col_names = self.data.columns[(self.data.columns.str.contains('les_')) |
                                      (self.data.columns.str.contains('stressful_life_events'))]
        col_names= col_names.insert(0,'study_id')
        life_events_scale = self.data[col_names]
        return life_events_scale

    def get_reproductive_history(self):
        col_names = self.data.columns[(self.data.columns.str.contains('reprod_')) ]
        col_names= col_names.insert(0,'study_id')
        reproductive_history = self.data[col_names]
        return reproductive_history

    def get_family_history_of_depression(self):
        col_names = self.data.columns[(self.data.columns.str.contains('fam_')) ]
        col_names= col_names.insert(0,'study_id')
        family_history_of_depression = self.data[col_names]
        return family_history_of_depression

    def get_cognition_conca(self):
        col_names = self.data.columns[(self.data.columns.str.contains('conca_')) ]
        col_names= col_names.insert(0,'study_id')
        cognition_conca = self.data[col_names]
        return cognition_conca

    def get_morphometry(self):
        col_names = self.data.columns[(self.data.columns.str.contains('morphometry_')) |
                                      (self.data.columns.str.contains('research_assistant_additional_information'))]
        col_names= col_names.insert(0,'study_id')
        morphometry = self.data[col_names]
        return morphometry

    def get_phlebotomy(self):
        col_names = self.data.columns[(self.data.columns.str.contains('phleb_')) |
                                      (self.data.columns.str.contains('person_doing_lab_work')) |
                                      (self.data.columns.str.contains('date_of_birth_confirmation')) |
                                      (self.data.columns.str.contains('date_of_birth_correction')) |
                                      (self.data.columns.str.contains('estimated_date_of_birth_confirmation')) |
                                      (self.data.columns.str.contains('estimated_date_of_birth_correction')) |
                                      (self.data.columns.str.contains('dates_conversions_notes_ethiopia_2')) |
                                      (self.data.columns.str.contains('if_no_yellow_tubes')) |
                                      (self.data.columns.str.contains('phlebotomy_additional_information'))]
        col_names= col_names.insert(0,'study_id')
        phlebotomy = self.data[col_names]
        return phlebotomy

    instrument_dict = {
        'participant_information'   : get_participant_information,
        'participant_screening'     : get_participant_screening,
        'alcohol_use_disorders_identification_test'     :get_alcohol_use_disorders_identification_test,
        'alcohol_smoking_and_substance_involvement_screening_test'      :get_alcohol_smoking_and_substance_involvement_screening_test,
        'clinical_global_impression'        :get_clinical_global_impression,
        'history_of_antidepressant_use':    get_history_of_antidepressant_use,
        'morisky_medication_adherence_scale': get_morisky_medication_adherence_scale,
        'antidepressant_side_effects'   :get_antidepressant_side_effects,
        'health_history'    :get_health_history,
        'sociodemographic_status'   :get_sociodemographic_status,
        'asset_register'    :get_asset_register,
        'household_food_insecurity_access_scale_measurement_tool'   :get_household_food_insecurity_access_scale_measurement_tool,
        'oslo_3_item_social_support_scale'   :get_oslo_3_item_social_support_scale,
        'world_health_organization_disability_assessment_schedule'   :get_world_health_organization_disability_assessment_schedule,
        'phq9'   : get_phq9,
        'gad7'     :get_gad7,
        'life_events_scale'     :get_life_events_scale,
        'reproductive_history'      :get_reproductive_history,
        'family_history_of_depression'        :get_family_history_of_depression,
        'cognition_conca':    get_cognition_conca,
        'morphometry': get_morphometry,
        'phlebotomy'   :get_phlebotomy
    }
        