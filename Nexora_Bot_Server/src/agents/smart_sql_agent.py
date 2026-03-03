import json
import sqlite3
import pandas as pd
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from src.config.index import appConfig

class SmartDataAgent:
    def __init__(self, file_paths: List[str], schema_json_path: str, model_name: str = "gpt-4o"):
        self.file_paths = file_paths
        self.schema_json_path = schema_json_path
        self.model_name = model_name
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model=model_name,
            api_key=appConfig["openai_api_key"],
            temperature=0
        )
        
        # Load Schema
        with open(schema_json_path, 'r') as f:
            self.schema = json.load(f)
            
        # Initialize Database
        self.conn = sqlite3.connect(":memory:")
        self._load_data_to_sqlite()

    def _load_data_to_sqlite(self):
        """Loads CSV/Excel files into SQLite tables matching the schema keys or filenames."""
        for path in self.file_paths:
            # Detect file type and load accordingly
            if path.endswith('.csv'):
                df = pd.read_csv(path)
            elif path.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(path)
            else:
                continue
                
            # Clean table name logic
            # 1. Get simple filename without path and extension
            simple_filename = path.split('/')[-1].split('\\')[-1].split('.')[0].lower()
            
            # 2. Match against schema table names
            matched_table_name = None
            if self.schema and "tables" in self.schema:
                for table_def in self.schema["tables"]:
                    schema_name = table_def["table_name"].lower()
                    # Check partial match: if schema name is in filename (e.g. 'movie' in 'final_movies')
                    # OR if filename is in schema name (e.g. 'movies' in 'movie_data') - less likely
                    if schema_name in simple_filename or simple_filename in schema_name:
                         matched_table_name = schema_name
                         break
            
            # 3. Fallback to cleaned filename if no match
            if matched_table_name:
                table_name = matched_table_name
            else:
                table_name = simple_filename

            print(f"DEBUG: Loading file {path} into table '{table_name}'")
            df.to_sql(table_name, self.conn, index=False, if_exists='replace')
        
        # Verify loaded tables
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"DEBUG: Tables in SQLite: {tables}")

    def filter_schema(self, user_query: str) -> Dict:
        """Step 1: LLM filters the schema to only required tables/columns."""
        system_prompt = """You are a strictly logical Data Architect.
        Given a user query and a database schema, return a JSON object containing ONLY 
        the tables and columns strictly required to generate a SQL query for the answer.
        
        IMPORTANT:
        - If the user asks about "all tables", "the whole schema", or "database statistics", return ALL tables and their primary keys/relevant columns.
        - Do NOT iterate or explain. Just output the JSON.
        
        Output format:
        {{
            "tables": [
                {{
                    "table_name": "name",
                    "definition": "description of table",
                    "columns": [
                        {{
                            "name": "col_name",
                            "definition": "description",
                            "data_type": "type",
                            "key_type": "PK/FK/None",
                            "example": "example_value"
                        }}
                    ]
                }}
            ]
        }}
        """
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "Schema: {schema}\n\nQuery: {query}")
        ])
        
        chain = prompt | self.llm | JsonOutputParser()
        return chain.invoke({"schema": json.dumps(self.schema), "query": user_query})

    def generate_sql(self, user_query: str, filtered_schema: Dict) -> str:
        """Step 2: Generate SQL using only the filtered schema."""
        system_prompt = """You are an expert SQL Developer.
        Generate a SQL query to answer the user's question. 
        USE ONLY the tables and columns provided in the schema below.
        
        CRITICAL INSTRUCTIONS:
        1. Return ONLY the raw SQL string.
        2. Do NOT use markdown code blocks (```sql).
        3. Do NOT include any explanations or conversational text.
        4. If the user asks for a count of rows in all tables, generate a query using `UNION ALL` to combine counts from each table.
           Example: `SELECT 'table1' as table_name, COUNT(*) as count FROM table1 UNION ALL SELECT 'table2', COUNT(*) FROM table2 ...`
        5. If you cannot answer the question using the schema, return the string "NO_SQL_POSSIBLE" and nothing else.
        """
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "Filtered Schema: {filtered_schema}\n\nQuestion: {query}")
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        sql_query = chain.invoke({"filtered_schema": json.dumps(filtered_schema), "query": user_query})
        
        # Basic cleanup
        return sql_query.replace("```sql", "").replace("```", "").strip()

    def execute_and_answer(self, user_query: str):
        try:
            # 1. Filter Schema
            print(f"DEBUG: User Query: '{user_query}'")
            print(f"DEBUG: Loaded Schema Keys: {list(self.schema.keys()) if self.schema else 'None'}")
            filtered_schema = self.filter_schema(user_query)
            print(f"DEBUG: Filtered Schema: {json.dumps(filtered_schema, indent=2)}")
            
            # 2. Generate SQL
            sql = self.generate_sql(user_query, filtered_schema)
            print(f"DEBUG: Generated SQL: {sql}")

            if "NO_SQL_POSSIBLE" in sql:
                 return {
                    "answer": "I apologize, but I could not generate a valid SQL query to answer your question based on the provided schema/data. The question might clearly require information not present in the tables.",
                    "sql": sql,
                    "data": []
                 }
            
            # 3. Execute
            cursor = self.conn.cursor()
            cursor.execute(sql)
            if cursor.description:
                columns = [description[0] for description in cursor.description]
                results = cursor.fetchall()
                data_result = [dict(zip(columns, row)) for row in results]
            else:
                data_result = []
                results = []
            
            # Format results as text table
            text_table = ""
            if data_result:
                # Create header
                headers = list(data_result[0].keys())
                
                # Simple text representation
                lines = []
                lines.append(" | ".join(headers))
                lines.append("-" * (sum(len(h) for h in headers) + 3 * (len(headers) - 1)))
                
                for row in data_result:
                    lines.append(" | ".join(str(val) for val in row.values()))
                
                text_table = "\n".join(lines)

            return {
                "answer": f"Executed SQL: `{sql}`\n\n{text_table}",
                "sql": sql,
                "data": data_result
            }
        except Exception as e:
            return f"Error executing SQL or processing request: {e}"

def create_smart_agent(file_paths, schema_path, model="gpt-4o"):
    return SmartDataAgent(file_paths, schema_path, model)
