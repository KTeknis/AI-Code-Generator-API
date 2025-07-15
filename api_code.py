from flask import *
import pandas as pd
from google import genai
from google.genai import types

app = Flask(__name__)

@app.route("/")
def home():
    try:
        key = open("api_key.txt").read()
        api_check = key
    except:
        api_check = "Not yet Inputted"

    try:
        intro = open("Intro.txt").read()
    except:
        intro_check = "Not yet created."
    else:
        intro_check = "Available"

    try:
        analysis_steps_txt = open("analysis_steps.txt")
    except:
        analysis_check = "Not yet created."
    else:
        analysis_check = "Available"

    try:
        step_1_txt = open("step_1.py")
    except:
        step_1_check = "Not yet created."
    else:
        step_1_check = "Available"    
    
    try:
        step_2_txt = open("step_2.py")
    except:
        step_2_check = "Not yet created."
    else:
        step_2_check = "Available"

    try:
        step_3_txt = open("step_3.py")
    except:
        step_3_check = "Not yet created."
    else:
        step_3_check = "Available"

    try:
        step_4_txt = open("step_4.py")
    except:
        step_4_check = "Not yet created."
    else:
        step_4_check = "Available"

    try:
        step_final_txt = open("step_final.py")
    except:
        step_final_check = "Not yet created."
    else:
        step_final_check = "Available"

    try:
        data = pd.read_csv("data.csv", delimiter = ",")
    except:
        return render_template('home_b.html', apicheck = api_check, introcheck = intro_check, analysischeck = analysis_check, step_1check = step_1_check, step_2check = step_2_check, step_3check = step_3_check, step_4check = step_4_check, step_finalcheck = step_final_check)
    else:
        return render_template('home_a.html', apicheck = api_check, tables=[data.to_html()], titles=[''], introcheck = intro_check, analysischeck = analysis_check, step_1check = step_1_check, step_2check = step_2_check, step_3check = step_3_check, step_4check = step_4_check, step_finalcheck = step_final_check)

@app.route('/api_setup', methods=['GET'])
def api_setup():
    target = request.args.get('target')
    if target is None:  # No number entered, show input form
        return render_template('api_form.html', message_text = "Input your Gemini AI API Key to be used for this API.")
    elif target.strip() == '':  # Empty input
        return render_template('api_form.html', message_text = "Please at least input SOMETHING.")
    try:
        client = genai.Client(api_key=target)
        chat = client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                tools=[types.Tool(code_execution=types.ToolCodeExecution)]
            ),
        )
        prompt = "Create a confirmation message that the API is working."
        analysis_ai = chat.send_message(prompt)
        with open("api_key.txt", "w") as f:
            f.write(target)

        return render_template('intro_ai.html', ai_text = "API is up and running!")
    except:
        return render_template('api_form.html', message_text = "An error has occured. Make sure the API Key is correct.")

@app.route('/intro_write', methods=['GET'])
def intro_write():
    target = request.args.get('target')
    if target is None:  # No number entered, show input form
        return render_template('target_form_intro.html', message_text = "Input the target variable to be predicted")
    elif target.strip() == '':  # Empty input
        return render_template('target_form_intro.html', message_text = "Please at least input SOMETHING.")
    try:
        data = pd.read_csv("data.csv", delimiter = ",")
        target_data = data[target]
        data_head = data.head(40)
        data_sample = data_head.to_string()

        api_key = open("api_key.txt").read()

        client = genai.Client(api_key=api_key)
        chat = client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                tools=[types.Tool(code_execution=types.ToolCodeExecution)]
            ),
        )
    
        prompt = "Make an introduction about analyzing and predicting the '"+target+"' feature based on the other features from the following data:\n" + data_sample
        analysis_ai = chat.send_message(prompt)
        with open("Intro.txt", "w") as f:
            f.write(analysis_ai.text)
        ai_result = analysis_ai.text
        return render_template('intro_ai.html', ai_text=ai_result)
    except:
        return render_template('target_form_intro.html', message_text = "An error has occured. Make sure the data is properly named (data.csv) and feature name is valid (It's Case-Sensitive!)")

@app.route('/intro_read')
def intro_read():
    try:
        ai_result = open("Intro.txt").read()
    except: 
        ai_result = "The Intro are not generated yet."
    return render_template('intro_ai.html', ai_text=ai_result)

