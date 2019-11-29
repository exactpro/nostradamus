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


import os
import shutil
from flask import Flask, render_template, request, jsonify, redirect, url_for, session


def check_session():
    """ Checks session activity.

    Returns:
        Boolean value.   

    """
    return 'username' not in session or 'session_id' not in session


def is_session_expired():
    if 'expired' in dict(request.args).keys():
        if request.args['expired'] == '1':
            return False
        else:
            return True
    else:
        return True


def remove_folder(path):
    for root, dirs, files in os.walk(path):
        if files:
            for file_name in files:
                os.chmod('{root}/{file_name}'.format(root=root, file_name=file_name), 0o664)
    shutil.rmtree(path)


def create_folder(path):
    os.makedirs(path)
    os.chmod(path, 0o775)

