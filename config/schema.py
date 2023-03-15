# strawberry graphql
import strawberry

# name:str = "seheon" # python의 경우 이러한 작업 필요 X

# @strawberry.type # python에선 그동안 type 선언이 없었는데 strawberry는 선언해야 API type을 알 수 있음
# class Query:
#     @strawberry.field # query field로 인식하게끔 선언 필요
#     def ping(self) -> str: # str return한다는 뜻
#         return "pong"
# # schema 선언
# schema = strawberry.Schema(query=Query)

import typing # 코드에 type annotation 을 추가할 수 있게 해줌

# 영화 API
@strawberry.type
class Movie:
    pk: int
    title: str
    year: int
    rating: int

movies_db = [
    Movie(pk=1, title="Godfather", year=1990, rating=10),
]

# resolver
@strawberry.type
class Query:
    @strawberry.field
    def movies(self) -> typing.List[Movie]:
        return movies_db

    @strawberry.field
    def movie(self, movie_pk:int) -> Movie:
        return movies_db[movie_pk - 1]
# 모든 영화 검색
# {
#   movies{
#     pk,
#     title,
#     year,
#     rating
#   }
# }

# pk로 영화 검색
# {
#   movie(moviePk:1) {
#     title
#     rating
#     year
#   }
# }

# mutation
@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_movie(self, title:str, year:int, rating:int) -> Movie:
        new_Movie = Movie(pk=len(movies_db)+1, title=title, year=year, rating=rating)
        movies_db.append(new_Movie)
        return new_Movie
# 새 양화 추가
# mutation {
#   addMovie(title:"Godfather II", year:1995, rating:9){
#     pk
#   }
# }

schema = strawberry.Schema(query=Query, mutation=Mutation)