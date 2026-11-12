from fastapi import FastAPI
from dotenv import load_dotenv
from routes.analyse import router as analyse_router

load_dotenv()

app=FastAPI(
    title="shikaku",
    description=" crop disease detection API",
    version="1.0.0",
)

@app.get("/")
async def root():
    return {
        "app":"shikaku",
        "version":"1.0.0",
        "endpoint":{
            "POST/analyse":"Upload an image to analyze the crop disease",
            "POST/analyse/batch":"Upload multiple images to analyze the crop disease",
            "GET/analyses":"Get the list of all analyses performed",
            "GET/analyse/{image_id}":"Get the analysis result of a specific image by its ID",
        }
    }


app.include_router(analyse_router)