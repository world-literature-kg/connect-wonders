import csv
import re
import pandas as pd

def normalize_header(header):
    if header.strip() == '#':
        return 'id'
    header = re.sub(r"[^\w\s]", '', header)
    header = re.sub(r"\s+", '_', header)
    return header.strip()

def load_country_lookup(countries_file):
    countries = pd.read_csv(countries_file)
    lookup = dict(zip(countries['countryLabel'], countries['CountryIsoCode']))
    lookup.update({'England': 'GBR', 'Massachussets, US': 'USA'})
    return lookup

LANGUAGE_LOOKUP = {
    'English': 'EN', 'Italian': 'IT', 'French': 'FR', 'Spanish': 'ES',
    'German': 'DE', 'Dutch': 'NL', 'Portuguese': 'PT', 'Russian': 'RU',
    'Chinese': 'ZH', 'Japanese': 'JA', 'Arabic': 'AR', 'Romanian': 'RO'
}

def clean_language_field(value):
    return value.strip().split()[0]

def normalize_csv(input_file, output_file, countries_file, extra_fields):
    country_lookup = load_country_lookup(countries_file)

    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        headers = next(reader)
        normalized_headers = [normalize_header(h) for h in headers]

        if 'country_field' in extra_fields and extra_fields['country_field'] in normalized_headers:
            normalized_headers.append(extra_fields['country_iso_col'])

        if 'language_field' in extra_fields and extra_fields['language_field'] in normalized_headers:
            normalized_headers.append(extra_fields['language_iso_col'])

        writer.writerow(normalized_headers)

        for row in reader:
            row_dict = dict(zip(normalized_headers[:len(headers)], row))

            new_row = row.copy()

            if 'country_field' in extra_fields:
                val = row_dict.get(extra_fields['country_field'], '').strip()
                iso = country_lookup.get(val, val)
                new_row.append(iso)

            if 'language_field' in extra_fields:
                raw_lang = row_dict.get(extra_fields['language_field'], '').strip()
                lang_code = LANGUAGE_LOOKUP.get(clean_language_field(raw_lang), raw_lang)
                new_row.append(lang_code)

            writer.writerow(new_row)
