const buddyList = require('./')

async function main() {
    const spDcCookie = 'AQCn5jbgg9UKgnm6YVcTVdzn3dq6q4L6kAsmaRR0kZf7RYyykqWvxtIVtwzzkI2rh6hYwID-SfCZWKQnq5R-uKDcs2Bu5TLHyuSlzWemot5r_1SuGiK5b3AcuQ0cKfXx1iFzBE8C73DXZu4ypwMzpKkkNXgjPrR9'

    const { accessToken } = await buddyList.getWebAccessToken(spDcCookie)
    const friendActivity = await buddyList.getFriendActivity(accessToken)

    console.log(JSON.stringify(friendActivity, null, 2))
}

main()
