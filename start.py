import requests
import json
import datetime


channelList = []


def getChannels():
    reqUrl = "https://jiotv.data.cdn.jio.com/apis/v1.4/getMobileChannelList/get/?os=android&devicetype=phone"
    response = requests.get(reqUrl)
    apiData = json.loads(response.text)
    return apiData["result"]


def getEpg(channelId, offset, langId):
    reqUrl = "https://jiotv.data.cdn.jio.com/apis/v1.3/getepg/get?channel_id=" + \
        str(channelId)+"&offset="+str(offset)+"&langId="+str(langId)
    response = requests.get(reqUrl)
    print("OK: " + str(response.ok) + " status: " + str(response.status_code))
    if (response.status_code == 200):
        apiData = json.loads(response.text or "{}")
        return apiData["epg"]
    return []


def initEpgFiles():
    f = open("channels.xml", "w")
    f.write("")
    f.close()

    f = open("program.xml", "w")
    f.write("")
    f.close()

    f = open("epg.xml", "w")
    f.write("")
    f.close()


def writeEpgChannel(id, name, iconId):
    if id is None or name is None:
        return
    f = open("channels.xml", "a", encoding='utf-8')
    f.write("\t<channel id=\""+str(id)+"\">\n")
    f.write("\t\t<display-name>"+str(name)+"</display-name>\n")
    f.write("\t\t<icon src=\"https://jiotv.catchup.cdn.jio.com/dare_images/images/" +
            str(iconId)+"\"></icon>\n")
    f.write("\t</channel>\n")
    f.close()


def writeEpgProgram(channelId, start, end, title, description, icon):
    if channelId is None or start is None or end is None or title is None:
        return
    startTime = datetime.datetime.fromtimestamp(int(start/1000))
    progStart = startTime.strftime("%Y%m%d%H%M%S +0000")

    endTime = datetime.datetime.fromtimestamp(int(end/1000))
    progEnd = endTime.strftime("%Y%m%d%H%M%S +0000")

    try:
        f = open("program.xml", "a", encoding='utf-8')
        f.write("\t<programme start=\""+str(progStart)+"\" stop=\"" +
                str(progEnd)+"\" channel=\""+str(channelId) + "\">\n")
        f.write("\t\t<title lang=\"en\">" + title + "</title>\n")
        f.write("\t\t<desc lang=\"en\">" + description + "</desc>\n")
        f.write("\t\t<icon src=\"https://jiotv.catchup.cdn.jio.com/dare_images/shows/" +
                str(icon)+"\"></icon>\n")
        f.write("\t</programme>\n")
        f.close()
    except UnicodeEncodeError:
        print("it was not a ascii-encoded unicode string")
        f.close()


def mergeEpgData():
    channelsFile = open("channels.xml", "r", encoding='utf-8')
    programsFile = open("program.xml", "r", encoding='utf-8')
    epgFile = open("epg.xml", "a", encoding='utf-8')

    epgFile.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
    epgFile.write("<!DOCTYPE tv SYSTEM \"xmltv.dtd\">\n")
    epgFile.write(
        "<tv generator-info-name=\"Arnab Ghosh\" generator-info-url=\"https://github.com/arnab8820\">\n")
    epgFile.write(channelsFile.read())
    epgFile.write(programsFile.read())
    epgFile.write("</tv>\n")


# Process starts here
initEpgFiles()
channelList = getChannels()
for channel in channelList:
    writeEpgChannel(channel["channel_id"],
                    channel["channel_name"], channel["logoUrl"])
    lowerRange = -7 if channel["isCatchupAvailable"] else -1
    for offset in range(0, 1):
        print("Getting EPG for "+str(channel["channel_id"]) +
              " "+channel["channel_name"]+" day "+str(offset))
        epgData = getEpg(channel["channel_id"], offset, 6)
        for epg in epgData:
            writeEpgProgram(channel["channel_id"],
                            epg["startEpoch"], epg["endEpoch"], epg["showname"],
                            epg["description"], epg["episodePoster"])
mergeEpgData()
print("Action complete")
