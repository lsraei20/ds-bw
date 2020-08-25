# import pandas as pd
#
# response = json = {
#     'title': 'Water bike',
#     'blurb': 'A bike that floats',
#     'goal': '5000',
#     'launch_date': '08/06/2020',
#     'deadline': '10/20/2020',
#     'category': 'sports'
# }
#
#
# def prep_data(response):
#     df = pd.DataFrame([dict(response)])
#     df['title'] = df['title'].astype(str)
#     df['blurb'] = df['blurb'].astype(str)
#     df['category'] = df['category'].astype(str)
#     df['goal'] = df['goal'].astype(int)
#     df['launch_date'] = pd.to_datetime(df['launch_date'], format='%m/%d/%Y')
#     df['deadline'] = pd.to_datetime(df['deadline'], format='%m/%d/%Y')
#     return df
#
#
# df = prep_data(response)
#
# print(df.dtypes)


