from hashlib import md5
import feedparser
import json
import os
import re

JSONDIR = "/home/vagrant/hermercury/json/"


def open_feed(FeedHost):
    FeedData = feedparser.parse(FeedHost)
    return FeedData.entries


def find_entry_by_title(SearchList, SearchString):
    EntryMatch = None

    for counter, entry in enumerate(SearchList):
        Match = re.search(SearchString, entry["title"], re.I)
        if Match:
            EntryMatch = SearchList[counter]
            break

    return EntryMatch


def find_entry_by_index(SearchList, Index):
    try:
        return SearchList[Index]
    except IndexError:
        return None


def create_object_with_wanted_parameters(OriginalObject, KeyList):
    StoreObject = {}

    if OriginalObject:
        for key in (key for key in KeyList if key in OriginalObject):
            StoreObject[key] = OriginalObject[key]

    return StoreObject


def save_object_as_json_to_disk(Object, Name):
    if Object:
        Object["dismissed"] = False
        Object["name"] = Name
        Object["id"] = md5(str(Object)).hexdigest()
        with open(JSONDIR + Name, "w") as SaveFile:
            json.dump(Object, SaveFile, sort_keys=True, indent=4, separators=(',', ': '))


def set_notification_as_dismissed(File):
    with open(JSONDIR + File, "r+") as JsonFile:
        JsonObject = json.load(JsonFile)
        JsonFile.seek(0)
        JsonFile.truncate()
        JsonObject["dismissed"] = True
        json.dump(JsonObject, JsonFile, sort_keys=True, indent=4, separators=(',', ': '))
        JsonFile.close()


def compare_notification_id(File, Object):
    if os.path.isfile(JSONDIR + File):
        with open(JSONDIR + File, "r") as JsonFile:
            JsonObject = json.load(JsonFile)
            JsonFile.close()

            Object["dismissed"] = False
            Object["name"] = File
            Object["id"] = md5(str(Object)).hexdigest()

            if Object["id"] == JsonObject["id"]:
                return False
            else:
                return True
    else:
        return True


def load_notification_object(File):
    if os.path.isfile(JSONDIR + File):
        with open(JSONDIR + File, "r") as JsonFile:
            JsonObject = json.load(JsonFile)
            JsonFile.close()

    return JsonObject


def search_method_switch(Feed, SearchStringOrIndex):
        if type(SearchStringOrIndex) == str:
            Entry = find_entry_by_title(Feed, SearchStringOrIndex)
        elif type(SearchStringOrIndex) == int:
            Entry = find_entry_by_index(Feed, SearchStringOrIndex)
        else:
            return None
        return Entry
