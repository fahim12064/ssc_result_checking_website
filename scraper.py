import requests
from bs4 import BeautifulSoup
import random

def get_result(exam, year, board, roll, reg):
    url = 'http://www.educationboardresults.gov.bd/'
    result_url = 'http://www.educationboardresults.gov.bd/result.php'

    s = requests.Session()

    # Multiple user-agents for better reliability
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15"
    ]

    headers = {
        'User-Agent': random.choice(user_agents),
        'Referer': url
    }

    cookies = {
        'PHPSESSID': 'jig55h716ghmeqi31n21oipf57'
    }

    # Captcha calculate
    def get_value_s():
        res = s.get(url, headers=headers, cookies=cookies)
        soup = BeautifulSoup(res.text, 'html.parser')
        value_table = soup.find('table', class_='black12bold')
        trs = value_table.find_all('tr')
        tds = trs[6].find_all('td')
        captcha_txt = tds[1].text.strip()
        X, Y = captcha_txt.split('+')
        return str(int(X) + int(Y))

    payload = {
        "sr": "3",
        "et": "2",
        "exam": exam,
        "year": year,
        "board": board,
        "roll": roll,
        "reg": reg,
        'value_s': get_value_s(),
        "button2": "Submit",
    }

    # POST request with headers + cookies
    result_res = s.post(result_url, data=payload, headers=headers, cookies=cookies)
    soup = BeautifulSoup(result_res.text, 'html.parser')

    try:
        # Student info table
        info_table = soup.find_all('table', class_='black12')[0]
        info_trs = info_table.find_all('tr')

        info = {
            "roll": info_trs[0].find_all('td')[1].text.strip(),
            "name": info_trs[0].find_all('td')[3].text.strip(),
            "board": info_trs[1].find_all('td')[1].text.strip(),
            "father_name": info_trs[1].find_all('td')[3].text.strip(),
            "group": info_trs[2].find_all('td')[1].text.strip(),
            "mother_name": info_trs[2].find_all('td')[3].text.strip(),
            "type": info_trs[3].find_all('td')[1].text.strip(),
            "dob": info_trs[3].find_all('td')[3].text.strip(),
            "result": info_trs[4].find_all('td')[1].text.strip(),
            "institute": info_trs[4].find_all('td')[3].text.strip(),
            "gpa": info_trs[5].find_all('td')[1].text.strip(),
        }

        # Subject-wise grade table
        grade_table = soup.find_all('table', class_='black12')[1]
        subject_data = []
        trs = grade_table.find_all('tr')[1:]

        for tr in trs:
            tds = tr.find_all('td')
            subject = {
                "code": tds[0].text.strip(),
                "subject": tds[1].text.strip(),
                "grade": tds[2].text.strip()
            }
            subject_data.append(subject)

        return {
            "student_info": info,
            "grades": subject_data
        }

    except Exception as e:
        return {"error": "Invalid input or result not found."}
