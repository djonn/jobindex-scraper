from bs4 import BeautifulSoup
from helpers import remove_blank_lines

def parse(content):
    soup = BeautifulSoup(content, "html.parser")
    job_postings_paid = soup.find_all("div", class_="jobsearch-result")

    print(f"Found {len(job_postings_paid)} postings")

    for _, job in enumerate(job_postings_paid):

        try:
            company = get_company(job)
            title = get_title(job)
            location = get_location(job)
            description = get_description(job)
            timestamp = get_timestamp(job)
            archive_link = get_archive_link(job)

            # print({
            #         "company": company,
            #         "title": title,
            #         "location": location,
            #         "description": description,
            #         "timestamp": timestamp,
            #         "archive_link": archive_link,
            #     })
        except:
            print(job)
            raise RuntimeError("stuff broke")

    # return True ## DELETE ME
    return is_last_page(soup)


def is_last_page(page):
    current_page = page.find("ul", class_="pagination").find_all("li", class_="active", limit=1)[0].get_text().strip()
    last_page = page.find("ul", class_="pagination").find_all(class_="page-link")[-1].get_text().strip()
    return current_page == last_page

def get_company(job):
    company = job.find(class_="jix-toolbar-top__company")

    if not company:
        return None

    return remove_blank_lines(company.get_text())

def get_title(job):
    return remove_blank_lines(job.find("h4").get_text())

def get_location(job):
    location = job.find(class_="jix_robotjob--area")

    if not location:
        return None

    return remove_blank_lines(location.get_text())

def get_description(job):
    p_arr = [remove_blank_lines(p.get_text()) for _i, p in enumerate(job.find_all("p"))]
    return "\n".join(p_arr)

def get_timestamp(job):
    return remove_blank_lines(job.find(class_="jix-toolbar__pubdate").find("time").get_text())

def get_archive_link(job):
    return "https://www.jobindex.dk" + job.find("a", class_="seejobdesktop")["data-click"]
