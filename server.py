from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/queue', methods=['GET'])
def get_queue_status():
    try:
        # Befehl, um die Anzahl der E-Mails in der Warteschlange abzurufen
        output = subprocess.check_output(['mailq'])
        # Die Ausgabe in eine Liste von Warteschlangen-Einträgen aufteilen
        queue_entries = output.decode('utf-8').split('\n\n')[1].split('\n')
        # Die Anzahl der E-Mails in der Warteschlange zählen
        num_emails = len(queue_entries)
        # Rückgabe als JSON
        return jsonify({
            'num_emails': num_emails,
            'queue_entries': queue_entries
        }), 200
    except subprocess.CalledProcessError:
        return jsonify({
            'error': 'Failed to fetch queue status'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
