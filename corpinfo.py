import fincorpinfo
from KDB import KDBAnalysisApp
from financial_visualization import main

def run():
    fincorpinfo.show_company_info()
    app = KDBAnalysisApp()
    app.run()
    main()

# Streamlit 실행
if __name__ == "__main__":
    run()