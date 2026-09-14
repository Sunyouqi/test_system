
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_cors import cross_origin
import subprocess
import yaml
import os

target_folder = '../iats-poc'
flask_directory = '../flask'
app = Flask(__name__)
# Allows the Vue PC to access the endpoints
CORS(app, resources={r"/api/*": {"origins": "http://10.136.195.144:5173/api"}})


@app.route('/api/data', methods=['GET'])
@cross_origin()
def get_data():
    return jsonify({"message": "Hello there from Flask on another PC !"})


@app.route('/api/submit', methods=['POST'])
@cross_origin()
def post_data():
    content = request.json
    username = content.get("username") or "Guest2"
    if username.endswith('.py'):
        try:
            filename = f'./service_DCN_CTTL_certification/testcase/{str(username)}'
            print("exeuting file:", filename)
            os.chdir(target_folder)
            result = subprocess.run([f"python", "-m", "pytest", filename], check=True)
            os.chdir(flask_directory)
            return jsonify({"message": f"Execution result, {result}! ", "status": "success"})
        except Exception:
            raise RuntimeError('failed to execute the test script!')


    return jsonify({"message": f"Welcome, {username}! this is not a paradise", "status": "success"})

@app.route('/api/submit/save-config', methods=['POST'])
@cross_origin()
def configure_data():
    content = request.json
    print(content)
    platformPath = content.get("platformPath") or "/"
    projectName = content.get("projectName") or "/"
    testcase = content.get("testCase") or "/"
    networkTopology = content.get("networkTopology") or "/"
    spirentConfig = content.get("spirentConfig") or "/"
    print("file path:", os.path.join(platformPath, projectName, 'config/case_config.xml'))
    yaml_path = os.path.join(platformPath, projectName, "config/case_config.yaml")
    def read_yaml(yaml_file_path):
        with open(yaml_file_path, "r", encoding='utf-8') as file:
            return yaml.safe_load(file)
    def write_yaml(yaml_file_path, data):
        with open(yaml_file_path, "w", encoding='utf-8') as file:
            yaml.safe_dump(data, file, allow_unicode=True, sort_keys=False, default_flow_style=False)
        return
    yaml_file = read_yaml(yaml_path)
    print("yaml file:", yaml_file)
    yaml_file[testcase]['enx'], yaml_file[testcase]['tester'] = networkTopology, spirentConfig
    write_yaml(yaml_path, yaml_file)
    return jsonify({"message": f"configure path:, {yaml_path}, {yaml_file}, {yaml_file[testcase]} ! ", "status": "success"})

if __name__ == '__main__':
    # host='0.0.0.0' makes Flask listen on all network interfaces
    app.run(host='0.0.0.0', port=5000, debug=True)




