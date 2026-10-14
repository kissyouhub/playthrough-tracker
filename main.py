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
    description: str | None = None
       
class GameCreate(GameBase):
    pass

class GameRead(GameBase):
    id: int
    
class GameUpdate(BaseModel):
    title: str | None = None
    release_year: int | None = None
    developer: str | None = None
    description: str | None = None    
    

@app.get('/games')
def get_list_of_games(year: int | None = None, developer: str | None = None, search: str | None = None ):
    result = []
    for game in games:
        if year is not None and game["release_year"] != year:
            continue
        if developer is not None and game["developer"] != developer:
            continue
        if search is not None and search not in (game["title"]).lower():
            continue
        result.append(game)
    return result


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

@app.get('/games/{id}/')
def get_game_by_id(id: int):
    if id is not None:
        for game in games:
            if game["id"] == id:
                return game 
    if year is not None:
            for game in games:
                if game["release_year"] == year:
                    return game 
    if developer is not None:
            for game in games:
                if game["developer"] == developer:
                    return game 
    if search is not None:
            for game in games:
                if game["title"] == search:
                    return game 
    
    raise HTTPException(status_code=409, detail="Game not found")

@app.patch('/games/{id}', status_code=202)
def game_update(game_id: int, game_update: GameUpdate):
    for game in games:
        if game["id"] == game_id:
            if game_update.title is not None:
                game["title"] = game_update.title
            if game_update.release_year is not None:
                game["release_year"] = game_update.release_year
            if game_update.developer is not None:
                game["developer"] = game_update.developer
            if game_update.description is not None:
                game["description"] = game_update.description
            return game
    raise HTTPException(status_code=404, detail="Game not found")

@app.delete("/games/{id}", status_code=204)
def game_delete(game_id: int):
    for game in games:
        if game["id"] == game_id:
            index = game_id - 1
            del games[index]
            return games
    raise HTTPException(status_code=404, detail="Game not found")