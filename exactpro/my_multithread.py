'''
/*******************************************************************************
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
******************************************************************************/
'''


import numpy
from multiprocessing import cpu_count, Pool
from multiprocessing import Process
import pandas


class Multithreaded:
    # processes parallelisation
    def parallelize(self, data, func):
        self.cores = cpu_count()
        self.split = numpy.array_split(data, self.cores) # DataFrame separation (DF parts count equals to cores count)
        self.pool = Pool(self.cores) # container which stores DataFrame's part for future concatenation
        try:
            data = pandas.concat(self.pool.map(func, self.split)) # DataFrame's parts concatenation
        except TypeError as e:
            raise TypeError(str(e))
        self.pool.close()
        self.pool.join()
        return data

    # running of two threads
    def run_in_parallel(self, flask, redis_expire):
        flask_proc = Process(target=flask) # thread 1: Flask processes
        flask_proc.start()
        expire_proc = Process(target=redis_expire, args=(flask_proc,)) # thread 2: session status activities
        expire_proc.start()
        proc = [flask_proc, expire_proc]
        for pr in proc:
            pr.join()

