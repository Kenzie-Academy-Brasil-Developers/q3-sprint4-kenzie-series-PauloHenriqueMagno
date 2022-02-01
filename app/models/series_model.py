from app.models import DatabaseConnector

VALUE_NAMES = ["id", "serie", "seasons", "released_date", "genre", "imdb_rating"]

class Serie(DatabaseConnector):
  def __init__(self, *args, **kwargs):
    self.serie          = kwargs["serie"].title()
    self.seasons        = kwargs["seasons"]
    self.released_date  = kwargs["released_date"]
    self.genre          = kwargs["genre"].title()
    self.imdb_rating    = kwargs["imdb_rating"]

  def save_serie(self):
    self.create_table()
    self.get_conn_cur()

    query = """
        INSERT INTO
            ka_series (serie, seasons, released_date, genre, imdb_rating)
        VALUES
            (%s, %s, %s ,%s, %s)
        RETURNING
            *;
    """

    query_values = list(self.__dict__.values())

    self.cur.execute(query, query_values)
    created_serie = self.cur.fetchone()
    
    self.commit_and_close()

    return created_serie
