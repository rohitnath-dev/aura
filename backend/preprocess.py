import os
import re
import json
import sys


# username

if len(sys.argv) < 2:

    raise ValueError(
        "Usage: python preprocess.py <username>"
    )

username = sys.argv[1]


# paths

RAW_DATA_FOLDER = (
    f"../users/{username}/raw_data"
)

OUTPUT_FILE = (
    f"../users/{username}/processed_data/"
    f"processed_user_data.json"
)


processed_data = []


if not os.path.exists(RAW_DATA_FOLDER):

    raise FileNotFoundError(
        f"Raw data folder not found: {RAW_DATA_FOLDER}"
    )


# clean normal text

def clean_text(text: str):

    text = re.sub(
        r"'''(.*?)'''",
        "",
        text,
        flags=re.DOTALL
    )

    text = re.sub(
        r'"""(.*?)"""',
        "",
        text,
        flags=re.DOTALL
    )

    cleaned_lines = []

    for line in text.splitlines():

        stripped = line.strip()

        if stripped.startswith("#"):
            continue

        if stripped == "":
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()


# preprocess whatsapp chats

def preprocess_whatsapp_chat(
    text: str,
    file_name: str
):

    cleaned_messages = []

    lines = text.splitlines()

    other_person_match = re.search(
        r"WhatsApp Chat with (.+)",
        file_name,
        re.IGNORECASE
    )

    OTHER_PERSON = (

        other_person_match.group(1)
        .replace(".txt", "")
        .strip()

        if other_person_match
        else "Unknown"
    )

    skip_patterns = [

        "Messages and calls are end-to-end encrypted",

        "<Media omitted>",

        "This message was deleted",

        "You deleted this message"
    ]

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if any(
            pattern in line
            for pattern in skip_patterns
        ):
            continue

        match = re.match(
            r"^\d{1,2}/\d{1,2}/\d{2,4},.*? - (.*?): (.*)$",
            line
        )

        if not match:
            continue

        sender = match.group(1).strip()

        message = match.group(2).strip()

        if not message:
            continue

        message = re.sub(
            r"<This message was edited>",
            "",
            message
        ).strip()

        if sender.lower() == OTHER_PERSON.lower():

            cleaned_messages.append(
                f"[other_person][weight=0.35]: {message}"
            )

        else:

            cleaned_messages.append(
                f"[user][weight=1.0]: {message}"
            )

    return "\n".join(cleaned_messages).strip()


# process txt

def process_txt_file(
    file_path,
    source_name
):

    try:

        file_name = os.path.basename(file_path)

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            raw_text = f.read()

        if "whatsapp" in file_name.lower():

            cleaned_text = preprocess_whatsapp_chat(
                raw_text,
                file_name
            )

        else:

            cleaned_text = clean_text(raw_text)

        if not cleaned_text:
            return

        processed_data.append({

            "source": source_name,

            "type": "text",

            "text": cleaned_text
        })

    except Exception as e:

        print(
            f"TXT processing failed: {file_path}"
        )

        print(e)


# process json

def process_json_file(
    file_path,
    source_name
):

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        if "_metadata" in data:

            del data["_metadata"]

        processed_data.append({

            "source": source_name,

            "type": "json",

            "text": json.dumps(
                data,
                ensure_ascii=False,
                indent=2
            )
        })

    except Exception as e:

        print(
            f"JSON processing failed: {file_path}"
        )

        print(e)


# walk through raw data

for root, dirs, files in os.walk(
    RAW_DATA_FOLDER
):

    for file in files:

        file_path = os.path.join(
            root,
            file
        )

        source_name = os.path.splitext(
            file
        )[0]

        if file.lower().endswith(".txt"):

            process_txt_file(
                file_path=file_path,
                source_name=source_name
            )

        elif file.lower().endswith(".json"):

            process_json_file(
                file_path=file_path,
                source_name=source_name
            )


# create output folder

os.makedirs(
    os.path.dirname(OUTPUT_FILE),
    exist_ok=True
)


# save processed output

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        processed_data,
        f,
        ensure_ascii=False,
        indent=2
    )


print("\nPreprocessing complete.")

print(f"Saved to: {OUTPUT_FILE}")

print(
    f"Total processed items: {len(processed_data)}"
)
