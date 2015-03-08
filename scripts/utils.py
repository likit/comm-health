import pandas as pd

def find_ms(df):
    subset_index = df[['BMI', 'Systolic', 'Diastolic',
                       'Triglyceride', 'HDL-C', 'Glucose',
                        'Total Cholesterol', 'Gender']].dropna().index

    df = df.ix[subset_index]
    df_bmi_lo = df.loc[df['BMI']<25.0,:]
    df_bmi_hi = df.loc[df['BMI']>=25.0,:]

    df_bmi_hi['TG-s'] = df_bmi_hi['Triglyceride']>=150.0
    df_bmi_hi['Gluc-s'] = df_bmi_hi['Glucose'] >= 100.0
    df_bmi_hi['Systolic-s'] = df_bmi_hi['Systolic']>=130.0
    df_bmi_hi['Diastolic-s'] = df_bmi_hi['Diastolic'] >=85.0

    df_bmi_hi['TG-s'] = df_bmi_hi['TG-s'].astype(int)
    df_bmi_hi['Gluc-s'] = df_bmi_hi['Gluc-s'].astype(int)
    df_bmi_hi['BP-s'] = df_bmi_hi['Systolic-s'] | df_bmi_hi['Diastolic-s']
    df_bmi_hi['BP-s'] = df_bmi_hi['BP-s'].astype(int)
    
    male_df_bmi_hi = df_bmi_hi[df_bmi_hi['Gender'] == 1]
    female_df_bmi_hi = df_bmi_hi[df_bmi_hi['Gender'] == 2]
    
    male_df_bmi_hi['HDL-C-s'] = male_df_bmi_hi['HDL-C'] < 40.0
    female_df_bmi_hi['HDL-C-s'] = female_df_bmi_hi['HDL-C'] < 50.0
    female_df_bmi_hi['HDL-C-s'] = female_df_bmi_hi['HDL-C-s'].astype(int)
    male_df_bmi_hi['HDL-C-s'] = male_df_bmi_hi['HDL-C-s'].astype(int)

    male_df_bmi_hi['MS'] = male_df_bmi_hi[['BP-s', 'Gluc-s',
    										'TG-s', 'HDL-C-s']].sum(axis=1)
    female_df_bmi_hi['MS'] = female_df_bmi_hi[['BP-s', 'Gluc-s',
    										'TG-s', 'HDL-C-s']].sum(axis=1)
    df_bmi_lo['MS'] = 0
    return pd.concat([df_bmi_lo, male_df_bmi_hi, female_df_bmi_hi])
    
def set_kpi(df):
    # BMI
    df['BMI-kpi'] = df['BMI']>=30
    
    # BP
    df['Systolic-kpi'] = df['Systolic']>=140.0
    df['Diastolic-kpi'] = df['Diastolic'] >=90.0
    df['BP-kpi'] = df['Systolic-kpi'] | df['Diastolic-kpi']
    
    # Glucose
    df['Glucose-kpi'] = df['Glucose'] >= 125.0

    # Creatinine
    df['Creatinine-kpi'] = df['Creatinine'] >=1.5
    
    # Total Cholesterol
    df['Total Cholesterol-kpi-a'] = df['Total Cholesterol'] >= 200
    df['Total Cholesterol-kpi-b'] = df['Total Cholesterol'] >= 240
    
    # HDL-C
    df['HDL-C-kpi'] = df['HDL-C'] <= 35
    
    # LDL-C (direct)
    df['LDL-C (Calculated)-kpi'] = df['LDL-C (Calculated)'] >=130
    
    # Hemoglobin
    df['CBC_Hemoglobin-kpi'] = df['CBC_Hemoglobin'] <= 10
    
def calculate_kpi_score(df):
    if len(df) == 0:
        return None

    bmi_kpi = df['BMI-kpi']
    bp_kpi = df['BP-kpi']
    glucose_kpi = df['Glucose-kpi']
    creat_kpi = df['Creatinine-kpi']
    choles_kpi_a = df['Total Cholesterol-kpi-a']
    choles_kpi_b = df['Total Cholesterol-kpi-b']
    hdl_kpi = df['HDL-C-kpi']
    ldl_kpi = df['LDL-C (Calculated)-kpi']
    hgb_kpi = df['CBC_Hemoglobin-kpi']
    ms_kpi = df['MS']>1


    bmi_kpi_percnt = len(df.ix[bmi_kpi,:])/float(len(df))
    bp_kpi_percnt = len(df.ix[bp_kpi,:])/float(len(df))
    glucose_kpi_percnt = len(df.ix[glucose_kpi,:])/float(len(df))
    creat_kpi_percnt = len(df.ix[creat_kpi,:])/float(len(df))
    choles_kpi_a_percnt = len(df.ix[choles_kpi_a,:])/float(len(df))
    choles_kpi_b_percnt = len(df.ix[choles_kpi_b,:])/float(len(df))
    hdl_kpi_percnt = len(df.ix[hdl_kpi,:])/float(len(df))
    ldl_kpi_percnt = len(df.ix[ldl_kpi,:])/float(len(df))
    hgb_kpi_percnt = len(df.ix[hgb_kpi,:])/float(len(df))
    ms_kpi_percnt = len(df.ix[ms_kpi,:])/float(len(df))
    
    #print 'bmi', bmi_kpi_percnt
    #print 'bp', bp_kpi_percnt
    #print 'glucose', glucose_kpi_percnt
    #print 'cretinine', creat_kpi_percnt
    #print 'cholesterol a', choles_kpi_a_percnt
    #print 'cholesterol b', choles_kpi_b_percnt
    #print 'HDL', hdl_kpi_percnt
    #print 'LDL', ldl_kpi_percnt
    #print 'hemoglobin', hgb_kpi_percnt
    #print 'metabolic syndrome', ms_kpi_percnt
    
    data = pd.Series()
    data['Year'] = df.year.tolist()[0]
    data['Location'] = df.Location.tolist()[0]
    
    if bmi_kpi_percnt <= 0.10:
        data['BMI'] = 1 
    else:
        data['BMI'] = 0 

    if bp_kpi_percnt <= 0.10:
        data['BP'] = 1
    else:
        data['BP'] = 0

    if glucose_kpi_percnt <= 0.05:
        data['Glucose'] = 1
    else:
        data['Glucose'] = 0

    if creat_kpi_percnt <= 0.03:
        data['Creatinine'] = 1
    else:
        data['Creatinine'] = 0
    
    if choles_kpi_a_percnt <= 0.5:
        data['Total Cholesterol-a'] = 1
    else:
        data['Total Cholesterol-a'] = 0

    if choles_kpi_b_percnt <= 0.5:
        data['Total Cholesterol-b'] = 1
    else:
        data['Total Cholesterol-b'] = 0

    if hdl_kpi_percnt <= 0.03:
        data['HDL-C'] = 1
    else:
        data['HDL-C'] = 0

    if ldl_kpi_percnt <= 0.5:
        data['LDL-C (Calculated)'] = 1
    else:
        data['LDL-C (Calculated)'] = 0

    if hgb_kpi_percnt <= 0.05:
        data['CBC_Hemoglobin'] = 1
    else:
        data['CBC_Hemoglobin'] = 0
    
    if ms_kpi_percnt <= 0.10:
        data['MS'] = 1
    else:
        data['MS'] = 0
    return data