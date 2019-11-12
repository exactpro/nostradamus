'''
*******************************************************************************
* Copyright 2016-2019 Exactpro (Exactpro Systems Limited)
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
*     http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*******************************************************************************
'''

from psycopg2 import connect, DatabaseError

class DatabaseProcessor:

    def __init__(self, connection_settings):
        self.connection_settings = connection_settings

    def __enter__(self):
        self.connection = connect(**self.connection_settings)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        if exc_val:
            raise

    def execute_query(self, sql_query):
        """ Executes the handled sql-query.

            Parameters:
                sql_query(str): sql-query.

        """
        with self as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                connection.commit()


