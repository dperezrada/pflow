import os
import json
import tempfile

from pflow.workflow import read_workflow


workflow_w_variable = [
  {
    "task": "set_env_var",
    "name": "DATA_ID",
    "value": "group3"
  },
  {
    "task": "yolo_v8.load_dataset",
    "folder_path": "{{BASE_FOLDER}}/datasets/downloaded/{{DATA_ID}}"
  }
]

def test_read_w_variable(dataset):
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, 'workflow_w_variable.json')
        with open(path, 'w') as f:
            f.write(json.dumps(workflow_w_variable))
        os.environ['BASE_FOLDER'] = tmp
        workflow, workflow_data = read_workflow(path)
        assert len(workflow) == 1
        first_task = workflow[0]
        assert first_task.params['folder_path'] == f"{tmp}/datasets/downloaded/group3"
  
def test_read_w_missing_variable(dataset):
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, 'workflow_w_missing_variable.json')
        with open(path, 'w') as f:
            f.write(json.dumps(workflow_w_variable))
        os.environ['BASE_FOLDER'] = ''
        # we expect an error here
        try:
            workflow, workflow_data = read_workflow(path)
            assert False
        except ValueError as e:
            assert True