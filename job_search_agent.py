# from bs4 import BeautifulSoup
# import requests
# import llm


# class JobSection:
#     pass





# def search_jobs(query):
#     url = f"https://www.indeed.com/jobs?q={query.replace(' ', '+')}&l="
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, "html.parser")
    
#     jobs = []
#     for job_elem in soup.find_all("div", class_="job_seen_beacon"):
#         title = job_elem.find("h2").text.strip()
#         company = job_elem.find("span", class_="companyName").text.strip()
#         link = "https://www.indeed.com" + job_elem.find("a")["href"]
#         jobs.append({"title": title, "company": company, "link": link})
#     print(jobs)
#     return jobs



# llm = llm.GroqModel()  # Or any LLM you prefer

# def match_jobs(resume_text, job_list):
#     query = f"""Given the resume:\n{resume_text}\n\nMatch it with the following job listings \nReturn the top 3 best matches."""
#     context = f"""job listings:\n{job_list}"""
#     response = llm.get_response(query=query , context=context)
#     return response


# jobs_list = search_jobs("deep learning engineer")



import asyncio
from pyppeteer import launch


async def scrape_indeed():
    browser = await launch(headless=False)
    page = await browser.newPage()


    await page.goto('https://www.indeed.com')


    await page.waitForSelector('#text-input-what')
    await page.waitForSelector('#text-input-where')


    await page.type('#text-input-what', 'Software Engineer')
    await page.type('#text-input-where', 'USA')


    await page.click('button[type="submit"]')


    await page.waitForNavigation()


    job_listings = await page.querySelectorAll('.resultContent')
    for job in job_listings:
        # Extract the job title
        title_element = await job.querySelector('h2.jobTitle span[title]')
        title = await page.evaluate('(element) => element.textContent', title_element)


        # Extract the company name
        company_element = await job.querySelector('div.company_location [data-testid="company-name"]')
        company = await page.evaluate('(element) => element.textContent', company_element)


        # Extract the location
        location_element = await job.querySelector('div.company_location [data-testid="text-location"]')
        location = await page.evaluate('(element) => element.textContent', location_element)


        print({'title': title, 'company': company, 'location': location})




    await browser.close()


# Run the coroutine
if __name__ == '__main__':
    asyncio.run(scrape_indeed())