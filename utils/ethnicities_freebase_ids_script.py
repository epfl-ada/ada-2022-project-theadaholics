import numpy as np
import pandas as pd
import time
import requests

def fetch_ethnicity_freebase_labels():
    # Load characters
    characters_header = ['wikipedia_movie_id','freebase_movie_id','movie_release_date','character_name','actor_birthdate','actor_gender','actor_height_meters','actor_ethnicity_freebase_id','actor_name','actor_age_at_movie_release','freebase_character_actor_map_id','freebase_character_id','freebase_actor_id']
    characters = pd.read_csv('../data/character.metadata.tsv', sep='\t', header=None, names=characters_header)

    # Obtain ethnicity unique ids
    characters_ehtnicity = characters.dropna(subset=['actor_ethnicity_freebase_id'])
    ethnicity_freebase_ids = np.unique(characters_ehtnicity['actor_ethnicity_freebase_id'], return_counts=False)
    
    ethnicity_labels = []
    for ehtnicity_id in ethnicity_freebase_ids:
        time.sleep(1) # Necessary to avoid server refusing the request

        query = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?format=json&query=PREFIX%20wd%3A%20%3Chttp%3A%2F%2Fwww.wikidata.org%2Fentity%2F%3E%0APREFIX%20wdt%3A%20%3Chttp%3A%2F%2Fwww.wikidata.org%2Fprop%2Fdirect%2F%3E%0APREFIX%20wikibase%3A%20%3Chttp%3A%2F%2Fwikiba.se%2Fontology%23%3E%0A%0ASELECT%20%20%3Fs%20%3FsLabel%20%3Fp%20%20%3Fo%20%3FoLabel%20WHERE%20%7B%0A%20%3Fs%20wdt%3AP646%20%22%2Fm%2F0" \
        + ehtnicity_id[4:] \
        + "%22%20%0A%0A%20%20%20SERVICE%20wikibase%3Alabel%20%7B%0A%20%20%20%20bd%3AserviceParam%20wikibase%3Alanguage%20%22en%22%20.%0A%20%20%20%7D%0A%20%7D"

        try:
            response = requests.get(query)
            ethnicity_wikidata_dict = response.json()
            try:
                ethnicity_label = ethnicity_wikidata_dict['results']['bindings'][0]['sLabel']['value']
            except:
                ethnicity_label = 'unknown'
        except ValueError:
            print(ValueError)
            ethnicity_label = ehtnicity_id

        print(ethnicity_label)
        ethnicity_labels.append(ethnicity_label)
    
    ethnicities_df = pd.DataFrame({'ethnicity_freebase_id': ethnicity_freebase_ids, 'ethnicity_label': ethnicity_labels})
    ethnicities_df.to_csv('../handled_data/ethnicities_freebase_ids.csv', sep=',', index=False)

    eth = pd.read_csv('../handled_data/ethnicities_freebase_ids.csv')
    #print(eth)

fetch_ethnicity_freebase_labels()