@app.route('/analysis_steps', methods=['GET'])
def analysis_steps():
    target = request.args.get('target')
    if target is None:  # No number entered, show input form
        return render_template('target_form.html', message_text = "Input the target variable to be predicted")
    elif target.strip() == '':  # Empty input
        return render_template('target_form.html', message_text = "Please at least input SOMETHING.")
    try:
        data = pd.read_csv("data.csv", delimiter = ",")
        target_data = data[target]
        data_head = data.head(40)
        data_sample = data_head.to_string()

        api_key = open("api_key.txt").read()

        client = genai.Client(api_key=api_key)
        chat = client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                tools=[types.Tool(code_execution=types.ToolCodeExecution)]
            ),
        )
    
        prompt = "Provide 4 steps needed to analyze and predict the '"+target+"' feature from the following data, with the steps being, in order: Data Understanding and Preparation, Exploratory Data Analysis (EDA), Model Building and Evaluation, and Results and Interpretation. Do not generate or run any codes yet\n" + data_sample
        analysis_ai = chat.send_message(prompt)
        with open("analysis_steps.txt", "w") as f:
            f.write(analysis_ai.text)
        analysis_plan = analysis_ai.text
        return render_template('intro_ai.html', ai_text=analysis_plan)
    except:
        return render_template('target_form.html', message_text = "An error has occured. Make sure the data is properly named (data.csv) and feature name is valid (It's Case-Sensitive!)")

@app.route('/steps_read')
def steps_read():
    try:
        ai_result = open("analysis_steps.txt").read()
    except:
        ai_result = "The Analysis Steps are not generated yet."
    return render_template('intro_ai.html', ai_text=ai_result)

@app.route('/step_1_write')
def step_1_write():
    try:
        data = pd.read_csv("data.csv", delimiter = ",")
        data_head = data.head(40)
        data_sample = data_head.to_string()

        analysis_steps_string = open("analysis_steps.txt").read()

        api_key = open("api_key.txt").read()

        client = genai.Client(api_key=api_key)
        chat = client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                tools=[types.Tool(code_execution=types.ToolCodeExecution)]
            ),
        )
    
        prompt = "Run an executable code in python to create function named 'step_1_code' to perform the first step that is listed on the following text:\n"+analysis_steps_string+ "\nHowever, skip the load data part and assume the user have a data already loaded in pd.dataframe format. Use the following data as a sample to test the function.\n"+data_sample
        ai_result = chat.send_message(prompt)
        ai_message = ai_result.text
        ai_code = ai_result.executable_code
        with open("step_1.py", "w") as f:
            f.write(ai_code)
        return render_template('steps_template.html', message = ai_message, code = ai_code)
    except:
        return "An error has occured when generating the code."

@app.route('/steps_1_read')
def steps_1_read():
    ai_message = "Step 1"
    try:
        ai_code = open("step_1.py").read()
    except:
        ai_code = "This step hasn't been generated yet."
    return render_template('steps_template.html', message = ai_message, code = ai_code)

@app.route('/step_2_write')
def step_2_write():
    try:
        data = pd.read_csv("data.csv", delimiter = ",")
        data_head = data.head(40)
        data_sample = data_head.to_string()
        step_1_text = open("step_1.py").read()

        analysis_steps_string = open("analysis_steps.txt").read()

        api_key = open("api_key.txt").read()

        client = genai.Client(api_key=api_key)
        chat = client.chats.create(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                tools=[types.Tool(code_execution=types.ToolCodeExecution)]
            ),
        )
    
        prompt = "Run an executable code in python to create function named 'step_2_code' to perform the second step that is listed on the following text:\n"+analysis_steps_string+ "\nAssume that the user will use this function to analyze their own data. The following are the code used for the previous step:\n"+step_1_text+"\nUse the following data as a sample to test the function.\n"+data_sample
        ai_result= chat.send_message(prompt)
        ai_message = ai_result.text
        ai_code = ai_result.executable_code
        with open("step_2.py", "w") as f:
            f.write(ai_code)
        return render_template('steps_template.html', message = ai_message, code = ai_code)
    except:
        return "An error has occured when generating the code."

@app.route('/steps_2_read')
def steps_2_read():
    ai_message = "Step 2"
    try:
        ai_code = open("step_2.py").read()
    except:
        ai_code = "This step hasn't been generated yet."
    return render_template('steps_template.html', message = ai_message, code = ai_code)

