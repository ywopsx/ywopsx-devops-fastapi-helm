from fastapi import FastAPI
import socket
import os

app = FastAPI()

@app.get("/")
async def get_info():
    try:
        hostname = socket.gethostname()
        return {
            "hostname": hostname,
            "environment": os.environ.get("ENVIRONMENT"),
            "db_host": os.environ.get("DB_HOST"),
            "db_port": os.environ.get("DB_PORT"),
            "db_name": os.environ.get("DB_NAME"),
            "db_username": os.environ.get("DB_USERNAME"),
            "db_password": os.environ.get("DB_PASSWORD")            
        }
    except Exception as e:
        return {"message": str(e)}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn. run(app, host="0.0.0.0", port=3000)