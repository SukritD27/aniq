import numpy as np
import matplotlib.pyplot as plt  # For visualization (optional)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import scipy.stats as stats
import utilities.weather_api
import utilities.chat




from enum import Enum

# get whether question falls under linear-regression, chi-square tesing, t-testing. 

# given the following row column data 


def linear_regression(x: list, y: list):
    x = np.array(x).reshape(-1, 1)
    y= np.array(y)
    x = np.array(x).reshape(-1, 1)
    y= np.array(y)
    model = LinearRegression()
    model.fit(X=x, y=y)
    y_predicted = model.predict(X=x)
    
    mse = mean_squared_error(y, y_predicted)
    print("Mean Squared Error:", mse)
    
    r2 = r2_score(y, y_predicted)
    print("R-squared:", r2)
    
    plt.scatter(x, y, color='blue', label='Actual Data')
    plt.plot(x, y_predicted, color='red', label='Predicted Data')
   

    linear_return ={
        "Mean-squared error": mse,
        "R-squared": r2
    }
    
    return str(linear_return)

def chi_square_testing(x: list, y: list):
    observed_table = np.array([
      x, y
    ])

    # Perform the chi-square test
    chi2, pval, dof, expected = stats.chi2_contingency(observed_table)

    # Interpretation (assuming p-value < 0.05)
    print("Chi-Square Statistic:", chi2)
    print("p-value:", pval)
    print("Degrees of Freedom:", dof)
    print("There is a statistically significant association between the variables (p-value < 0.05).")

    chi2_return = {
        "Chi-squared statistic": chi2,
        "P-value": pval,
        "Degrees of freedom": dof
    }
    return str(chi2_return)
    
    
    
    
def t_testing(x: list, y: list):
    # Sample data
    group1 = np.array(x)
    group2 = np.array(y)

    # Perform the t-test
    result = stats.ttest_ind(group1, group2)
    tstat = result.statistic
    pval = result.pvalue
    dof = result.df

    # Interpretation (assuming p-value < 0.05)
    print("t-statistic:", tstat)
    print("p-value:", pval)
    print("Degrees of freedom:", dof)
    print("There is a statistically significant difference between the means (p-value < 0.05).")

    t_return = {
        "T-statistic": tstat,
        "P-value": pval,
        "Degrees of freedom": dof
    }
    

    return str(t_return)
    

class HypothesisTestType(Enum):
    LINEAR_REGRESSION = linear_regression
    CHI_SQUARE_TESTING = chi_square_testing
    T_TEST = t_testing

def getAnswer(question: str) -> str:
    test_type_string = utilities.chat.testType(question).lower()
    test_type = HypothesisTestType.T_TEST
    
    if test_type_string == "linear regression".lower():
        test_type = HypothesisTestType.LINEAR_REGRESSION
    if test_type_string == "chi square testing":
        test_type = HypothesisTestType.CHI_SQUARE_TESTING
    if test_type_string == "T test":
        test_type = HypothesisTestType.T_TEST
    if test_type_string == "none":
        return {}
        
    fields = utilities.chat.column_to_use(question,test_type_string, utilities.weather_api.hourly_dataframe.keys().to_list())

    summary_p1 = test_type(utilities.weather_api.hourly_dataframe[fields[0]].to_list(), utilities.weather_api.hourly_dataframe[fields[1]].to_list() )
    
    summary_of = utilities.chat.summarize(test_type_string, summary_p1, question)
    
    return summary_of
