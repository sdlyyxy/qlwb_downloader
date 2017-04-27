import urllib2,os,re,urllib,PyPDF2,pdb,time
maxpdfs = 5	
# the max number of issues of the paper on local disk 
index='http://epaper.qlwb.com.cn/qlwb/pdf/'
header='Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5'
workdir='/var/www/html/app/qlwb/'

def gettime():
	s=time.strftime('%Y-%m-%d,%H:%M:%S',time.localtime(time.time()))
	return s
# return a string of present time

def checkpdfs():
	num=0;
	for root,dirs,files in os.walk(workdir):
		if(root!=workdir):break
		for file in files:
			if('pdf' in file):num+=1
	return num
#return number of pdfs in workdir

logfile=open(workdir+'log','a')
logfile.write(gettime()+' program began\n')
logfile.write('present pdfs '+str(checkpdfs())+'\n')
logfile.close()
#write a log of this python program began

def download(_date):
	d_request = urllib2.Request(index+_date)
	d_request.add_header('User-Agent', header)
	d_html = urllib2.urlopen(d_request).read()
	d_pattern=re.compile(r'/qlwb/pdf/(......../.?.?.?.?.?.?.?\.pdf)')
	d_match=d_pattern.findall(d_html)
	d_pages=len(d_match)

	i=0
	out=PyPDF2.PdfFileMerger()
	out.strict=False
	os.system('rm -rf '+workdir+'data/'+_date)
	os.mkdir(workdir+'data/'+_date)
	for s in d_match:
		i+=1;
		pdfpath=workdir+'data/'+_date+'/'+'%d'%i+'.pdf'
		urllib.urlretrieve(index+s,pdfpath)
		tmppdf=PyPDF2.PdfFileReader(open(pdfpath,'rb'))
		pdfinfo=tmppdf.getDocumentInfo()
		if('C0' in pdfinfo.title):
			break
		out.append(pdfpath,False)
		if(i%10==0):
			print 'Downloaded '+'%d'%i+' of all '+'%d'%d_pages+' pages......'
	print 'Download complete.Merging,this needs much time......'
	out.write(workdir+_date+'.pdf')
	print 'Done.'
# download qlwb on _date
	
def checkexist():
	for root,dirs,files in os.walk(workdir):
		if(root!=workdir):break
		for file in files:
			if(_tmpdate in file):return True
	return False
# check qlwb of day _tmpdate whether exists
	
def getoldest():
	tmp='9999999999'
	for root,dirs,files in os.walk(workdir):
		if(root!=workdir):break
		for file in files:
			if(('pdf' in file)and(file<tmp)):tmp=file
	return tmp
# return a string which content is the filename of the oldest pdf on local disk

# pdb.set_trace()

request = urllib2.Request(index)
request.add_header('User-Agent', header)
html = urllib2.urlopen(request).read()
pattern=re.compile(r'<A HREF="/qlwb/pdf/(........)...........</A><br>')
alldates=pattern.findall(html)
lastdate=len(alldates)-1
_lastdate=alldates[lastdate]
	
	
for tmpdate in range(lastdate-maxpdfs+1,lastdate+1):
	_tmpdate=alldates[tmpdate]
	if(not checkexist()):
		download(_tmpdate)
'''
tmpdate=lastdate
_tmpdate=alldates[tmpdate]
while (checkpdfs()<maxpdfs):
	download(_tmpdate)
	tmpdate-=1
	_tmpdate=alldates[tmpdate]

#pdb.set_trace()
	
tmpdate=lastdate
_tmpdate=alldates[tmpdate]
while (not checkexist()):
	#os.system('delete')
	oldest=getoldest()
	os.system('rm -rf '+workdir+'data/'+oldest[0:8])
	os.system('rm -f '+oldest)
	download(_tmpdate)
	tmpdate-=1
	_tmpdate=alldates[tmpdate]
'''

	
logfile=open(workdir+'log','a')
logfile.write(gettime()+'download completed\n')
logfile.write('present pdfs '+str(checkpdfs())+'\n')
while(checkpdfs()>maxpdfs):
#delete old files
	logfile.write(gettime()+' present pdfs: '+str(checkpdfs())+'\n')
	tmp='99999999'
	for root,dirs,files in os.walk(workdir):
		if(root!=workdir):break
		for file in files:
			if(('pdf' in file)and(file<tmp)):tmp=file
	os.system('rm -f '+workdir+tmp)
	os.system('rm -rf '+workdir+'data/'+tmp[0:8])
logfile.write(gettime()+'clear old completed\n')
logfile.write('present pdfs '+str(checkpdfs())+'\n')
logfile.close()
#tmp='99999999'
#datadir=workdir+'data/'
#for root,dirs,files in os.walk(datadir):
#	if(root!=datadir):break
#	for dir in dirs:
#		if(('	
