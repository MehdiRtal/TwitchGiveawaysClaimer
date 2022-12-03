from playwright.sync_api import sync_playwright
import re

with open("accounts.txt") as f:
    accounts = f.read().splitlines()

user_match = input("Enter username to match: ")
start_pattern = input("Enter giveaway start pattern: ")
end_pattern = input("Enter giveaway end pattern: ")
streamer = input("Enter streamer username: ")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    while True:
        page.goto("https://www.twitch.tv/" + streamer)
        print("Checking for giveaways...")
        while True:
            start_match = re.findall(start_pattern, page.locator("css=[data-test-selector='chat-line-message']", has=page.locator("css=[data-a-target='chat-message-username']", has_text=user_match)).locator("css=[data-a-target='chat-message-text']").last.inner_text())[0]
            if start_match:
                print("Giveaway started!")
                break
        for account in accounts:
            context2 = browser.new_context()
            context2.add_cookies([{"name": "auth-token", "value": account.split("|")[1], "domain": "twitch.tv"}])
            page2 = context2.new_page()
            page2.goto("https://www.twitch.tv/" + streamer)
            page2.locator("css=[data-a-target='chat-input-textarea']").fill(start_match)
            page2.locator("css=[data-a-target='chat-send-button']").click()
        context2.close()
        while True:
            end_match = re.findall(end_pattern, page.locator("css=[data-test-selector='chat-line-message']", has=page.locator("css=[data-a-target='chat-message-username']", has_text=user_match)).locator("css=[data-a-target='chat-message-text']").last.inner_text())[0]
            if end_match:
                print("Giveaway ended!")
                if end_match in accounts:
                    print(end_match  + " won!")
                else:
                    print("You didn't win!")
                break