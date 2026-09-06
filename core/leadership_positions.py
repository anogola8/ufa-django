# leadership_positions.py - Central file for all leadership positions

# County Level Positions
COUNTY_POSITIONS = [
    ('county_chairperson', 'County Chairperson'),
    ('county_vice_chairperson', 'County Vice Chairperson'),
    ('county_secretary', 'County Secretary'),
    ('county_organizing_secretary', 'County Organizing Secretary'),
    ('county_treasurer', 'County Treasurer'),
    ('county_youth_leader', 'County Youth Leader'),
    ('county_women_rep', 'County Women Representative'),
    ('county_pwd_leader', 'County PWD Leader'),
    ('county_exofficial_male', 'County Ex-official Member (Male)'),
    ('county_exofficial_female', 'County Ex-official Member (Female)'),
]

# Ward Level Positions
WARD_POSITIONS = [
    ('ward_chairperson', 'Ward Chairperson'),
    ('ward_vice_chairperson', 'Ward Vice Chairperson'),
    ('ward_secretary', 'Ward Secretary'),
    ('ward_organizing_secretary', 'Ward Organizing Secretary'),
    ('ward_treasurer', 'Ward Treasurer'),
    ('ward_youth_leader', 'Ward Youth Leader'),
    ('ward_women_rep', 'Ward Women Representative'),
    ('ward_pwd_leader', 'Ward PWD Leader'),
]

# National Level Positions
NATIONAL_POSITIONS = [
    ('national_chairperson', 'National Chairperson'),
    ('national_vice_chairperson', 'National Vice Chairperson'),
    ('national_secretary_general', 'Secretary General'),
    ('national_organizing_secretary', 'National Organizing Secretary'),
    ('national_treasurer', 'National Treasurer'),
    ('national_youth_leader', 'National Youth Leader'),
    ('national_women_rep', 'National Women Representative'),
    ('national_pwd_leader', 'National PWD Leader'),
    ('national_programs_director', 'National Programs Director'),
]

# All positions combined
ALL_POSITIONS = COUNTY_POSITIONS + WARD_POSITIONS + NATIONAL_POSITIONS

# Position type mapping
POSITION_TYPES = {
    'county': 'County Position',
    'ward': 'Ward Position',
    'national': 'National Position',
}

# Position level mapping
POSITION_LEVELS = {
    'county': 'County Level',
    'ward': 'Ward Level',
    'national': 'National Level',
}

def get_position_type(position_key):
    """Get the type of position (county, ward, or national)"""
    county_keys = [p[0] for p in COUNTY_POSITIONS]
    ward_keys = [p[0] for p in WARD_POSITIONS]
    national_keys = [p[0] for p in NATIONAL_POSITIONS]
    
    if position_key in county_keys:
        return 'county'
    elif position_key in ward_keys:
        return 'ward'
    elif position_key in national_keys:
        return 'national'
    return None

def get_position_level(position_key):
    """Get the level of position (County, Ward, or National)"""
    position_type = get_position_type(position_key)
    if position_type:
        return position_type.capitalize()
    return None
