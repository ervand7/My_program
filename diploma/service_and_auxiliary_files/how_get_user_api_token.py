# 1) log in in VKontakte: https://vk.com/login
# 2) create your oun standalone application here: https://vk.com/apps?act=manage
# 3) put in this file in variable APP_ID your standalone app's id
# 4) run this file
# 5) follow re result link
# 6) select by double click text in browser line after "token="
# 7) paste in file <input_data> in variable <user_api_token>
from urllib.parse import urlencode

# info from https://vk.com/dev/
oauth_api_base_url = 'https://oauth.vk.com/authorize'
APP_ID = 7717337  # my own last: 7717337 7723910 7716393 7649081
redirect_uri = 'https://oauth.vk.com/blank.html'
scope = 'friends'

oauth_params = {
    'redirect_uri': redirect_uri,
    'scope': scope,
    'response_type': 'token',
    'client_id': APP_ID
}

print('?'.join([oauth_api_base_url, urlencode(oauth_params)]))
