import os
import uuid
import json


def add_new_dam(db_directory, location, name, owner, river, date_built):
    """
    Persist new dam.
    """
    # Convert GeoJSON to Python dictionary
    location_dict = json.loads(location)

    # Serialize data to json
    new_dam_id = uuid.uuid4()
    dam_dict = {
        'id': str(new_dam_id),
        'location': location_dict['geometries'][0],
        'name': name,
        'owner': owner,
        'river': river,
        'date_built': date_built
    }

    dam_json = json.dumps(dam_dict)

    # Write to file in {{db_directory}}/dams/{{uuid}}.json
    # Make dams dir if it doesn't exist
    dams_dir = os.path.join(db_directory, 'dams')
    if not os.path.exists(dams_dir):
        os.mkdir(dams_dir)

    # Name of the file is its id
    file_name = str(new_dam_id) + '.json'
    file_path = os.path.join(dams_dir, file_name)

    # Write json
    with open(file_path, 'w') as f:
        f.write(dam_json)


def get_all_dams(db_directory):
    """
    Get all persisted dams.
    """
    # Write to file in {{db_directory}}/dams/{{uuid}}.json
    # Make dams dir if it doesn't exist
    dams_dir = os.path.join(db_directory, 'dams')
    if not os.path.exists(dams_dir):
        os.mkdir(dams_dir)

    dams = []

    # Open each file and convert contents to python objects
    for dam_json in os.listdir(dams_dir):
        # Make sure we are only looking at json files
        if '.json' not in dam_json:
            continue

        dam_json_path = os.path.join(dams_dir, dam_json)
        with open(dam_json_path, 'r') as f:
            dam_dict = json.loads(f.readlines()[0])
            dams.append(dam_dict)

    return dams