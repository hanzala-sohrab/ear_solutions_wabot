from zcrmsdk import ZCRMRestClient, ZohoOAuth

configuration_dictionary = {
    'apiBaseUrl': 'https://www.zohoapis.in',
    'apiVersion': 'v2',
    'currentUserEmail': 'sorb.hanzala@gmail.com',
    'sandbox': 'False',
    'applicationLogFilePath': './log/',
    'client_id': '1000.N76BCBFN5BC2XF2RI2VD0LWN6AKHSJ',
    'client_secret': '31af817b839c9ace17247a73b7ae18195c8682afeb',
    'redirect_uri': 'https://www.abc.com',
    'accounts_url': 'https://accounts.zoho.in',
    'token_persistence_path': '.',
    'access_type': 'online'
}

ZCRMRestClient.get_instance().initialize(configuration_dictionary)
oauth_client = ZohoOAuth.get_client_instance()
grant_token = "1000.43eb215696874896c64b9857de58b413.29abb3b77b7b7c8405668335e84a7292"
oauth_tokens = oauth_client.generate_access_token(grant_token)
