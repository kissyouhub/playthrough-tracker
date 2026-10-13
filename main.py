from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import date, datetime
app = FastAPI()


games = []
next_id = 1

@app.get('/')
def read_root():
    return {"message": "Hello, FastAPI!"}


class GameBase(BaseModel):
    title: str
    release_year: int
    developer: str
    description: str = str('None')
       
class GameCreate(GameBase):
    pass

class GameRead(GameBase):
    id: int
    
@app.get('/games')
def get_list_of_games():
    return games

@app.post('/games', status_code=201)
def create_game(game: GameCreate):
    global next_id
    if any(g["title"]== game.title for g in games):
        raise HTTPException(status_code=409, detail="Game already exists")
            
    else:
        new_game = {
                    "id": next_id,
                    "title": game.title,
                    "release_year": game.release_year,
                    "developer": game.developer,
                    "description": game.description
                    }
        games.append(new_game)
        next_id += 1
        return new_game

@app.get('/games/{id}')
def get_game_by_id(id: int):
    for game in games:
        if game["id"] == id:
            return game 
    
    raise HTTPException(status_code=409, detail="Game not found")