from flask import Flask, jsonify
import subprocess
import re

app = Flask(__name__)

def parse_mailq_output(output):
    # Initialisieren Sie eine Liste für die E-Mail-Daten
    emails = []

    # Die Ausgabe decodieren und in Zeilen aufteilen
    lines = output.decode('utf-8').split('\n')

    # Pattern für das Extrahieren von Mail-IDs
    mail_id_pattern = re.compile(r'^([0-9A-F]{6,})')

    # Variablen für Mail-Details
    current_mail = None
    for line in lines:
        if line.startswith(' '):  # Diese Zeilen gehören zur aktuellen Mail
            if current_mail:
                if line.startswith('  '):
                    current_mail['details'].append(line.strip())
                continue
        else:
            # Neue Mail gefunden
            match = mail_id_pattern.match(line)
            if match:
                if current_mail:
                    emails.append(current_mail)
                current_mail = {
                    'id': match.group(1),
                    'details': []
                }
    
    if current_mail:
        emails.append(current_mail)

    return emails

@app.route('/queue', methods=['GET'])
def get_queue_status():
    try:
        # Befehl, um die E-Mails in der Warteschlange abzurufen
        output = subprocess.check_output(['mailq'])
        
        # E-Mail-Daten aus der `mailq`-Ausgabe extrahieren
        emails = parse_mailq_output(output)

        # Rückgabe als JSON
        return jsonify({
            'num_emails': len(emails),
            'emails': emails
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
