def compose(rss_rich, medium="twitter"):
    """Compose social media messages from RSS calendar updates

    Args:
        rss_rich (list[dict]): the enriched RSS feed
        medium (str, optional): What social media the posts are meant for. Defaults to "twitter".

    Returns:
        list[str]: a list of social media posts
    """

    # Time for character management :-) You're probably not paying for Twitter (X?) Blue
    TWEET_LENGTH = 280
    LINK_LENGTH = 23 + 1 # as per https://developer.twitter.com/en/docs/counting-characters
    # the '+ 1' is for the space

    # will hold all messages we have to post
    messages = []

    for event in rss_rich:
        if not "change" in event:
            continue

        body_text = ""
        if event["change"] == "added":
            body_text = f"🆕 New event! "
        elif event["change"] == "changed":
            if "date" in event["changes"]:
                body_text = f"📅⚠️ Date change! "
            elif "time" in event["changes"]:
                body_text = f"⏰⚠️ Time change! "
            else:
                # Other changes do not matter
                continue

        chars_left = TWEET_LENGTH - len(body_text)
        event_title = event["title"]

        # We only truncate if the social medium is Twitter
        if chars_left < len(event["title"]) and medium == "twitter":
            print("Big problems!", event["title"])
            # We truncate the title to the number of chars left, minus one for the …
            event_title = event["title"][:chars_left - 1] + "…"

        body_text = f"{body_text}{event_title} {event['link']}"

        messages.append(body_text)

    return messages