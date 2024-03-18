import mlflow
from jinja2 import Environment, BaseLoader

def generate_spec(model):
    model_info = mlflow.models.get_model_info(model)

    with open('spec.j2', 'r') as template_file:
        template = template_file.read()

    data = {
        "outputs": parseTypes(model_info.signature.outputs),
        "inputs": parseTypes(model_info.signature.inputs),
        "params": parseTypes(model_info.signature.params)
    }

    rtemplate = Environment(loader=BaseLoader()).from_string(template).render(data = data)
    return rtemplate

def convertType(field_type):
    print(field_type)
    if field_type == "boolean":
        return "boolean"
    elif field_type == "integer":
        return "integer"
    elif field_type in ["double", "float", "long"]:
        return "number"
    elif field_type == "string":
        return "string"
    else:
        return "string"

def parseTypes(signature_field):
    if signature_field == None:
        return []
    
    signature_field = signature_field.to_dict()
    
    generated_name_index = 1
    for i in range(len(signature_field)):
        field  = signature_field[i]

        if 'name' not in field:
            signature_field[i]['name'] = "field_" + str(generated_name_index)
            generated_name_index += 1
        
        signature_field[i]["type"] = convertType(field["type"])

    return signature_field
