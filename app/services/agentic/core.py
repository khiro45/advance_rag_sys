
propmpts_dir = "app/services/agentic/core/propmt_templates/"

def propmt_loader(propmt_name:str , propmt_args:dict):

    with open(f"{propmpts_dir}{propmt_name}.md", 'r') as f:
        propmt_template = f.read()

    for key, value in propmt_args.items():
        propmt_template = propmt_template.replace(f"{{{key}}}", str(value))

    return propmt_template