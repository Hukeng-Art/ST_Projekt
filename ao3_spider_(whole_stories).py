import scrapy
import re
import json
import os



class AO3Spider(scrapy.Spider):
    '''
    A Scrapy spider for archiveofourown.org that takes a search URL and extracts all found Fanfics.
    This spider scrapes whole stories by modifying the story-URL to lead to a view with all chapters
    on one page. Thus it produces only 1 top-level text element for stories with multiple chapters. 
    '''
    UPPER_LIMIT = 200
    name = 'ao3-rated'
    allowed_domains = ['archiveofourown.org']
    start_urls = [
        'https://archiveofourown.org/works/search?work_search%5Bquery%5D=&work_search%5Btitle%5D=&work_search%5Bcreators%5D=&work_search%5Brevised_at%5D=&work_search%5Bcomplete%5D=T&work_search%5Bcrossover%5D=&work_search%5Bsingle_chapter%5D=0&work_search%5Bword_count%5D=5000-50000&work_search%5Blanguage_id%5D=en&work_search%5Bfandom_names%5D=&work_search%5Brating_ids%5D=9&work_search%5Bcharacter_names%5D=&work_search%5Brelationship_names%5D=&work_search%5Bfreeform_names%5D=&work_search%5Bhits%5D=&work_search%5Bkudos_count%5D=&work_search%5Bcomments_count%5D=&work_search%5Bbookmarks_count%5D=&work_search%5Bsort_column%5D=kudos_count&work_search%5Bsort_direction%5D=desc&commit=Search'
        # 'https://archiveofourown.org/works/search?work_search%5Bquery%5D=&work_search%5Btitle%5D=&work_search%5Bcreators%5D=&work_search%5Brevised_at%5D=&work_search%5Bcomplete%5D=T&work_search%5Bcrossover%5D=&work_search%5Bsingle_chapter%5D=0&work_search%5Bword_count%5D=5000-50000&work_search%5Blanguage_id%5D=en&work_search%5Bfandom_names%5D=&work_search%5Brating_ids%5D=10&work_search%5Bcharacter_names%5D=&work_search%5Brelationship_names%5D=&work_search%5Bfreeform_names%5D=&work_search%5Bhits%5D=&work_search%5Bkudos_count%5D=&work_search%5Bcomments_count%5D=&work_search%5Bbookmarks_count%5D=&work_search%5Bsort_column%5D=kudos_count&work_search%5Bsort_direction%5D=desc&commit=Search'
        # 'https://archiveofourown.org/works/search?work_search%5Bquery%5D=&work_search%5Btitle%5D=&work_search%5Bcreators%5D=&work_search%5Brevised_at%5D=&work_search%5Bcomplete%5D=T&work_search%5Bcrossover%5D=&work_search%5Bsingle_chapter%5D=0&work_search%5Bword_count%5D=5000-50000&work_search%5Blanguage_id%5D=en&work_search%5Bfandom_names%5D=&work_search%5Brating_ids%5D=11&work_search%5Bcharacter_names%5D=&work_search%5Brelationship_names%5D=&work_search%5Bfreeform_names%5D=&work_search%5Bhits%5D=&work_search%5Bkudos_count%5D=&work_search%5Bcomments_count%5D=&work_search%5Bbookmarks_count%5D=&work_search%5Bsort_column%5D=kudos_count&work_search%5Bsort_direction%5D=desc&commit=Search'
        # 'https://archiveofourown.org/works/search?work_search%5Bquery%5D=&work_search%5Btitle%5D=&work_search%5Bcreators%5D=&work_search%5Brevised_at%5D=&work_search%5Bcomplete%5D=T&work_search%5Bcrossover%5D=&work_search%5Bsingle_chapter%5D=0&work_search%5Bword_count%5D=5000-50000&work_search%5Blanguage_id%5D=en&work_search%5Bfandom_names%5D=&work_search%5Brating_ids%5D=12&work_search%5Bcharacter_names%5D=&work_search%5Brelationship_names%5D=&work_search%5Bfreeform_names%5D=&work_search%5Bhits%5D=&work_search%5Bkudos_count%5D=&work_search%5Bcomments_count%5D=&work_search%5Bbookmarks_count%5D=&work_search%5Bsort_column%5D=kudos_count&work_search%5Bsort_direction%5D=desc&commit=Search'
        # 'https://archiveofourown.org/works/search?work_search%5Bquery%5D=&work_search%5Btitle%5D=&work_search%5Bcreators%5D=&work_search%5Brevised_at%5D=&work_search%5Bcomplete%5D=T&work_search%5Bcrossover%5D=&work_search%5Bsingle_chapter%5D=0&work_search%5Bword_count%5D=5000-50000&work_search%5Blanguage_id%5D=en&work_search%5Bfandom_names%5D=&work_search%5Brating_ids%5D=13&work_search%5Bcharacter_names%5D=&work_search%5Brelationship_names%5D=&work_search%5Bfreeform_names%5D=&work_search%5Bhits%5D=&work_search%5Bkudos_count%5D=&work_search%5Bcomments_count%5D=&work_search%5Bbookmarks_count%5D=&work_search%5Bsort_column%5D=kudos_count&work_search%5Bsort_direction%5D=desc&commit=Search'
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 5,
        'ROBOTSTXT_OBEY': False,
        'AUTOTHROTTLE_ENABLED': True
    }

    def parse(self, response):
        '''Extracts and follows links to fanfic chapters on a search page'''

        story_urls = response.xpath('//li/div/h4/a[1]/@href').getall()
        for story_url in story_urls:
            self.logger.debug('fanfic link: %s', story_url)
            yield response.follow(url=story_url + '?view_full_work=true', callback=self.parse_fanfic)

        next_page = response.xpath('//a[@rel="next"]/@href').get()
        if next_page:
            self.logger.debug('next search page: %s', next_page)
            yield response.follow(next_page, self.parse)

    def parse_fanfic(self, response):
        '''Extracts all relevant data from a fanfic chapter page'''
        
        directory_contents = os.listdir('scraped_pages')

        if len(directory_contents) >= AO3Spider.UPPER_LIMIT:
            self.log('parsed enough pages for current link')
            return

        ao3id = re.search(r'(?:/works/)([0-9]+)', response.url).group(1)

        if f'f{ao3id}.json' in directory_contents:
            self.log('already parsed this page!')
            return



        # if the page contains an age confirmation prompt, follow the confirmation link instead and return
        confirmation = response.xpath('//a[text()="Proceed"]')
        if confirmation:
            self.logger.debug('Adult content, confirmation needed!')
            href = confirmation.attrib['href']
            yield response.follow(href, self.parse_fanfic)
            return


        title = response.xpath('//h2[@class="title heading"]/text()').get()
        if title is not None:
            title = title.strip()
        
        author = response.xpath('//h3/a[@rel="author"]/text()').getall() # multiple authors are possible!

        metagroup = response.xpath('//dl[@class="work meta group"]')
        rating = metagroup.css('dd.rating.tags li ::text').get()
        archive_warnings = metagroup.css('dd.warning.tags li ::text').getall()
        categories = metagroup.css('dd.category.tags li ::text').getall()
        fandoms = metagroup.css('dd.fandom.tags li ::text').getall()
        relationships = metagroup.css('dd.relationship.tags li ::text').getall()
        characters = metagroup.css('dd.character.tags li ::text').getall()
        additional_tags = metagroup.css('dd.freeform.tags li ::text').getall()
        language = metagroup.css('dd.language ::text').get().strip()
        series = metagroup.css('dd.series span.position ::text').getall()
        if series is not None:
            series = "".join(series)
        published = metagroup.css('dd.stats dd.published ::text').get()
        completed = metagroup.css('dd.stats dd.status ::text').get()
        words = metagroup.css('dd.stats dd.words ::text').get()
        chapters = metagroup.css('dd.stats dd.chapters ::text').get()
        comments = metagroup.css('dd.stats dd.comments ::text').get()
        kudos = metagroup.css('dd.stats dd.kudos ::text').get()
        bookmarks = metagroup.css('dd.stats dd.bookmarks ::text').get()
        hits = metagroup.css('dd.stats dd.hits ::text').get()

        paragraphs = response.css('div.summary.module p').getall()
        summary = '\n'.join(paragraphs)

        paragraphs = response.css('div.notes.module p').getall()
        notes = '\n'.join(paragraphs)

        paragraphs = response.css('div.userstuff p').getall()
        text = '\n'.join(paragraphs)

        story_dict = {
            'id': ao3id,
            'url': response.url,
            'author': author,
            'title': title,
            'rating': rating,
            'archive_warnings': archive_warnings,
            'categories': categories,
            'fandoms': fandoms,
            'relationships': relationships,
            'characters': characters,
            'additional_tags': additional_tags,
            'language': language,
            'series': series,
            'published': published,
            'completed': completed,
            'words': words,
            'chapters': chapters,
            'comments': comments,
            'kudos': kudos,
            'bookmarks': bookmarks,
            'hits': hits,
            'summary': summary,
            'notes': notes,
            'text': text
        }

        with open(f'scraped_pages/{story_dict["id"]}.json', 'w') as f:
            f.write(json.dumps(story_dict, indent=2))
            


