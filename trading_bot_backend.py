from openai import OpenAI
import yfinance as yf
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class TradingBot:

    def __init__(self, llm_model='gpt-4o-mini'):

        self.llm_model = llm_model
        self.client = OpenAI()

    def get_df(self):

        spx = yf.Ticker('^GSPC')
        df = spx.history(period='max')

        df['Return'] = df['Close'].pct_change()

        return df

    def code_generator(self, user_query: str) -> str:

        today = datetime.today().strftime('%Y-%m-%d')
        system_prompt = f"You are an intellegent agent that needs to generate python code that will provide output to answer user questions. The dataframe is named df and contains historical data for the S&P500 from 1927-12-30 to {today}. df has the following columns: Open, High, Low, Close, and Return. df has a datetime index. Only return the code an nothing else. Make sure the final result you would like the user to see is assigned to a variable called result."

        completion = self.client.chat.completions.create(
        model=self.llm_model,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": user_query
            }
        ]
        )

        response = completion.choices[0].message.content
        parsed_response = response.split(sep="```python")[1].split("```")[0]

        return parsed_response

    def code_executor(self, code_snippet: str):

        local_namespace = {}
        df = self.get_df()
        local_namespace.update({'df':df})

        code_snippet = "import pandas as pd\n" + code_snippet

        try:
            # Execute the provided code within the local namespace
            exec(code_snippet, {}, local_namespace)
            # Retrieve the variable 'result' from the local namespace
            if 'result' in local_namespace:
                return local_namespace['result']
            else:
                return "Error: 'result' variable not found in the code snippet."
        except Exception as e:
            return f"Error: {e}"
