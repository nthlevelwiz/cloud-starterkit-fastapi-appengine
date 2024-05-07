from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# import psycopg2_binary as psycopg2
from psycopg2 import sql
import psycopg2

app = FastAPI()

# Database connection
conn_string = "postgresql://fastapi_neondb_user:G9wOJYdcrPM7@ep-green-math-a585lr9v.us-east-2.aws.neon.tech/wizNeonDB?sslmode=require"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

# Pydantic models for request and response bodies
class Video(BaseModel):
    id: int
    videotitle: str
    creatorsusername: str
    videodescription: str
    summary: str
    transcript: str
    dateofvideocreation: str
    tags: str
    videofileorurl: str
    metadatadate: str

class Tag(BaseModel):
    id: int
    tagname: str

# Routes
@app.get("/videos/{video_id}")
async def get_video(video_id: int):
    cursor.execute(sql.SQL("SELECT * FROM video WHERE id = %s"), (video_id,))
    video_data = cursor.fetchone()
    if video_data:
        return Video(
            id=video_data[0],
            videotitle=video_data[1],
            creatorsusername=video_data[2],
            videodescription=video_data[3],
            summary=video_data[4],
            transcript=video_data[5],
            dateofvideocreation=video_data[6],
            tags=video_data[7],
            videofileorurl=video_data[8],
            metadatadate=video_data[9]
        )
    else:
        raise HTTPException(status_code=404, detail="Video not found")

@app.get("/tags/{tag_id}")
async def get_tag(tag_id: int):
    cursor.execute(sql.SQL("SELECT * FROM tags WHERE id = %s"), (tag_id,))
    tag_data = cursor.fetchone()
    if tag_data:
        return Tag(
            id=tag_data[0],
            tagname=tag_data[1]
        )
    else:
        raise HTTPException(status_code=404, detail="Tag not found")
