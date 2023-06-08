
# Armand Croitoru Resume App


## ⇁ Installation
Steps:
```bash
# git clone git@github.com:baloops/flask_resume.git
# cd flask_resume   
# docker build -t flask_resume_app .
# docker run -p 8081:8081 -v ./:/code/ --name armand_resume flask_resume_app
```


## ⇁ Usage
Access these urls from your browser or using a cli tool like httpie(http) or curl
* http://localhost:8081/personal
* http://localhost:8081/experience
* http://localhost:8081/education

As for the cli commans, there are two:
get-chapter is suppose to give you each chapter one by one 
compose-resume can combine chapters in case you want to skip one

```bash
# docker exec -it armand_resume flask get-chapter experience
# docker exec -it armand_resume flask get-chapter personal   
# docker exec -it armand_resume flask get-chapter education   
# docker exec -it armand_resume flask get-chapter all  # for the whole resume

# docker exec -it armand_resume flask compose-resume --personal --education
```

Please use flask --help or flask command --help for further information

For the api responses, they look like this 
```json
{
    "data": {
        "interests": "I am passionate about web development and embedded systems.",
        "name": "Armand Croitoru",
        "phone": "+40 749 364 644"
    },
    "error_code": null,
    "message": null,
    "status": "success"
}
```
or like this: 
```json
{
    "data": {},
    "error_code": "resume.file.not.found",
    "message": "File resume.jjson does not exist.",
    "status": "failed"
}
```
in case there are errors.

help messages: 
```
$ docker exec -it armand_resume flask get-chapter --help
Usage: flask get-chapter [OPTIONS] CHAPTER

  Get a chapter of the resume.

  Example: flask get-chapter experience

  CHAPTER is the part of the resume that you want returned: personal,
  education, experience, all.

Options:
  --help  Show this message and exit.
```

```
docker exec -it armand_resume flask compose-resume --help
Usage: flask compose-resume [OPTIONS]

  Add the chapters by setting the flags that interest you.

  Example: flask compose-resume --education --personal

Options:
  --personal    Set flag to get the personal chapter
  --experience  Set flag to get the experience chapter
  --education   Set flag to get the education chapter
  --help        Show this message and exit.
 ```

