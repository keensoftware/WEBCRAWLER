from crawlee import Crawler,  Request,  Response



class ContactExtractor(Crawler):

    async def request(self, request: Request) -> Response:

        response = await self.make_request(request)



        # Extract email addresses from the 'contact-info' section

        email_elements = response.html.querySelectorAll(".contact-info a")

        for email_element in email_elements:

            email = email_element.text

            # Use regular expression to validate email format if needed

            if re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):

                yield {"email": email}



# Create a crawler instance

crawler = ContactExtractor()



# Start crawling the website

await crawler.run([Request("https://www.example.com/contact-us")]) 

