import spacy
from spacy.matcher import Matcher

from services import sparql_query_builder_for_preferences
nlp = spacy.load("en_core_web_sm")  # Load a small English language model

def create_entity_matcher_patterns(file_path):

    with open(file_path, 'r') as file:
        names = [line.strip().lower() for line in file.readlines()]

    patterns = []
    for name in names:
        pattern = [{"LOWER": name}]
        patterns.append(pattern)

    return patterns

def extract_info_with_spacy(text, artist_file_path, genre_file_path):
    result = {"like": {"artist": set(), "genre": set(), "before_year": None, "after_year": None},
              "dislike": {"artist": set(), "genre": set(), "before_year": None, "after_year": None}, 
              "love": {"artist": set(), "genre": set(), "before_year": None, "after_year": None},
              "hate": {"artist": set(), "genre": set(), "before_year": None, "after_year": None},
              "sentiments": []}

    doc = nlp(text)

    artist_patterns = create_entity_matcher_patterns(artist_file_path)
    genre_patterns = create_entity_matcher_patterns(genre_file_path)

    artist_matcher = Matcher(nlp.vocab)
    genre_matcher = Matcher(nlp.vocab)

    artist_matcher.add("ARTIST", artist_patterns)
    genre_matcher.add("GENRE", genre_patterns)

    active_set = None 

    for i, token in enumerate(doc):
        if token.text.lower() in ["like", "dislike", "love", "hate"]:
            active_set = result[token.text.lower()]

        if token.text.lower() == "by":
            continue

        for matcher, entity_type in [(artist_matcher, "artist"), (genre_matcher, "genre")]:
            matches = matcher(doc)
            for match_id, start, end in matches:
                entity = doc[start:end].text.lower()
                if active_set is not None:
                    active_set[entity_type].add(entity)
    sentiment = None
    for i, token in enumerate(doc):
        if token.text.lower() in ["like", "love", "hate", "dislike"]:
            sentiment = token.text.lower()
            next_token = doc[i + 1].text.lower() if i + 1 < len(doc) else None
            
    for i, token in enumerate(doc):
          if token.text.lower() in ["before", "after"]:
            if sentiment is not None:
                relation = token.text.lower()
                next_token = doc[i + 1].text.lower() if i + 1 < len(doc) else None
                if next_token.isdigit():
                    active_set[f"{relation}"] = int(next_token)

    return result

def clean_preferences(preferences):
    for info in preferences:
        if isinstance(preferences[info], dict):
            info_temp = {key: value for key, value in preferences[info].items() if value is not None and (not isinstance(value, set) or len(value) > 0)}
            preferences[info] = info_temp
    # print(preferences)
    return preferences

def combine_dict(preferences1, preferences2):
    for key, value2 in preferences2.items():
        if key in preferences1:
            value1 = preferences1[key]
            if isinstance(value1, dict) and isinstance(value2, dict):
                preferences1[key] = {**value1, **value2}
            elif isinstance(value1, set) and isinstance(value2, set):
                preferences1[key] = value1.union(value2)
            else:
                preferences1[key] = value2
        else:
            preferences1[key] = value2

    return preferences1

def get_input_from_text(text):

    artist_file_path = "services/artists.txt"  # Replace with the actual path to your artist names file
    genre_file_path = "services/genres.txt"   # Replace with the actual path to your genre names file

    my_preferences = extract_info_with_spacy(text, artist_file_path, genre_file_path)

    my_preferences = clean_preferences(my_preferences)

    return my_preferences
    
def set_user_preferences(text):
    sentences = text.split('. ')
    my_preferences_union = dict()
    for sentence in sentences:
        my_preferences = get_input_from_text(sentence)
        my_preferences_union = combine_dict(my_preferences_union, my_preferences)
    
    print(my_preferences_union)

    for key, value in my_preferences_union.items():
        if isinstance(value, dict):
            for nested_key, nested_value in value.items():
                if isinstance(nested_value, set):
                    my_preferences_union[key][nested_key] = list(nested_value)
   

    return sparql_query_builder_for_preferences(my_preferences_union)