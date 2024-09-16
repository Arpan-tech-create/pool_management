from flask import Flask,request,jsonify,render_template
import db


app=Flask(__name__,template_folder='templates')


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/pool_data")
def pool_name():
    try:
        pools= db.get_pool_details()
        print(pools)
        return jsonify(pools)

    except Exception as e:
        return jsonify(error=str(e))

@app.route("/slave_data",methods=['GET'])
def slave_data():
    pool_name = request.args.get('pool_name')
    try:
        slaves = db.get_slave_details(pool_name)
        return jsonify(slaves)
    except Exception as e:
        return jsonify(error=str(e))
app.run(debug=True,host='0.0.0.0')