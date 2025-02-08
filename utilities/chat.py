from urllib import response
from openai import OpenAI
import os
from dotenv import load_dotenv

import json

load_dotenv()

client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))

# Have to still know what to return but works for the most part
def testType(prompt):
    print("prompt:", prompt)
    completion = client.chat.completions.create(
    model="gpt-4-turbo",
    response_format = {"type": "json_object"},
    messages=[
        {"role": "system", "content": "You are a data analyst assistant designed to output JSON."},
        {"role": "user", "content": "Hello! For the following question: \n" + prompt + "\n Tell me should I perform linear regression, T test, or chi square testing to find the anwer in the prompt?"}
    ]
    )

    response = completion.choices[0].message.content
    json_dict = json.loads(response)
    first_key = next(iter(json_dict))
    testT = json_dict[first_key]


    print(testT)
    
    return testT

    # for test_type in HypothesisTestType:
    #     if test_type.value == testT:
    #         return test_type

    # return "Nothing found!"

# Confused about what is data type and therefore what to look for in response
def column_to_use(data, test_type, columns):
    n = 0
    if test_type == 't_testing':
        n = 2
    elif test_type == 'linear_regression':
        n = 2
    elif test_type == 'chi_square_testing':
        n = 2
    
    
    completion = client.chat.completions.create(
    model="gpt-4-turbo",
    response_format = {"type": "json_object"},
    messages=[
        {"role": "system", "content": "You are a data analyst assistant designed to output JSON."},
        {"role": "user", "content": "Given these following column values" + " ".join(columns) + ". Insert only " + str(n) + " column values into selected_columns that I should use in order to do " + test_type + " on the following data: \n"+ data + " The entered columns should be different and not only by measurement like o to 3cm"}
    ]
    )

    response = completion.choices[0].message.content

    print("RESPONSE Colunmsssss:", response)
    json_dict = json.loads(response)
    return json_dict["selected_columns"]

# I think should work
# Need to test with a sample question  
def summarize(test_type: str, number_summary: str, question: str) -> str:
    completion = client.chat.completions.create(
    model="gpt-4-turbo",
    response_format = {"type": "json_object"},
    messages=[
        {"role": "system", "content": "You are a data analyst assistant designed to output JSON."},
       {"role": "user", "content": "Given the following test type of " + test_type + "the number summary" + number_summary + "Summarize what this means in terms of the question " + question + ". Include this summary in the JSON with the field named summary. Also return major takeaways in field major_takeaways and issues in field issues that might occur when comparing the values. All the values for the JSON fields should be strings."}
    ]
    )

    response = completion.choices[0].message.content
    # json_dict = json.loads(response)
    # first_key = next(iter(json_dict))
    # num = json_dict[first_key]

    print("RESPONSE SUMMARRYYYYYY", response)
    json_dict = json.loads(response)
    str1 = json_dict["summary"]
    str2 = json_dict["major_takeaways"]    
    str3 = json_dict["issues"]
    return "Summary: " + str1+ "\nMajor Takeaways: " +str2+ "\nIssues Possible: "+str3

    # print("ANALYSIS METHOD: ", num)
    # return num

# print("TEST TYPE FOUND: ", testType("What is the relationship between wind direction 180m and soil temperature 0cm?"))