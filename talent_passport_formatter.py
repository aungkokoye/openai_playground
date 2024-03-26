import re


def strip_html_tag(html):
    return re.sub(r'<[^<]+?>', '', html)


def get_talent_data(json, result):
    if 'talent' in json:
        talent_data = json['talent']
        result = get_talent(talent_data, result)
    else:
        result['talent'] = {}
    return result


def get_talent(talent_data, result):
    talent_info = {
        'uuid': talent_data['uuid'],
        'first_name': talent_data['first_name'],
        'last_name': talent_data['last_name'],
        'job_title': talent_data['job_title'],
        'telephone': talent_data['telephone'],
        'email': talent_data['email'],
        'personal_statement': strip_html_tag(talent_data['personal_statement']),
        'min_day_rate': talent_data['min_day_rate'],
        'max_day_rate': talent_data['max_day_rate'],
        'avatar_photo_url': talent_data['avatar_metadata']['source_url'],
        'profile_completeness': talent_data['profile_completeness'],
        'applied_projects_count': talent_data['applied_projects_count'],
        'hired_projects_count': talent_data['hired_projects_count'],
        'currency': talent_data['day_rate_currency']['symbol'],
        'country': get_country(talent_data['country']),
        'full_name': talent_data['full_name'],
        'role_name': talent_data['role_name'],
        'years_of_experience': talent_data['years_of_experience']
    }
    
    result['talent_information'] = talent_info  
    result = get_applications_data(talent_data, result)
    result['talent_information']['total_applications'] = len(result['talent_information'].get('applications', []))
    
    return result


def get_country(country):
    return {
        'continent_name': country.get('continent_name'),
        'name': country.get('name')
    }


def get_applications_data(talent_data, result):
    applications = talent_data.get('applications', [])
    result = get_applications(applications, result)
    return result


def get_applications(applications, result):
    result_applications = []
    for application in applications:
        application_new_data = {
            'status': application.get('status'),
            'status_name': application.get('status_name'),
            'project': get_project(application.get('project'))
        }
        result_applications.append(application_new_data)

    result['talent_information']['applications'] = result_applications
    return result


def get_project(project):
    return {
        'id': project.get('id'),
        'uuid': project.get('uuid'),
        'name': project.get('name')
    }


def get_work_history_data(json, result):
    if 'work-history' in json:
        work_history_data = json['work-history']
        result = get_work_history(work_history_data, result)
    else:
        result['work_history'] = {}
    return result


def get_work_history(work_history_data, result):
    result['work_history'] = {}
    result['work_history']['total_work_experiences'] = work_history_data['hydra:totalItems']
    result = get_work_experience_data(work_history_data, result)
    
    return result


def get_work_experience_data(work_history_data, result):
    if 'hydra:member' in work_history_data:
        work_experiences = work_history_data['hydra:member']
        result = get_work_experiences(work_experiences, result)
    else:
        result['work_history']['work_experiences'] = []
    return result


def get_tag_data(tags):
    tag_data = []
    for tag in tags:
        tag_data.append({
            'field_name': tag['tag']['name'],
            'sub_field_name': tag['tag']['taxonomy']['name']
        })
    return tag_data
            

def get_work_experiences(work_experiences, result):
    result['work_history']['work_experiences'] = []
    for work_experience in work_experiences:
        work_experience_new_data = {
            'id': work_experience['id'],
            'title': work_experience['title'],
            'company': work_experience['company'],
            'date_from': work_experience['date_from'],
            'date_to': work_experience['date_to'],
            'summary': strip_html_tag(work_experience['summary']),
            'experience_fields': get_tag_data(work_experience['tags'])
        }   
        result['work_history']['work_experiences'].append(work_experience_new_data)
    return result


def get_education_experiences(education_experiences, result):
    result['educational_history']['education_experiences'] = []
    for education_experience in education_experiences:
        education_experience_new_data = {
            'id': education_experience['id'],
            'name': education_experience['name'],
            'degree': education_experience['degree'],
            'field': education_experience['field'],
            'date_from': education_experience['date_from'],
            'date_to': education_experience['date_to'],
            'educational_apply_fields': get_tag_data(education_experience['tags'])
        }   
        result['educational_history']['education_experiences'].append(education_experience_new_data)
    return result


def get_education_experience_data(education_experience_data, result):
    if 'hydra:member' in education_experience_data:
        education_experiences = education_experience_data['hydra:member']
        result = get_education_experiences(education_experiences, result)
    else:
        result['educational_history']['education_experiences'] = []
    return result


