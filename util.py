import time
import sys

def type_yes_to_save(save_flag, scenarios):
    if save_flag:
        string_scenarios = [str(i)+"\n" for i in scenarios]
        console_input = input("This will overwrite the scenarios \n " + "".join(string_scenarios) + "\nDo you want to save the plots, tables, labels, captions? Type 'yes'")
        if console_input == "yes":
            save_flag = True
            print("##############Plots and tables will be saved.##############")
            print("##############Plots and tables will be saved.##############")
            print("##############Plots and tables will be saved.##############")
            print("##############Plots and tables will be saved.##############")
            print("##############Plots and tables will be saved.##############")
            # print count down in console to give time to abort
            print("Countdown to save: ")
            for i in range(5,0,-1):
                print(i)
                time.sleep(1)
                sys.stdout.write("\033[F")
        else:
            save_flag = False
            print("No plots and tables will be saved.")
    return save_flag