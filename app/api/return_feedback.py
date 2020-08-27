"""Returns feedback to the user based on other successful kickstarters"""
import pandas as pd


def feedback(df):
    # Title feedback
    if len(df.loc[0, 'title']) > 45:
        title_feedback = "Hmm. You should remove some words from the title, it is quite " \
                         "longer than most winning campaigns."
    elif len(df.loc[0, 'title']) < 35:
        title_feedback = "Your title is shorter than the average successful campaign," \
                         " you should try adding to it!"
    else:
        title_feedback = "Your title looks great!"

    # Description feedback
    if len(df.loc[0, 'description']) > 140:
        description_feedback = "Uh oh. Your bio is longer than the average successful" \
                               " Kickstarter. We found it can be the most important " \
                               "section to your success!"
    elif len(df.loc[0, 'description']) < 110:
        description_feedback = "Can you say a bit more? Most winning Kickstarter's " \
                               "have a longer bio, and we found it can be the most " \
                               "important section to your success!"
    else:
        description_feedback = "Perfect bio!"

    # Campaign length feedback
    def campaign_len(df):
        df['finish_date'] = df['finish_date']
        df['launch_date'] = df['launch_date']
        df['finish_date'] = pd.to_datetime(df['finish_date'], format="%Y/%m/%d")
        df['launch_date'] = pd.to_datetime(df['launch_date'], format="%Y/%m/%d")
        # create new column
        df['cam_length'] = df['finish_date'] - df['launch_date']
        return df

    # tes = campaign_len(df)
    campaign_len_feedback = 'yes'
    if campaign_len(df)['cam_length'].mean().days > 37:
        campaign_len_feedback = "Your campaign lasts quite longer than most winning" \
                                " campaigns. Believe it or not a shorter campaign can" \
                                " actually increase your funding!"
    elif campaign_len(df)['cam_length'].mean().days < 27:
        campaign_len_feedback = "Some more time perhaps? your campaign is quite " \
                                "shorter than most successful campaigns. You should" \
                                " consider giving people more time to fund! good: " \
                                "Your campaign length is right in line with the most " \
                                "successful Kickstarters!"
    else:
        campaign_len_feedback = "Your campaign length is right in line with the most " \
                                "successful Kickstarters!"

    # Monetary goal feedback
    if df.loc[0, 'monetary_goal'] > 6000:
        monetary_feedback = "Your goal is higher than most successful campaigns. You " \
                            "should consider lowering it for more chances of success. " \
                            "(keep in mind this is just a suggestion and there are a " \
                            "lot of other variables like the nature of your product)"
    elif df.loc[0, 'monetary_goal'] < 4000:
        monetary_feedback = "Your goal is lower than average for successful campaigns." \
                            " Why not bump it up a bit? (keep in mind this is just a " \
                            "suggestion and there are a lot of other variables like " \
                            "the nature of your product)"
    else:
        monetary_feedback = "Your goal is right in line with successful campaigns " \
                            "like yours! (keep in mind this is just a suggestion and " \
                            "there are a lot of other variables like the nature of " \
                            "your product)"

    # Release month feedback
    month_proba_dic = {1: 0.35793357933579334,
                       2: 0.34205933682373474,
                       3: 0.36556603773584906,
                       4: 0.3522012578616352,
                       5: 0.41466957153231665,
                       6: 0.3893499308437068,
                       7: 0.3267080745341615,
                       8: 0.34620786516853935,
                       9: 0.34942528735632183,
                       10: 0.3561643835616438,
                       11: 0.3744740532959327,
                       12: 0.3109815354713314}

    if month_proba_dic[df.loc[0, "launch_date"].month] < \
       month_proba_dic[df.loc[0, "launch_date"].month + 1]:
        month_launched_feedback = "By looking at other posts like yours, we detected " \
                                  "that the chances of your Kickstarter success may be " \
                                  "higher if you wait to post next month. Something to" \
                                  " think about!"
    else:
        month_launched_feedback = "You picked a great time to post! This month gives you " \
                                  "the greatest chances of success when compared to next" \
                                  " month, so get posting!"

    return monetary_feedback, title_feedback, description_feedback, campaign_len_feedback, month_launched_feedback
