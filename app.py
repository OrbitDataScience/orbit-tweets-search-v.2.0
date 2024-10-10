from scripts import getTweetsRecentCount, getRecentTweets, formatDates
from flask import Flask, jsonify, request, Response
import pandas as pd
from flask_cors import CORS
import io

app = Flask(__name__)
CORS(app)

if __name__ == "__main__":    
    app.run(host='0.0.0.0', port=5000)


@app.route("/", methods=['GET'])
def index():

    return jsonify("Hello Frontend. Backend here!")

#---------------------- TWEETS COUNT ------------------------------------
# get the tweets counto for the last 7 days
@app.route("/tweetscount", methods=['POST', 'GET'])
def tweetscount():
    # get the data from frontend
    data = request.json
    
    print(data)
    
    query = data['query']
    lang = data['lang']
    twitterAccount = data['twitterAccount']

    # format the dates do Api spcified format
    fromDt, toDt = formatDates(data['fromDate'], data['toDate'], 'recent')

    # get tweets data
    df = getTweetsRecentCount(query, lang, fromDt, toDt, twitterAccount)

    # Create an in-memory Excel writer
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    # Write the DataFrame to the Excel writer
    df.to_excel(writer, sheet_name='Sheet1', index=False)

    # Save the Excel writer to the in-memory stream
    writer.close()
    output.seek(0)

    return Response(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


#---------------------- TWEETS SEARCH ------------------------------------
# get the tweets  for the last 24 HOURS
@app.route("/tweetssearch", methods=['POST', 'GET'])
def tweetssearch():
    # get the data from frontend
    data = request.json
    query = data['query']
    lang = data['lang']
    twitterAccount = data['twitterAccount']

    # format the dates do Api spcified format
    fromDt, toDt = formatDates(data['fromDate'], data['toDate'], 'recent')

    # get tweets data
    df = getRecentTweets(query, lang, fromDt, toDt, twitterAccount)

    # Create an in-memory Excel writer
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    # Write the DataFrame to the Excel writer
    df.to_excel(writer, sheet_name='Sheet1', index=False)

    # Save the Excel writer to the in-memory stream
    writer.close()
    output.seek(0)

    return Response(output.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')




