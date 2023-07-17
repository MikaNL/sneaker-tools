import requests, pickle, os, time, cloudscraper

class StockX:
    def __init__(self):
        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,ja-JP;q=0.8,ja;q=0.7,la;q=0.6",
            "appos": "web",
            "appversion": "0.1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
        }

    def getCookies(self):
        if os.path.exists("cookies.pkl"):
            with open("cookies.pkl", "rb") as f:
                data = pickle.load(f)
            if data["expiration"] < time.time():
                data = self.updateCookies()
        else:
            data = self.updateCookies()
        return data["cookie"]

    def updateCookies(self):
        data = {"cookie": {}}
        response = requests.get("https://stockx.com/", headers=self.headers)
        data["cookie"]["stockx_device_id"] = response.cookies.get("stockx_device_id")
        data["cookie"]["__cf_bm"] = response.cookies.get("__cf_bm")
        data["cookie"]["stockx_session_id"] = response.cookies.get("stockx_session_id")
        data["expiration"] = time.time() + 3600
        with open("cookies.pkl", "wb") as f:
            pickle.dump(data, f)
        return data
    
    def search(self, query: str):
        scraper = cloudscraper.create_scraper()
        cookies = self.getCookies()
        self.headers["cookie"] = cookies['__cf_bm']
        self.headers["Apollographql-Client-Name"] = "Iron"
        self.headers["Apollographql-Client-Version"] = "2023.07.02.05"
        self.headers["App-Platform"] = "Iron"
        self.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        self.headers["X-Operation-Name"] = "GetSearchResults"
        self.headers["Content-Type"] = "application/json"
        self.headers["Accept"] = "application/json"
        self.headers["Accept-Encoding"] = "gzip, deflate, br"
        self.headers["App-Version"] = "2023.07.02.05"
        self.headers["X-Stockx-Device-Id"] = cookies["stockx_device_id"]
        self.headers["X-Stockx-Session-Id"] = cookies["stockx_session_id"]
        payload = {"query":"query GetSearchResults($filtersVersion: Int, $query: String!, $page: BrowsePageInput, $sort: BrowseSortInput, $staticRanking: BrowseExperimentStaticRankingInput) {\n  browse(\n    query: $query\n    page: $page\n    sort: $sort\n    filtersVersion: $filtersVersion\n    experiments: {staticRanking: $staticRanking}\n  ) {\n    categories {\n      id\n      name\n      count\n    }\n    results {\n      edges {\n        objectId\n        node {\n          ... on Product {\n            id\n            urlKey\n            primaryTitle\n            secondaryTitle\n            media {\n              thumbUrl\n            }\n            brand\n            productCategory\n            ...FavoriteProductFragment\n          }\n          ... on Variant {\n            id\n            product {\n              id\n              urlKey\n              primaryTitle\n              secondaryTitle\n              media {\n                thumbUrl\n              }\n              brand\n              productCategory\n            }\n          }\n        }\n      }\n      pageInfo {\n        limit\n        page\n        pageCount\n        queryId\n        queryIndex\n        total\n      }\n    }\n    sort {\n      id\n      order\n    }\n  }\n}\n\nfragment FavoriteProductFragment on Product {\n  favorite\n}","variables":{"filtersVersion":4,"query":f"{query.replace(' ', '%20')}","sort":{"id":"featured","order":"DESC"},"staticRanking":{"enabled":False},"page":{"index":1,"limit":10}},"operationName":"GetSearchResults"}
        response = scraper.post("https://stockx.com/api/p/e", json=payload, headers=self.headers)
        return response.json()
    
    def getProductInfo(self, urlKey: str):
        scraper = cloudscraper.create_scraper()
        payload = {"query":"query GetProduct($id: String!, $currencyCode: CurrencyCode, $countryCode: String!, $marketName: String) {\n  product(id: $id) {\n    id\n    listingType\n    deleted\n    gender\n    browseVerticals\n    ...ProductMerchandisingFragment\n    ...AffirmCalloutFragment\n    ...BreadcrumbsFragment\n    ...BreadcrumbSchemaFragment\n    ...HazmatWarningFragment\n    ...HeaderFragment\n    ...NFTHeaderFragment\n    ...LastSaleFragment\n    ...UrgencyBadgeFragment\n    ...MarketActivityFragment\n    ...MediaFragment\n    ...MyPositionFragment\n    ...ProductDetailsFragment\n    ...ProductMetaTagsFragment\n    ...ProductSchemaFragment\n    ...ScreenTrackerFragment\n    ...SizeSelectorWrapperFragment\n    ...StatsForNerdsFragment\n    ...ThreeSixtyImageFragment\n    ...TrackingFragment\n    ...UtilityGroupFragment\n    ...FavoriteProductFragment\n  }\n}\n\nfragment ProductMerchandisingFragment on Product {\n  id\n  merchandising {\n    title\n    subtitle\n    image {\n      alt\n      url\n    }\n    body\n    trackingEvent\n    link {\n      title\n      url\n      urlType\n    }\n  }\n}\n\nfragment AffirmCalloutFragment on Product {\n  productCategory\n  urlKey\n  market(currencyCode: $currencyCode) {\n    bidAskData(country: $countryCode, market: $marketName) {\n      lowestAsk\n    }\n  }\n  variants {\n    id\n    market(currencyCode: $currencyCode) {\n      bidAskData(country: $countryCode, market: $marketName) {\n        lowestAsk\n      }\n    }\n  }\n}\n\nfragment BreadcrumbsFragment on Product {\n  breadcrumbs {\n    name\n    url\n    level\n  }\n}\n\nfragment BreadcrumbSchemaFragment on Product {\n  breadcrumbs {\n    name\n    url\n  }\n}\n\nfragment HazmatWarningFragment on Product {\n  id\n  hazardousMaterial {\n    lithiumIonBucket\n  }\n}\n\nfragment HeaderFragment on Product {\n  primaryTitle\n  secondaryTitle\n  condition\n  productCategory\n  reciprocal {\n    id\n    urlKey\n    variants {\n      id\n      traits {\n        size\n      }\n    }\n  }\n}\n\nfragment NFTHeaderFragment on Product {\n  primaryTitle\n  secondaryTitle\n  productCategory\n  editionType\n}\n\nfragment LastSaleFragment on Product {\n  id\n  market(currencyCode: $currencyCode) {\n    statistics(market: $marketName) {\n      ...LastSaleMarketStatistics\n    }\n  }\n  variants {\n    id\n    market(currencyCode: $currencyCode) {\n      statistics(market: $marketName) {\n        ...LastSaleMarketStatistics\n      }\n    }\n  }\n}\n\nfragment LastSaleMarketStatistics on MarketStatistics {\n  lastSale {\n    amount\n    changePercentage\n    changeValue\n    sameFees\n  }\n}\n\nfragment UrgencyBadgeFragment on Product {\n  id\n  productCategory\n  primaryCategory\n  sizeDescriptor\n  listingType\n  market(currencyCode: $currencyCode) {\n    ...LowInventoryBannerMarket\n  }\n  variants {\n    id\n    market(currencyCode: $currencyCode) {\n      ...LowInventoryBannerMarket\n    }\n  }\n  traits {\n    name\n    value\n    visible\n  }\n}\n\nfragment LowInventoryBannerMarket on Market {\n  bidAskData(country: $countryCode, market: $marketName) {\n    numberOfAsks\n    lowestAsk\n  }\n  salesInformation {\n    lastSale\n    salesLast72Hours\n  }\n}\n\nfragment MarketActivityFragment on Product {\n  id\n  title\n  productCategory\n  primaryTitle\n  secondaryTitle\n  media {\n    smallImageUrl\n  }\n}\n\nfragment MediaFragment on Product {\n  id\n  productCategory\n  title\n  brand\n  urlKey\n  variants {\n    id\n    hidden\n    traits {\n      size\n    }\n  }\n  media {\n    gallery\n    imageUrl\n  }\n}\n\nfragment MyPositionFragment on Product {\n  id\n  urlKey\n}\n\nfragment ProductDetailsFragment on Product {\n  id\n  title\n  productCategory\n  contentGroup\n  browseVerticals\n  description\n  gender\n  traits {\n    name\n    value\n    visible\n    format\n  }\n}\n\nfragment ProductMetaTagsFragment on Product {\n  id\n  urlKey\n  productCategory\n  brand\n  model\n  title\n  description\n  condition\n  styleId\n  breadcrumbs {\n    name\n    url\n  }\n  traits {\n    name\n    value\n  }\n  media {\n    thumbUrl\n    imageUrl\n  }\n  market(currencyCode: $currencyCode) {\n    bidAskData(country: $countryCode, market: $marketName) {\n      lowestAsk\n      numberOfAsks\n    }\n  }\n  variants {\n    id\n    hidden\n    traits {\n      size\n    }\n    market(currencyCode: $currencyCode) {\n      bidAskData(country: $countryCode, market: $marketName) {\n        lowestAsk\n      }\n    }\n  }\n}\n\nfragment ProductSchemaFragment on Product {\n  id\n  urlKey\n  productCategory\n  brand\n  model\n  title\n  description\n  condition\n  styleId\n  traits {\n    name\n    value\n  }\n  media {\n    thumbUrl\n    imageUrl\n  }\n  market(currencyCode: $currencyCode) {\n    bidAskData(country: $countryCode, market: $marketName) {\n      lowestAsk\n      numberOfAsks\n    }\n  }\n  variants {\n    id\n    hidden\n    traits {\n      size\n    }\n    market(currencyCode: $currencyCode) {\n      bidAskData(country: $countryCode, market: $marketName) {\n        lowestAsk\n      }\n    }\n    gtins {\n      type\n      identifier\n    }\n  }\n}\n\nfragment ScreenTrackerFragment on Product {\n  id\n  brand\n  productCategory\n  primaryCategory\n  title\n  market(currencyCode: $currencyCode) {\n    bidAskData(country: $countryCode, market: $marketName) {\n      highestBid\n      lowestAsk\n      numberOfAsks\n      numberOfBids\n    }\n    salesInformation {\n      lastSale\n    }\n  }\n  media {\n    imageUrl\n  }\n  traits {\n    name\n    value\n  }\n  variants {\n    id\n    traits {\n      size\n    }\n    market(currencyCode: $currencyCode) {\n      bidAskData(country: $countryCode, market: $marketName) {\n        highestBid\n        lowestAsk\n        numberOfAsks\n        numberOfBids\n      }\n      salesInformation {\n        lastSale\n      }\n    }\n  }\n  tags\n  reciprocal {\n    id\n    variants {\n      id\n    }\n  }\n}\n\nfragment SizeSelectorWrapperFragment on Product {\n  id\n  ...SizeSelectorFragment\n  ...SizeSelectorHeaderFragment\n  ...SizesFragment\n  ...SizesOptionsFragment\n  ...SizeChartFragment\n  ...SizeChartContentFragment\n  ...SizeConversionFragment\n  ...SizesAllButtonFragment\n}\n\nfragment SizeSelectorFragment on Product {\n  id\n  title\n  productCategory\n  browseVerticals\n  sizeDescriptor\n  availableSizeConversions {\n    name\n    type\n  }\n  defaultSizeConversion {\n    name\n    type\n  }\n  variants {\n    id\n    hidden\n    traits {\n      size\n    }\n    sizeChart {\n      baseSize\n      baseType\n      displayOptions {\n        size\n        type\n      }\n    }\n  }\n}\n\nfragment SizeSelectorHeaderFragment on Product {\n  sizeDescriptor\n  productCategory\n  availableSizeConversions {\n    name\n    type\n  }\n}\n\nfragment SizesFragment on Product {\n  id\n  productCategory\n  listingType\n  title\n}\n\nfragment SizesOptionsFragment on Product {\n  id\n  listingType\n  variants {\n    id\n    hidden\n    group {\n      shortCode\n    }\n    traits {\n      size\n    }\n    sizeChart {\n      baseSize\n      baseType\n      displayOptions {\n        size\n        type\n      }\n    }\n    market(currencyCode: $currencyCode) {\n      bidAskData(country: $countryCode, market: $marketName) {\n        lowestAsk\n      }\n    }\n  }\n}\n\nfragment SizeChartFragment on Product {\n  availableSizeConversions {\n    name\n    type\n  }\n  defaultSizeConversion {\n    name\n    type\n  }\n}\n\nfragment SizeChartContentFragment on Product {\n  availableSizeConversions {\n    name\n    type\n  }\n  defaultSizeConversion {\n    name\n    type\n  }\n  variants {\n    id\n    sizeChart {\n      baseSize\n      baseType\n      displayOptions {\n        size\n        type\n      }\n    }\n  }\n}\n\nfragment SizeConversionFragment on Product {\n  productCategory\n  browseVerticals\n  sizeDescriptor\n  availableSizeConversions {\n    name\n    type\n  }\n  defaultSizeConversion {\n    name\n    type\n  }\n}\n\nfragment SizesAllButtonFragment on Product {\n  id\n  sizeAllDescriptor\n  market(currencyCode: $currencyCode) {\n    bidAskData(country: $countryCode, market: $marketName) {\n      lowestAsk\n    }\n  }\n}\n\nfragment StatsForNerdsFragment on Product {\n  id\n  title\n  productCategory\n  sizeDescriptor\n  urlKey\n}\n\nfragment ThreeSixtyImageFragment on Product {\n  id\n  title\n  variants {\n    id\n  }\n  productCategory\n  media {\n    all360Images\n  }\n}\n\nfragment TrackingFragment on Product {\n  id\n  productCategory\n  primaryCategory\n  brand\n  title\n  market(currencyCode: $currencyCode) {\n    bidAskData(country: $countryCode, market: $marketName) {\n      highestBid\n      lowestAsk\n    }\n  }\n  variants {\n    id\n    market(currencyCode: $currencyCode) {\n      bidAskData(country: $countryCode, market: $marketName) {\n        highestBid\n        lowestAsk\n      }\n    }\n  }\n}\n\nfragment UtilityGroupFragment on Product {\n  id\n  ...FollowFragment\n  ...FollowContentFragment\n  ...FollowShareContentFragment\n  ...FollowSuccessFragment\n  ...PortfolioFragment\n  ...PortfolioContentFragment\n  ...ShareFragment\n}\n\nfragment FollowFragment on Product {\n  id\n  productCategory\n  title\n  variants {\n    id\n    traits {\n      size\n    }\n  }\n}\n\nfragment FollowContentFragment on Product {\n  title\n}\n\nfragment FollowShareContentFragment on Product {\n  id\n  title\n  sizeDescriptor\n  urlKey\n  variants {\n    id\n    traits {\n      size\n    }\n  }\n}\n\nfragment FollowSuccessFragment on Product {\n  id\n  title\n  productCategory\n  sizeDescriptor\n  media {\n    smallImageUrl\n  }\n  variants {\n    id\n    traits {\n      size\n    }\n  }\n}\n\nfragment PortfolioFragment on Product {\n  id\n  title\n  productCategory\n  variants {\n    id\n  }\n  traits {\n    name\n    value\n  }\n}\n\nfragment PortfolioContentFragment on Product {\n  id\n  productCategory\n  sizeDescriptor\n  variants {\n    id\n    traits {\n      size\n    }\n  }\n}\n\nfragment ShareFragment on Product {\n  id\n  productCategory\n  title\n  media {\n    imageUrl\n  }\n}\n\nfragment FavoriteProductFragment on Product {\n  favorite\n}","variables":{"id":f"{urlKey}","currencyCode":"EUR","countryCode":"NL","marketName":"NL"},"operationName":"GetProduct"}
        self.headers["X-Operation-Name"] = "GetProduct"
        response = scraper.post("https://stockx.com/api/p/e", json=payload, headers=self.headers)
        return response.json()


