from pappyproxy.http import Request, get_request, post_request, request_by_id
from pappyproxy.context import set_tag
from pappyproxy.iter import *

## Iterator cheat sheet:
# fuzz_path_trav() - Values for fuzzing path traversal
# fuzz_sqli() - Values for fuzzing SQLi
# fuzz_xss() - Values for fuzzing XSS
# common_passwords() - Common passwords
# common_usernames() - Common usernames
# fuzz_dirs() - Common web paths (ie /wp-admin)

MACRO_NAME = '{{macro_name}}'
SHORT_NAME = '{{short_name}}'

###########
## Requests
# It's suggested that you call .copy() on these and then edit attributes
# as needed to create modified requests
##

{% set count = 1 %}{% for params, lines in zip(req_params, req_lines) %}
req{{ count }} = Request(({% for line in lines %}
    '{{ line }}'{% endfor %}{% set count = count+1 %}
){{ params }})
{% endfor %}

def run_macro(args):
    # Example:
    # req = req1.copy() # Copy req1
    # req.submit() # Submit the request to get a response
    # print req.response.raw_headers # print the response headers
    # req.save() # save the request to the data file
    # or copy req1 into a loop and use string substitution to automate requests
    pass
