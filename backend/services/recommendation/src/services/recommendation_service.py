# from datetime import datetime, timedelta
import datetime
from services import combine_dict

def get_data_for_each_period(preferences):
    # print(preferences)
    s = datetime.datetime.now().strftime("%d/%m/%Y")

    result = {
        "last_day": [],
        "last_week": [],
        "other": []
    }

    for elem in preferences['preferences']:
        elem_date = datetime.datetime.strptime(elem, "%d/%m/%Y")
        diff = datetime.datetime.strptime(s, "%d/%m/%Y") - elem_date
        if diff.days <= 1:
            result["last_day"].append(preferences['preferences'][elem])
        elif diff.days <= 7:
            result["last_week"].append(preferences['preferences'][elem])
        else:
            result["other"].append(preferences['preferences'][elem])
    return result

def get_recommendation_for_user(preferences):
    data = get_data_for_each_period(preferences)
    # print(data)
    result = {
        "last_day": {
            "artists": {},
            "genres": {},
            "years": {}
        },
        "last_week": {
            "artists": {},
            "genres": {},
            "years": {}
        },
        "other": {
            "artists": {},
            "genres": {},
            "years": {}
        }
    }
    for period in data.keys():
        if len(data[period]) > 0:
            for elem in data[period]:
                for key_field in elem.keys():
                    for concrete_elem in elem[key_field].keys():
                        if concrete_elem in result[period][key_field]:
                            result[period][key_field][concrete_elem] += elem[key_field][concrete_elem]
                        else:
                            result[period][key_field][concrete_elem] = elem[key_field][concrete_elem]
    return result



preferences = {
    "user_id": 1,
    "preferences": {
        "30/01/2024": {
            "artists": {
                "Beatles": 3,
                "Queen": 2
            },
            "genres": {
                "rock": 3,
                "pop": 2
            },
            "years": {
                "1960": 3,
                "1970": 2
            }
        },
        "17/01/2024": {
            "artists": {
                "Elvis Presley": 4,
                "Michael Jackson": 1
            },
            "genres": {
                "rock": 2,
                "pop": 3
            },
            "years": {
                "1950": 2,
                "1980": 3
            }
        },
        "05/02/2024": {
            "artists": {
                "Bob Dylan": 2,
                "Led Zeppelin": 2,
                "Pink Floyd": 1
            },
            "genres": {
                "folk": 2,
                "rock": 2,
                "psychedelic": 1
            },
            "years": {
                "1960": 2,
                "1970": 2,
                "1980": 1
            }
        },
        "04/02/2024": {
            "artists": {
                "Prince": 3,
                "David Bowie": 1,
                "Madonna": 2
            },
            "genres": {
                "pop": 3,
                "funk": 1,
                "rock": 2
            },
            "years": {
                "1970": 2,
                "1980": 3,
                "1990": 1
            }
        },
        "20/02/2023": {
            "artists": {
                "The Rolling Stones": 2,
                "U2": 3,
                "Radiohead": 1
            },
            "genres": {
                "rock": 3,
                "alternative": 1,
                "pop": 2
            },
            "years": {
                "1960": 1,
                "1980": 2,
                "1990": 1
            }
        }
    }
    } 
# get_recommendation_for_user(preferences['preferences'])


