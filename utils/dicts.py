##### Palette colors #####
main_lineages_color_scheme = {'A': '#6c483a', 'A.23.1': '#9f8377',
                              # more: https://coolors.co/6c483a-9f8377-aea198-b9b8ae-cdcfc8
                              'B.1': '#586f6b', 'B.1.1': '#7f9183', 'B.1.1.1': '#b8b8aa', 'B.1.1.318/AZ.x': '#cfc0bd',
                              'B.1.16': '#DDD5D0',
                              'B.1.1.448': '#d4baca', 'B.1.1.54': '#e69ac8', 'B.1.1.529 (Omicron)': '#e83368',  # pink
                              'Omicron': '#e83368',
                              'B.1.1.7 (Alpha)': '#696969', 'Alpha': '#696969', # more: https://coolors.co/696969-c9c9c9 grey
                              'B.1.237': '#faf0ca', 'B.1.351 (Beta)': '#ffe45e', 'Beta': '#ffe45e', 'B.1.351': '#ffe45e',  # yellow
                              'B.1.525 (Eta)': '#cdb4db', 'B.1.540': '#c7e8f3', 'B.1.549': '#FFDDD2',
                              'B.1.617.2/AY.x (Delta)': '#2a9d8f', 'Delta':'#2a9d8f',
                              'C.1/C.1.1/C.1.2': '#0D5789', 'C.16': '#3B98C6', 'C.36/C.36.3': '#3B98C6',
                              # more: https://coolors.co/0d5789-3b98c6-edf6f9-ffddd2-e29578
                              'Other Lineages': '#EDF6F9',
                              'Gamma': '#E29578'
                              }
##### Dictionary to convert names of variants #####
variant_names = {'B.1.1.7': 'Alpha', 'B.1.1.7 (Alpha)': 'Alpha',
                 'B.1.351': 'Beta', 'B.1.351.2': 'Beta', 'B.1.351.3': 'Beta', 'B.1.351 (Beta)': 'Beta',
                 'P.1': 'Gamma', 'P.1.1': 'Gamma',
                 'B.1.617.2/AY.x': 'Delta', 'B.1.617.2': 'Delta', 'B.1.617.2/AY.x (Delta)': 'Delta',
                 'B.1.525 (Eta)' : 'B.1.525', 'B.1.1.529 (Omicron)': 'Omicron',
                 'B.1.1.529':'Omicron', 'BA.1': 'Omicron', 'BA.1.1': 'Omicron', 'BA.2': 'Omicron', 'BA.3':'Omicron'}

# Concerned variants based on WHO Feb 16
concerned_variants = ['Alpha', 'Beta', 'Gamma', 'Delta', 'Omicron', 'Other Lineages']

###### Dictionary to select countries per region ####
countries_regions = {'Central Africa': {'Burundi', 'Cameroon', 'Central African Republic', 'Republic of Chad',
                                        'Republic of Congo', 'Democratic Republic of Congo',
                                        'Republic of Equatorial Guinea', 'Gabonese Republic', 'São Tomé and Principe'},
                     'Eastern Africa': {'Comoros', 'Djibouti', 'State of Eritrea', 'Ethiopia', 'Kenya', 'Madagascar',
                                        'Mauritius', 'Rwanda', 'Seychelles', 'Somalia', 'Sudan', 'South Sudan',
                                        'Tanzania',
                                        'Uganda'},
                     'Northern Africa': {'Algeria', 'Egypt', 'Libya', 'Mauritania', 'Morocco', 'Sahrawi', 'Tunisia'},
                     'Southern Africa': {'Angola', 'Botswana', 'Eswatini', 'Lesotho', 'Malawi', 'Mozambique', 'Namibia',
                                         'South Africa', 'Zambia', 'Zimbabwe'},
                     'Western Africa': {'Benin', 'Faso', 'Cabo Verde', 'Côte d\'Ivoire', 'Gambia', 'Ghana', 'Guinea',
                                        'Guinea Bissau', 'Liberia', 'Mali', 'Niger', 'Nigeria', 'Senegal',
                                        'Sierra Leone',
                                        'Togolese'}}