@app.route('/step_3_write')
def step_3_write():
    data = pd.read_csv("data.csv", delimiter = ",")
    data_head = data.head(40)
    data_sample = data_head.to_string()
        
    step_1_text = open("step_1.py").read()
    step_2_text = open("step_2.py").read()

    analysis_steps_string = open("analysis_steps.txt").read()

    api_key = open("api_key.txt").read()

    client = genai.Client(api_key=api_key)
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            tools=[types.Tool(code_execution=types.ToolCodeExecution)]
        ),
    )
    
    prompt = "Run an executable code in python to create function named 'step_3_code' to perform the third step that is listed on the following text:\n"+analysis_steps_string+ "\nAssume that the user will use this function to analyze their own data. The following are the codes used for the previous step:\n"+step_1_text+"\n"+step_2_text+"\nUse the following data as a sample to test the function.\n"+data_sample
    ai_result= chat.send_message(prompt)
    ai_message = ai_result.text
    ai_code = ai_result.executable_code
    with open("step_3.py", "w") as f:
        f.write(ai_code)
    return render_template('steps_template.html', message = ai_message, code = ai_code)

@app.route('/steps_3_read')
def steps_3_read():
    ai_message = "Step 3"
    try:
        ai_code = open("step_3.py").read()
    except:
        ai_code = "This step hasn't been generated yet."
    return render_template('steps_template.html', message = ai_message, code = ai_code)

@app.route('/step_4_write')
def step_4_write():
    data = pd.read_csv("data.csv", delimiter = ",")
    data_head = data.head(40)
    data_sample = data_head.to_string()
        
    step_1_text = open("step_1.py").read()
    step_2_text = open("step_2.py").read()
    step_3_text = open("step_3.py").read()

    analysis_steps_string = open("analysis_steps.txt").read()

    api_key = open("api_key.txt").read()

    client = genai.Client(api_key=api_key)
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            tools=[types.Tool(code_execution=types.ToolCodeExecution)]
        ),
    )
    
    prompt = "perform the fourth step that listed on the following text:\n"+analysis_steps_string+ "\nIf necessary, generate and run an exectuable code to generate function named 'step_4_code' to perform the aformentioned step. Assume that the user will use this function to analyze their own data. The following are the code used for the previous steps:\n"+step_1_text+step_2_text+step_3_text+"\nUse the following data as a sample to perform said step.\n"+data_sample
    ai_result= chat.send_message(prompt)
    ai_message = ai_result.text
    ai_code = ai_result.executable_code
    with open("step_4.py", "w") as f:
        f.write(ai_code)
    with open("step_4_result.txt", "w") as f:
        f.write(ai_message)
    return render_template('steps_template.html', message = ai_message, code = ai_code)

@app.route('/steps_4_read')
def steps_4_read():
    try:
        ai_message = open("step_4_result.txt").read()
        ai_code = open("step_4.py").read()
    except:
        ai_message = "Step 4"
        ai_code = "This step hasn't been generated yet."
    return render_template('steps_template.html', message = ai_message, code = ai_code)
    
@app.route('/step_final_write')
def step_final_write():
    data = pd.read_csv("data.csv", delimiter = ",")
    data_head = data.head(40)
    data_sample = data_head.to_string()
        
    step_1_text = open("step_1.py").read()
    step_2_text = open("step_2.py").read()
    step_3_text = open("step_3.py").read()
    step_4_text = open("step_4.py").read()

    analysis_steps_string = open("analysis_steps.txt").read()

    api_key = open("api_key.txt").read()

    client = genai.Client(api_key=api_key)
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            tools=[types.Tool(code_execution=types.ToolCodeExecution)]
        ),
    )

    prompt = "Combine each of the following 'step_x_code' functions in the following codes into a single 'data_analysis' function to analyze and predict the data:\n"+step_1_text+step_2_text+step_3_text+step_4_text+"\nAssume that the user will use this function to analyze their own data. Use the following data as a sample to test the new function.\n"+data_sample
    ai_result= chat.send_message(prompt)
    ai_message = ai_result.text
    ai_code = ai_result.executable_code
    with open("step_final.py", "w") as f:
        f.write(ai_code)
    with open("step_final_result.txt", "w") as f:
        f.write(ai_message)
    return render_template('steps_template.html', message = ai_message, code = ai_code)

@app.route('/steps_final_read')
def steps_final_read():
    try:
        ai_message = open("step_final_result.txt").read()
        ai_code = open("step_final.py").read()
    except:
        ai_message = "Combined Steps"
        ai_code = "This step hasn't been generated yet."
    return render_template('steps_template.html', message = ai_message, code = ai_code)


if __name__ == "__main__":
    app.run(debug=True)