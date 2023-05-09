#!/usr/bin/env python
# coding: utf-8

# In[5]:


import openai
import csv
import pandas as pd
import re
import random
import connect



class ChatBot:
    def __init__(self):
        openai_api_key = connect.sky_v()
        self.gpt3_api_key = openai_api_key
        self.openai_api_key = openai_api_key
        self.prompts = {
            'ingredients': 'What are the ingredients for ',
            'recipe': 'Can you give me a recipe for ',
            'technique': 'What is the best technique for ',
            'tip': 'Do you have any tips for ',
            'cuisine': 'How do I make ',
            'how to prepare': 'How do I prepare ',
            'tell me how to': 'Tell me how to make '
        }
        self.cuisine_prompts = {
            'italian': 'How do I make an authentic Italian ',
            'japanese': 'What are the key ingredients for Japanese ',
            'mexican': 'Can you give me a recipe for Mexican ',
            'african': 'Can you give me a recipe for African ',
            'uk': 'Can you give me a recipe for UK ',
        }
        
        
      
    # Random greeting message for welcoming users.
      
    def greetings(self):
        greetings = ["Hi there!. I'm CookGenie", "Hi, I'm CookGenie!", "Hello!", "Welcome dear!", "Good to have you here!"]
        return random.choice(greetings)

    #  prompt the user to enter their first name.
    def prompt_for_name(self):
        prompts = ["Can I get your first name please?", "May I have your first name?", "What is your first name?", "Your first name please.", "What can I call you?"]
        return random.choice(prompts)

    # prompt for the user to enroll for cooking training.
    def prompt_to_enroll(self):
        prompts = ["Would you like to enroll for our cooking training?", "Would you want to register for our cooking training?", "Would you want to learn to cook?"]
        return random.choice(prompts)

    #  prompts the user to indicate whether they need assistance with a recipe, cooking technique or not. 
    def prompt_for_help(self):
        return "Would you like to get assistance with a recipe or cooking technique? (Enter 'recipe','technique' or 'no')"
        
    #prompts the user to indicate their preferred cuisine.
    def prompt_for_cuisine(self):
        return "What type of cuisine are you interested in? (Enter any country. eg=>  'italian', 'japanese', 'mexican', 'african', 'uk' or 'no preference')"

    #prompts user to provide their information for registration and returns a completion message.
    def enroll(self):
        email_address = input("CooKGenie: Please enter your email address: ")

        while not re.match(r"[^@]+@[^@]+\.[^@]+", email_address):
            email_address = input("Please enter a valid email address: ")
        else:
            first_name = input("Enter your first name:  ")
            surname = input("Enter your surname: ")
            phone_number = input("Enter your phone number: ")
            while len(phone_number) != 11:
                phone_number = input("Please enter a valid 11-digit phone number: ")
            enrollment_number = self.update_enrollment_csv(first_name, surname, email_address, phone_number)
        return f"CooKGenie: Your have successfully enrolled.\nYour enrolment number is {enrollment_number}.\nWe will contact you for the next step!"

      #Add  user's registered details to the database: enrollment.csv file.

    def update_enrollment_csv(self, first_name, surname, email_address, phone_number):
        fieldnames = ['enrollment_number', 'first_name', 'surname', 'email_address', 'phone_number']
        row = {'first_name': first_name, 'surname': surname, 'email_address': email_address, 'phone_number': phone_number}

        # Get the number of existing rows in the CSV file
        with open('enrollment.csv', mode='r') as enrollment_file:
            reader = csv.DictReader(enrollment_file)
            num_rows = sum(1 for row in reader)

        # Generate the new enrollment number
        enrollment_number = num_rows + 1
        row['enrollment_number'] = enrollment_number

        # Write the new row with the updated enrollment number
        with open('enrollment.csv', mode='a', newline='') as enrollment_file:
            writer = csv.DictWriter(enrollment_file, fieldnames=fieldnames)
            if enrollment_file.tell() == 0:
                writer.writeheader()
            writer.writerow(row)

        return enrollment_number

    
    
    #returns a list of possible user inputs indicating that they need assistance with cooking techniques.
    def technique_reply(self):
        reply = ['technique','food technique', 'I want food technique', 'I need food technique', 'give me food technique','food technique', 'technique please']
        return reply

    #returns a list of possible user inputs indicating that they need recipe recommendations.
    def recipe_reply(self):
        reply =['recipe', 'food recipe', 'I want to get food recipe', 'I need food recipe','give me food recipe','food recipe, please','recipe please']
        return reply

    # returns a list of possible user inputs indicating that they want to enroll for cooking training.
    def enrol_affirmation(self):
        reply = ['yes', 'yeah','yea','yah', 'certainly' 'sure', 'i want to register', 'i want to enroll', 'enroll me', 'enrol me','register now','ok', 'okey', 'alright', 'go on', 'yes please', 'yes, please', 'pls', 'yup', 'go', 'go ahead', 'right away'] 
        return reply

    # returns a list of possible user inputs indicating that the user does not want to enroll for cooking training.
    def enroll_rejection(self):
        reply = ['no', 'nope', 'nay', 'i dont', 'later', 'not interested', 'not sure', 'some day', 'not today', 'no please', 'no pls', 'nay nay', 'no, please', 'no, pls', 'not ready', 'not ready now', 'not yet', 'later', 'not now']
        return reply
    
    #returns a list of possible user inputs indicating that the user does not need assistance with a recipe or cooking techniq
    def help_reply(self):
        reply = ['no', 'nope', 'nay', 'i dont', 'later','thanks', 'no thanks', 'than you',"nothing else", "thanks for now", "no please", "no pls", "nay nay", "no, please", "no, pls", "later", "not now"]
        return reply

    #returns a random message to prompt the user to rephrase their input if it's not understood.
    def re_try(self):
        response = ["I'm sorry, I didn't understand your response. Please try again.", "Your response is not clear to me. can you rephrase it?"]
        return random.choice(response)
       
    #returns a random prompt to check if the user needs any further assistance.
    def anything_else(self):
        prompts = ["Okay, let me know if you need anything else!", "anything else?", "Do you need additonal help?"]
        return random.choice(prompts)
        
        
    def check_exit(self):
        """
        Checks if the user has entered an exit keyword and returns a boolean value to indicate whether to exit the chatbot or not.
        """
        exit_keywords = ['exit', 'bye', 'see you later', 'bye bye', 'goodbye']
        if input_text.lower() in exit_keywords:
            return True
        else:
            return False
     
        
    def generate_recipe_response(self, cuisine):
        """
        Generates a recipe response given a cuisine type and dish name.

        Args:
            cuisine (str): A string indicating the cuisine type.

        Returns:
            str: A string representing the generated recipe, including ingredients and instructions.
        """
        # Get the dish name from user input
        dish = input("What dish would you like to make? ")

        # Get the prompt for the given cuisine type, or use a default prompt if not available
        prompt = self.cuisine_prompts.get(cuisine.lower(), "Can you give me a recipe for ")
        prompt += dish + "\n\n"


        # Use OpenAI's API to generate a recipe based on the given prompt
        try:
            openai.api_key = self.openai_api_key
            model_engine = "text-davinci-002"
            response = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                temperature=0.7,
                max_tokens=1024,
                n=1,
                stop=None,
                frequency_penalty=0,
                presence_penalty=0
            )
            recipe = response.choices[0].text.strip()
        except Exception as e:
            print(f"An error occurred while generating the recipe: {e}")
            return f"Sorry, an error occurred while generating the recipe for {dish}. Please try again later."

        # Parse the generated recipe into ingredients and instructions
        if recipe:
            recipe = recipe.replace("Recipe:", "")
            recipe = recipe.strip()
            recipe_list = recipe.split("\n")
            ingredients = []
            instructions = []
            for line in recipe_list:
                if line.startswith("*"):
                    ingredients.append(line.replace("*", "").strip())
                else:
                    instructions.append(line.strip())
            ingredients_str = "\n".join(ingredients)
            instructions_str = "\n".join(instructions)
            #print(f"Here are the ingredients and instructions for {dish}")
            output = f"Here are the ingredients  and instructions for {dish}\n{ingredients_str}\n{instructions_str}"
            
        else:
            output = f"Sorry, I couldn't find a recipe for {dish}."
        return output 

    def generate_technique_response(self, cuisine):
        """
        Generates a cooking technique response given a cuisine type and dish name.

        Args:
            cuisine (str): A string indicating the cuisine type.

        Returns:
            str: A string representing the generated cooking technique.
        """
        # Get the dish name from user input
        dish = input("What dish are you cooking? ")

        # Get the prompt for the given cuisine type, or use a default prompt if not available
        prompt = self.cuisine_prompts.get(cuisine.lower(), "Can you give me a technique for ")
        prompt += dish + "\n\n"

        # Use OpenAI's API to generate a cooking technique based on the given prompt
        try:
            openai.api_key = self.openai_api_key
            model_engine = "text-davinci-002"
            response = openai.Completion.create(
                engine=model_engine,
                prompt=prompt,
                temperature=0.7,
                max_tokens=1024,
                n=1,
                stop=None,
                frequency_penalty=0,
                presence_penalty=0
            )
            technique = response.choices[0].text.strip()
        except Exception as e:
            print(f"An error occurred while generating the cooking technique: {e}")
            return f"Sorry, an error occurred while generating the cooking technique for {dish}. Please try again later."

        # Format the generated text into a list of steps
        if technique:
            output = f"Here's a technique you can use for {dish}:\n{technique}"
        else:
            output = f"Sorry, I couldn't find a technique for {dish}."
        return output
    
 
        
    def ask_for_more(self):
        
        """
        This function asks the user if they need more help from the virtual cooking assistant, and provides appropriate 
        responses based on their input.

        Returns:
        - True if the user wants more help
        - False if the user doesn't want more help or if their input is unrecognized
        
        It also provide information about the CookGenie, including its developer  
        """
        
        
        while True:
            question = print("CooKGenie: Is there anything else I can help you with?")
            response = input("You: ").lower()
            if response in ['yes', 'yup', 'yeah', 'yea','yah', 'sure']:
                return True
            elif response in ['thank you', 'thanks', 'many thanks']:
                print("CooKGenie: You're welcome! I'm always here to help.")
            elif response in ['bye', 'exit', 'that is it for now', 'nothing']:
                print("CooKGenie: Okay, goodbye! Have a nice day!")
                return False
            elif response in ['tell me about yourself', 'who are you?', 'what is your name?', 'explain yourself', 'introduce your self']:
                print("CooKGenie: I am CooKGenie - a virtual cooking assistant.\nI was created as a course project by a group of 3 Solent Universty students: Othniel, Rudolf and Eze\nI was trained on a dataset of billions of information related to cooking.\nI can provide you with recipes and techniques for cooking different dishes, and I can also help you enroll in cooking training if you're interested in improving your skills.\nAll you have to do is tell me what food recipe or techniques you're looking for, and I will provide you with the information you need.\nThink of it like having a personal cooking coach that you can access anytime, anywhere.\nWhether you're a beginner or an experienced cook, I was designed to make your cooking journey easier and more enjoyable.")
            elif response in ['who made you?', 'who developed you?', 'who created you?']:
                print("CooKGenie: I was created as a course project by a group of 3 Solent Universty students: Othniel, Rudolf and Eze.\nI was trained on a dataset of billions of information related to cooking.")
            elif response in ['what can you do?', 'what are your features?', 'what are your functionalities?']:
                print("CooKGenie: I can provide you with recipes and techniques for cooking different dishes, and I can also help you enroll in cooking training if you're interested in improving your skills.\nAll you have to do is tell me what food recipe or techniques you're looking for, and I will provide you with the information you need.\nThink of it like having a personal cooking coach that you can access anytime, anywhere.\nWhether you're a beginner or an experienced cook, I was designed to make your cooking journey easier and more enjoyable.")
            else:
                continue






# In[ ]:



