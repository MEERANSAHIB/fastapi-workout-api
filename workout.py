from fastapi import FastAPI,Query,Path,HTTPException,status
from pydantic import BaseModel,Field
from typing import Optional

app=FastAPI()
class Exercise():
    id:int
    movement_name:str
    muscle_group:str
    recommended_sets:int
    difficulty_level:int
    def __init__(self,id,movement_name,muscle_group,recommended_sets,difficulty_level):
        self.id=id
        self.movement_name=movement_name
        self.muscle_group=muscle_group
        self.recommended_sets=recommended_sets
        self.difficulty_level=difficulty_level

class exercise_request(BaseModel):
    id:Optional[int]=None
    movement_name:str=Field(min_length=3)
    muscle_group:str
    recommended_sets:int=Field(gt=0,lt=11)
    difficulty_level:int=Field(gt=0,le=5)
    

    model_config={
        "json_schema_extra":{
            "example":{
                "movement_name":"movement",
                "muscle_group":"muslce group",
                "recommended_sets":3,
                "difficulty_level":3
            }
        }
    }
workouts=[Exercise(1,"Lat_Pulldown","back",3,3),
          Exercise(2,"shoulder press","shoulders",3,3),
          Exercise(3,"Bicep curls","bicep",3,2),
          Exercise(4,"leg press","leg",3,3),
          Exercise(5,"Squats","leg",3,4)
          ]
@app.get("/workouts",status_code=status.HTTP_200_OK)
async def return_all_workouts():
    return workouts
@app.get("/workouts/Workouts_by_muscle/")
async def Workouts_by_muscle(muscle:str=Query(default=None)):
    workouts_to_return= [Exercise for Exercise in workouts if muscle.casefold()== Exercise.muscle_group.casefold()]
    if len(workouts_to_return)==0:
        raise(HTTPException(status_code=404,detail="Can't find the workout with given muscle type"))
    else:
        return workouts_to_return
@app.get("/workouts/get_workouts_by_id/{id}",status_code=status.HTTP_200_OK)
async def get_workouts_by_id(id:int):
    return [Exercise for Exercise in workouts if id == Exercise.id]
@app.post("/workouts/create_new_workout/")
async def create_new_workout(exercise:exercise_request):
    new_workout=Exercise(**exercise.model_dump())
    set_id_to_the_workout(new_workout)
    workouts.append(new_workout)

def set_id_to_the_workout(workout:exercise_request):
    if len(workouts)>0:
        workout.id=workouts[-1].id+1
    else:
        workout.id=1

@app.put("/workouts/update_a_existing_Exercise")
async def update_a_existing_Exercise(new_exercise:exercise_request):
    for i in range(len(workouts)):
        if workouts[i].id==new_exercise.id:
            workouts[i]=Exercise(**new_exercise.model_dump())
            return {"message":"success"}
    raise HTTPException(status_code=404,detail="Can't find the workout with given id")
@app.delete("/workouts/delete_a_existing_workout/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_a_existing_workout(id: int = Path(gt=0)): 
     for i in range(len(workouts)):
        if workouts[i].id == id:
            workouts.pop(i)
            return {"message": "success"}
            
     raise HTTPException(status_code=404, detail="Can't find the workout with given id")
            