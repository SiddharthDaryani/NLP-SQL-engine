from flask import Flask, request, jsonify, render_template
from logger import logging
from modules import build_prompt, generate_sql, is_valid_sql, execute_sql, clean_generated_sql_output

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/query', methods=['GET', 'POST'])
def query():
    if request.method == 'GET':
        return jsonify({'message': 'API is working. Please use POST with JSON to query.'}), 200

    if request.method == 'POST':
        if not request.is_json:
            logging.warning("POST request missing JSON body or Content-Type header.")
            return jsonify({'error': 'Content-Type must be application/json'}), 415

        data = request.get_json()
        prompt = data.get('prompt', '').strip()
        logging.info(f"Received prompt: {prompt}")

        if not prompt:
            logging.warning("POST request missing 'prompt' in JSON body.")
            return jsonify({'error': 'Missing \"prompt\" in request body'}), 400

        try:
            full_prompt = build_prompt(prompt)
            generated = generate_sql(full_prompt)
            sql_query = clean_generated_sql_output(generated)
            logging.info(f"Generated SQL: {sql_query}")

            if not is_valid_sql(sql_query):
                logging.error(f"Generated output is not valid SQL: {sql_query}")
                return jsonify({'error': 'Generated output is not valid SQL.'}), 400

            result = execute_sql(sql_query)
            if (
                isinstance(result, list) and 
                len(result) == 1 and 
                isinstance(result[0], dict)
            ):
                row = result[0]
                count_value = next(iter(row.values()))
                return jsonify({'result': count_value})

            # Fallback if not a single count value
            logging.info(f"Query result: {result}")
            return jsonify({'result': result})

        except Exception as e:
            logging.error(f"Error processing query: {e}")
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Run on all interfaces so browser can access it
    app.run(host='0.0.0.0', port=8080, debug=False)