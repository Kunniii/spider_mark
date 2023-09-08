import pandas as pd
from os import listdir
from os.path import abspath, join
from DataProcessor import Processor

processor = Processor("./data.csv")

ignores = ("OJS", "VOV", "GDQP", "LAB", "ENT", "SSS", "ĐNH", "OJT", "OJB")

header = ["MSSV", "Ho va Ten", "GPA", "Total Credits"]
data = []

for file in listdir(abspath("./downloads")):
    mssv = file.split("_")[-1].split(".")[0]
    try:
        full_path = abspath(join("./downloads", file))
        gpa, total_credit = processor.calc_gpa(
            full_path, make_sure_all_passed=True, ignore=ignores
        )
        sv = processor.lookup_by_roll_number(mssv)
        data.append([mssv, sv.get("Fullname"), gpa, total_credit])
    except:
        print(f"{mssv} does not qualified!")

pd.DataFrame(data, columns=header).to_excel(abspath("./gpa.xlsx"), index=False)
