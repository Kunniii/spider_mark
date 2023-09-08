import pandas as pd
from os.path import abspath
from bs4 import BeautifulSoup
import re


class Processor:
    def __init__(self, file_path: str) -> None:
        self.file_path = abspath(file_path)
        self.master_df = pd.read_csv(self.file_path)
        self.header = self.master_df.columns.tolist()
        print(f"Loaded {file_path}")

    def filter(self, K: int, select: tuple) -> list:
        """
        Filter and select what data you need.

        Args:
            K (int): K14 K15 etc.
            select (tuple): What fields to select

        Returns:
            A list of filtered and selected data.

        Example:
            >>> filter(K=15, select=("Field1", "Filed2"))
            [["data1", "data2"], ["data3", "data4"]]

        """

        print("Filter started")

        pattern = "^C." + str(K) + "\d{4}$"

        filtered_df = self.master_df[
            self.master_df["RollNumber"].str.match(pattern, na=False)
        ]
        filtered_list = filtered_df.values.tolist()

        if select:
            selected_list = []
            field_index = []
            for field in select:
                field_index.append(self.header.index(field))
            for data in filtered_list:
                temp = []
                for index in field_index:
                    temp.append(data[index])
                selected_list.append(temp)
            return selected_list
        else:
            return filtered_list

    def lookup_by_roll_number(self, roll_number: str) -> dict:
        for row in self.master_df.itertuples():
            if row.RollNumber == roll_number:
                return {
                    "RollNumber": row.RollNumber,
                    "MemberCode": row.MemberCode,
                    "Fullname": row.Fullname,
                    "Email": row.Email,
                }
        return None

    def calc_gpa(
        self, transcript: str, ignore: tuple, make_sure_all_passed=False
    ) -> list:
        """
        Calculate GPA of a given `transcript`

        Args:
            `transcript` (`str`): path to downloaded transcript
            `make_sure_all_passed` (`boolean`): make sure all subjects are `passed`
            `ignore` (`tuple`): what subject to ignore

        Returns:
            `list`: contains EnrollNumber and GPA

        Example:
            >>> calc_gpa("/path/to/transcript.xls", ignore=("VOV",))
            ['CS123456', 7.345789]
        """
        table1, table2 = self._parse_transcript(transcript)

        if make_sure_all_passed:
            table1_ok = (table1["Status"] == "Passed").all()
            table2_ok = (table2["Status"] == "Passed").all()
            if not all([table1_ok, table2_ok]):
                raise ValueError("Not all subjects passed")
        total_credit = 0
        total_grade = 0
        for row in table1.itertuples():
            if re.sub(r"\d", "", row.Subject_Code) not in ignore:
                credit = int(row.Credit)
                grade = float(row.Grade)
                total_grade += grade * credit
                total_credit += credit
        return format(total_grade / total_credit, ".5f"), total_credit

    def _parse_transcript(self, transcript) -> pd.DataFrame:
        soup = BeautifulSoup(open(abspath(transcript), "rb"), "lxml")
        tables = soup.find_all("table", {"class": "table table-hover"})

        # table 1
        thead1 = tables[0].find("thead")
        tbody1 = tables[0].find("tbody")

        header1 = []
        body1 = []
        for th in thead1.find("tr").find_all("th"):
            header1.append(th.text.strip().replace(" ", "_"))

        for tr in tbody1.find_all("tr"):
            data = []
            for td in tr.find_all("td"):
                data.append(td.text.strip())
            body1.append(data)

        df_table1 = pd.DataFrame(body1, columns=header1)

        # table 2
        thead2 = tables[1].find("thead")
        tbody2 = tables[1].find("tbody")

        header2 = []
        body2 = []
        for th in thead2.find("tr").find_all("th"):
            header2.append(th.text.strip().replace(" ", "_"))

        for tr in tbody2.find_all("tr"):
            data = []
            for td in tr.find_all("td"):
                data.append(td.text.strip())
            body2.append(data)

        df_table2 = pd.DataFrame(body2, columns=header2)

        return df_table1, df_table2
