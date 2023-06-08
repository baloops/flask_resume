import json
import click 
from enum import Enum

from flask import Flask


app = Flask(__name__)


json_resume = 'resume.jjson'


class ApplicationError(Exception):
    code = 'default'
    def __init__(self, message):
        self.message = message


class JsonSyntaxError(ApplicationError):
    code = 'json.syntax.error'


class ResumeFileNotFound(ApplicationError):
    code = 'resume.file.not.found'


class Chapters(Enum):
    PERSONAL = 'personal'
    EXPERIENCE = 'experience'
    EDUCATION = 'education'
    ALL = 'all'


def get_resume_json(chapter: Chapters):
    try:
        with open(json_resume, 'r') as f:
            data = json.loads(f.read())
    except json.decoder.JSONDecodeError as e:
        raise JsonSyntaxError('JOSN resume syntax error: ' + str(e))
    except FileNotFoundError as e:
        raise ResumeFileNotFound(f'File {json_resume} does not exist.')

    rv = data if Chapters(chapter) == Chapters.ALL else data.get(chapter.value)
    return rv or {}


@app.errorhandler(404)
def handle_not_found_error(error):
    response = {
        'message': 'Resource not found',
        'error_code': '404.not.found'
    }
    return response, 404


@app.after_request
def add_status(response):
    content_type = response.headers.get('Content-Type')
    if content_type != 'application/json':
        return response
    
    data = json.loads(response.data)
        
    enhanced_data = {
        'status': 'success' if not data.get('error_code') else 'failed',
        'data': data.get('data', {}),
        'error_code': data.get('error_code', None),
        'message': data.get('message', None)
    }
    response.data = json.dumps(enhanced_data)
    if enhanced_data.get('error_code') and response.status.startswith('2'):
        response.status = 500 
    return response 


def api_error_catcher(func):
    def wrapper(*args, **kwargs):
        try:
            rv = func(*args, **kwargs)
        except ApplicationError as e:
            return {
                'error_code': e.code,
                'message': e.message 
            } 
        return rv
    return wrapper


@app.route("/personal", methods=['GET'], endpoint='get_personal')
@api_error_catcher
def get_personal():
    return {'data': get_resume_json(Chapters.PERSONAL)}


@app.route("/experience", methods=['GET'], endpoint='get_experience')
@api_error_catcher
def get_experience():
    return {'data': get_resume_json(Chapters.EXPERIENCE)}


@app.route("/education", methods=['GET'], endpoint='get_education')
@api_error_catcher
def get_education():
    return {'data': get_resume_json(Chapters.EDUCATION)}


@app.cli.command()
@click.argument('chapter', type=Chapters)
def get_chapter(chapter: Chapters):
    """Get a chapter of the resume. 
    
    Example: flask get-chapter experience

    CHAPTER is the part of the resume that you want returned: personal, 
    education, experience, all.
    """
    click.echo(json.dumps(get_resume_json(chapter), indent=4))


@app.cli.command()
@click.option('--personal', is_flag=True, help='Set flag to get the personal chapter')
@click.option('--experience', is_flag=True, help='Set flag to get the experience chapter')
@click.option('--education', is_flag=True, help='Set flag to get the education chapter')
def compose_resume(personal, experience, education):
    """Add the chapters by setting the flags that interest you.

    Example: flask compose-resume --education --personal 
    """

    resume = {}
    mapping = {
        Chapters.PERSONAL: personal,
        Chapters.EXPERIENCE: experience,
        Chapters.EDUCATION: education,
    }
    try:
        for chapter in filter(lambda x: mapping[x], mapping):
            resume[chapter.value] = get_resume_json(Chapters(chapter))
    except ApplicationError as e:
        raise click.ClickException(e.message)

    click.echo(json.dumps(resume, indent=4))

