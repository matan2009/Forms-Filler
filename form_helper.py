import json
import os

from action_choice import ActionChoice


class FormHelper:

    def __init__(self):
        self.exported_forms_path = "./exported_forms/"
        self.filled_forms_path = "./filled_forms/"

    @staticmethod
    def validate_user_choice(num_of_forms: int = 0) -> int or ActionChoice:
        while True:
            try:
                user_choice = int(input())
                if num_of_forms:
                    user_choice_list = []
                    for index in range(num_of_forms):
                        user_choice_list.append(index + 1)
                    if user_choice not in user_choice_list:
                        raise ValueError("Invalid input. Please try again.")
                    return user_choice
                else:
                    if user_choice not in [1, 2, 3]:
                        raise ValueError("Invalid input. Please try again.")
                return ActionChoice(user_choice)
            except Exception as ex:
                print(f"{type(ex).__name__}: {ex}")

    @staticmethod
    def validate_form_path(form_path: str):
        if not isinstance(form_path, str):
            raise ValueError
        if not os.path.exists(form_path):
            raise ValueError("Form cannot be found. Please try again")
        split_form_name = os.path.splitext(form_path)
        form_name_extension = split_form_name[1]
        if not form_name_extension == ".json":
            raise ValueError("This form is not a json file. Please try again")

    @staticmethod
    def extract_options(question: str) -> list:
        parts = question.split("(options:")
        options = parts[1].replace(")", "").strip()
        option_list = options.split(", ")
        return option_list

    def get_user_choice(self, first_choice: bool) -> int or ActionChoice:
        if not first_choice:
            print("please choose an action:")
        print("1. import a form")
        print("2. fill in a form")
        print("3. exit program")
        user_choice = self.validate_user_choice()
        return user_choice

    def import_form(self):
        while True:
            try:
                form_path = input("please enter the form path: ")
                self.validate_form_path(form_path)
                with open(form_path, 'r') as imported_form:
                    imported_data = json.load(imported_form)
                if not os.path.exists(self.exported_forms_path):
                    os.mkdir(self.exported_forms_path)
                file_name = os.path.basename(form_path)
                with open(self.exported_forms_path + file_name, 'w') as exported_form:
                    json.dump(imported_data, exported_form)
                print("form imported successfully")
                return

            except Exception as ex:
                print(f"{type(ex).__name__}: {ex}")

    def validate_forms(self) -> list:
        if not os.path.exists(self.exported_forms_path):
            raise ValueError("Before fill in a form, you must import it first")
        forms = os.listdir(self.exported_forms_path)
        if not forms:
            raise ValueError("Before fill in a form, you must import it first")
        return forms

    def validate_answer(self, question: str, answer: str):
        options = self.extract_options(question)
        if answer not in options:
            raise ValueError("Invalid input. Please try again.")

    def export_filled_form(self, selected_form_name: str, filled_form: dict):
        if not os.path.exists(self.filled_forms_path):
            os.mkdir(self.filled_forms_path)
        with open(self.filled_forms_path + selected_form_name + ".json", 'w') as complete_form:
            json.dump(filled_form, complete_form)
        print("Thank you for filling the form! Here is the filled form:")
        print(filled_form)

    def get_form_answers(self, imported_data: dict) -> dict:
        first_question, main_answer = True, None
        filled_form = {}
        while True:
            if first_question:
                try:
                    main_question = imported_data["question"]
                    main_answer = input(main_question)
                    self.validate_answer(main_question, main_answer)
                    filled_form.update({main_question: main_answer})
                except Exception as ex:
                    print(f"{type(ex).__name__}: {ex}")
                    continue

            first_question = False
            try:
                question = imported_data[main_answer]
                answer = input(question)
                self.validate_answer(question, answer)
                filled_form.update({question: answer})
            except Exception as ex:
                print(f"{type(ex).__name__}: {ex}")
                continue
            return filled_form

    def fill_form(self):
        forms = self.validate_forms()
        forms_mapping = {}
        print("choose a form: ")
        for index, form in enumerate(forms):
            split_form_name = os.path.splitext(form)
            form_name = split_form_name[0]
            forms_mapping.update({index + 1: form_name})
            print(str(index + 1) + ". " + form_name)
        num_of_forms = len(forms)
        user_choice = self.validate_user_choice(num_of_forms)
        selected_form_name = forms_mapping[user_choice]
        print(f"the selected form is: {selected_form_name}")
        selected_form_path = self.exported_forms_path + selected_form_name + ".json"
        with open(selected_form_path, 'r') as imported_form:
            imported_data = json.load(imported_form)
        filled_form = self.get_form_answers(imported_data)
        self.export_filled_form(selected_form_name, filled_form)
