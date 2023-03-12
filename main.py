from form_helper import FormHelper


def main():
    print("Welcome, please choose an action:")
    first_choice = True
    while True:
        try:
            choice = form_helper.get_user_choice(first_choice)
            if choice.name == "ImportForm":
                form_helper.import_form()
            elif choice.name == "FillForm":
                form_helper.fill_form()
            else:  # exit program option has been selected
                exit()
            first_choice = False
        except Exception as ex:
            print(f"{type(ex).__name__}: {ex}")


if __name__ == '__main__':
    form_helper = FormHelper()
    main()
