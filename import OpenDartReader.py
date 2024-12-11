import OpenDartReader
from dotenv import load_dotenv
import os

load_dotenv()
dart = OpenDartReader(os.environ["DART_API_KEY"])
company_name = "삼성전자"
corp_code = dart.find_corp_code(company_name)
report_year=2023
fs = dart.finstate(corp_code, report_year)
fs