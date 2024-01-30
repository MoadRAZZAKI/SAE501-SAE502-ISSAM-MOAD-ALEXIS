import json
from flask import Flask, jsonify
from data_manager import DBConnector

app = Flask(__name__)
db_connector = DBConnector()

@app.route('/api/data', methods=['GET'])
def get_data():
    db = db_connector.connect()
    data = db.packet_DHCP.find()  
    result = [{"Type": item["Type"], "Ether": item["Ether"], "IP": item["IP"], "DHCP": item["DHCP"], "UDP": item["UDP"], "BOOTP": item["BOOTP"]} for item in data]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
