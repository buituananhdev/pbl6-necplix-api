from typing import List, Union

from beanie import PydanticObjectId

from models.user import User
from models.student import Student
from models.movie import Movie

user_collection = User
student_collection = Student
movie_collection = Movie 


async def add_user(new_user: User) -> User:
    user = await new_user.create()
    return user

async def retrieve_movies() -> List[Movie]:
    movies = await movie_collection.all().to_list()
    return movies

async def retrieve_movie(id: PydanticObjectId) -> Movie:
    movie = await movie_collection.get(id)
    if movie:
        return movie

async def add_movie(new_movie: Movie) -> Movie:
    movie = await new_movie.create()
    return movie

async def delete_movie(id: PydanticObjectId) -> bool:
    movie = await movie_collection.get(id)
    if movie:
        await movie.delete()
        return True
    
async def update_movie_data(id: PydanticObjectId, data: dict) -> Union[bool, Movie]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {field: value for field, value in des_body.items()}}
    movie = await movie_collection.get(id)
    if movie:
        await movie.update(update_query)
        return movie
    return False

async def retrieve_students() -> List[Student]:
    students = await student_collection.all().to_list()
    return students


async def add_student(new_student: Student) -> Student:
    student = await new_student.create()
    return student


async def retrieve_student(id: PydanticObjectId) -> Student:
    student = await student_collection.get(id)
    if student:
        return student


async def delete_student(id: PydanticObjectId) -> bool:
    student = await student_collection.get(id)
    if student:
        await student.delete()
        return True


async def update_student_data(id: PydanticObjectId, data: dict) -> Union[bool, Student]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {field: value for field, value in des_body.items()}}
    student = await student_collection.get(id)
    if student:
        await student.update(update_query)
        return student
    return False
