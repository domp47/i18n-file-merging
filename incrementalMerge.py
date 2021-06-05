import sys
import xml.etree.ElementTree as ET


# Steps:
# 1. Go through all the one's in source
#  - if not found in destination add it with a note in the text
#  - if found update the context-group and notes just in case it changed just be consistent
# 2. Go through all the one's in the destination
#  - if not found in source delete this one

NAME_SPACES = {"xlf": "urn:oasis:names:tc:xliff:document:1.2"}

if len(sys.argv) < 3:
    print("usage: python3 i18nMerge.py [inputFile] [destinationFile]")
    exit(1)

ET.register_namespace("", "urn:oasis:names:tc:xliff:document:1.2")
source = ET.parse(sys.argv[1])
destination = ET.parse(sys.argv[2])

destination_body = destination.find(".//xlf:body", NAME_SPACES)

for source_trans_unit in source.findall(".//xlf:trans-unit", NAME_SPACES):
    trans_id = source_trans_unit.attrib["id"]

    dest_trans_unit = destination.find(f".//xlf:trans-unit[@id=\"{trans_id}\"]", NAME_SPACES)

    if not dest_trans_unit or dest_trans_unit is None:
        source_text = source_trans_unit.find("xlf:source", NAME_SPACES)
        source_text.text = f"(NEEDS TRANSLATION){source_text.text}"

        destination_body.append(source_trans_unit)
    else:
        dest_ctx_groups = dest_trans_unit.findall("xlf:context-group", NAME_SPACES)
        for ctx_group in dest_ctx_groups:
            dest_trans_unit.remove(ctx_group)

        src_ctx_groups = source_trans_unit.findall("xlf:context-group", NAME_SPACES)
        for ctx_group in src_ctx_groups:
            dest_trans_unit.append(ctx_group)

        dest_notes = dest_trans_unit.findall("xlf:note", NAME_SPACES)
        for note in dest_notes:
            dest_trans_unit.remove(note)

        src_notes = source_trans_unit.findall("xlf:note", NAME_SPACES)
        for note in src_notes:
            dest_trans_unit.append(note)


for dest_trans_unit in destination.findall(".//xlf:trans-unit", NAME_SPACES):
    trans_id = dest_trans_unit.attrib["id"]

    source_trans_unit = source.find(f".//xlf:trans-unit[@id=\"{trans_id}\"]", NAME_SPACES)

    if not source_trans_unit or source_trans_unit is None:
        destination_body.remove(dest_trans_unit)

destination.write(sys.argv[2], encoding="UTF-8", xml_declaration=True)
