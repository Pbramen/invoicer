REDIRECT_ALLOWED_LIST = [
    '/invoice/',
    '/invoice',
    '/invoice/view/',
    '/invoice/view'
]

VENDOR_REDIRECT_ALLOW_LIST = [
    '/invoice/create/',
    '/invoice/create',
]
VENDOR_REDIRECT_ALLOW_LIST.extend(REDIRECT_ALLOWED_LIST)
