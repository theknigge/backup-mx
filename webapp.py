from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/queue', methods=['GET'])
def get_queue_status():
    try:
        # Befehl, um die Anzahl der E-Mails in der Warteschlange abzurufen
        output = subprocess.check_output(['mailq'])
        decoded_output = output.decode('utf-8').strip()
        
        # Die Ausgabe aufteilen und verarbeiten
        if not decoded_output:
            return jsonify({
                'num_emails': 0,
                'queue_entries': []
            }), 200
        
        parts = decoded_output.split('\n\n')
        if len(parts) < 2:
            return jsonify({
                'num_emails': 0,
                'queue_entries': decoded_output.split('\n')
            }), 200

        queue_entries = parts[1].split('\n')
        num_emails = len(queue_entries) if queue_entries else 0

        # Rückgabe als JSON
        return jsonify({
            'num_emails': num_emails,
            'queue_entries': queue_entries
        }), 200
    except subprocess.CalledProcessError as e:
        return jsonify({
            'error': 'Failed to fetch queue status',
            'details': str(e)
        }), 500
    except Exception as e:
        return jsonify({
            'error': 'An unexpected error occurred',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