def get_education_history_data(json, result):
    if 'educational-history' in json:
        education_history_data = json['educational-history']
        result = get_education_history(education_history_data, result)
    else:
        result['educational_history'] = {}
    return result


def get_education_history(education_history_data, result):
    result['educational_history'] = {}
    result['educational_history']['total_education_experiences'] = education_history_data['hydra:totalItems']
    result = get_education_experience_data(education_history_data, result)
    
    return result


def get_industry_experiences(industry_experiences, result):
    result['industry_history']['industry_experiences'] = []
    for industry_experience in industry_experiences:
        industry_experience_new_data = {
            'id': industry_experience['id'],
            'years_of_experience': industry_experience['years'],
            # 'industry_name': industry_experience['industry']['name'],
        }   
        result['industry_history']['industry_experiences'].append(industry_experience_new_data)
    return result


def get_industry_experience_data(industry_history_data, result):
    if 'hydra:member' in industry_history_data:
        industry_experiences = industry_history_data['hydra:member']
        result = get_industry_experiences(industry_experiences, result)
    else:
        result['industry_history']['industry_experiences'] = []
    return result


def get_industry_history(industry_history_data, result):
    result['industry_history'] = {}
    result['industry_history']['total_industry_experiences'] = industry_history_data['hydra:totalItems']
    result = get_industry_experience_data(industry_history_data, result)
    
    return result


def get_industry_history_data(json, result):
    if 'industry-experience' in json:
        industry_history_data = json['industry-experience']
        result = get_industry_history(industry_history_data, result)
    else:
        result['industry_history'] = {}
    return result


def get_job_function_experiences(job_function_experiences, result):
    result['job_function_history']['job_function_experiences'] = []
    for job_function_experience in job_function_experiences:
        job_function_experience_new_data = {
            'id': job_function_experience['id'],
            'years_of_experience': job_function_experience['years'],
            'job_function_name': job_function_experience['job_function']['name'],
        }   
        result['job_function_history']['job_function_experiences'].append(job_function_experience_new_data)
    return result


def get_job_function_experience_data(job_function_experience_data, result):
    if 'hydra:member' in job_function_experience_data:
        job_function_experiences = job_function_experience_data['hydra:member']
        result = get_job_function_experiences(job_function_experiences, result)
    else:
        result['job_function_history']['job_function_experiences'] = []
    return result


def get_job_function_history(job_function_experience_data, result):
    result['job_function_history'] = {}
    result['job_function_history']['total_job_function_experiences'] = job_function_experience_data['hydra:totalItems']
    result = get_job_function_experience_data(job_function_experience_data, result)
    
    return result

    
def get_job_function_history_data(json, result):
    if 'job-function-experience' in json:
        job_function_experience_data = json['job-function-experience']
        result = get_job_function_history(job_function_experience_data, result)
    else:
        result['job_function_history'] = {}
    return result


def get_language_experiences(language_experiences, result):
    result['language_history']['language_experiences'] = []
    for language_experience in language_experiences:
        language_experience_new_data = {
            'id': language_experience['id'],
            'proficiency_level': language_experience['proficiency'],
            'job_function_name': language_experience['language']['name'],
        }   
        result['language_history']['language_experiences'].append(language_experience_new_data)
    return result


def get_language_experience_data(language_experience_data, result):
    if 'hydra:member' in language_experience_data:
        language_experiences = language_experience_data['hydra:member']
        result = get_language_experiences(language_experiences, result)
    else:
        result['language_history']['language_experiences'] = []
    return result


def get_language_history(language_experience_data, result):
    result['language_history'] = {}
    result['language_history']['total_language_experiences'] = language_experience_data['hydra:totalItems']
    result = get_language_experience_data(language_experience_data, result)
    
    return result 
    
    
def get_language_history_data(json, result):
    if 'language-experience' in json:
        language_experience_data = json['language-experience']
        result = get_language_history(language_experience_data, result)
    else:
        result['language_history'] = {}
    return result


def get_talent_passport_json_data(raw_json):
    final_result = {}
    final_result = get_talent_data(raw_json, final_result)
    final_result = get_work_history_data(raw_json, final_result)
    final_result = get_education_history_data(raw_json, final_result)
    final_result = get_industry_history_data(raw_json, final_result)
    final_result = get_job_function_history_data(raw_json, final_result)
    final_result = get_language_history_data(raw_json, final_result)
    
    return final_result
