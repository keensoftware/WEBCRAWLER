from crawlee import SimpleCrawler, Request, Actor
import re

async def process_page(request, crawler):
    """Processes a single page to extract company name and emails."""
    page = await request.page()
    content = await page.content()

    # Extract company name (try multiple common locations)
    company_name = await page.title()
    if not company_name:
        company_name_tag = await page.querySelector('meta[property="og:site_name"]')
        if company_name_tag:
            company_name = await page.evaluate('(element) => element.content', company_name_tag)
    if not company_name:
        h1 = await page.querySelector('h1')
        if h1:
            company_name = await page.evaluate('(element) => element.textContent', h1)
    if not company_name:
        h2 = await page.querySelector('h2')
        if h2:
            company_name = await page.evaluate('(element) => element.textContent', h2)
    if not company_name:
        company_name = request.url.split('//')[-1].split('/')[0] #fallback to domain name

    # Extract email addresses using regex
    email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    emails = re.findall(email_regex, content)
    emails = list(set(emails))

    if company_name and emails:
        print(f"Company: {company_name}")
        print(f"Emails: {', '.join(emails)}")
        print("-" * 20)
    elif company_name:
        print(f"Company: {company_name}")
        print("No emails found.")
        print("-" * 20)
    else:
        print(f"Could not extract info from {request.url}")
        print("-" * 20)


async def main():
    """Sets up and runs the crawler."""
    crawler = SimpleCrawler(
        run_context=Actor.run_context(),  # Important for actor-based execution
        max_requests_per_crawl=100,  # Limit the number of pages crawled
        max_concurrency=10, #limits the amount of concurrent pages being processed.
        process_request_function=process_page,
    )

    website_urls = [
        "https://www.example.com",
        "https://www.anycompany.com/contact",
        "https://www.another-example.co.uk",
    ]

    requests = [Request(url) for url in website_urls]
    await crawler.run(requests)

if __name__ == "__main__":
    Actor.main(main)
