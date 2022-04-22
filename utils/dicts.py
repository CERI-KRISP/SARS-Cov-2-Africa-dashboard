##### Palette colors #####
main_lineages_color_scheme = {'A': '#6c483a', 'A.23.1': '#9f8377',
                              # more: https://coolors.co/6c483a-9f8377-aea198-b9b8ae-cdcfc8
                              'B.1': '#586f6b', 'B.1.1': '#7f9183', 'B.1.1.1': '#b8b8aa', 'B.1.1.318/AZ.x': '#cfc0bd',
                              'B.1.16': '#DDD5D0',
                              'B.1.1.448': '#d4baca', 'B.1.1.54': '#e69ac8', 'B.1.1.529 (Omicron)': '#e83368',  # pink
                              'Omicron': '#e83368',
                              'B.1.1.7 (Alpha)': '#696969', 'Alpha': '#696969',
                              # more: https://coolors.co/696969-c9c9c9 grey
                              'B.1.237': '#faf0ca', 'B.1.351 (Beta)': '#ffe45e', 'Beta': '#ffe45e',
                              'B.1.351': '#ffe45e',  # yellow
                              'B.1.525 (Eta)': '#cdb4db', 'B.1.540': '#c7e8f3', 'B.1.549': '#FFDDD2',
                              'B.1.617.2/AY.x (Delta)': '#2a9d8f', 'Delta': '#2a9d8f',
                              'C.1/C.1.1/C.1.2': '#0D5789', 'C.16': '#3B98C6', 'C.36/C.36.3': '#3B98C6',
                              # more: https://coolors.co/0d5789-3b98c6-edf6f9-ffddd2-e29578
                              'Other Lineages': '#EDF6F9',
                              'Gamma': '#E29578'
                              }
##### Dictionary to convert names of variants #####
variant_names = {'B.1.1.7': 'Alpha', 'B.1.1.7 (Alpha)': 'Alpha',
                 'VOC Alpha GRY (B.1.1.7+Q.*) first detected in the UK': 'Alpha',
                 'B.1.351': 'Beta', 'B.1.351.2': 'Beta', 'B.1.351.3': 'Beta', 'B.1.351 (Beta)': 'Beta',
                 'VOC Beta GH/501Y.V2 (B.1.351+B.1.351.2+B.1.351.3) first detected in South Africa': 'Beta',
                 'P.1': 'Gamma', 'P.1.1': 'Gamma',
                 'VOC Gamma GR/501Y.V3 (P.1+P.1.*) first detected in Brazil/Japan': 'Gamma',
                 'B.1.617.2/AY.x': 'Delta', 'B.1.617.2': 'Delta', 'B.1.617.2/AY.x (Delta)': 'Delta',
                 'VOC Delta GK (B.1.617.2+AY.*) first detected in India': 'Delta',
                 'B.1.525 (Eta)': 'B.1.525', 'B.1.1.529 (Omicron)': 'Omicron',
                 'B.1.1.529': 'Omicron', 'BA.1': 'Omicron', 'BA.1.1': 'Omicron',
                 'BA.1.1.11': 'Omicron', 'BA.1.15': 'Omicron',
                 'BA.2': 'Omicron', 'BA.3': 'Omicron', 'BA.1.1.1': 'Omicron', 'BA.1.1.4': 'Omicron', 'BA.1.1.6': 'Omicron',
                 'BA.1.1.9': 'Omicron', 'BA.1.17.2': 'Omicron', 'BA.1.18': 'Omicron', 'BA.1.14': 'Omicron',
                 'BA.1.13': 'Omicron', 'BA.1.17': 'Omicron', 'BA.1.1.14': 'Omicron', 'BA.1.16': 'Omicron',
                 'VOC Omicron GRA (B.1.1.529+BA.*) first detected in Botswana/Hong Kong/South Africa': 'Omicron'}

# Concerned variants based on WHO Feb 16
concerned_variants = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Omicron', 'Other Lineages']

# Variant cutoffs (based on first importated data from Pango Report)
variant_cutoffs = {"Alpha": "2020-09-03", "Beta": "2020-09-01", "Gamma": "2020-10-01", "Delta": "2021-03-01",
                   "Omicron": "2021-10-07", "Other Lineages": ""}

