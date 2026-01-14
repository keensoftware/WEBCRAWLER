import { CheerioCrawler, Dataset } from 'crawlee';

const crawler = new CheerioCrawler({
    async requestHandler({ $, request }) {
        const companies = $('.company-listing').map((_, el) => ({
            name: $(el).find('.company-name').text(),
            industry: $(el).find('.company-industry').text(),
            size: $(el).find('.company-size').text(),
            website: $(el).find('.company-website').attr('href'),
        })).get();

        await Dataset.pushData(companies);
    },
});

await crawler.run(['https://example-business-directory.com/listings']);

