import subprocess
import re
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

ACCESS_CODE = 'b-mx-24'

def parse_mailq_output(output):
    emails = []
    lines = output.decode('utf-8').split('\n')
    
    # Regex patterns to match queue ID and extract fields
    mail_id_pattern = re.compile(r'^([0-9A-F]{6,})')
    
    current_mail = None

    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check if the line contains a queue ID
        match = mail_id_pattern.match(line)
        if match:
            # Save the previous email details if available
            if current_mail:
                emails.append(current_mail)

            # Start a new email entry
            current_mail = {
                'id': match.group(1),
                'recipients': '',
                'sender': '',
                'details': []
            }
        
        elif current_mail:
            # Extract sender and recipient details
            if '@' in line:
                if current_mail['sender'] == '':
                    current_mail['sender'] = line
                else:
                    current_mail['recipients'] = line
            else:
                # Collect additional details
                current_mail['details'].append(line)
    
    # Append the last email entry
    if current_mail:
        emails.append(current_mail)
    
    return emails

@app.route('/queue', methods=['GET'])
def get_queue_status():
    try:
        output = subprocess.check_output(['mailq'])
        emails = parse_mailq_output(output)
        return jsonify({
            'num_emails': len(emails),
            'emails': emails
        }), 200
    except subprocess.CalledProcessError as e:
        return jsonify({'error': 'Failed to fetch queue status', 'details': str(e)}), 500
    except Exception as e:
        return js
