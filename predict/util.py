from include import *
from auth import getAuthenticationHeader
import requests


def ArgParser():
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--input', action='store', type=str, required=True)
    my_parser.add_argument('--model', action='store', type=str, required=True)
    return my_parser.parse_args()


def readInputFile(dataPath):
    testInputLines = []

    with open(dataPath) as file_in:
        for line in file_in:
            testInputLines.append(line)

    return testInputLines


def getIDFromSongURL(url):
    songID = url.replace("https://open.spotify.com/track/", "").split('?')[0]
    return songID;


def parseInputLines(inputLines):
    requestParameters = "?ids="
    for songURL in inputLines:
        songID = getIDFromSongURL(songURL)
        requestParameters += songID + "%2C"
    return requestParameters


def getApiRequestURL(apiRequestParameters):
    BASE_URL = 'https://api.spotify.com/v1/'
    return BASE_URL + 'audio-features/' + apiRequestParameters


def getTracksFeatures(inputPath):
    inputLines = readInputFile(inputPath)
    apiRequestParameters = parseInputLines(inputLines)

    requestURL = getApiRequestURL(apiRequestParameters)
    authenticationHeader = getAuthenticationHeader()

    apiResponse = requests.get(requestURL, headers=authenticationHeader)
    apiResponseJSON = apiResponse.json()

    data = json.loads(str(apiResponseJSON).replace("\'", "\""))

    inputDataFrame = pd.json_normalize(data['audio_features'])
    return inputDataFrame
