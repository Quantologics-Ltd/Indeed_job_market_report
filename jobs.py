from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request
import numpy as np
import pandas as pd

def refresh(address):
   hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'none','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}
   req = Request(address, headers=hdr)
   try:
       page = urlopen(req)
   except:
       pass
   soup = BeautifulSoup(page,"lxml")
   return soup


def get_salary(soup, i):
	soup = str(soup)
	txt = soup.split('label="Salary"')[i].split('</div>')[i-1].split('</svg>')[1]
	return txt


def get_salaries(soup):
	i = 1
	salaries = []
	soup = str(soup)
	txt = soup.split('label="Salary"')
	try:
		page = soup.split('"pagination-page-current">')[1].split('</button>')[0]
	except:
		return salaries, 1
	print('len txt', len(txt))
	for i in range(1,len(txt)+1):
		print(i)
		try:
			salary = txt[i].split('</div>')[0].split('</svg>')[1]
			salaries.append(salary)
			i+=1
		except:
			pass
	return salaries, int(page)

def get_all_pages(keyword):
	print(keyword)
	print('first page', 'https://uk.indeed.com/jobs?q='+keyword)
	soup = refresh('https://uk.indeed.com/jobs?q='+keyword)
	sals, page = get_salaries(soup)
	page = page
	recent_page = 0
	print(sals, page)	
	p = 10
	while recent_page < page and page <100:
		try:
			print('fetching address:', 'https://uk.indeed.com/jobs?q='+keyword+'&start='+str(p))
			soup = refresh('https://uk.indeed.com/jobs?q='+keyword+'&start='+str(p))
			p+=10
			recent_page = page
			#page+=1
		except:
			print('break1')
			break
		s,page = get_salaries(soup)
		print('recent page', recent_page)
		print('new page', page)
		if recent_page < page:
			sals = sals + s
	return sals
	
def get_figure(string):
	if '-' in string:
		parts = string.split('-')
		down = float(parts[0].split('£')[1].replace(',', ''))
		up = float(parts[1].split('£')[1].split()[0].replace(',', ''))
		unit = parts[1].split('£')[1].split()[2]
		print(up, down, unit, len(unit))
		return (up+down)/2, unit
	else:
		figure = float(string.split('£')[1].split()[0].replace(',', ''))
		unit = string.split('£')[1].split()[2]
		return figure, unit


def keyword_adjustment(keyword):
	if ' ' in keyword:
		keyword = keyword.replace(' ','+')
	return keyword
	
	
def statistics(annual, daily, hourly):
	stats = []
	stats.append(np.mean(annual))
	stats.append(np.median(annual))
	stats.append(np.std(annual))
	stats.append(len(annual))
	stats.append(np.mean(daily))
	stats.append(np.median(daily))
	stats.append(np.std(daily))
	stats.append(len(daily))
	stats.append(np.mean(hourly))
	stats.append(np.median(hourly))
	stats.append(np.std(hourly))
	stats.append(len(hourly))
	return stats

			
if __name__ == "__main__":		
	df = pd.DataFrame({'keyword':[], 'annual_mean':[], 'annual_median': [], 'annual_std': [], 'annual_ads_no': [], 
					'daily_mean': [],'daily_median': [], 'daily_std': [], 'daily_ads_no': [],
					'hourly_mean': [], 'hourly_median': [], 'hourly_std': [],'hourly_ads_no': []})	
					
	keywords = ['python', 'java', 'c++', 'rust', 'golang', 'react', 'kotlin', 'scala', 'javascript','php' ,'r',
			'aws', 'azure', 'gcp', 'dbt', 'hadoop' , 'sql', 'crm', 'c#', 'kdb', 'matlab',
			'data scientist', 'data engineer', 'data analyst', 'software engineer', 'software developer', 
			 'actuarial analyst', 'actuary', 'quantitative developer', 'quantitative analyst', 'cloud engineer', 
			 'android', 'linux', 'nlp', 'ai', 'machine learning', 'trading', 'fintech', 'insurtech', 'blockchain', 'defi',
			'credit risk','cyber security', 'quantum computing']		
	
	for i in range(0,len(keywords)):
		keyword = keywords[i]
		key = keyword_adjustment(keyword)
		sals = get_all_pages(key)
		annual = []
		daily = []
		hourly = []	
		for el in sals:
			fig, unit = get_figure(el)
			print(fig, unit, len(unit))
			if unit == 'year':
				annual.append(fig)
			elif unit == 'day':
				daily.append(fig)
			elif unit == 'hour':
				hourly.append(fig)
		stats = statistics(annual, daily, hourly)
		df = df.append({'keyword': keyword,'annual_mean':"{:.2f}".format(stats[0]), 'annual_median': "{:.2f}".format(stats[1]), 
						'annual_std': "{:.2f}".format(stats[2]), 'annual_ads_no': stats[3], 'daily_mean': "{:.2f}".format(stats[4]),
						'daily_median': "{:.2f}".format(stats[5]), 'daily_std': "{:.2f}".format(stats[6]), 'daily_ads_no': stats[7],
						'hourly_mean': "{:.2f}".format(stats[8]), 'hourly_median': "{:.2f}".format(stats[9]), 'hourly_std': "{:.2f}".format(stats[10]),
						'hourly_ads_no': stats[11]}, ignore_index=True)
		print(df)
		#df.to_csv('job_market_UK_2023_April'+str(i)+'.csv')	
		i+=1
									
	print(df)
	df.to_csv('job_market_UK_2023_April.csv')
	
	


		
	


