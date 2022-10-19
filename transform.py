import pandas as pd

def list2df(rules):
    rules_pd = pd.DataFrame(rules, columns=['antecedents', 'consequents', 'confidence'])
    rules_pd['antecedents'] = rules_pd['antecedents'].map(lambda x: str(x)[12:-3])
    rules_pd['consequents'] = rules_pd['consequents'].map(lambda x: str(x)[12:-3])
    rules_pd['confidence'] = rules_pd['confidence'].map(lambda x: round(x, 4))
    return rules_pd