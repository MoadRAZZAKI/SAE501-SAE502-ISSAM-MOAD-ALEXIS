import json
from flask import Flask, jsonify, request, make_response
from data_manager import DBConnector
from flask_httpauth import HTTPBasicAuth
import socket


app = Flask(__name__)

db_connector = DBConnector()
auth = HTTPBasicAuth()
host = socket.gethostbyname(socket.gethostname())

with open('C:\\Users\\m.razzaki\\OneDrive - Biodiv-wind\\Bureau\\SAE501\\SAE501\\ApiWeb\\config.json', 'r') as fichier:
    users = json.load(fichier)

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

@app.route('/api/data', methods=['GET'])
@auth.login_required
def get_all_data():
    db = db_connector.connect()
    data = db.packet_dhcp.find()  
    result = [{"Type": item["Type"], "Ethernet": item["Ethernet"], "IP": item["IP"], "UDP": item["UDP"], "BOOTP": item["BOOTP"], "DHCP options": item["DHCP options"]} for item in data]
    return jsonify(result)

@app.route('/api/data/<packet_type>', methods=['GET'])
@auth.login_required
def filter_data_by_type(packet_type):
    db = db_connector.connect()
    data = db.packet_dhcp.find({"Type": packet_type})  
    result = [{"Type": item["Type"], "Ethernet": item["Ethernet"], "IP": item["IP"], "UDP": item["UDP"], "BOOTP": item["BOOTP"], "DHCP options": item["DHCP options"]} for item in data]
    return jsonify(result)

@app.route('/api/data/dhcp/source_mac/<source_mac>', methods=['GET'])
@auth.login_required
def get_dhcp_packets_by_source_mac(source_mac):
    db = db_connector.connect()
    data = db.packet_dhcp.find({"Ethernet.src": source_mac})  
    result = [{"Type": item["Type"], "Ethernet": item["Ethernet"], "IP": item["IP"], "UDP": item["UDP"], "BOOTP": item["BOOTP"], "DHCP options": item["DHCP options"]} for item in data]
    return jsonify(result)

@app.route('/api/data/dhcp/destination_mac/<destination_mac>', methods=['GET'])
@auth.login_required
def get_dhcp_packets_by_destination_mac(destination_mac):
    db = db_connector.connect()
    data = db.packet_dhcp.find({"Ethernet.dst": destination_mac})  
    result = [{"Type": item["Type"], "Ethernet": item["Ethernet"], "IP": item["IP"], "UDP": item["UDP"], "BOOTP": item["BOOTP"], "DHCP options": item["DHCP options"]} for item in data]
    return jsonify(result)

@app.route('/api/data/dhcp/source_ip/<source_ip>', methods=['GET'])
@auth.login_required
def get_dhcp_packets_by_source_ip(source_ip):
    db = db_connector.connect()
    data = db.packet_dhcp.find({"IP.src": source_ip})  
    result = [{"Type": item["Type"], "Ethernet": item["Ethernet"], "IP": item["IP"], "UDP": item["UDP"], "BOOTP": item["BOOTP"], "DHCP options": item["DHCP options"]} for item in data]
    return jsonify(result)

@app.route('/api/data/dhcp/destination_ip/<destination_ip>', methods=['GET'])
@auth.login_required
def get_dhcp_packets_by_destination_ip(destination_ip):
    db = db_connector.connect()
    data = db.packet_dhcp.find({"IP.dst": destination_ip})  
    result = [{"Type": item["Type"], "Ethernet": item["Ethernet"], "IP": item["IP"], "UDP": item["UDP"], "BOOTP": item["BOOTP"], "DHCP options": item["DHCP options"]} for item in data]
    return jsonify(result)

@app.route('/api/data/dhcp/requested_address/<requested_address>', methods=['GET'])
@auth.login_required
def get_dhcp_packets_by_requested_address(requested_address):
    db = db_connector.connect()
    data = db.packet_dhcp.find({"DHCP options.requested_addr": requested_address})  
    result = [{"Type": item["Type"], "Ethernet": item["Ethernet"], "IP": item["IP"], "UDP": item["UDP"], "BOOTP": item["BOOTP"], "DHCP options": item["DHCP options"]} for item in data]
    return jsonify(result)

@app.route('/api/data/dhcp/source_port/<source_port>', methods=['GET'])
@auth.login_required
def get_dhcp_packets_by_source_port(source_port):
    db = db_connector.connect()
    data = db.packet_dhcp.find({"UDP.sport": int(source_port)})  
    result = [{"Type": item["Type"], "Ethernet": item["Ethernet"], "IP": item["IP"], "UDP": item["UDP"], "BOOTP": item["BOOTP"], "DHCP options": item["DHCP options"]} for item in data]
    return jsonify(result)

@app.route('/api/data/dhcp/destination_port/<destination_port>', methods=['GET'])
@auth.login_required
def get_dhcp_packets_by_destination_port(destination_port):
    db = db_connector.connect()
    data = db.packet_dhcp.find({"UDP.dport": int(destination_port)})  
    result = [{"Type": item["Type"], "Ethernet": item["Ethernet"], "IP": item["IP"], "UDP": item["UDP"], "BOOTP": item["BOOTP"], "DHCP options": item["DHCP options"]} for item in data]
    return jsonify(result)

@app.route('/api/data/dhcp/server_id/<server_id>', methods=['GET'])
@auth.login_required
def get_dhcp_packets_by_server_id(server_id):
    db = db_connector.connect()
    data = db.packet_dhcp.find({"DHCP options.server_id": server_id})  
    result = [{"Type": item["Type"], "Ethernet": item["Ethernet"], "IP": item["IP"], "UDP": item["UDP"], "BOOTP": item["BOOTP"], "DHCP options": item["DHCP options"]} for item in data]
    return jsonify(result)

@app.route('/api/data/json/<packet_type>', methods=['GET'])
@auth.login_required
def filter_data_by_type_json(packet_type):
    db = db_connector.connect()
    data = db.packet_dhcp.find({"Type": packet_type})  
    result = [{"Type": item["Type"], "Ethernet": item["Ethernet"], "IP": item["IP"], "UDP": item["UDP"], "BOOTP": item["BOOTP"], "DHCP options": item["DHCP options"]} for item in data]
    
    # Convert result to JSON
    json_data = json.dumps(result, indent=4)
    
    # Prepare response
    response = make_response(json_data)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Content-Disposition'] = 'attachment; filename=data.json'
    
    return response

if __name__ == '__main__':
    app.run(host=host)