###### Dictionary to standardize duplicated countries ####
standardize_country_names = {'Republic of Burundi': 'Burundi', 'Republic of Cameroon': 'Cameroon',
                             'Republic of Chad': 'Chad', 'Republic of Equatorial Guinea': 'Equatorial Guinea',
                             'Gabonese Republic': 'Gabon',
                             'Democratic Republic of São Tomé and Principe': 'São Tomé and Principe',
                             'Union of the Comoros': 'Comoros', 'Republic of Djibouti': 'Djibouti',
                             'State of Eritrea': 'Eritrea', 'Federal Democratic Republic of Ethiopia': 'Ethiopia',
                             'Republic of Kenya': 'Kenya', 'Republic of Madagascar': 'Madagascar',
                             'Republic of Mauritius': 'Mauritius', 'Republic of Rwanda': 'Rwanda',
                             'Republic of Seychelles': 'Seychelles', 'Federal Republic of Somalia': 'Somalia',
                             'Republic of Sudan': 'Sudan', 'Republic of South Sudan': 'South Sudan',
                             'United Republic of Tanzania': 'Tanzania', 'Republic of Uganda': 'Uganda',
                             'Peoples Republic of Algeria': 'Algeria', 'Arab Republic of Egypt': 'Egypt',
                             'State of Libya': 'Libya', 'Islamic Republic of Mauritania': 'Mauritania',
                             'Kingdom of Morocco': 'Morocco', 'Republic of Tunisia': 'Tunisia',
                             'Republic of Angola': 'Angola', 'Republic of Botswana': 'Botswana',
                             'Kingdom of eSwatini': 'eSwatini', 'Swaziland': 'eSwatini',
                             'Kingdom of Lesotho': 'Lesotho',
                             'Republic of Malawi': 'Malawi', 'Republic of Mozambique': 'Mozambique',
                             'Republic of Namibia': 'Namibia', 'Republic of South Africa': 'South Africa',
                             'Republic of Zambia': 'Zambia', 'Republic of Zimbabwe': 'Zimbabwe',
                             'Republic of Benin': 'Benin', 'Cape Verde': 'Cabo Verde',
                             'Republic of Cabo Verde': 'Cabo Verde',
                             'Republic of Côte d\'Ivoire': 'Cote d\'Ivoire', 'Ivory Coast': 'Cote d\'Ivoire',
                             'Republic of Gambia': 'Gambia',
                             'Republic of Ghana': 'Ghana', 'Republic of Guinea': 'Guinea',
                             'Republic of Guinea-Bissau': 'Guinea-Bissau', 'Republic of Liberia': 'Liberia',
                             'Republic of Mali': 'Mali',
                             'Republic of Niger': 'Niger', 'Federal Republic of Nigeria': 'Nigeria',
                             'Republic of Senegal': 'Senegal',
                             'Republic of Sierra Leone': 'Sierra Leone', 'Togolese': 'Togo',
                             'Togolese Republic': 'Togo', 'La Reunion': 'Reunion',
                             'DR Congo': 'Democratic Republic of the Congo', 'Congo':'Republic of the Congo'}

###### Dictionary to select countries per region ####
countries_regions = {'Central Africa': {'Burundi', 'Cameroon', 'Central African Republic', 'Chad',
                                        'Republic of the Congo', 'Democratic Republic of the Congo',
                                        'Equatorial Guinea', 'Gabon', 'São Tomé and Principe'},
                     'Eastern Africa': {'Comoros', 'Djibouti', 'Eritrea', 'Ethiopia', 'Kenya', 'Madagascar',
                                        'Mauritius', 'Rwanda', 'Seychelles', 'Somalia', 'Sudan', 'South Sudan',
                                        'Tanzania',
                                        'Uganda'},
                     'Northern Africa': {'Algeria', 'Egypt', 'Libya', 'Mauritania', 'Morocco', 'Sahrawi', 'Tunisia'},
                     'Southern Africa': {'Angola', 'Botswana', 'eSwatini', 'Lesotho', 'Malawi', 'Mozambique', 'Namibia',
                                         'South Africa', 'Zambia', 'Zimbabwe'},
                     'Western Africa': {'Benin', 'Burkina Faso', 'Cabo Verde', 'Côte d\'Ivoire', 'Gambia', 'Ghana',
                                        'Guinea', 'Guinea-Bissau', 'Liberia', 'Mali', 'Niger', 'Nigeria', 'Senegal',
                                        'Sierra Leone', 'Togo'},
                     'Dependencies in Africa': {'Reunion', 'Western Sahara', 'Mayotte', 'Saint Helena'}}

missing_country_codes = {'Guinea-Bissau': 'GNB', 'Mauritius': 'MUS', 'Republic of the Congo': 'COG', 'Reunion': 'REU',
                         'Seychelles': 'SYC', 'Mayotte': 'MYT', 'Cabo Verde': 'CPV', "Cote d'Ivoire": 'CIV',
                         'Eswatini': 'SWZ', 'Tanzania': 'TZA', 'South Sudan': 'SSD'}

vocs_color_pallet = {'Alpha': 'Greys', 'Beta': 'YlOrBr', 'Gamma': 'Oranges', 'Delta': 'algae', 'Omicron': 'RdPu',
                     'Other Lineages': 'Blues'}
