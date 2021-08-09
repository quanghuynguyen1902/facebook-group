map_code_error = {
    "102": {
        "name": "API Session",
        "what_to_do": "If no subcode is present, the login status or access token has expired, been revoked, or is otherwise invalid. Get a new access token. If a subcode is present, see the subcode.",
    },
    "1": {
        "name": "API Unknown",
        "what_to_do": "Possibly a temporary issue due to downtime. Wait and retry the operation. If it occurs again, check that you are requesting an existing API.",
    },
    "2": {
        "name": "API Service",
        "what_to_do": "Temporary issue due to downtime. Wait and retry the operation.",
    },
    "3": {
        "name": "API Method",
        "what_to_do": "Capability or permissions issue. Make sure your app has the necessary capability or permissions to make this call",
    },
    "4": {
        "name": "API Too Many Calls",
        "what_to_do": "Temporary issue due to throttling. Wait and retry the operation, or examine your API request volume.",
    },
    "17": {
        "name": "API User Too Many Calls",
        "what_to_do": "Temporary issue due to throttling. Wait and retry the operation, or examine your API request volume.",
    },
    "10": {
        "name": "API Permission Denied",
        "what_to_do": "Permission is either not granted or has been removed. Handle the missing permissions.",
    },
    "190": {"name": "Access token has expired", "what_to_do": "Get a new access token."},
    "341": {
        "name": "Application limit reached",
        "what_to_do": "Temporary issue due to downtime or throttling. Wait and retry the operation, or examine your API request volume.",
    },
    "368": {
        "name": "Temporarily blocked for policies violations",
        "what_to_do": "Wait and retry the operation.",
    },
    "506": {
        "name": "Duplicate Post",
        "what_to_do": "Duplicate posts cannot be published consecutively. Change the content of the post and try again.",
    },
    "1609005": {
        "name": "Error Posting Link ",
        "what_to_do": "There was a problem scraping data from the provided link. Check the URL and try again.",
    },
}


def log_error(map_code_error, response):
    if "error" in response:
        error_code = str(response["error"]["code"])
        if error_code not in map_code_error:
            raise ValueError(
                response["error"]["message"]
                + " - code: "
                + error_code
                + " - code name: API Permission (Multiple values depending on permission)"
                + "- what to do: Permission is either not granted or has been removed. Handle the missing permissions"
            )
        else:
            raise ValueError(
                response["error"]["message"]
                + " - code: "
                + error_code
                + " - code name: "
                + map_code_error[error_code]["name"]
                + " - what to do: "
                + map_code_error[error_code]["what_to_do"]
            )
