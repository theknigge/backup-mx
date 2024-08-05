import subprocess
import re
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

ACCESS_CODE = 'b-mx-24'

def parse_mailq_output(output):
    emails = []
    lines = output.decode('utf-8').split('\n')
    
    mail_id_pattern = re.compile(r'^([0-9A-F]{6,})')
    current_mail = None
    
    for line in lines:
        if line.startswith(' '):
            if current_mail:
                if line.startswith('  '):
                    current_mail['details'].append(line.strip())
                elif line.startswith('To:'):
                    current_mail['recipients'] = line[len('To:'):].strip()
                elif line.startswith('From:'):
                    current_mail['sender'] = line[len('From:'):].strip()
        else:
            match = mail_id_pattern.match(line)
            if match:
                if current_mail:
                    emails.append(current_mail)
                current_mail = {
                    'id': match.group(1),
                    'recipients': '',
                    'sender': '',
                    'details': []
                }

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
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    access_code = request.args.get('access_code')
    if access_code != ACCESS_CODE:
        return jsonify({'error': 'Unauthorized access'}), 403

    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Postfix Queue Status</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }
            th, td {
                padding: 12px;
                text-align: left;
                border: 1px solid #ddd;
            }
            th {
                background-color: #4CAF50;
                color: white;
            }
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
            .container {
                max-width: 1200px;
                margin: auto;
            }
            .header {
                text-align: center;
                margin-bottom: 20px;
            }
            .loading {
                text-align: center;
                font-size: 18px;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Postfix Queue Status</h1>
            </div>
            <div id="status" class="loading">Loading...</div>
        </div>
        <script>
            function fetchQueueStatus() {
                fetch('/queue')
                    .then(response => response.json())
                    .then(data => {
                        const statusDiv = document.getElementById('status');
                        if (data.num_emails === 0) {
                            statusDiv.innerHTML = '<p>No emails in the queue.</p>';
                            return;
                        }

                        let tableHtml = `
                        <table>
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Empfänger</th>
                                    <th>Absender</th>
                                    <th>Details</th>
                                </tr>
                            </thead>
                            <tbody>
                        `;

                        data.emails.forEach(email => {
                            tableHtml += `<tr>
                                <td>${email.id}</td>
                                <td>${email.recipients}</td>
                                <td>${email.sender}</td>
                                <td>${email.details.join('<br>')}</td>
                            </tr>`;
                        });

                        tableHtml += `
                            </tbody>
                        </table>
                        `;

                        statusDiv.innerHTML = tableHtml;
                    })
                    .catch(error => {
                        console.error('Error fetching queue status:', error);
                        document.getElementById('status').innerHTML = '<p>Error loading data</p>';
                    });
            }

            fetchQueueStatus();
            setInterval(fetchQueueStatus, 60000); // Refresh every 60 seconds
        </script>
    </body>
    </html>
    """
    return render_template_string(html_content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
