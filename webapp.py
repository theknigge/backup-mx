from flask import Flask, render_template_string
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/queue', methods=['GET'])
def get_queue_status():
    try:
        # Befehl, um die Anzahl der E-Mails in der Warteschlange abzurufen
        output = subprocess.check_output(['mailq'])
        decoded_output = output.decode('utf-8').strip()
        
        # Die Ausgabe aufteilen und verarbeiten
        if not decoded_output:
            return '''
            <div class="loading">No emails in the queue.</div>
            '''
        
        parts = decoded_output.split('\n\n')
        if len(parts) < 2:
            return '''
            <div class="loading">No emails in the queue.</div>
            '''

        queue_entries = parts[1].split('\n')
        num_emails = len(queue_entries) if queue_entries else 0

        # HTML Tabelle
        table_html = '''
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Details</th>
                </tr>
            </thead>
            <tbody>
        '''
        for entry in queue_entries:
            table_html += f'<tr><td>{entry}</td><td>Details here</td></tr>'
        
        table_html += '''
            </tbody>
        </table>
        '''
        return table_html
    except subprocess.CalledProcessError as e:
        return '<p>Error fetching queue status</p>', 500
    except Exception as e:
        return '<p>An unexpected error occurred</p>', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
