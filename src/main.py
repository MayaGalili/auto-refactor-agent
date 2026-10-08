from analyzer import AutoRefactorTool

def main(code_base):
    print(f"Starting Code Base analyzing for code base:\n {code_base}")
    AutoRefactorTool(code_base).run()
    print("The code base analysis is done!")



if __name__ == "__main__":
    # code_base = input("please place here your codebase path for analysis:\n")
    
    code_base = "/Users/maya/projects/LeetCodeSolutions"
    main(code_base)