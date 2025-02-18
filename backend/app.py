from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import boto3
import time
import os
from fastapi.middleware.cors import CORSMiddleware
# AWS Configuration
AWS_REGION = "us-east-1"  # Change to your AWS region
ATHENA_DB = "kafka-project-db"
OUTPUT_BUCKET = "s3://test-proj-athena-results-bucket/"

client = boto3.client("athena", region_name=AWS_REGION)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://main.d383hwbdqho0dx.amplifyapp.com/"],  # Change this to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

def execute_athena_query(query: str):
    """Run the query and fetch results"""
    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={"Database": ATHENA_DB},
        ResultConfiguration={"OutputLocation": OUTPUT_BUCKET},
    )
    query_execution_id = response["QueryExecutionId"]

    # Wait for query completion
    while True:
        query_status = client.get_query_execution(QueryExecutionId=query_execution_id)
        state = query_status["QueryExecution"]["Status"]["State"]
        if state in ["SUCCEEDED", "FAILED", "CANCELLED"]:
            break
        time.sleep(1)

    if state != "SUCCEEDED":
        raise HTTPException(status_code=400, detail="Query execution failed")

    # Get results
    result_response = client.get_query_results(QueryExecutionId=query_execution_id)
    results = []
    for row in result_response["ResultSet"]["Rows"]:
        results.append([col.get("VarCharValue", "") for col in row["Data"]])
    
    return results

@app.post("/query")
# @app.get("/")
def run_query(request: QueryRequest):
    """API endpoint to execute Athena query"""
    print("Request: ", request)
    return {"results": execute_athena_query(request.query)}
    # return {"message": "Query executed successfully"}

