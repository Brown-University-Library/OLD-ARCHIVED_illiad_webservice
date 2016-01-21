### overview ###

This is a [django](https://www.djangoproject.com) web-wrapper around our [module](https://github.com/Brown-University-Library/illiad-client) for programmatic access to [Illiad Interlibrary Loan](http://www.atlas-sys.com/illiad/) software.


### usage ###

    # -*- coding: utf-8 -*-

    from __future__ import unicode_literals

    """ Shows sample call to webservice. """

    import os
    import requests


    ## setup
    ARTICLE_OPENURL = 'rft.jtitle=Facial plastic surgery : FPS&rft.atitle=Anatomy for blepharoplasty and brow-lift.&rft.pages=177-85&rft.date=2010&rft.volume=26&rft.end_page=85&ctx_ver=Z39.88-2004&rft.genre=article'

    BOOK_OPENURL = 'sid=FirstSearch%3AWorldCat&genre=book&isbn=9780688002305&title=Zen+and+the+art+of+motorcycle+maintenance%3A+an+inquiry+into+values%2C&date=1974&aulast=Pirsig&aufirst=Robert&auinitm=M&id=doi%3A&pid=673595%3Cfssessid%3E0%3C%2Ffssessid%3E&url_ver=Z39.88-2004&rfr_id=info%3Asid%2Ffirstsearch.oclc.org%3AWorldCat&rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Abook&rft.genre=book&req_dat=%3Csessionid%3E0%3C%2Fsessionid%3E&rfe_dat=%3Caccessionnumber%3E673595%3C%2Faccessionnumber%3E&rft_id=info%3Aoclcnum%2F673595&rft_id=urn%3AISBN%3A9780688002305&rft.aulast=Pirsig&rft.aufirst=Robert&rft.auinitm=M&rft.btitle=Zen+and+the+art+of+motorcycle+maintenance%3A+an+inquiry+into+values%2C&rft.date=1974&rft.isbn=9780688002305&rft.place=New+York&rft.pub=Morrow&rft.genre=book&checksum=8bf1504d891b0a2551ab879c3a555a8c&title=Brown University&linktype=openurl&detail=RBN'

    API_URL = os.environ['url']
    API_AUTH_KEY = os.environ['key']
    USERNAME = os.environ['username']
    OPENURL = ARTICLE_OPENURL  # or BOOK_OPENURL
    REQUEST_ID = 1234  # used to easily track web-service log entries for a single request

    ## hit api
    params = {
        'auth_key': API_AUTH_KEY,
        'username':USERNAME,
        'openurl': OPENURL,
        'request_id': REQUEST_ID
        }
    r = requests.post( API_URL, data=params )

    ## view response
    print r.content  # eg, { "status": "submission_successful", "transaction_number": "2468" }


### notes ###

- Though the underlying [module](https://github.com/Brown-University-Library/illiad-client) supports new-user-registration, this webservice focuses solely on submitting requests.

---
