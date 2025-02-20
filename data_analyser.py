import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import StringIO
import xlsxwriter 
import api_keys
from instruments import Instruments
from redcap_api_handler import RedcapApiHandler 


class DataAnalyser:
    def __init__(self, resource_dir, data, site):
        self.data = data
        self.instruments = Instruments(data)
        self.resource_dir = resource_dir
        self.site = site
    
    def instrument_outliers(self, instrument_data, data_frame, instrument_key):

            for col in instrument_data.columns:
                if col in self.ignored_cols:
                    continue
                data = instrument_data[col]

                # Skip iteration if all data is NaN
                if data.dropna().size == 0:
                    continue

                data = data.dropna()
                print(data)
                

                # Remove -999 (missing data)  
                data = data[data != -999]

                q1 = data.quantile(0.25)
                q3 = data.quantile(0.75)
                mean = np.round(data.mean(),1)
                std = np.round(data.std(),1)
                median = np.round(data.median(),1)
                iqr = q3 - q1

                # Skip iteration if IQR = 0
                if iqr == 0:
                    continue

                upper_limit_iqr = q3 + 1.5 * iqr
                lower_limit_iqr = q1 - 1.5 * iqr

                upper_limit_std = mean + std * 3
                lower_limit_std = mean - std * 3

                upper_limit = max(upper_limit_iqr, upper_limit_std)
                lower_limit = min(lower_limit_iqr, lower_limit_std)

                # Find outliers i.e. values outside the range (q1 - 1.5 * iqr, q3 + 1.5 * iqr)
                mask = data.between(lower_limit, upper_limit, inclusive='both')
                outliers = data[~mask].dropna()

                # Skip iteration if there are no outliers
                if outliers.size == 0:
                    continue

                # self.plot_histogram(data, col, outliers)

                outliers = outliers.to_frame()

                outliers.rename(columns={col:'Value'}, inplace=True)
                outliers['Data Field'] = col
                outliers['Instrument'] = instrument_key
                # outliers['Median'] = median
                outliers['Lower Limit'] = lower_limit
                outliers['Upper Limit'] = upper_limit

                # outliers['Limit'] = np.where( ( outliers['Value'] >= upper_limit ), upper_limit, lower_limit )
                # outliers['Comment'] = ''

                data_frame = pd.concat([data_frame, outliers]) #data_frame = data_frame.append(outliers)

            return data_frame


    def write_outliers_report(self, outliers_xlsx_writer):
        exceptions = RedcapApiHandler(self.site).get_exceptions_from_redcap()

        df = pd.DataFrame()

        for instrument_key, instrument_getter in self.instruments.instrument_dict.items():
            if instrument_key == 'participant_information':
                continue
            instrument_data = instrument_getter(self.instruments)
            instrument_data.set_index(['study_id'], inplace=True)
            instrument_data = instrument_data.select_dtypes(include=np.number)
            df = self.instrument_outliers(instrument_data, df, instrument_key)

        # Remove exceptions from outliers frame
        df = pd.merge(df, exceptions, on=['study_id','Data Field'], how='outer', indicator='source')
        df = df[df['source'] == 'left_only'].drop('source', axis=1)

        df['Is Correct'] = ''
        df['Comment/Updated Value'] = ''
        df = df[['Data Field', 'Instrument', 'Value', 'Lower Limit', 'Upper Limit', 'Is Correct', 'Comment/Updated Value']]
        df = df.sort_values(by=['study_id', 'Instrument'])
        df.reset_index(inplace=True)
        df.to_excel(outliers_xlsx_writer, sheet_name='Outliers', startcol=0, startrow=3, index=False)

        lower_limit_text = 'Lower Limit = min(mean - std * 3, 1st quartile - 1.5 * IQR)'
        upper_limit_text = 'Upper Limit = max(mean + std * 3, 3rd quartile + 1.5 * IQR)'

        outliers_xlsx_writer.sheets['Outliers'].write(0, 0, lower_limit_text)
        outliers_xlsx_writer.sheets['Outliers'].write(1, 0, upper_limit_text)
        outliers_xlsx_writer.sheets['Outliers'].set_column(0, 0 , 15)
        outliers_xlsx_writer.sheets['Outliers'].set_column(1, 1 , 30)
        outliers_xlsx_writer.sheets['Outliers'].set_column(2, 2 , 30)
        outliers_xlsx_writer.sheets['Outliers'].set_column(3, 3 , 10)
        outliers_xlsx_writer.sheets['Outliers'].set_column(4, 4 , 12)
        outliers_xlsx_writer.sheets['Outliers'].set_column(5, 5 , 12)
        outliers_xlsx_writer.sheets['Outliers'].set_column(6, 6 , 20)
        outliers_xlsx_writer.sheets['Outliers'].set_column(7, 7 , 30)

    # Skip all dropdowns/checkboxes/radio buttons
    ignored_cols = ['country', # dropdowns
                    'lang_used_nigeria',
                    'study_site_nigeria',
                    'study_site_ethiopia'
                    'date_of_birth_known',
                    'sex',
                    'ethnicity_ethiopia',
                    'ethnicity_nigeria',
                    'father_ethnicity_nigeria',
                    'father_ethnicity_ethiopia',
                    'mother_ethnicity_nigeria',
                    'mother_ethnicity_ethiopia',
                    'first_language_nigeria',
                    'first_language_ethiopia',
                    'father_first_language_nigeria',
                    'mother_first_language_nigeria',
                    'father_first_language_ethiopia',
                    'mother_first_language_ethiopia',
                    'control_selected_from',
                    'cgi_severity_of_illness',
                    'cgi_global_improvement',
                    'antidepressant_number_medications',
                    'antidepressant_how_long_flu',
                    'antidepressant_how_long_cita',
                    'antidepressant_how_long_tric',
                    'antidepressant_how_long_sert',
                    'antidepressant_how_long_other',
                    'health_history_diabetes_type,'
                    'highest_level_education',
                    'father_highest_level_of_education',
                    'mother_highest_level_of_education',
                    'current_employment_status',
                    'empl_days_work',
                    'marital_status',
                    'hfias_how_often_not_enough_food,'
                    'hfias_how_often_lack_resources',
                    'hfias_how_often_eat_limited',
                    'hfias_how_often_eat_food_not_want',
                    'hfias_how_often_eat_smaller_meals',
                    'hfias_how_often_eat_fewer_meals_in_aday',
                    'how_often_no_food',
                    'hfias_how_often_sleep_hungry',
                    'hfias_how_often_day_night_without_eating',
                    'social_support_number_of_people',
                    'ocial_support_concern',
                    'social_support_practical_help',
                    'reprod_history_last_period_mm',
                    'antidepressant_type', # checkboxes
                    'glad_sideeffect_fluoxetine',
                    'glad_sideeffect_citalopram',
                    'glad_sideeffect_tricyclic',
                    'glad_sideeffect_setraline',
                    'glad_sideeffect_other',
                    'glad_worstaspect_sideeffects',
                    'health_history_type_diabetes_treatment',
                    'aseet_household_items_nigeria',
                    'asset_anyoneinhousehold_hasitemsnigeria',
                    'les_relative_lost',
                    'les_illness_relatives',
                    'les_most_distressing_event',
                    'urban_or_rural', # radio
                    'case_control', 
                    'cidi_felt_sad_blue_or_depressed',
                    'cidi_lost_interest_in_hobbies_work',
                    'scan_information_source_pse',
                    'scan_source_information_ps',
                    'scan_source_information_re_lb',
                    'scan_clinical_history_schedule',
                    'scan_episode_type_second_section',
                    'scan_expansive_mood',
                    'scan_mixed_episodes_during_course',
                    'scan_interference_with_activities_due_to_section_1_7_4_symptoms',
                    'scan_organic_cause_of_section_1_7_4_symptoms',
                    'scan_periods_of_elation',
                    'scan_increased_goal_directed_activity',
                    'scan_distructibility',
                    'scan_decreased_need_for_sleep_hypomania',
                    'scan_inflated_self_esteem',
                    'scan_sharpened_unusually_creative_thinking',
                    'scan_increased_sociability',
                    'scan_more_talkative',
                    'scan_thoughts_racing',
                    'scan_more_witty_than_usual',
                    'scan_increased_involvement_sex',
                    'scan_increase_in_other_pleasurable_activities',
                    'scan_over_optimism_exaggeration_past_achievements',
                    'scan_periods_of_irritability',
                    'scan_2_or_more_years_hypomania_remisions_less_than_2_months',
                    'scan_2_plus_years_of_subdepression_only',
                    'scan_2_plus_years_of_instability_of_mood',
                    'scan_continuity_major_affective_syndrome_with_present_cyclothymia',
                    'scan_continuity_major_affective_syndrome_with_past_cyclothymia',
                    'scan_interference_with_activities_due_to_persistent_hypomania_and_cyclothymia',
                    'scan_organic_cause_hypomania_cyclothymia',
                    'scan_episode_type',
                    'scan_depressed_mood',
                    'scan_tearfulness_and_crying',
                    'scan_anhedonia',
                    'scan_loss_of_hope',
                    'scan_feeling_of_loss_of_feeling',
                    'scan_loss_of_reactivity',
                    'scan_morning_depression',
                    'scan_preoccupation_death_catastrophe',
                    'scan_suicide_self_harm',
                    'scan_tedium_vitae',
                    'scan_pathological_guilt',
                    'scan_guilty_ideas_of_reference',
                    'scan_loss_of_self_confidence_with_other_people',
                    'scan_social_withdrawal',
                    'scan_loss_of_self_esteem',
                    'scan_delusions_of_guilt',
                    'scan_delusions_of_catastrophe',
                    'scan_hypochondriacal_delusions',
                    'scan_congruence_of_auditory_hallucinations',
                    'scan_depression_or_anxiety_primary',
                    'scan_relation_of_somatoform_to_depressive_symptoms',
                    'scan_relation_of_obsessional_to_depressive_symptoms',
                    'scan_interference_with_activities',
                    'scan_organic_cause_of_depressive_symptoms',
                    'scan_personality_prior_to_depression_onset',
                    'scan_severity_affective_episodes',
                    'scan_two_or_more_episodes_recovery',
                    'scan_response_to_antidepressive_therapy',
                    'scan_2_or_more_years_depression',
                    'scan_reduction_in_energy_activity',
                    'scan_insomnia',
                    'scan_hypersomnia',
                    'scan_loss_of_self_confidence',
                    'scan_difficulty_concentrating_making_decisions',
                    'scan_frequent_tearfulness',
                    'scan_loss_of_interest_enjoyment',
                    'scan_feeling_hoplessness_despair',
                    'scan_decreased_productivity_inability_to_cope',
                    'scan_pessimism_future_brooding_over_past',
                    'scan_social_withdrawal_persistent_depressive_states',
                    'scan_reduced_talkativeness',
                    'scan_poor_appetite_over_eating',
                    'scan_chronic_fatigue_tiredness',
                    'scan_feelings_of_guilt',
                    'scan_irritability_excessive_anger',
                    'scan_interference_with_activities_due_to_symptoms',
                    'scan_organic_cause_of_dysthymia_symptoms',
                    'scan_recurrent_brief_depressive_episode',
                    'scan_short_duration_of_depressive_phase',
                    'scan_not_solely_related_to_menstrual_cycle',
                    'scan_interference_with_activities_due_to_brief_recurrent_depressiive_disorder',
                    'scan_organic_cause_of_brief_depressive_phase',
                    'scan_identify_organic_cause_of_brief_depressive_phase',
                    'scan_positive_cognitive_functioning',
                    'scan_loss_of_concentration',
                    'scan_subjectively_inefficient_thinking',
                    'scan_loss_of_interests',
                    'scan_feeling_of_retardation',
                    'scan_loss_of_energy',
                    'scan_feeling_overwhelmed_by_everyday_tasks',
                    'scan_interference_with_activities_due_to_section7_symptoms',
                    'scan_organic_cause_of_section7_symptoms',
                    'scan_change_in_appetite',
                    'scan_loss_of_weight',
                    'scan_gain_of_weight',
                    'scan_sleep_problem_with_depressed_mood',
                    'scan_effect_of_tablets_on_sleep_pattern',
                    'scan_delayed_sleep',
                    'scan_poor_quality_sleep',
                    'scan_middle_insomnia',
                    'scan_early_waking',
                    'scan_disturbance_of_normal_sleep_wake_cycle',
                    'scan_hypersomnia2',
                    'scan_interference_with_activities_due_to_sleep_problems',
                    'scan_organic_cause_of_sleep_problems',
                    'scan_loss_of_libido',
                    'scan_loss_of_libido_associated_with_depression',
                    'scan_sexual_problems',
                    'scan_interference_with_activities_due_to_sexual_dysfunction',
                    'scan_organic_cause_of_sexual_dyfunction',
                    'scan_clinical_impression',
                    'audit_drink_alcohol',
                    'audit_number_drinks',
                    'audit_how_often_six_or_more_drinks',
                    'audit_not_able_to_stop_drinking',
                    'audit_failed_to_do_normal_tasks',
                    'audit_had_hangover',
                    'audit_had_guilt_after_drinking',
                    'audit_blanked_out_after_drinking',
                    'audit_injured_drinking',
                    'audit_cut_down_drinking',
                    'assist_howoften_pastthreemonth_tobacco',
                    'assist_howoften_pastthreemonth_tobacco_desire',
                    'assist_tobacco_ledto_problems',
                    'assist_led_to_problems_tobacco',
                    'assist_people_concerned_tobaccouse',
                    'assist_cut_down_tobacco',
                    'assist_howoften_pastthreemonth_khat',
                    'assist_howoften_pastthreemonth_khat_desire',
                    'assist_khat_ledto_problems',
                    'assist_howoften_failed_normaltasks_khat',
                    'assist_people_concerned_khat_use',
                    'assist_cut_down_khat',
                    'assist_howoften_pastthreemonth_cannabis',
                    'assist_howoften_pastthreemonth_cannabis_desire',
                    'assist_cannabis_ledto_problem',
                    'assist_howoften_failed_normaltask_cannabis',
                    'assist_people_concerned_cannabisuse',
                    'assist_cut_down_cannabis',
                    'assist_howoften_pastthreemonth_cocaine',
                    'assist_howoften_pastthreemonth_cocaine_desire',
                    'assist_cocaine_ledto_problem',
                    'assist_howoften_failed_normaltask_cocaine',
                    'assist_people_concerned_cocianeuse',
                    'assist_cutdown_cocaine',
                    'assist_howoften_pastthreemonth_amphetamine',
                    'assist_howoften_pastthreemonths_amphetamine_desire',
                    'assist_amphetamine_ledto_problems',
                    'assist_howoften_failed_normaltasks_amphetamine',
                    'assist_people_concerned_amphetamineuse',
                    'assist_cutdown_amphetamine',
                    'assist_howoften_pastthreemonth_inhalents',
                    'assist_howoften_pasttheemonth_inhalent_desire',
                    'assist_inhalent_ledto_problem',
                    'assist_howoften_failed_normaltask_inhalents',
                    'assist_people_concerned_inhalents',
                    'assist_cutdown_inhalents',
                    'assist_howoften_pastthreemonth_sedatives',
                    'assist_howoften_pastthreemonth_sedatives_desire',
                    'assist_sedatives_ledto_problems',
                    'assist_howoften_failed_normaltask_sedatives',
                    'assist_people_concerned_sedatives',
                    'assist_cut_down_sedatives',
                    'assist_past_three_months_hallucinogens',
                    'assist_urge_past_months_hallucinogens',
                    'assist_use_hallucinogens_led_to_problems',
                    'assist_failed_to_do_normal_tasks_hallucinogens',
                    'assist_people_concerned_hallucinogens',
                    'assist_cut_down_hallucinogens',
                    'assist_howoften_pastthree_months_opioids',
                    'assist_strong_desire_opioids',
                    'assist_led_to_problems_opioids',
                    'assist_failed_todo_normal_task_opioids',
                    'assist_people_concerned_opioids',
                    'assist_cut_down_opioids',
                    'assist_howoften_pastthree_months_over_the_counter',
                    'assist_strong_desire_over_the_counter',
                    'assist_ledtoproblems_overcounter',
                    'assist_failed_todo_normally_expected_overcounter',
                    'assist_people_concerned_overcounter',
                    'assist_cutdown_overcounter',
                    'assist_howoften_pastthreemonth_othersubstances',
                    'assist_howoften_pastthreemonth_othersubstance_desire',
                    'assist_othersubstance_ledto_problems',
                    'assist_howoften_failed_normaltasks_othersubstance',
                    'assist_people_concerned_othersubstanceuse',
                    'assist_cut_down_othersubstances',
                    'tramadol',
                    'morphine',
                    'pethidine',
                    'other_drug_injection',
                    'antidepressant_efficacy_flu',
                    'antidepressant_efficacy_cita',
                    'antidepressant_efficacy_tric',
                    'antidepressant_efficacy_sert',
                    'antidepressant_efficacy_other',
                    'antidepressant_impr_flu',
                    'antidepressant_impr_cita',
                    'antidepressant_impr_tric',
                    'antidepressant_impr_sert',
                    'antidepressant_impr_other',
                    'mmas_forget_take_medicine',
                    'mmas_problem_remembering_take_medicine',
                    'mmas_stop_taking_medicine_better',
                    'mmas_stop_taking_medicine_worse',
                    'sideeffect_dry_mouth_flu',
                    'sideeffect_sweating_flu',
                    'sideeffect_nausea_flu',
                    'sideeffect_vomiting_flu',
                    'sideeffect_diarrhoea_flu',
                    'sideeffect_constipation_flu',
                    'sideeffect_headache_flu',
                    'sideeffect_dizziness_flu',
                    'sideeffect_memory_problems_flu',
                    'sideeffect_attention_difficulties_flu',
                    'sideeffect_shaking_flu',
                    'sideeffect_muscle_pain_flu',
                    'sideeffect_sleepiness_flu',
                    'sideeffect_difficulty_sleeping_flu',
                    'sideeffect_increased_anxiety_flu',
                    'sideeffect_fast_heart_beat_flu',
                    'sideeffect_restlessness_flu',
                    'sideeffect_fatigue',
                    'sideeffect_change_in_appetite_flu',
                    'sideeffect_weight_gain_flu',
                    'sideeffect_weight_loss_flu',
                    'sideeffect_itching_flu',
                    'sideeffect_rash_flu',
                    'sideeffect_runny_nose_flu',
                    'sideeffect_reduced_sexual_desire_flu',
                    'sideeffect_menstrual_problems_flu',
                    'sideeffect_blurred_vision_flu',
                    'sideeffect_suicidal_thoughts_flu',
                    'sideeffect_attempted_suicide_flu',
                    'sideeffect_other_flu',
                    'sideeffect_dry_mouth_cita',
                    'sideeffect_sweating_cita',
                    'sideeffect_nausea_cita',
                    'sideeffect_vomiting_cita',
                    'sideeffect_diarrhoea_cita',
                    'sideeffect_constipation_cita',
                    'sideeffect_headache_cita',
                    'sideeffect_dizziness_cita',
                    'sideeffect_memoryproblems_cita',
                    'sideeffect_attentiondifficulties_cita',
                    'sideeffect_shaking_cita',
                    'sideeffect_muscle_pain_cita',
                    'sideeffect_sleepiness_cita',
                    'sideeffect_difficulty_sleep_cita',
                    'sideeffect_increased_anxiety_cita',
                    'sideeffect_fastheartbeat_cita',
                    'sideeffect_restlessness_cita',
                    'sideeffect_fatigue_cita',
                    'sideeffect_change_appetite_cita',
                    'sideeffect_weightgain_cita',
                    'sideeffect_weight_loss_cita',
                    'sideeffect_itching_cita',
                    'sideeffect_rash_cita',
                    'sideeffect_runny_nose_cita',
                    'sideeffect_reduced_sexual_desire_cita',
                    'sideeffect_menstrual_problems_cita',
                    'sideeffect_blurred_vision_cita',
                    'sideeffect_suicidal_thoughts_cita',
                    'sideeffect_attempted_suicide_cita',
                    'sideeffect_other_cita',
                    'sideeffect_dry_mouth_tric',
                    'sideeffect_sweating_tric',
                    'sideeffect_nausea_tric',
                    'sideeffect_vomiting_tric',
                    'sideeffect_diarrhoea_tric',
                    'sideeffect_constipation_tric',
                    'sideeffect_headache_tric',
                    'sideeffect_dizziness_tric',
                    'sideeffect_memory_problems_tric',
                    'sideeffect_attention_difficulties_tric',
                    'sideeffect_shaking_tric',
                    'sideeffect_muscle_pain_tric',
                    'sideeffect_sleepiness_tric',
                    'sideeffect_difficulty_sleep_tric',
                    'sideeffect_increased_anxiety_tric',
                    'sideeffect_fast_heart_beat_tric',
                    'sideeffect_restlessness_tric',
                    'sideeffect_fatigue_tric',
                    'sideeffect_change_appetite_tric',
                    'sideeffect_weight_gain_tric',
                    'sideeffect_weight_loss_tric',
                    'sideeffect_itching_tric',
                    'rsideeffect_rash_tric',
                    'sideeffect_runny_nose_tric',
                    'sideeffect_reduced_sexual_desire_tric',
                    'sideeffect_menstrual_problems_tric',
                    'sideeffect_blurred_vision_tric',
                    'sideeffect_suicidal_thoughts_tric',
                    'sideeffect_attempted_suicide_tric',
                    'sideeffect_other_tric',
                    'sideeffect_drymouth_sert',
                    'sideeffect_sweating_sert',
                    'sideeffect_nausea_sert',
                    'sideeffect_vomiting_sert',
                    'sideeffect_diarrhoea_sert',
                    'sideeffect_constipation_sert',
                    'sideeffect_headache_sert',
                    'sideeffect_dizziness_sert',
                    'sideeffect_memory_problems_sert',
                    'sideeffect_attention_concentration_difficulties_sert',
                    'sideeffect_shaking_sert',
                    'sideeffect_muscle_pain_sert',
                    'sideeffect_sleepinness_sert',
                    'sideeffect_difficulty_getting_sleep_sert',
                    'sideeffect_increased_anxiety_sert',
                    'sideeffect_fast_heart_beat_sert',
                    'sideeffect_restlessness_sert',
                    'sideeffect_fatigue_sert',
                    'sideeffect_change_appetite_sert',
                    'sideeffect_weight_gain_sert',
                    'sideeffect_weight_loss_sert',
                    'sideeffect_itching_sert',
                    'sideeffect_rash_sert',
                    'sideeffect_runny_nose_sert',
                    'sideeffect_reduced_sexual_desire_sert',
                    'sideeffect_menstrual_problems_sert',
                    'sideeffect_blurred_vision_sert',
                    'sideeffect_suicidal_thoughts_sert',
                    'sideeffect_attempted_suicide_sert',
                    'sideeffect_other_sert',
                    'sideeffect_dry_mouth_other',
                    'sideffect_sweating_other',
                    'sideffect_nausea_other',
                    'sideffect_vomiting_other',
                    'sideffect_diarrhoea_other',
                    'sideffect_constipation_other',
                    'sideffect_headache_other',
                    'sideffect_dizziness_other',
                    'sideffect_memory_problems_other',
                    'sideffect_attention_difficulties_other',
                    'sideffect_shaking_other',
                    'sideffect_muscle_pain_other',
                    'sideffect_sleepiness_other',
                    'sideffect_difficulty_getting_to_sleep_other',
                    'sideffect_increased_anxiety_other',
                    'fast_heart_beat',
                    'sideffect_restlessness_other',
                    'sideffect_fatigue_other',
                    'sideffect_change_in_appetite_other',
                    'sideffect_weight_gain_other',
                    'sideffect_weight_loss_other',
                    'sideffect_itching_other',
                    'sideffect_rash_other',
                    'sideffect_runny_nose_other',
                    'sideffect_reduced_sexual_desire_other',
                    'sideffect_menstrual_problems_other',
                    'sideffect_blurred_vision_other',
                    'sideffect_suicidal_thoughts_other',
                    'sideffect_attempted_suicide_other',
                    'sideffect_other_other',
                    'sideeffect_dosage_taken',
                    'ledto_discontinue_dry_mouth',
                    'ledto_discontinue_sweating',
                    'ledto_discontinue_nausea',
                    'ledto_discontinue_vomiting',
                    'ledto_discontinue_diarrhoea',
                    'ledto_discontinue_constipation',
                    'ledto_discontinue_headache',
                    'ledto_discontinue_dizziness',
                    'ledto_discontinue_memory_problems',
                    'ledto_discontinue_attention_difficulties',
                    'ledto_discontinue_shaking',
                    'ledto_discontinue_muscle_pain',
                    'ledto_discontinue_sleepiness',
                    'ledto_discontinue_difficulty_sleep',
                    'ledto_discontinue_increased_anxiety',
                    'ledto_discontinue_fast_heart_beat',
                    'ledto_discontinue_restlessness',
                    'ledto_discontinue_fatigue',
                    'ledto_discontinue_change_in_appetite',
                    'ledto_discontinue_weight_gain',
                    'ledto_discontinue_weight_loss',
                    'ledto_discontinue_itching',
                    'ledto_discontinue_rash',
                    'ledto_discontinue_runny_nose',
                    'ledto_discontinue_reduced_sexual_desire',
                    'ledto_discontinue_menstrual_problems',
                    'ledto_discontinue_blurred_vision',
                    'ledto_discontinue_suicidal_thoughts',
                    'ledto_discontinue_attempted_suicide',
                    'ledto_discontinue_other_sideeffect',
                    'treated_dry_mouth',
                    'treated_sweating',
                    'treated_nausea',
                    'treated_vomiting',
                    'treated_diarrhoea',
                    'treated_constipation',
                    'treated_headache',
                    'treated_dizziness',
                    'treated_memory_problems',
                    'treated_attention_difficulties',
                    'treated_shaking',
                    'treated_muscle_pain',
                    'treated_sleepiness',
                    'treated_difficulty_sleep',
                    'treated_increased_anxiety',
                    'treated_fast_heart_beat',
                    'treated_restlessness',
                    'treated_fatigue',
                    'treated_change_in_appetite',
                    'treated_weight_gain',
                    'treated_weight_loss',
                    'treated_itching',
                    'treated_rash',
                    'treated_runny_nose',
                    'treated_reduced_sexual_desire',
                    'treated_menstrual_problems',
                    'treated_blurred_vision',
                    'treated_suicidal_thoughts',
                    'treated_attempted_suicide',
                    'treated_other_sideeffect',
                    'health_history_bp_pressure',
                    'health_history_when_pregnant',
                    'health_history_regular_medication',
                    'health_history_diabetes',
                    'health_history_pregnant_diabetes',
                    'health_history_taking_regular_medication',
                    'health_history_asthma',
                    'health_history_asthma_treatment',
                    'health_history_regular_asthma_medication',
                    'health_history_asthma_medication',
                    'health_history_epilepsy',
                    'health_history_epilepsy_treatment',
                    'health_history_regular_epilepsy_medication',
                    'health_history_cancer',
                    'health_history_cancer_treatment',
                    'health_history_cancer_regular_treatment',
                    'health_history_kidney_disease',
                    'health_history_kidney_treatment',
                    'health_history_kidney_regular',
                    'health_history_stroke',
                    'health_history_stroke_treatment',
                    'health_history_stroke_regular_treatment',
                    'health_history_heartattack',
                    'health_history_heartattack_treat',
                    'health_history_heartattack_regular_treat',
                    'health_history_angina',
                    'health_history_angina_treatment',
                    'health_history_angina_regular_treatment',
                    'health_history_tb',
                    'health_history_tb_treatment',
                    'health_history_hiv',
                    'health_history_hiv_treatment',
                    'health_history_sickle_cell',
                    'health_history_sickle_cell_treatment',
                    'father_had_formal_education',
                    'mother_had_formal_education',
                    'asset_electricity_ethiopia',
                    'asset_radio_ethiopia',
                    'asset_television_ethiopia',
                    'asset_refrigerator_ethiopia',
                    'asset_electric_mitad_ethiopia',
                    'asset_table_ethiopia',
                    'asset_chair_ethiopia',
                    'asset_bed_ethiopia',
                    'asset_bank_account_ethiopia',
                    'asset_water_source_ethiopia',
                    'asset_toilet_facility_ethiopia',
                    'asset_cooking_fuel_ethiopia',
                    'asset_floor_material_ethiopia',
                    'asset_wall_material_ethiopia',
                    'asset_roof_material_ethiopia',
                    'asset_water_source_nigeria',
                    'asset_toilet_facility_nigeria',
                    'asset_cooking_fuel_nigeria',
                    'asset_other_cooking_fuel_nigeria',
                    'asset_cooking_place_nigeria',
                    'asset_floor_nigeria',
                    'asset_roof_nigeria',
                    'asset_rent_nigeria',
                    'disability_standing_long_periods',
                    'disability_taking_care_household',
                    'disability_learning_new_task',
                    'disability_joining_community_activities',
                    'disability_emotionally_affected',
                    'disability_concentrating',
                    'disability_walking_long_distances',
                    'disability_washing_body',
                    'disability_getting_dressed',
                    'disability_dealing_with_strangers',
                    'disability_maintaining_friendship',
                    'disability_daily_work',
                    'phq9_feeling_down',
                    'phq9_little_interest_pleasure',
                    'phq9_trouble_with_sleep',
                    'phq9_type_sleeping_disorder',
                    'phq9_feeling_tired',
                    'phq9_poor_appettite_overeating',
                    'phq9_type_food_disorder',
                    'phq9_feeling_bad_about_self',
                    'phq9_trouble_concentrating',
                    'phq9_moving_or_speaking_slowly',
                    'phq9_type_of_movement_disorder',
                    'phq9_suicidal_thoughts',
                    'phq9_difficulty_work',
                    'gad7_feeling_nervous',
                    'gad7_wont_stop_worrying',
                    'gad7_worrring_different_things',
                    'gad7_trouble_relaxing',
                    'gad7_feeling_restless',
                    'gad7_beeing_annoyed',
                    'gad7_feeling_afraid',
                    'les_married_engaged',
                    'les_serious_arguments',
                    'les_divorced_separated',
                    'les_closeness_change',
                    'les_lost_relative',
                    'les_illness_relative',
                    'les_unable_to_work',
                    'les_loss_of_income',
                    'les_trouble_with_employer',
                    'les_major_illness',
                    'les_hospitalised',
                    'les_motor_vehicle_accident',
                    'les_physically_attacked',
                    'les_robbed',
                    'les_unsafe_neighborhood',
                    'les_attacked_animal',
                    'les_isolated_sickessnes',
                    'les_physically_abused',
                    'les_property_loss',
                    'les_extremely_stressful',
                    'reprod_depression_during_pregrancy',
                    'phleb_one_purple_tube',
                    'phleb_one_yellow_tube',
                    'phleb_number_plasma_aliquots',
                    'phleb_number_blood_pellet_aliquots',
                    'phleb_number_serum_aliquots']
    

    


